from app import app, df, models, scalers, currency_codes
from flask import request, jsonify, send_file, make_response
from app.util import missing_param_handler
import pandas as pd
from constants import MODEL_SAVE_PATH, WINDOW_SIZE
from operator import itemgetter
from datetime import datetime, timedelta
import os
import tempfile
from flask_cors import cross_origin
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def transform_json(from_myr, date_string, currency_code, prev_data, is_prediction=False, to_myr=None):
    rate_changed_to_myr = 0
    rate_is_increased_to_myr = True
    rate_changed_from_myr = 0
    rate_is_increased_from_myr = True
    if to_myr is None:
        to_myr = round(1.0/from_myr, 4)

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


def split_x_y(data, look_back):
    datax, datay = [],[]
    for i in range(len(data)-look_back):
        datax.append(data[i:(i + look_back), 0])
        datay.append(data[i + look_back, 0])
    datax = np.array(datax)
    datay = np.array(datay)
    return datax.reshape(datax.shape[0], datax.shape[1], 1), datay.reshape(-1, 1)

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
        _model_input.append([d["from_myr"]])
    _model_input = scaler.transform(_model_input)
    return _model_input.reshape(_model_input.shape[0], _model_input.shape[1], 1)

def forecast_next_n_days(model, scaler, currency_code, prev_data, begin_date, n, only_from_myr=False):
    data = []
    cur_date = begin_date
    model_inputs = prev_data
    for i in range(n):
        if only_from_myr:
            # Process the inputs
            model_inputs = model_inputs.reshape(1, model_inputs.shape[0], model_inputs.shape[1])
            from_myr_predicted = model.predict(model_inputs)

            # Track it in the windows
            model_inputs = np.concatenate((model_inputs[0], from_myr_predicted))
            model_inputs = model_inputs[1:]

            data.append(from_myr_predicted[0])
        else:
            cur_date = cur_date + timedelta(days=1)
            cur_date_string = cur_date.strftime('%Y-%m-%d')
            model_inputs = preprocess_data(prev_data[currency_code], scaler)

            from_myr_predicted = model.predict(model_inputs)
            from_myr_predicted = round(float(scaler.inverse_transform(from_myr_predicted)[0][0]), 4)

            cur_data = transform_json(from_myr_predicted, cur_date_string, currency_code, prev_data, is_prediction=True)

            # Track it in the window
            prev_data = put_into_window(prev_data, cur_data, currency_code)
            data.append(cur_data)
    return data

@app.route("/dashboard")
@cross_origin(origin='*')
@missing_param_handler
def get_dashboard():
    try: 
        data = []
        prev_data = {}
        cur_date = None
        for i, row in df.iterrows():
            cur_date = row['date']
            cur_date_string = cur_date.strftime('%Y-%m-%d')
                
            cur_data = transform_json(row['from_myr'], cur_date_string, row['currency_code'], prev_data, to_myr=row['from_myr'])

            # Track it in the window
            prev_data = put_into_window(prev_data, cur_data, row['currency_code'])
            data.append(cur_data)

        if cur_date is None:
            return jsonify({"message": "Successful", "data": data}), 200

        # Predict next n days currency rate
        for currency_code in currency_codes:
            model = models[currency_code]
            scaler = scalers[currency_code]
            data = data + forecast_next_n_days(model, scaler, currency_code, prev_data, cur_date, 7)
                
        data.sort(key=itemgetter('date'), reverse=True)
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400


@app.route("/graph/modelperformance")
@cross_origin(origin='*')
@missing_param_handler
def get_model_actual_predicted_graph():
    currency_code = request.args.get('currency_code', None)
    directory = os.path.join(MODEL_SAVE_PATH, currency_code)

    filename = ""
    for f in os.listdir(directory):
        if f.endswith(".png"):
            filename = os.path.join(directory, f)
            break
    try:
        # append . here because send_file is using relative path
        r = send_file("." + filename, as_attachment=False)
    except Exception as e:
        print(e)
    return r

