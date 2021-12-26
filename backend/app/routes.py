from app import app, df, currency_codes, malaysia_df
from flask import request, jsonify, send_file, make_response
from app.util import missing_param_handler
from constants import MODEL_SAVE_PATH, WINDOW_SIZE, MODEL_FILENAME, CURRENCY_TO_COUNTRY, USERS, ACCESS_DENIED_ERROR
from operator import itemgetter
from datetime import timedelta, datetime
import os
from flask_cors import cross_origin
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from modeltrainer import ModelTrainer
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
import joblib
from constants import MODEL_WITH_CPI, MODEL_WITH_GDP, MODEL_WITH_GDP_AND_CPI, MODEL_ONLY_RATE
import jwt

#######
# API #
#######
@app.route("/authenticate", methods=['POST'])
@cross_origin(origin='*')
@missing_param_handler
def auth_route():
    """
    Parameters (json)
    -----------------
    JSON that contains the username and password
    entered by the user

        Format of the JSON
        ------------------
        {
            username: <username>,
            password: <password>
        }

    Return
    ------
    Authentication successful
        resp: JSON
            Response that contains the token for the user
            The JSON also contains the jwt token in 
            the cookie for the frontend to communicate
            with backends API

            Format of the resp
            ------------------
            {
                role: <role>,
                username: <username>
            }
        
    Methods Allowed
    ---------------
    POST
        Authenticate the username and password entered
        by the user
    """
    if request.json is not None and 'username' in request.json and 'password' in request.json:
        username, password = request.json["username"], request.json["password"]
        user = USERS.get(username, None)
        if user is None:
            return jsonify({"isError": True, "code": "Non-existing User", "message": "There is no existing user which matches the username."}), 400

        if user["password"] == password:
            token = jwt.encode({
                "role": user["role"],
                "sub": username,
                "iat": datetime.utcnow()
            }, app.config['SECRET_KEY'])
            resp = make_response(jsonify({"role": user["role"], "username": username}), 200)

            expire_date = datetime.now()
            expire_date = expire_date + timedelta(hours=24)
            resp.set_cookie('jwt', token.decode('utf-8'), httponly=True, secure=False, samesite='None', expires=expire_date)
            return resp
    return jsonify({"isError": True, "code": "Invalid Credential", "message": "Wrong username or password."}), 403

