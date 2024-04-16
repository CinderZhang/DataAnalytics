# LSTM for time series prediction

# %% Import necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import yfinance as yf

# %% Function to organize data for LSTM
def organize_data(sequence_data, history_length=1):
    input_data, target_data = [], []
    for idx in range(len(sequence_data)-history_length-1):
        fragment = sequence_data[idx:(idx+history_length), 0]
        input_data.append(fragment)
        target_data.append(sequence_data[idx + history_length, 0])
    return np.array(input_data), np.array(target_data)

#%% Main function to execute the time series prediction
def lstm_stock_prediction(stock_symbol, start_date, end_date):
    # Fetch stock data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    # Compute daily returns
    stock_data['Returns'] = stock_data['Adj Close'].pct_change()
    stock_data.dropna(inplace=True)  # Remove any NaN values that pct_change might have caused

    # Plot the returns
    plt.figure(figsize=(10,6))
    plt.plot(stock_data['Returns'], label='Daily Returns')
    plt.title(f'{stock_symbol} Stock Returns')
    plt.legend()
    plt.show()

    # Preprocess the dataset
    returns_array = stock_data['Returns'].values.reshape(-1,1).astype('float32')
    scaler_toolbox = MinMaxScaler(feature_range=(0, 1))
    normalized_returns_data = scaler_toolbox.fit_transform(returns_array)

    # Split into training and testing sets
    partition_size = int(len(normalized_returns_data) * 0.67)
    train_partition, test_partition = normalized_returns_data[0:partition_size,:], normalized_returns_data[partition_size:len(normalized_returns_data),:]

    # Prepare dataset for LSTM
    history_length = 1
    train_input, train_target = organize_data(train_partition, history_length)
    test_input, test_target = organize_data(test_partition, history_length)

    # Reshape input for LSTM
    train_input = np.reshape(train_input, (train_input.shape[0], 1, train_input.shape[1]))
    test_input = np.reshape(test_input, (test_input.shape[0], 1, test_input.shape[1]))

    # Build and train LSTM model
    model = Sequential()
    model.add(LSTM(4, input_shape=(1, history_length)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(train_input, train_target, epochs=100, batch_size=1, verbose=2)

    # Make predictions
    train_prediction = model.predict(train_input)
    test_prediction = model.predict(test_input)

    # Invert predictions to original scale
    train_prediction = scaler_toolbox.inverse_transform(train_prediction)
    train_target_inverted = scaler_toolbox.inverse_transform([train_target])
    test_prediction = scaler_toolbox.inverse_transform(test_prediction)
    test_target_inverted = scaler_toolbox.inverse_transform([test_target])

    # Calculate and print Root Mean Squared Error
    train_rmse = np.sqrt(mean_squared_error(train_target_inverted[0], train_prediction[:,0]))
    test_rmse = np.sqrt(mean_squared_error(test_target_inverted[0], test_prediction[:,0]))
    print(f'Train RMSE: {train_rmse}')
    print(f'Test RMSE: {test_rmse}')

    # Correcting the plotting logic
    plt.figure(figsize=(10,6))
    adjusted_dates = stock_data.index[1:]  # Adjust dates to match the prediction lengths

    # Flatten predictions for plotting
    train_prediction_flat = train_prediction.flatten()
    test_prediction_flat = test_prediction.flatten()

    # Plot original returns with predictions
    plt.plot(adjusted_dates, stock_data['Returns'][1:], color='blue', label='Original Returns')
    plt.plot(adjusted_dates[:len(train_prediction_flat)], train_prediction_flat, color='red', label='Train Prediction')
    plt.plot(adjusted_dates[len(train_prediction_flat):len(train_prediction_flat)+len(test_prediction_flat)], test_prediction_flat, color='green', label='Test Prediction')

    plt.title(f'{stock_symbol} Stock Returns Prediction')
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.legend()
    plt.show()

#%% Example usage with WMT stock from Jan 1, 2019 to Dec 31, 2019
lstm_stock_prediction('NVDA', '2020-08-01', '2024-03-31')

# %%