@app.route("/modelperformance")
@cross_origin(origin='*')
@missing_param_handler
def get_model_performance():
    currency_code = request.args.get('currency_code', None)
    directory = os.path.join(MODEL_SAVE_PATH, currency_code)

    filename = ""
    for f in os.listdir(directory):
        if f.endswith(".png"):
            # remove extension name
            filename = os.path.splitext(f)[0]
            break
    try:
        # get the metrics
        data = {}
        metrics = filename.split(",")
        for metric in metrics:
            name_value = metric.split("=")
            data[name_value[0]] = name_value[1]
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/graph/statistic")
@cross_origin(origin='*')
@missing_param_handler
def get_actual_predicted_graph():

    def _plot_actual_predict_graph(y_test, y_pred, date, currency_code):
        # Visualizing the results
        plt.figure(figsize=(10, 5))
        plt.title(f'Foreign Exchange Rate of MYR-{currency_code}')
        plt.plot_date(date, y_test, '-g', label = 'Actual')
        plt.plot_date(date, y_pred, '-r', label = 'Predicted')
        plt.legend()

        # Specify formatter for the dates on X-axis
        locator = mdates.MonthLocator(interval=3)
        fmt = mdates.DateFormatter('%b\n%Y')
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)

    FORECAST_DAYS = 30
    try:
        currency_code = request.args.get('currency_code', None)
        # Load the dataset, model and scaler
        model = models[currency_code]
        scaler = scalers[currency_code]

        # Skip the first n, window size in which it can't make predictions on it
        _df = df[df['currency_code'] == currency_code]
        date = _df["date"].tolist()[WINDOW_SIZE:]

        # Data Preprocessing
        datax = scaler.transform(np.array(_df["from_myr"]).reshape(-1, 1))
        datax, datay = split_x_y(datax, WINDOW_SIZE)

        y_pred = model.predict(datax)
        # Predict next n days currency rate
        future_forecast = forecast_next_n_days(model, scaler, currency_code, datax[-1], date[-1], FORECAST_DAYS, only_from_myr=True)
        y_pred = np.concatenate((y_pred, future_forecast))

        # Transform back to the normal values
        y_pred = scaler.inverse_transform(y_pred)
        y_actual = scaler.inverse_transform(datay)

        # Append date and data for the 30 days forecast
        for i in range(FORECAST_DAYS):
            date.append(date[-1] + timedelta(days=1))
            y_actual = np.concatenate((y_actual, np.array([[None]])))

        # Plot the actual predict graph and save it to be sent to frontend
        _plot_actual_predict_graph(y_actual, y_pred, date, currency_code)
        tmpdir = tempfile.mkdtemp() 
        directory = os.path.join(tmpdir, 'actual_predicted_graph.png')
        plt.savefig(directory)
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400
    try:
        r = send_file(directory, as_attachment=False)
        return r
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/statistic")
@cross_origin(origin='*')
@missing_param_handler
def get_statistic():
        currency_code = request.args.get('currency_code', None)
        _df = df[df['currency_code'] == currency_code]
        _df.reset_index(inplace=True)
        min_rate = _df['from_myr'][0]
        min_date = _df['date'][0].strftime('%d %b %Y')
        max_rate = _df['from_myr'][0]
        max_date = _df['date'][0].strftime('%d %b %Y')

        for i, row in _df.iterrows():
            if row['from_myr'] <= min_rate:
                min_rate = row['from_myr']
                min_date = row['date'].strftime('%d %b %Y')
            elif row['from_myr'] >= max_rate:
                max_rate = row['from_myr']
                max_date = row['date'].strftime('%d %b %Y')
        data = {
            "min_rate": min_rate,
            "min_date": min_date,
            "max_rate": max_rate,
            "max_date": max_date,
        }
        return jsonify({"message": "Successful", "data": data}), 200

@app.route("/currencylist")
@cross_origin(origin='*')
@missing_param_handler
def get_currency_list():
    try: 
        return jsonify({"message": "Successful", "data": currency_codes}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400