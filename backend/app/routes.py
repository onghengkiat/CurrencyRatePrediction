from app import app
from flask import request, jsonify, send_file, make_response
from app.util import cors_allow, missing_param_handler
import pandas as pd
from constants import DATA_FILENAME, MODEL_FILENAME, SCALAR_FILENAME, GRAPH_FILENAME, MODEL_SAVE_PATH, WINDOW_SIZE
from operator import itemgetter
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
import joblib
import os

def transform_json(to_myr, date_string, currency_code, prev_data, is_prediction=False):
    rate_changed_to_myr = 0
    rate_is_increased_to_myr = True
    rate_changed_from_myr = 0
    rate_is_increased_from_myr = True
    from_myr = round(1.0/to_myr, 4)

    if prev_data.get(currency_code, None) is not None:
        # getting the last data from the windows of data captured
        last_data = prev_data[currency_code][-1]
        rate_changed_to_myr = round( ((to_myr - last_data["to_myr"])/last_data["to_myr"]) * 100, 4)
        if rate_changed_to_myr < 0:
            rate_is_increased_to_myr = False
            rate_changed_to_myr = round(-1.0 * rate_changed_to_myr, 4)

        rate_changed_from_myr = round( ((from_myr - last_data["from_myr"])/last_data["from_myr"]) * 100, 4)
        if rate_changed_from_myr < 0:
            rate_is_increased_from_myr = False
            rate_changed_from_myr = round(-1.0 * rate_changed_from_myr, 4)

    return {
        "date": date_string,
        "currency_code": currency_code,
        "to_myr": to_myr,
        "from_myr": from_myr,
        "rate_changed_to_myr": rate_changed_to_myr,
        "rate_is_increased_to_myr": rate_is_increased_to_myr,
        "rate_changed_from_myr": rate_changed_from_myr,
        "rate_is_increased_from_myr": rate_is_increased_from_myr,
        "is_prediction": is_prediction,
    }

def put_into_window(prev_data, cur_data, currency_code):
    if prev_data.get(currency_code, None) is None:
        prev_data[currency_code] = [cur_data]
    else:
        if len(prev_data[currency_code]) < WINDOW_SIZE:
            prev_data[currency_code].append(cur_data)
        else:
            prev_data[currency_code] = prev_data[currency_code][1:]
            prev_data[currency_code].append(cur_data)
    return prev_data

def preprocess_data(list_of_dict, scaler):
    # [{
    #     "date": datetime.strptime(row['date'], '%d %b %Y').strftime('%Y-%m-%d'),
    #     "currency_code": currency_code,
    #     "to_myr": to_myr,
    #     "from_myr": from_myr,
    #     "rate_changed_to_myr": rate_changed_to_myr,
    #     "rate_is_increased_to_myr": rate_is_increased_to_myr,
    #     "rate_changed_from_myr": rate_changed_from_myr,
    #     "rate_is_increased_from_myr": rate_is_increased_from_myr,
    # }, ...]
    _model_input = []
    for d in list_of_dict:
        _model_input.append([d["to_myr"]])
    _model_input = scaler.transform(_model_input)
    return _model_input.reshape(_model_input.shape[0], _model_input.shape[1], 1)

@app.route("/dashboard")
@cors_allow
@missing_param_handler
def get_dashboard():
    try: 
        df = pd.read_csv(DATA_FILENAME, index_col=0)
        # First column is date
        currency_codes = df.columns[1:]
        data = []
        prev_data = {}
        cur_date = None
        for i, row in df.iterrows():
            cur_date = datetime.strptime(row['date'], '%d %b %Y')
            cur_date_string = cur_date.strftime('%Y-%m-%d')
            for currency_code in currency_codes:
                
                cur_data = transform_json(row[currency_code], cur_date_string, currency_code, prev_data)

                # Track it in the window
                prev_data = put_into_window(prev_data, cur_data, currency_code)
                data.append(cur_data)

        if cur_date is None:
            return jsonify({"message": "Successful", "data": data}), 200

        # Predict next day currency rate
        for i in range(1):
            cur_date = cur_date + timedelta(days=1)
            cur_date_string = cur_date.strftime('%Y-%m-%d')
            for currency_code in currency_codes:
                model = load_model(os.path.join(MODEL_SAVE_PATH, currency_code, MODEL_FILENAME))
                scaler = joblib.load(os.path.join(MODEL_SAVE_PATH, currency_code, SCALAR_FILENAME))
                model_inputs = preprocess_data(prev_data[currency_code], scaler)

                to_myr_predicted = model.predict(model_inputs)
                to_myr_predicted = round(float(scaler.inverse_transform(to_myr_predicted)[0][0]), 4)

                cur_data = transform_json(to_myr_predicted, cur_date_string, currency_code, prev_data, is_prediction=True)

                # Track it in the window
                prev_data = put_into_window(prev_data, cur_data, currency_code)
                data.append(cur_data)
                
                
        data.sort(key=itemgetter('date'), reverse=True)
        data.sort(key=itemgetter('currency_code'))
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400


@app.route("/graph")
@cors_allow
@missing_param_handler
def get_model_actual_predicted_graph():
    currency_code = request.args.get('currency_code', None)
    directory = os.path.join("." + MODEL_SAVE_PATH, currency_code, GRAPH_FILENAME)
    try:
        r = send_file(directory, as_attachment=False)
    except Exception as e:
        print(e)
    return r


@app.route("/statistic")
@cors_allow
@missing_param_handler
def get_statistic():
    try: 
        currency_code = request.args.get('currency_code', None)
        df = pd.read_csv(DATA_FILENAME, index_col=0)
        df["date"] = pd.to_datetime(df["date"], format='%d %b %Y')
        # remove the timezone
        df["date"] = df["date"].dt.tz_localize(None)
        # convert to datetime
        df["date"] = df["date"].dt.to_pydatetime()
        df = df[['date', currency_code]]

        min_rate = df[currency_code][0]
        min_date = df['date'][0].strftime('%d %b %Y')
        max_rate = df[currency_code][0]
        max_date = df['date'][0].strftime('%d %b %Y')

        for i, row in df.iterrows():
            if row[currency_code] <= min_rate:
                min_rate = row[currency_code]
                min_date = row['date'].strftime('%d %b %Y')
            elif row[currency_code] >= max_rate:
                max_rate = row[currency_code]
                max_date = row['date'].strftime('%d %b %Y')
        data = {
            "min_rate": min_rate,
            "min_date": min_date,
            "max_rate": max_rate,
            "max_date": max_date,
        }
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/currencylist")
@cors_allow
@missing_param_handler
def get_currency_list():
    try: 
        df = pd.read_csv(DATA_FILENAME, index_col=0)
        # First column is date
        currency_codes = df.columns[1:].values.tolist()
        return jsonify({"message": "Successful", "data": currency_codes}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400