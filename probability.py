import yfinance as yf
from scipy.stats import norm
import numpy as np

def calculate_drop_probability(yahoo_finance_link, percentage_threshold):
    # Extract the stock ticker symbol from the Yahoo Finance link
    ticker = yahoo_finance_link.split("/")[-2].upper()

    # Fetch historical data for the stock
    stock_data = yf.download(ticker, period="max")

    # Calculate daily logarithmic returns
    stock_data["LogReturn"] = np.log(stock_data["Close"] / stock_data["Close"].shift(1))

    # Remove the first row with NaN value
    stock_data = stock_data.dropna()

    # Calculate mean and standard deviation of logarithmic returns
    mu = stock_data["LogReturn"].mean()
    sigma = stock_data["LogReturn"].std(ddof=1)

    # Calculate the probability using the normal distribution CDF
    threshold = -percentage_threshold / 100  # Convert percentage threshold to decimal
    prob_drop = norm.cdf(threshold, mu, sigma)

    return prob_drop

# Example usage
yahoo_finance_link = "https://finance.yahoo.com/quote/GOOGL/history?p=GOOGL"
percentage_threshold = 1.0  # Specify the desired percentage threshold
drop_prob = calculate_drop_probability(yahoo_finance_link, percentage_threshold)
print(f"The probability of the stock price dropping over {percentage_threshold}% in a day is: {drop_prob:.2%}")
