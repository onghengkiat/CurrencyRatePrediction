from app import app, df, scalers, currency_codes, malaysia_df
from flask import request, jsonify, send_file
from app.util import missing_param_handler
from constants import MODEL_SAVE_PATH, WINDOW_SIZE, MODEL_FILENAME
from operator import itemgetter
from datetime import timedelta
import os
import tempfile
from flask_cors import cross_origin
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tensorflow.keras.models import load_model
from modeltrainer import ModelTrainer
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
import joblib
from constants import MODEL_WITH_CPI, MODEL_WITH_GDP, MODEL_WITH_GDP_AND_CPI, MODEL_ONLY_RATE

#######
# API #
#######
@app.route("/dataset")
@cross_origin(origin='*')
@missing_param_handler
def get_dashboard():
    def _transform_json(row, prev_data):
        from_myr = row['from_myr']
        currency_code = row['currency_code']
        rate_changed_to_myr = 0
        rate_is_increased_to_myr = True
        rate_changed_from_myr = 0
        rate_is_increased_from_myr = True
        to_myr = round(1.0/from_myr, 4)

        if prev_data.get(currency_code, None) is not None:
            # getting the last data from the windows of data captured
            last_data = prev_data[currency_code]
            rate_changed_to_myr = round( ((to_myr - last_data["to_myr"])/last_data["to_myr"]) * 100, 4)
            if rate_changed_to_myr < 0:
                rate_is_increased_to_myr = False
                rate_changed_to_myr = round(-1.0 * rate_changed_to_myr, 4)

            rate_changed_from_myr = round( ((from_myr - last_data["from_myr"])/last_data["from_myr"]) * 100, 4)
            if rate_changed_from_myr < 0:
                rate_is_increased_from_myr = False
                rate_changed_from_myr = round(-1.0 * rate_changed_from_myr, 4)

        return {
            "date": row['date'].strftime('%Y-%m-%d'),
            "currency_code": currency_code,
            "to_myr": to_myr,
            "from_myr": from_myr,
            "rate_changed_to_myr": rate_changed_to_myr,
            "rate_is_increased_to_myr": rate_is_increased_to_myr,
            "rate_changed_from_myr": rate_changed_from_myr,
            "rate_is_increased_from_myr": rate_is_increased_from_myr,
            "gdp": round(row['gdp'], 4),
            "cpi": round(row['cpi'], 4),
        }

    try: 
        data = []
        prev_data = {}
        for _, row in df.iterrows():
                
            cur_data = _transform_json(row, prev_data)
            data.append(cur_data)

            # Track it in the window
            prev_data[row['currency_code']] = cur_data
                
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
    algorithm = request.args.get('algorithm', 'LSTM')
    include_cpi = request.args.get('include_cpi', 'false') == 'true'
    include_gdp = request.args.get('include_gdp', 'false') == 'true'
    directory = os.path.join(MODEL_SAVE_PATH, currency_code, algorithm)

    if include_cpi and include_gdp:
        directory = os.path.join(directory, MODEL_WITH_GDP_AND_CPI)
    elif include_cpi:
        directory = os.path.join(directory, MODEL_WITH_CPI)
    elif include_gdp:
        directory = os.path.join(directory, MODEL_WITH_GDP)
    else:
        directory = os.path.join(directory, MODEL_ONLY_RATE)

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
    algorithm = request.args.get('algorithm', 'LSTM')
    include_cpi = request.args.get('include_cpi', 'false') == 'true'
    include_gdp = request.args.get('include_gdp', 'false') == 'true'
    directory = os.path.join(MODEL_SAVE_PATH, currency_code, algorithm)

    if include_cpi and include_gdp:
        directory = os.path.join(directory, MODEL_WITH_GDP_AND_CPI)
    elif include_cpi:
        directory = os.path.join(directory, MODEL_WITH_CPI)
    elif include_gdp:
        directory = os.path.join(directory, MODEL_WITH_GDP)
    else:
        directory = os.path.join(directory, MODEL_ONLY_RATE)

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
    def _preprocess_data(_df, scaler, algorithm, include_cpi=False, include_gdp=False):
        def _split_x_y(data, look_back, include_cpi=False, include_gdp=False):
            datax, datay = [],[]
            for i in range(len(data)-look_back):
                datax.append(data[i:(i + look_back), 0])
                if include_cpi:
                    datax[i] = np.append(datax[i], data[i + look_back, 1])
                if include_gdp:
                    datax[i] = np.append(datax[i], data[i + look_back, 2])
                datay.append(data[i + look_back, 0])
            return np.array(datax), np.array(datay)

        _df['gdp'] = malaysia_df['gdp'] - _df['gdp']
        _df['cpi'] = malaysia_df['cpi'] - _df['cpi']

        _df[['from_myr']] = scaler.fit_transform(_df[['from_myr']])
        _temp_scaler = MinMaxScaler()
        _df[['cpi']] = _temp_scaler.fit_transform(_df[['cpi']])
        _temp_scaler = MinMaxScaler()
        _df[['gdp']] = _temp_scaler.fit_transform(_df[['gdp']])

        _df = np.array(_df[['from_myr', 'cpi', 'gdp']]).reshape(-1, 3)

        x, y = _split_x_y(_df, WINDOW_SIZE, include_cpi=include_cpi, include_gdp=include_gdp)

        if algorithm == "LSTM":
            x = x.reshape(x.shape[0], x.shape[1], 1)
        elif (algorithm == "POLYNOMIAL" or algorithm == "LINEAR" or 
            algorithm == "LASSO" or algorithm == "RIDGE"):
            x = x.reshape(x.shape[0], x.shape[1])

        _prev = x[-1]

        if algorithm == "POLYNOMIAL":   
            poly = PolynomialFeatures(degree=WINDOW_SIZE + include_cpi + include_gdp, interaction_only=True)
            x = poly.fit_transform(x)

        y = y.reshape(y.shape[0], 1)
        return x, y, _prev

    def _forecast_next_n_days(model, include_cpi, include_gdp, input_data, prev_data, n):
        results = []
        model_inputs = input_data
        if algorithm == "POLYNOMIAL":
            prev = prev_data
            poly = PolynomialFeatures(degree=WINDOW_SIZE + include_cpi + include_gdp, interaction_only=True)

        for _ in range(n):
            # Process the inputs
            if algorithm == "LSTM":
                model_inputs = model_inputs.reshape(1, model_inputs.shape[0], 1)
            elif algorithm == "LINEAR" or algorithm == "LASSO" or algorithm == "RIDGE":
                model_inputs = model_inputs.reshape(1, model_inputs.shape[0])
            elif  algorithm == "POLYNOMIAL":   
                prev = prev.reshape(1, prev.shape[0])
                model_inputs = poly.fit_transform(prev)
            
            predicted_data = model.predict(model_inputs)

            # Track it in the windows)

            if algorithm == "POLYNOMIAL":
                prev = prev[0]
                prev = np.insert(prev, WINDOW_SIZE, predicted_data[0])
                prev.reshape(prev.shape[0], 1)
                prev = prev[1:]
            else:
                model_inputs = model_inputs[0]
                model_inputs = np.insert(model_inputs, WINDOW_SIZE, predicted_data[0])
                model_inputs.reshape(model_inputs.shape[0], 1)
                model_inputs = model_inputs[1:]

            results.append(predicted_data[0])
        results = np.array(results)
        results = results.reshape(results.shape[0], 1)
        return results

    def _plot_actual_predict_graph(y_test, y_pred, date, currency_code):
        # Visualizing the results
        plt.figure(figsize=(10, 5))
        plt.title(f'Foreign Exchange Rate of MYR-{currency_code}')
        plt.plot_date(date, y_test, fmt='-', color = 'blue', label = 'Actual')
        plt.plot_date(date, y_pred, fmt='-', color = 'orange', label = 'Predicted')
        plt.legend()

        # Specify formatter for the dates on X-axis
        locator = mdates.MonthLocator(interval=1)
        fmt = mdates.DateFormatter('%b\n%Y')
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)

    FORECAST_DAYS = 30
    try:
        currency_code = request.args.get('currency_code', None)
        algorithm = request.args.get('algorithm', 'LSTM')
        include_cpi = request.args.get('include_cpi', 'false') == 'true'
        include_gdp = request.args.get('include_gdp', 'false') == 'true'

        # Load the dataset, model and scaler
        model_location = os.path.join(MODEL_SAVE_PATH, currency_code, algorithm)
        if include_cpi and include_gdp:
            model_location = os.path.join(model_location, MODEL_WITH_GDP_AND_CPI, MODEL_FILENAME)
        elif include_cpi:
            model_location = os.path.join(model_location, MODEL_WITH_CPI, MODEL_FILENAME)
        elif include_gdp:
            model_location = os.path.join(model_location, MODEL_WITH_GDP, MODEL_FILENAME)
        else:
            model_location = os.path.join(model_location, MODEL_ONLY_RATE, MODEL_FILENAME)

        if algorithm == "LSTM":
            model = load_model(model_location)
        else:
            model = joblib.load(model_location)
        scaler = scalers[currency_code]

        # Skip the first n, window size in which it can't make predictions on it
        _df = df[df['currency_code'] == currency_code].reset_index(drop=True)
        _df = _df[-90:]
        date = _df["date"].tolist()[WINDOW_SIZE:]
        date = date[-90:]

        # Data Preprocessing
        x, y, prev_data = _preprocess_data(_df, scaler, algorithm, include_cpi=include_cpi, include_gdp=include_gdp)
        y_pred = model.predict(x)
        y_pred = y_pred.reshape(y_pred.shape[0], 1)

        # Predict next n days currency rate
        future_forecast = _forecast_next_n_days(model, include_cpi, include_gdp, x[-1], prev_data, FORECAST_DAYS)
        y_pred = np.concatenate((y_pred, future_forecast))

        # Transform back to the normal values
        y_pred = scaler.inverse_transform(y_pred)
        y_actual = scaler.inverse_transform(y)

        # Append date and data for actual for the 30 days forecast
        for _ in range(FORECAST_DAYS):
            date.append(date[-1] + timedelta(days=1))
            # Actual datapoints will be empty
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
        try: 
            _df = df[df['currency_code'] == currency_code]
            _df.reset_index(inplace=True)
            min_rate = _df['from_myr'][0]
            min_date = _df['date'][0].strftime('%d %b %Y')
            max_rate = _df['from_myr'][0]
            max_date = _df['date'][0].strftime('%d %b %Y')

            for _, row in _df.iterrows():
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
        except Exception as e:
            print(e)
            return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/currencylist")
@cross_origin(origin='*')
@missing_param_handler
def get_currency_list():
    try: 
        return jsonify({"message": "Successful", "data": currency_codes}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400


@app.route("/algorithmlist")
@cross_origin(origin='*')
@missing_param_handler
def get_algorithm_list():
    try: 
        return jsonify({"message": "Successful", "data": ModelTrainer.ALGORITHMS_AVAILABLE}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400