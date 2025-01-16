import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# FMP API base URL
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
FMP_API_KEY = "j6kCIBjZa1pHewFjf7XaRDlslDxEFuof"  # Replace with your actual API key

# Function to fetch financial statements
def get_financial_statements(ticker):
    url = f"{FMP_BASE_URL}/financials/income-statement/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("financials", [])
    return None

# Function to fetch valuation analysis
def get_valuation_analysis(ticker):
    url = f"{FMP_BASE_URL}/valuation/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to plot financial data
def plot_financials(financials, metric):
    df = pd.DataFrame(financials)
    df["date"] = pd.to_datetime(df["date"])
    df[metric] = pd.to_numeric(df[metric], errors="coerce")
    df = df.sort_values("date")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df[metric], marker="o", linestyle="-", color="blue")
    ax.set_title(f"{metric} Over Time", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel(metric, fontsize=12)
    ax.grid(True)
    return fig

# Streamlit app
def main():
    st.title("Financial Analysis App")
    st.subheader("Enter a stock ticker to get financial insights and valuation analysis")

    ticker = st.text_input("Stock Ticker", placeholder="e.g., AAPL, TSLA")

    if st.button("Fetch Data"):
        if ticker:
            st.info(f"Fetching data for {ticker.upper()}...")

            # Fetch financial statements
            financials = get_financial_statements(ticker.upper())
            if financials:
                st.header("Financial Statements Overview")
                st.write("Raw Financial Data:")
                st.dataframe(pd.DataFrame(financials))

                st.write("Visualize Key Metrics:")
                metric = st.selectbox(
                    "Select a metric to plot", 
                    options=["Revenue", "Gross Profit", "Net Income"]
                )
                if metric:
                    fig = plot_financials(financials, metric)
                    st.pyplot(fig)
            else:
                st.error("Failed to fetch financial statements.")

            # Fetch valuation analysis
            valuation = get_valuation_analysis(ticker.upper())
            if valuation:
                st.header("Valuation Analysis")
                valuation_df = pd.DataFrame([valuation])
                st.write(valuation_df)

                # Plot valuation metrics using Plotly
                st.write("Valuation Metrics Visualization:")
                fig = px.bar(
                    valuation_df.melt(var_name="Metric", value_name="Value"),
                    x="Metric", y="Value",
                    title="Valuation Metrics",
                    text="Value"
                )
                st.plotly_chart(fig)
            else:
                st.error("Failed to fetch valuation analysis.")
        else:
            st.warning("Please enter a valid ticker symbol.")

if __name__ == "__main__":
    main()
