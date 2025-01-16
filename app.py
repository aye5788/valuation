import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# FMP API base URL and API key
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
FMP_API_KEY = "j6kCIBjZa1pHewFjf7XaRDlslDxEFuof"  # Replace with your actual API key


# Function to fetch key metrics
def get_key_metrics(ticker):
    url = f"{FMP_BASE_URL}/key-metrics/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return pd.DataFrame(data)[
                ["date", "revenuePerShare", "debt", "operatingCashFlowPerShare"]
            ]  # Filter relevant metrics
    return None


# Function to fetch company ratings
def get_company_ratings(ticker):
    url = f"{FMP_BASE_URL}/rating/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


# Function to fetch DCF reports
def get_dcf_reports(ticker):
    url = f"{FMP_BASE_URL}/discounted-cash-flow/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]  # Return the first (and only) entry in the list
    return None


# Function to fetch financial scores
def get_financial_scores(ticker):
    url = f"{FMP_BASE_URL}/v4/score?symbol={ticker}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]  # Return the first (and only) entry in the list
    return None


# Streamlit app
def main():
    st.title("Financial Insights App")
    st.subheader("Enter a stock ticker to fetch financial insights")

    # Input for ticker
    ticker = st.text_input("Stock Ticker", placeholder="e.g., AAPL, TSLA")
    if st.button("Fetch Data"):
        if ticker:
            st.info(f"Fetching data for {ticker.upper()}...")

            # Fetch data from APIs
            key_metrics = get_key_metrics(ticker.upper())
            company_ratings = get_company_ratings(ticker.upper())
            dcf_reports = get_dcf_reports(ticker.upper())
            financial_scores = get_financial_scores(ticker.upper())

            # Display Key Metrics
            if key_metrics is not None:
                st.header("Key Metrics")
                st.write(key_metrics)

                st.write("Visualize Key Metrics:")
                metric = st.selectbox(
                    "Select a metric to plot",
                    options=["revenuePerShare", "debt", "operatingCashFlowPerShare"],
                    key="metrics_plot",
                )
                if metric:
                    fig = px.line(
                        key_metrics, x="date", y=metric, title=f"{metric} Over Time"
                    )
                    st.plotly_chart(fig)
            else:
                st.error("Failed to fetch Key Metrics.")

            # Display Company Ratings
            if company_ratings and len(company_ratings) > 0:
                st.header("Company Ratings")
                ratings_df = pd.DataFrame([company_ratings[0]])
                st.write(ratings_df)

                st.write("Ratings Breakdown:")
                fig = px.bar(
                    ratings_df.melt(var_name="Rating Type", value_name="Value"),
                    x="Rating Type",
                    y="Value",
                    title="Company Ratings",
                    text="Value",
                )
                st.plotly_chart(fig)
            else:
                st.error("Failed to fetch Company Ratings.")

            # Display DCF Reports
            if dcf_reports and "dcf" in dcf_reports:
                st.header("Discounted Cash Flow (DCF) Report")
                st.write(f"Date: {dcf_reports['date']}")
                st.metric(label="Discounted Cash Flow (DCF)", value=dcf_reports["dcf"])
                st.metric(label="Stock Price", value=dcf_reports.get("Stock Price", "N/A"))
            else:
                st.error("Failed to fetch DCF Reports.")

            # Display Financial Scores
            if financial_scores:
                st.header("Financial Scores")
                st.write(pd.DataFrame([financial_scores]))
            else:
                st.error("Failed to fetch Financial Scores.")
        else:
            st.warning("Please enter a valid ticker symbol.")


if __name__ == "__main__":
    main()
