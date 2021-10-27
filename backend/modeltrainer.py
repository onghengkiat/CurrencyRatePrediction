# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
from sklearn.preprocessing import MinMaxScaler
import joblib
from keras.models import Sequential
from keras.layers import Dense, LSTM
import os
from constants import MODEL_FILENAME, SCALAR_FILENAME, GRAPH_FILENAME, MODEL_SAVE_PATH

class ModelTrainer():

  def __init__(self, currency_code, window_size=3):
    self.window_size = window_size
    self.currency_code = currency_code
    self.scaler = None
    self.model = None
    self.algorithm = "LSTM"

  def set_window_size(self, window_size):
    self.window_size = window_size

  def set_currency_code(self, currency_code):
    self.currency_code = currency_code

  def introduce(self):
    print("MODEL ATTRIBUTES")
    print("----------------")
    print("Window Size: " + str(self.window_size))
    print("Currency Code: " + str(self.currency_code))
    print("Algorithm: " + self.algorithm)
    print("Scaling Method: " + "Min Max Scaling")

  def build(self, df):
    self.introduce()
    print("\n\n")

    x_test, x_train, y_test, y_train = self._preprocess_data(df)
    print("\n\n")

    self._train_model(x_train, y_train)
    print("\n\n")

    self._evaluate_model(x_test, y_test)
    print("\n\n")

  def save(self):
    model_filename = os.path.join(MODEL_SAVE_PATH, self.currency_code, MODEL_FILENAME)
    scaler_filename = os.path.join(MODEL_SAVE_PATH, self.currency_code, SCALAR_FILENAME)
    img_filename = os.path.join(MODEL_SAVE_PATH, self.currency_code, GRAPH_FILENAME)

    self.model.save(model_filename, save_format="h5")
    joblib.dump(self.scaler, scaler_filename) 
    plt.savefig(img_filename)

  def _preprocess_data(self, df):
    def _split_train_test(data, test_size=0.2):
      total_size = len(data)
      stop_index = int(test_size*total_size)
      return data[:stop_index], data[stop_index:]

    def _split_x_y(data, look_back):
      datax, datay = [],[]
      for i in range(len(data)-look_back-1):
        datax.append(data[i:(i + look_back), 0])
        datay.append(data[i + look_back, 0])
      return np.array(datax), np.array(datay)
    
    print("PREPROCESSING DATA")
    print("------------------")
    _df = df[self.currency_code]
    _df = np.array(_df).reshape(-1,1)

    # Normallization
    print("Performing Min Max Scaling...")
    self.scaler = MinMaxScaler()
    _df = self.scaler.fit_transform(_df)
    print("Done Scaling.")

    # Split features and train test set
    print("Splitting Dataset...")
    _test, _train = _split_train_test(_df)
    _x_test, _y_test = _split_x_y(_test, self.window_size)
    _x_train, _y_train = _split_x_y(_train, self.window_size)
    print("Done Splitting.")

    # We need to add one more dimension to X, i.e Num of features in 1 sample of time step. as we are doing a univariate prediction which means number of features are 1 only
    print("Reshaping Dataset for LSTM usage...")
    _x_train = _x_train.reshape(_x_train.shape[0], _x_train.shape[1], 1)
    _x_test = _x_test.reshape(_x_test.shape[0], _x_test.shape[1], 1)
    print("Done Reshaping.")

    print("X test set shape: " + str(_x_test.shape))
    print("Y test set shape: " + str(_y_test.shape))
    print("X train set shape: " + str(_x_train.shape))
    print("Y train set shape: " + str(_y_train.shape))
    return _x_test, _x_train, _y_test, _y_train

  def _train_model(self, x_train, y_train):
    print("TRAINING MODEL")
    print("--------------")
    print("Building Layers...")
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(self.window_size, 1)))
    model.add(Dense(1))
    print("Done Building.")

    print("Compiling Model...")
    model.compile(optimizer='adam', loss='mse')
    print("Done Compiling.")

    print("Fitting to Dataset...")
    model.fit(x_train, y_train, epochs = 10, batch_size=1)
    print("Done Fitting.")

    self.model = model
    
  def _evaluate_model(self, x_test, y_test):
    def _plot_actual_predict_graph(y_test, y_pred, currency_code, window_size):
      # Visualizing the results
      plt.figure(figsize=(10, 5))
      plt.title(f'Foreign Exchange Rate of MYR-{currency_code} with Window Size of {window_size}')
      plt.plot(y_test, label = 'Actual', color = 'g')
      plt.plot(y_pred, label = 'Predicted', color = 'r')
      plt.legend()

    print("EVALUATING MODEL")
    print("----------------")

    print("Predicting on Test Set...")
    _y_pred = self.model.predict(x_test)
    _y_pred = self.scaler.inverse_transform(_y_pred)
    _y_test = np.array(y_test).reshape(-1, 1)
    _y_test = self.scaler.inverse_transform(_y_test)
    print("Done Predicting.")

    print("Plotting Actual & Predict Graph")
    _plot_actual_predict_graph(_y_test, _y_pred, self.currency_code, self.window_size)
    print("Done Plotting.")