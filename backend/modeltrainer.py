# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import math
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.linear_model import LinearRegression, Ridge, Lasso
import os
import joblib

# Remove the false warning
pd.options.mode.chained_assignment = None

class ModelTrainer():

  ALGORITHMS_AVAILABLE = ["LSTM", "POLYNOMIAL", "LINEAR", "LASSO", "RIDGE"]

  def __init__(self, currency_code, model_filename, model_save_path, 
               model_with_cpi, model_with_gdp, model_with_gdp_and_cpi, model_only_rate,
               algorithm="LSTM",  window_size=3, include_cpi=False, include_gdp=False, include_interest_rate=False, 
               num_of_neuron=100, num_of_iteration=10, dropout=0, alpha=0, test_n_months=12,
               compute_difference=True, predict_change=False, same_scale=False):
    self.COLUMNS_TO_PROPAGATE = ['gdp', 'cpi', 'interest_rate']
    self.COLUMNS_TO_CALCULATE_DIFFERENCE = ['gdp', 'cpi', 'interest_rate']
    self.same_scale = same_scale

    self.currency_code = currency_code
    self.scaler = None
    self.model = None
    self.compute_difference = compute_difference
    self.predict_change = predict_change

    self.window_size = window_size
    self.algorithm = algorithm
    self.include_cpi = include_cpi
    self.include_gdp = include_gdp
    self.include_interest_rate = include_interest_rate
    self.num_of_feature = self.window_size + self.include_cpi + self.include_gdp + self.include_interest_rate

    self.num_of_neuron = num_of_neuron
    self.num_of_iteration = num_of_iteration
    self.dropout = dropout

    self.alpha = alpha

    # Models saving directory
    self.model_with_cpi = model_with_cpi
    self.model_with_gdp = model_with_gdp
    self.model_with_gdp_and_cpi = model_with_gdp_and_cpi
    self.model_only_rate = model_only_rate
    self.model_filename = model_filename
    self.graph_filename = ""
    self.model_save_path = model_save_path

    self.test_n_months = test_n_months

  # Setter for the Parameters
  def set_algorithm(self, algorithm):
    self.algorithm = algorithm

  def set_window_size(self, window_size):
    self.window_size = window_size

  def set_currency_code(self, currency_code):
    self.currency_code = currency_code
    
  def set_num_of_neuron(self, num_of_neuron):
    self.num_of_neuron = num_of_neuron

  def set_num_of_iteration(self, num_of_iteration):
    self.num_of_iteration = num_of_iteration

  def set_include_cpi(self, include_cpi):
    self.include_cpi = include_cpi
    self.num_of_feature = self.window_size + self.include_cpi + self.include_gdp + self.include_interest_rate

  def set_include_gdp(self, include_gdp):
    self.include_gdp = include_gdp
    self.num_of_feature = self.window_size + self.include_cpi + self.include_gdp + self.include_interest_rate

  def set_include_interest_rate(self, include_interest_rate):
    self.include_interest_rate = include_interest_rate
    self.num_of_feature = self.window_size + self.include_cpi + self.include_gdp + self.include_interest_rate

  ##################
  # PUBLIC METHODS #
  ##################
  def introduce(self):
    print("MODEL ATTRIBUTES")
    print("----------------")
    print("Window Size: " + str(self.window_size))
    print("Currency Code: " + str(self.currency_code))
    print("Algorithm: " + self.algorithm)
    print("Scaling Method: " + "Min Max Scaling")
    print("CPI Included: " + str(self.include_cpi))
    print("GDP Included: " + str(self.include_gdp))
    print("Number of Features: " + str(self.num_of_feature))
    if self.algorithm == "LSTM":
      print("Number of Iterations: " + str(self.num_of_iteration))
      print("Number of Neurons in Hidden Layer: " + str(self.num_of_neuron))
  
  def build(self, df, malaysia_df, only_show_evaluation=False):
    """
    Parameters
    ----------
    df: Pandas Dataframe
      The dataframe storing the values of the targeted currency and country
    
    malaysia_df: Pandas Dataframe
      The dataframe storing the values of the Malaysia and its currency

    only_show_evaluation: Boolean
      It decides whether or not to show the progresses when building the model.
      If this value is True, it will only printed out the evaluations of the model.

    Description
    -----------
    Train the model, evaluate the model and save it inside the class object
    """
    main_evaluation_metric = -99999
    target = -99998
    while main_evaluation_metric < target:
      self.num_of_feature = self.window_size + self.include_cpi + self.include_gdp + self.include_interest_rate
      self.introduce()
      print("\n\n")

      if self.compute_difference:
        x_test, x_train, y_test, y_train, last = self._preprocess_data(df, malaysia_df, verbose=not only_show_evaluation)
      else:
        x_test, x_train, y_test, y_train = self._preprocess_data(df, malaysia_df, verbose=not only_show_evaluation)

      if not only_show_evaluation:
        print("\n\n")

      self._train_model(x_train, y_train, verbose=not only_show_evaluation)
      if not only_show_evaluation:
        print("\n\n")

      if self.compute_difference:
        main_evaluation_metric = self._evaluate_model(x_test, y_test, last=last)
      else:
        main_evaluation_metric = self._evaluate_model(x_test, y_test)
      print("\n\n")

  def save(self):
    """
    Description
    -----------
    Save 2 files in the folder for the respective currency code and algorithm
    1) Model file
    2) Prediction vs Actual Graph (The filename consists of the model performance 
    such as R square and MSE)
    """
    if self.model is None:
      print("There is no model being trained yet.")
      return
    
    directory = os.path.join(self.model_save_path, self.currency_code, self.algorithm)
    if self.include_cpi and self.include_gdp:
      directory = os.path.join(directory, self.model_with_gdp_and_cpi)
    elif self.include_cpi:
      directory = os.path.join(directory, self.model_with_cpi)
    elif self.include_gdp:
      directory = os.path.join(directory, self.model_with_gdp)
    else:
      directory = os.path.join(directory, self.model_only_rate)

    ###
    ### Clear the directory
    ###
    print("Clearing the folder to save the models...")

    if os.path.exists(directory):
      for filename in os.listdir(directory):
        os.remove(os.path.join(directory, filename))
    else:
      os.makedirs(directory)

    print("Done clearing.")
        
    ###
    ### Save it
    ###
    model_filename = os.path.join(directory, self.model_filename)
    img_filename = os.path.join(directory, self.graph_filename)

    print("Saving model...")
    if self.algorithm == "LSTM":
      self.model.save(model_filename, save_format="h5")
    else:
      joblib.dump(self.model, model_filename)
    print("Done saving model.")

    print("Saving prediction vs actual graph...")
    plt.savefig(img_filename)
    print("Done saving.")


  ###################
  # PRIVATE METHODS #
  ###################
  def _preprocess_data(self, df, malaysia_df, verbose=True):
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

      _df = _df.set_index(_df['date'])
      _df[['gdp', 'cpi', 'interest_rate']] = _df[['gdp', 'cpi','interest_rate']].resample('D').interpolate(method='linear')
      return _df

    def _split_train_test(data, last_n_months):
      now = datetime.now()
      month = int(now.strftime("%m")) - last_n_months
      year = int(now.strftime("%Y"))
      while month <= 0:
        month = month + 12
        year = year - 1
      test_start_month = month + 1
      test_start_year = year
      if test_start_month > 12:
        test_start_month = 1
        test_start_year = year + 1
        
      return data[:f"{year}-{month}-31"], data[f"{test_start_year}-{test_start_month}-01":]

    def _split_x_y(data, look_back, include_cpi=False, include_gdp=False, include_interest_rate=False):
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
    
    if verbose:
      print("PREPROCESSING DATA")
      print("------------------")
      
    ### 
    ### Propagating Data
    ###   
    if verbose:
      print("Propagating yearly and monthly data to daily...")
    
    _df = df
    _df = propagate_data_to_daily(_df, self.COLUMNS_TO_PROPAGATE)
    _malaysia_df = propagate_data_to_daily(malaysia_df, self.COLUMNS_TO_PROPAGATE)

    if verbose:
      print("Done propagating.")

    ### 
    ### Constructing Features
    ###   
    if verbose:
      print("Constructing Features...")
    
    _df['target'] = _df['from_myr']
    last = _df['from_myr']

    for col in self.COLUMNS_TO_CALCULATE_DIFFERENCE:
      _df[col] = _malaysia_df[col] - _df[col]

    if self.compute_difference:
      _df['from_myr'] = _df['from_myr'].diff().fillna(0)
      if self.predict_change:
        _df['target'] = _df['from_myr']
      # rolling = _df['from_myr'].rolling(window=3)
      # _df['from_myr'] = rolling.mean().fillna(0)

    if verbose:
      print("Done Constructing.")

    ###
    ### Scaling the data
    ###
    if verbose:
      print("Performing Min Max Scaling...")

    self.scaler = MinMaxScaler()
    _df[['from_myr']] = self.scaler.fit_transform(_df[['from_myr']])
    _df[['cpi']] = MinMaxScaler().fit_transform(_df[['cpi']])
    _df[['gdp']] = MinMaxScaler().fit_transform(_df[['gdp']])
    _df[['interest_rate']] = MinMaxScaler().fit_transform(_df[['interest_rate']])
    
    if verbose:
      print("Done Scaling.")

    ### 
    ### Split Dataset
    ###
    if verbose:
      print("Splitting Dataset...")

    _train, _test = _split_train_test(_df, self.test_n_months)
    last = last[len(_train) - 1]

    if verbose:
      print("Done Splitting.")
    
    ###
    ### Extracting Features
    ###
    if verbose:
      print("Extracting Features...")
      
    _train = np.array(_train[['from_myr', 'cpi', 'gdp', 'interest_rate', 'target']]).reshape(-1, 5)
    _test = np.array(_test[['from_myr', 'cpi', 'gdp', 'interest_rate', 'target']]).reshape(-1, 5)

    if self.algorithm == "XGBOOST":
      if not self.include_cpi:
        _test.drop('cpi', inplace=True, axis=1)
        _train.drop('cpi', inplace=True, axis=1)

      if not self.include_gdp:
        _test.drop('gdp', inplace=True, axis=1)
        _train.drop('gdp', inplace=True, axis=1)

      _x_test = _test.drop('from_myr', axis=1).drop('target', axis=1)
      _y_test = _test.target
      _x_train = _train.drop('from_myr', axis=1).drop('target', axis=1)
      _y_train = _train.target
    else:
      _x_test, _y_test = _split_x_y(_test, self.window_size, self.include_cpi, self.include_gdp, self.include_interest_rate)
      _x_train, _y_train = _split_x_y(_train, self.window_size, self.include_cpi, self.include_gdp, self.include_interest_rate)

    if verbose:
      print("Done Extracting.")

    ### 
    ### Reshape Dataset
    ###
    if verbose:
      print("Reshaping Dataset for LSTM usage...")

    if self.algorithm == "LSTM":
      _x_train = _x_train.reshape(_x_train.shape[0], _x_train.shape[1], 1)
      _x_test = _x_test.reshape(_x_test.shape[0], _x_test.shape[1], 1)
    elif (self.algorithm == "POLYNOMIAL" or self.algorithm == "LINEAR" or 
          self.algorithm == "LASSO" or self.algorithm == "RIDGE"):
      _x_train = _x_train.reshape(_x_train.shape[0], _x_train.shape[1])
      _x_test = _x_test.reshape(_x_test.shape[0], _x_test.shape[1])

    if verbose:
      print("Done Reshaping.")

    ###
    ### Output Datasets
    ### 
    if verbose:
      print("X test set shape: " + str(_x_test.shape))
      print("Y test set shape: " + str(_y_test.shape))
      print("X train set shape: " + str(_x_train.shape))
      print("Y train set shape: " + str(_y_train.shape))
    
    if self.compute_difference:
      return _x_test, _x_train, _y_test, _y_train, last
    else:
      return _x_test, _x_train, _y_test, _y_train

  def _train_model(self, x_train, y_train, verbose=True):
    if verbose:
      print("TRAINING MODEL")
      print("--------------")

    if self.algorithm == "POLYNOMIAL":
      ###
      ### Make Polynomial Features
      ###
      if verbose:
        print("Making Polynomial Features...")

      poly = PolynomialFeatures(degree=2, interaction_only=True)
      x_poly = poly.fit_transform(x_train)

      if verbose:
        print("Done Making.")

      model = LinearRegression()

      ###
      ### Fit Model to Dataset
      ###
      if verbose:
        print("Fitting to Dataset...")

      model.fit(x_poly, y_train)
      
      if verbose:
        print("Done Fitting.")

    elif self.algorithm == "LINEAR":
      
      model = LinearRegression()

      ###
      ### Fit Model to Dataset
      ###
      if verbose:
        print("Fitting to Dataset...")

      model.fit(x_train, y_train)
      
      if verbose:
        print("Done Fitting.")

    elif self.algorithm == "RIDGE":
      model = Ridge(alpha=self.alpha)

      ###
      ### Fit Model to Dataset
      ###
      if verbose:
        print("Fitting to Dataset...")

      model.fit(x_train, y_train)
      
      if verbose:
        print("Done Fitting.")
    
    elif self.algorithm == "LASSO":
      model = Lasso(alpha=self.alpha)

      ###
      ### Fit Model to Dataset
      ###
      if verbose:
        print("Fitting to Dataset...")

      model.fit(x_train, y_train)
      
      if verbose:
        print("Done Fitting.")
      
    elif self.algorithm == "LSTM":
      ###
      ### Build Layers Structure
      ###
      if verbose:
        print("Building Layers...")

      model = Sequential()
      # Input Layer
      model.add(LSTM(self.num_of_neuron, activation='relu', 
                     input_shape=(self.num_of_feature, 1)))
      
      model.add(Dropout(self.dropout))
      
      # Output Layer
      model.add(Dense(1))
      
      if verbose:
        print("Done Building.")

      ### 
      ### Compile Model
      ###
      if verbose:
        print("Compiling Model...")

      model.compile(optimizer='adam', loss='mse')

      if verbose:
        print("Done Compiling.")

      ###
      ### Fit Model to Dataset
      ###
      if verbose:
        print("Fitting to Dataset...")

      model.fit(x_train, y_train, validation_split=0.2, epochs = self.num_of_iteration, batch_size=30)

      if verbose:
        print("Done Fitting.")
        
    elif self.algorithm == "XGBOOST":
      data = xgb.DMatrix(x_train,label=y_train) 
      #train the data
      model = xgb.train({}, data)

    self.model = model
    
  def _evaluate_model(self, x_test, y_test, verbose=True, last=None):
    def _plot_actual_predict_graph(y_test, y_pred, currency_code, window_size):
      max_bound = max(y_test)
      min_bound = min(y_test)
      max_bound = max_bound + 0.05*max_bound
      min_bound = min_bound - 0.05*min_bound
      plt.figure(figsize=(15, 10))
      plt.subplot(2, 1, 1)
      if self.same_scale:
        plt.ylim([min_bound, max_bound])
      plt.title(f'Foreign Exchange Rate of MYR-{currency_code} with Window Size of {window_size} ({self.algorithm})')
      plt.plot(y_test, label = 'Actual', color = 'blue')
      plt.plot(y_pred, label = 'Predicted', color = 'orange')
      plt.legend()

    def _plot_feature_importance():
      _index = []
      for i in range(self.window_size):
        _index.append("Rate (" + str(self.window_size - i) + " Days Ago)")

      if self.include_cpi:
        _index.append("CPI")

      if self.include_gdp:
        _index.append("GDP Growth Rate")

      if self.include_interest_rate:
        _index.append("Interest Rate")

      if self.algorithm == "LSTM" or self.algorithm == "XGBOOST":
        return

      total = sum(map(abs, self.model.coef_))
      if self.algorithm == "POLYNOMIAL":
        feat_importances = pd.Series(self.model.coef_/total)
      else:
        feat_importances = pd.Series(self.model.coef_/total, index=_index)

      plt.subplot(2, 1, 2)

      plt.title(f'Feature Importance')
      feat_importances.plot(kind='barh')

    if verbose:
      print("EVALUATING MODEL")
      print("----------------")

    ###
    ### Do Predictions
    ###
    if verbose:
      print("Predicting on Test Set...")

    _x_test = x_test
    if self.algorithm == "POLYNOMIAL":
      poly = PolynomialFeatures(degree=2, interaction_only=True)
      _x_test = poly.fit_transform(x_test)
    elif self.algorithm == "XGBOOST":
      _x_test = xgb.DMatrix(x_test)

    _y_pred = self.model.predict(_x_test)
    _y_pred = np.array(_y_pred).reshape(-1, 1)
    _y_test = np.array(y_test).reshape(-1, 1)

    if last is not None and self.predict_change:
      _prev_pred = last
      _prev_actual = last
      for i in range(_y_pred.shape[0]):
        _y_pred[i][0] = _y_pred[i][0] + _prev_pred
        _prev_pred = _y_pred[i][0]
        _y_test[i][0] = _y_test[i][0] + _prev_actual
        _prev_actual = _y_test[i][0]
      _y_pred = np.append(np.array([[last]]), _y_pred )
      _y_test = np.append(np.array([[last]]), _y_test )

    if verbose:
      print("Done Predicting.")

    ### 
    ### Calculating Metrics
    R2 = round(r2_score(_y_test, _y_pred), 4)
    RMSE = round(math.sqrt(mean_squared_error(_y_test, _y_pred)), 4)
    MAE = round(mean_absolute_error(_y_test, _y_pred), 4)
    if verbose:
      print(f"R SQUARE: {R2}")
      print(f"RMSE: {RMSE}")
      print(f"MAE: {MAE}")

    self.graph_filename = f"R2={R2},RMSE={RMSE},MAE={MAE}.png"

    ###
    ### Plot Prediction vs Actual Graph
    ###
    if verbose:
      print("Plotting Actual & Predict Graph...")

    _plot_actual_predict_graph(_y_test, _y_pred, self.currency_code, self.window_size)
    _plot_feature_importance()
    
    if verbose:
      print("Done Plotting.")

    return R2

    