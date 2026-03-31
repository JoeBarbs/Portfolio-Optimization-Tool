import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="Portfolio Optimizer", layout="wide")
st.title("📊 Portfolio Optimization Tool")
st.write("Optimize a portfolio using real market data, risk, and return.")

# -------------------------
# SIDEBAR INPUTS
# -------------------------
st.sidebar.header("Inputs")

tickers_input = st.sidebar.text_input(
    "Enter tickers (comma separated)",
    "AAPL,MSFT,GOOGL,NVDA,AMZN"
)

tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip() != ""]

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"))

risk_free_rate = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 10.0, 2.0) / 100
max_weight = st.sidebar.slider("Max weight per stock (%)", 10, 100, 50) / 100

# -------------------------
# LOAD DATA (ROBUST VERSION)
# -------------------------
@st.cache_data
def load_data(tickers, start, end):
    raw = yf.download(tickers, start=start, end=end)

    if raw.empty:
        return None

    # Handle multi-index columns safely
    if isinstance(raw.columns, pd.MultiIndex):
        if "Adj Close" in raw.columns.levels[0]:
            data = raw["Adj Close"]
        elif "Close" in raw.columns.levels[0]:
            data = raw["Close"]
        else:
            return None
    else:
        # Single ticker case
        if "Adj Close" in raw.columns:
            data = raw["Adj Close"]
        elif "Close" in raw.columns:
            data = raw["Close"]
        else:
            return None

    # Ensure dataframe format
    if isinstance(data, pd.Series):
        data = data.to_frame()

    return data

data = load_data(tickers, start_date, end_date)

# -------------------------
# ERROR HANDLING
# -------------------------
if data is None or data.empty:
    st.error("⚠️ Could not load stock data. Try different tickers.")
    st.stop()

returns = data.pct_change().dropna()

# Clean bad columns
returns = returns.dropna(axis=1, how='all')

if returns.shape[1] < 2:
    st.error("⚠️ Need at least 2 valid stocks.")
    st.stop()

# -------------------------
# CALCULATIONS
# -------------------------
mean_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

num_assets = len(mean_returns)

# -------------------------
# PORTFOLIO FUNCTIONS
# -------------------------
def portfolio_performance(weights):
    returns = np.dot(weights, mean_returns)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, volatility

def negative_sharpe(weights):
    r, v = portfolio_performance(weights)
    return -(r - risk_free_rate) / v

# -------------------------
# OPTIMIZATION
# -------------------------
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, max_weight) for _ in range(num_assets))
initial_weights = num_assets * [1. / num_assets]

optimized = minimize(
    negative_sharpe,
    initial_weights,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

opt_weights = optimized.x
opt_return, opt_vol = portfolio_performance(opt_weights)
opt_sharpe = (opt_return - risk_free_rate) / opt_vol

# -------------------------
# DISPLAY RESULTS
# -------------------------
st.subheader("📌 Optimal Portfolio Allocation")

weights_df = pd.DataFrame({
    "Ticker": mean_returns.index,
    "Weight (%)": opt_weights * 100
}).sort_values(by="Weight (%)", ascending=False)

st.dataframe(weights_df, use_container_width=True)

col1, col2, col3 = st.columns(3)

col1.metric("Expected Return", f"{opt_return*100:.2f}%")
col2.metric("Volatility", f"{opt_vol*100:.2f}%")
col3.metric("Sharpe Ratio", f"{opt_sharpe:.2f}")

# -------------------------
# EFFICIENT FRONTIER
# -------------------------
st.subheader("📈 Efficient Frontier")

results = []

for _ in range(3000):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)

    r, v = portfolio_performance(weights)
    results.append([v, r])

results = np.array(results)

fig, ax = plt.subplots()

ax.scatter(results[:, 0], results[:, 1], alpha=0.3)
ax.scatter(opt_vol, opt_return, color='red', s=100, label='Optimal')

ax.set_xlabel("Risk (Volatility)")
ax.set_ylabel("Return")
ax.set_title("Efficient Frontier")
ax.legend()

st.pyplot(fig)

# -------------------------
# RAW DATA VIEW
# -------------------------
with st.expander("📊 Show Raw Price Data"):
    st.dataframe(data.tail())