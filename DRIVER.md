D – Discover \& Define



Objective:

Develop a portfolio optimization application that allows users to input multiple stock tickers and generate an optimal asset allocation based on risk-return tradeoffs.



The goal is to help users understand how to allocate capital efficiently across assets using quantitative financial modeling techniques, specifically by maximizing the Sharpe ratio under user-defined constraints.



R – Represent



The system was designed with the following structure:



Data Retrieval Module

Uses the yfinance API to download historical stock price data.

Return \& Risk Module

Calculates daily returns, expected annual returns, and the covariance matrix.

Optimization Engine

Uses numerical optimization (SciPy) to determine portfolio weights that maximize the Sharpe ratio.

Constraint Handling

Includes user-defined constraints such as maximum allocation per asset.

Visualization Module

Generates an efficient frontier to visualize the tradeoff between risk and return.

I – Implement



The application was implemented in Python using:



Streamlit for the interactive user interface

pandas \& NumPy for data manipulation and calculations

yfinance for financial data retrieval

SciPy for portfolio optimization

Matplotlib for visualization



The interface allows users to:



Input stock tickers

Adjust risk-free rate

Set maximum weight constraints

View optimized portfolio allocation and performance metrics

V – Validate



The model was validated through:



Testing multiple sets of stock tickers

Ensuring weights sum to 100% under constraints

Verifying that higher risk tolerance leads to higher expected return

Checking that the efficient frontier reflects realistic risk-return tradeoffs

Confirming that optimization results are consistent across repeated runs

E – Evolve



The application was improved by:



Adding error handling for missing or inconsistent financial data

Supporting both single and multiple ticker inputs

Enhancing UI layout for clarity and usability

Improving robustness of data retrieval (handling “Adj Close” vs “Close”)

Including visualization tools to better interpret results

R – Reflect



The model demonstrates that portfolio performance is highly sensitive to:



Expected return estimates

Covariance between assets

User-imposed constraints



The optimization results show that a small number of assets may dominate the portfolio depending on their risk-return profile, especially when constraints are limited.



Additionally, the efficient frontier highlights the tradeoff between maximizing return and minimizing risk, reinforcing core principles of modern portfolio theory.

