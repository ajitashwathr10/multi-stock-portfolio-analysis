import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy import stats

class AdvancedStockAnalyzer:
    def __init__(self, tickers, start_date, end_date):
        """
        Initialize stock analyzer with multiple tickers and date range.
        
        Args:
            tickers (list): List of stock ticker symbols
            start_date (str): Start date for data retrieval
            end_date (str): End date for data retrieval
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = self.fetch_stock_data()
    
    def fetch_stock_data(self):
        """
        Fetch historical stock data for multiple tickers.
        
        Returns:
            dict: Dictionary of DataFrames with stock data
        """
        stock_data = {}
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            data = stock.history(start = self.start_date, end = self.end_date)
            stock_data[ticker] = {
                'price_data': data,
                'info': stock.info,
                'recommendations': stock.recommendations,
                'earnings': stock.earnings
            }
        
        return stock_data
    
    def calculate_advanced_indicators(self, ticker):
        """
        Calculate advanced technical and statistical indicators.
        
        Args:
            ticker (str): Stock ticker symbol
        
        Returns:
            pandas.DataFrame: Data with advanced indicators
        """
        data = self.stock_data[ticker]['price_data'].copy()
        data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
        
        # MACD (Moving Average Convergence Divergence)

        data['MACD_Line'] = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()

        data['Signal_Line'] = data['MACD_Line'].ewm(span=9, adjust=False).mean()
        data['MACD_Histogram'] = data['MACD_Line'] - data['Signal_Line']
        data['Daily_Returns'] = data['Close'].pct_change()
        data['Rolling_Volatility'] = data['Daily_Returns'].rolling(window=20).std() * np.sqrt(252)
        data['Z_Score'] = stats.zscore(data['Close'])
        data['Cumulative_Return'] = (1 + data['Daily_Returns']).cumprod() - 1
        
        return data
    
    def portfolio_analysis(self):
        """
        Perform portfolio-level analysis.
        
        Returns:
            dict: Portfolio-level metrics and analysis
        """
        portfolio_data = {}
        for ticker in self.tickers:
            data = self.calculate_advanced_indicators(ticker)
            
            portfolio_data[ticker] = {
                'Total_Return': data['Cumulative_Return'].iloc[-1],
                'Annualized_Return': (1 + data['Cumulative_Return'].iloc[-1]) ** (252 / len(data)) - 1,
                'Volatility': data['Rolling_Volatility'].mean(),
                'Sharpe_Ratio': self._calculate_sharpe_ratio(data['Daily_Returns']),
                'Max_Drawdown': self._calculate_max_drawdown(data['Close'])
            }
        
        return portfolio_data
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """
        Calculate Sharpe Ratio for a stock.
        
        Args:
            returns (pd.Series): Daily returns
            risk_free_rate (float): Annual risk-free rate
        
        Returns:
            float: Sharpe Ratio
        """
        annualized_return = (1 + returns.mean()) ** 252 - 1
        annualized_volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
        return sharpe_ratio
    
    def _calculate_max_drawdown(self, prices):
        """
        Calculate maximum drawdown for a stock.
        
        Args:
            prices (pd.Series): Stock closing prices
        
        Returns:
            float: Maximum drawdown percentage
        """
        cumulative_max = prices.cummax()
        drawdown = (prices - cumulative_max) / cumulative_max
        return drawdown.min()
    
    def visualize_advanced_analysis(self, ticker):
        """
        Create comprehensive interactive visualization.
        
        Args:
            ticker (str): Stock ticker symbol
        
        Returns:
            plotly.graph_objs.Figure: Advanced stock analysis visualization
        """
        data = self.calculate_advanced_indicators(ticker)
        fig = make_subplots(
            rows = 3, cols = 1, 
            shared_xaxes = True, 
            vertical_spacing = 0.02,
            row_heights = [0.5, 0.25, 0.25]
        )
        
        candlestick = go.Candlestick(
            x = data.index,
            open = data['Open'],
            high = data['High'],
            low = data['Low'],
            close = data['Close'],
            name = f'{ticker} Price'
        )
        
        ema_20 = go.Scatter(
            x = data.index, 
            y = data['EMA_20'], 
            mode = 'lines', 
            name = 'EMA 20', 
            line = dict(color = 'blue', width = 2)
        )
        
        ema_50 = go.Scatter(
            x = data.index, 
            y = data['EMA_50'], 
            mode = 'lines', 
            name = 'EMA 50', 
            line = dict(color = 'red', width = 2)
        )

        macd_line = go.Scatter(
            x = data.index, 
            y = data['MACD_Line'], 
            mode = 'lines', 
            name = 'MACD Line', 
            line = dict(color = 'blue', width = 1)
        )
        
        signal_line = go.Scatter(
            x = data.index, 
            y = data['Signal_Line'], 
            mode = 'lines', 
            name = 'Signal Line', 
            line = dict(color = 'red', width = 1)
        )
        
        macd_histogram = go.Bar(
            x = data.index, 
            y = data['MACD_Histogram'], 
            name = 'MACD Histogram',
            marker_color = data['MACD_Histogram'].apply(lambda x: 'green' if x > 0 else 'red')
        )
        
        volatility = go.Scatter(
            x = data.index, 
            y = data['Rolling_Volatility'], 
            mode = 'lines', 
            name = 'Rolling Volatility', 
            line = dict(color='purple', width=2)
        )
        
        fig.add_trace(candlestick, row = 1, col = 1)
        fig.add_trace(ema_20, row = 1, col = 1)
        fig.add_trace(ema_50, row = 1, col = 1)
        fig.add_trace(macd_line, row = 2, col = 1)
        fig.add_trace(signal_line, row = 2, col = 1)
        fig.add_trace(macd_histogram, row = 2, col = 1)
        fig.add_trace(volatility, row = 3, col = 1)
        
        fig.update_layout(
            title = f'{ticker} Stock Analysis',
            height = 800,
            xaxis_rangeslider_visible = False
        )
        return fig

def main():
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    
    analyzer = AdvancedStockAnalyzer(tickers, start_date, end_date)

    portfolio_metrics = analyzer.portfolio_analysis()
    print("Portfolio Metrics:")
    for ticker, metrics in portfolio_metrics.items():
        print(f"\n{ticker} Performance:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.2%}")

    for ticker in tickers:
        fig = analyzer.visualize_advanced_analysis(ticker)
        fig.write_html(f'{ticker}stock_analysis.html')

if __name__ == "__main__":
    main()