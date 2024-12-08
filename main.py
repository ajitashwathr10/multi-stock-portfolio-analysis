import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def fetch_stock_data(ticker, start_date, end_date):

    """
    Fetch historical stock data

    Args:
        ticker (str): Ticker symbol of the stock
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.DataFrame: DataFrame containing the historical stock data
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start = start_date, end = end_date)
    return data

def calculate_returns(data):
    """
    Calculate returns for each stock

    Args:
        data (pd.DataFrame): DataFrame containing the historical stock data

    Returns:
        pd.DataFrame: DataFrame containing the returns for each stock
    """
    returns = data.pct_change()
    return returns

def calculate_technical_indicators(data):
    """
    Calculate technical indicators for stock analysis

    Args:
        data (pd.DataFrame): DataFrame containing the historical stock data

    Returns:            
        pd.DataFrame: DataFrame containing the calculated technical indicators
    """

    #Simple Moving Average
    data['SMA_20'] = data['Close'].rolling(window = 20).mean()
    data['SMA_50'] = data['Close'].rolling(window = 50).mean()
    data['SMA_200'] = data['Close'].rolling(window = 200).mean()

    #Bollinger Bands
    data['BB_Middle'] = data['Close'].rolling(window = 20).mean()
    data['BB_Upper'] = data['BB_Middle'] + 2 * data['Close'].rolling(window = 20).std()
    data['BB_Lower'] = data['BB_Middle'] - 2 * data['CLose'].rolling(window = 20).std()

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window = 14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window = 14).mean()

    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def visualize_stock_analysis(data, ticker):
    
