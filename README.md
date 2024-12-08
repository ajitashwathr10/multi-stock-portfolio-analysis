# Multi Stock Portfolio Analysis

## Overview
Stock Market Analysis Toolkit is a sophisticated Python-based financial analysis library designed to provide in-depth insights into stock market performance, portfolio management, and investment strategy evaluation.

## Key Features
1. Comprehensive Data Retrieval
   - Fetch historical stock data for multiple tickers
   - Flexible date range selection
   - Access to additional stock metadata (company info, recommendations, earnings)

2. Advanced Technical Indicators
   - Multiple Moving Averages
       - Simple Moving Average (SMA)
       - Exponential Moving Average (EMA)

   - Momentum Indicators
       - Moving Average Convergence Divergence (MACD)

   - Volatility Analysis
       - Rolling Volatility Calculation
       - Z-Score Analysis
        
3. Portfolio Performance Metrics
   - Total Return Calculation
   - Annualized Returns
   - Sharp Ratio
   - Maximum Drawdown
   - Risk-Adjusted Performance Metrics

4. Interactive Visualization
   - Comprehensive Plotly-based interactive charts
   - Multiple subplot analysis
      - Candlestick price chart
      - Moving averages overlay
      - MACD analysis
      - Volatility tracking

## Installation
### Prerequisites
- Python 3.12+
- pip package manager

### Required Libraries
```python
pip install yfinance pandas plotly scipy numpy
```

### Usage Example
```python
from advanced_stock_analyzer import AdvancedStockAnalyzer
```

# Define stocks, date range
```python
tickers = ['AAPL', 'GOOGL', 'MSFT']
start_date = '2023-01-01'
end_date = '2024-01-01'
```

### Initialize Analyzer
```python
analyzer = AdvancedStockAnalyzer(tickers, start_date, end_date)
```

### Generate Portfolio Analysis
```python
portfolio_metrics = analyzer.portfolio_analysis()
```

### Visualize Individual Stock Analysis
```python
for ticker in tickers:
    fig = analyzer.visualize_advanced_analysis(ticker)
    fig.write_html(f'{ticker}_analysis.html')
```

## Detailed Analysis Capabilities
### Technical Analysis
- Moving Averages:
   - Identify trend directions
   - Detect potential support and resistance levels
   - Generate trading signals
     
- MACD Analysis:
   - Momentum indicator
   - Identifies trend changes
   - Provides buy/sell signal generation

- Volatility Tracking:
   - Measure stock price fluctuations
   - Assess market risk
   - Compare stock stability
     
### Performance Metrics
- Sharpe Ratio:
   - Measures risk-adjusted return
   - Compares portfolio return against risk-free rate
   - Higher ratio indicates better risk-adjusted performance

- Maximum Drawdown
   - Calculates the largest peak-to-trough decline
   - Measures potential downside risk
   - Critical for understanding investment risk

## Output and Visualization
The toolkit generates:
   - Detailed portfolio performance metrics
   - Interactive HTML visualizations
   - Comprehensive stock analysis reports

### Visualization Components
   - Candlestick price chart
   - Exponential Moving Averages (20 and 50-day)
   - MACD Line and Signal Line
   - MACD Histogram
   - Rolling Volatility Tracking

## Advanced Use Cases
  - Investment Strategy Development
  - Portfolio Risk Management
  - Algorithmic Trading Research
  - Financial Data Analysis
  - Investment Performance Tracking

## Customization Options
  - Adjust risk-free rate
  - Modify technical indicator parameters
  - Add custom financial metrics
  - Extend visualization capabilities

## Limitations and Disclaimer
  - Data accuracy depends on yfinance API
  - Past performance doesn't guarantee future results
  - Recommended to combine with fundamental analysis
  - Not financial advice - for educational purposes

## Contributing
Contributions are welcome! Please:
  - Fork the repository
  - Create feature branches
  - Submit pull requests
  - Follow PEP 8 guidelines