@app.route("/user", methods=['GET', 'POST', 'DELETE', 'PUT'])
@cross_origin(origin='*')
@missing_param_handler
def user_route():
    """
    Arguments (query string)
    ------------------------
    id (optional): string
        The username
    
    Methods Allowed
    ---------------
    GET (with id)
        Return json contains only the details of the user 
        which matches the id. If id is none, it will return the list 
        of users.

    PUT
        Update the details of an user into the table 
        according to the JSON data received
    
    POST
        Insert a new user into the table according to the 
        JSON data received
    
    DELETE
        Delete an user from the table according to the 
        JSON data received
    """
    
    def get_user(id):
        """
        Parameters
        ----------
        id: string
            The username

        Return
        ------
        data: dictionary
            Details of the user which matches the username

            Format of the data
            ------------------
            {
                username: <username>,
                fullname: <fullname>,
                email: <email>,
                role: <role>
            } 
            or
            [
                {
                    username: <username>,
                    fullname: <fullname>,
                    email: <email>,
                    role: <role>
                },
                ...
            ]
            
        Description
        -----------
        Return data contains only the details of the user 
        which matches the username. If id is None, it will return the 
        list of users.
        """
        if id is None:
            data = []
            for value in USERS.values():
                data.append(value)
        else:
            data = USERS.get(id, {})
        return data
    try:
        if request.method == 'GET':
            id = request.args.get('id')
            data = get_user(id)
            return jsonify({"data": data}), 200

        elif request.method == 'PUT':
            return jsonify({"message": "ok"}), 200

        elif request.method == 'POST':
            return jsonify({"message": "ok"}), 200

        elif request.method == 'DELETE':
            return jsonify({"message": "ok"}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400
    return jsonify({"isError": True, "code": "Invalid request method", "message": "Invalid HTTP request method is being used"}), 400


@app.route("/password/change", methods=['PUT'])
@cross_origin(origin='*')
@missing_param_handler
def password_route():
    """
    Parameters (json)
    -----------------
    JSON that contains the username, old password and
    new password entered by the user

        Format of the JSON
        ------------------
        {
            username: <username>,
            oldPassword: <oldPassword>,
            newPassword: <newPassword>
        }

    Return
    ------
    If the old password entered correctly
        resp: JSON
            JSON containing the successful message

            Format of the resp
            ------------------
            {
                message: <message>
            }

    Methods Allowed
    ---------------
    PUT
        Update the the password of the user
    """

    try:

        if request.method == 'PUT':
            username = request.json['username']
            oldPassword = request.json['oldPassword']
            newPassword = request.json['newPassword']
            
            user = USERS.get(username, None)

            if user is None:
                return jsonify({"isError": True, "code": "Non-existing User", "message": "There is no existing user which matches the username."}), HTTPStatusCode.BAD_REQUEST

            if user["password"] == oldPassword:
                return jsonify({"message": "ok"}), 200
            return jsonify({"isError": True, "code": "Invalid Credential", "message": "Wrong password."}), 403
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400
    return jsonify({"isError": True, "code": "Invalid request method", "message": "Invalid HTTP request method is being used"}), 400

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
            "interest_rate": round(row['interest_rate'], 4),
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

@app.route("/dashboard/currencydetail")
@cross_origin(origin='*')
@missing_param_handler
def get_dashboard_currencydetail():
    currency_code = request.args.get('currency_code', None)
    try: 
        latest_data = df[df['currency_code'] == currency_code].iloc[-1]
        data = {
            "updated_date": latest_data["date"].strftime("%d/%m/%Y"),
            "from_myr": round(latest_data["from_myr"], 4),
            "to_myr": round(latest_data["to_myr"], 4),
            "currency_code": currency_code,
            "country": CURRENCY_TO_COUNTRY.get(currency_code, "Missing")
        }
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/dashboard/rateconversion")
@cross_origin(origin='*')
@missing_param_handler
def get_dashboard_rateconversion():
    currency_code = request.args.get('currency_code', None)
    try: 
        latest_data = df[df['currency_code'] == currency_code].iloc[-1]
        myr_to_others = {}
        for currency_code in currency_codes:
            myr_to_others[currency_code] = df[df['currency_code'] == currency_code].iloc[-1]["from_myr"]
        data = {
            "currency_list": currency_codes,
            "to_myr": latest_data["to_myr"],
            "myr_to_others": myr_to_others
        }
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/dashboard/timetrend")
@cross_origin(origin='*')
@missing_param_handler
def get_dashboard_timetrend():
    currency_code = request.args.get('currency_code', None)
    try: 
        _df = df[df['currency_code'] == currency_code]
        _df = _df.groupby([pd.DatetimeIndex(_df.date).to_period('M')]).nth(0).reset_index(drop=True)
        _df['date'] = _df['date'].dt.strftime("%Y/%m/%d")
        data = {
            "gdp": _df[["date", "gdp"]].values.tolist(),
            "cpi": _df[["date", "cpi"]].values.tolist(),
            "interest_rate": _df[["date", "interest_rate"]].values.tolist(),
            "from_myr": _df[["date", "from_myr"]].values.tolist()
        }
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400

@app.route("/dashboard/actualpred")
@cross_origin(origin='*')
@missing_param_handler
def get_actual_predicted_graph():
    def _preprocess_data(df, malaysia_df, algorithm, adjust_y_intercept_interval=1, include_cpi=False, include_gdp=False, include_interest_rate=False):
        def propagate_data_to_daily(_df, columns_to_be_interpolated):
            prev = {}
            for idx, row in _df.iterrows():
                for col in columns_to_be_interpolated:
                    if idx == 0:
                        prev[col] = _df.at[0, col]
                    elif _df.at[idx, col] == prev[col]:
                        _df.at[idx, col] = None
                    else:
                        prev[col] = _df.at[idx, col]
            temp_df = _df.set_index(_df['date'])
            temp_df[['gdp', 'cpi', 'interest_rate']] = temp_df[['gdp', 'cpi','interest_rate']].resample('D').interpolate(method='linear')
            return temp_df

        def split_x_y(data, look_back, include_cpi=False, include_gdp=False, include_interest_rate=False):
            datax, datay = [],[]
            for i in range(len(data)-look_back):
                datax.append(data[i:(i + look_back), 0])
                if include_cpi:
                    datax[i] = np.append(datax[i], data[i + look_back, 1])
                if include_gdp:
                    datax[i] = np.append(datax[i], data[i + look_back, 2])
                if include_interest_rate:
                    datax[i] = np.append(datax[i], data[i + look_back, 3])
                datay.append(data[i + look_back, 4])
            return np.array(datax), np.array(datay)

        _df = df[['from_myr', 'cpi', 'gdp', 'interest_rate', 'date', 'year']]
        _df['month'] = _df.date.dt.month

        COLUMNS_TO_PROPAGATE = ['gdp', 'cpi', 'interest_rate']
        _df = propagate_data_to_daily(_df, COLUMNS_TO_PROPAGATE)
        _malaysia_df = propagate_data_to_daily(malaysia_df, COLUMNS_TO_PROPAGATE)

        COLUMNS_TO_CALCULATE_DIFFERENCE = ['gdp', 'cpi', 'interest_rate']
        for col in COLUMNS_TO_CALCULATE_DIFFERENCE:
            _df[col] = _malaysia_df[col] - _df[col]

        _df['target'] = _df['from_myr']
        _df['from_myr'] = _df['from_myr'].diff().fillna(0)

        from_myr_scaler = MinMaxScaler(feature_range=(-1, 1))
        _df[['from_myr']] = from_myr_scaler.fit_transform(_df[['from_myr']])
        _df[['cpi']] = MinMaxScaler(feature_range=(-1, 1)).fit_transform(_df[['cpi']])
        _df[['gdp']] = _df[['gdp']]/100
        _df[['interest_rate']] = _df[['interest_rate']]/100

        _df = _df[_df['year'] == 2021].reset_index(drop=True)

        points_to_adjust_y_intercept = []
        begin_idx = 0
        begin_month = None
        idx = 0
        for _, row in _df.iterrows():
            if idx == 0:
                begin_month = row['month']
            elif (row['month'] - begin_month) == adjust_y_intercept_interval:
                points_to_adjust_y_intercept.append({
                    'begin': begin_idx,
                    'end': idx + 1
                })
                begin_idx = idx + 1
                begin_month = row['month']
            idx = idx + 1

        _df = np.array(_df[['from_myr', 'cpi', 'gdp', 'interest_rate', 'target']]).reshape(-1, 5)

        x, y = split_x_y(_df, WINDOW_SIZE, include_cpi=include_cpi, include_gdp=include_gdp, include_interest_rate=include_interest_rate)

        if algorithm == "LSTM":
            x = x.reshape(x.shape[0], x.shape[1], 1)
        elif (algorithm == "POLYNOMIAL" or algorithm == "LINEAR" or 
            algorithm == "LASSO" or algorithm == "RIDGE"):
            x = x.reshape(x.shape[0], x.shape[1])

        _prev = x[-1]

        if algorithm == "POLYNOMIAL":   
            poly = PolynomialFeatures(degree=2, interaction_only=True)
            x = poly.fit_transform(x)

        y = y.reshape(y.shape[0], 1)
        return x, y, _prev, from_myr_scaler, points_to_adjust_y_intercept

    def _predict_data(model, algorithm, _x_test, _y_test, points_to_adjust_y_intercept, adjust_y_intercept = 1):

        _y_pred = np.array([]).reshape(-1, 1)

        if adjust_y_intercept and (algorithm == "LINEAR" or algorithm == "RIDGE"):
            begin = 0
            for point in points_to_adjust_y_intercept:
                temp_x_test = _x_test[point['begin'] : point['end']]
                temp_y_test = _y_test[point['begin'] : point['end']]
                temp_pred = model.predict(temp_x_test)
                temp_pred = np.array(temp_pred).reshape(-1, 1)

                model.intercept_ = model.intercept_ - np.mean(temp_pred - temp_y_test)

                if begin == 0:
                    temp_pred = model.predict(temp_x_test)
                    temp_pred = np.array(temp_pred).reshape(-1, 1)

                begin = point['end']
                _y_pred = np.append(_y_pred, temp_pred)

            temp_x_test = _x_test[begin : ]
            temp_y_test = _y_test[begin : ]
            if len(temp_x_test) != 0:
                temp_pred = model.predict(temp_x_test)
                temp_pred = np.array(temp_pred).reshape(-1, 1)

                model.intercept_ = model.intercept_ - np.mean(temp_pred - temp_y_test)
                # temp_pred = model.predict(temp_x_test)
                # temp_pred = np.array(temp_pred).reshape(-1, 1)
                _y_pred = np.append(_y_pred, temp_pred)
        else:
            _y_pred = model.predict(_x_test).reshape(-1, 1)

        return _y_pred, model

    def _forecast_next_n_days(model, scaler, input_data, prev_data, last_y_value, n):
        results = []
        model_inputs = input_data
        last_y = last_y_value
        if algorithm == "POLYNOMIAL":
            prev = prev_data
            poly = PolynomialFeatures(degree=2, interaction_only=True)

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
            # Track it in the windows
            if algorithm == "POLYNOMIAL":
                prev = prev[0]
                prev = np.insert(prev, WINDOW_SIZE, scaler.transform([[predicted_data[0] - last_y]])[0])
                prev.reshape(prev.shape[0], 1)
                prev = prev[1:]
            elif algorithm == "LSTM":
                model_inputs = model_inputs[0]
                model_inputs = np.insert(model_inputs, WINDOW_SIZE, scaler.transform([[predicted_data[0][0] - last_y]])[0])
                model_inputs.reshape(model_inputs.shape[0], 1)
                model_inputs = model_inputs[1:]
                last_y = predicted_data[0][0]
            else:
                model_inputs = model_inputs[0]
                model_inputs = np.insert(model_inputs, WINDOW_SIZE, scaler.transform([[predicted_data[0] - last_y]])[0])
                model_inputs.reshape(model_inputs.shape[0], 1)
                model_inputs = model_inputs[1:]
                last_y = predicted_data[0]

            results.append(predicted_data[0])
        results = np.array(results)
        results = results.reshape(results.shape[0], 1)
        return results

    # One month except for working days
    FORECAST_DAYS = 22
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

        _df = df[df['currency_code'] == currency_code].reset_index(drop=True)

        _df['year'] = _df.date.dt.year

        # Skip the first n, window size in which it can't make predictions on it
        date = _df[_df["year"] == 2021]["date"].tolist()[WINDOW_SIZE:]

        # Data Preprocessing
        x, y, prev_data, from_myr_scaler , points_to_adjust_y_intercept = _preprocess_data(_df, malaysia_df, algorithm, include_cpi=include_cpi, include_gdp=include_gdp)

        # To mark the beginning of forecast
        y_pred, model = _predict_data(model, algorithm, x, y, points_to_adjust_y_intercept)
        y_pred = y_pred.reshape(y_pred.shape[0], 1)

        # y_pred = y_pred[-90:]
        # y = y[-90:]
        # date = date[-90:]
        markLineIndex = len(date) - 1

        # Predict next n days currency rate
        future_forecast = _forecast_next_n_days(model, from_myr_scaler, x[-1], prev_data, y[-1][0], FORECAST_DAYS)
        y_pred = np.concatenate((y_pred, future_forecast))

        # Append date and data for actual for the 30 days forecast
        for _ in range(FORECAST_DAYS):
            date.append(date[-1] + timedelta(days=1))
            # Actual datapoints will be empty
            y = np.concatenate((y, np.array([[None]])))

        date = [d.strftime("%Y/%m/%d") for d in date]
        markLinePos = date[markLineIndex]
        data = {
            "actual": (np.vstack((date, y.flatten())).T).tolist(),
            "predicted": (np.vstack((date, y_pred.flatten())).T).tolist(),
            "markLinePos": markLinePos
        }
        return jsonify({"message": "Successful", "data": data}), 200
    except Exception as e:
        print(e)
        return jsonify({"isError": True, "code": "Error", "message": "Something wrong happens"}), 400