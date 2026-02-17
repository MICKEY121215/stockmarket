import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simple Stock Dashboard", layout="centered")

st.title("📈 Simple Stock Market Dashboard")
st.write("This app explains stock data in very simple language.")

# User input
stock_symbol = st.text_input("Enter Stock Symbol (Example: TCS.NS or AAPL)")

if stock_symbol:
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="6mo")

        if data.empty:
            st.error("Invalid stock symbol. Please try again.")
        else:
            current_price = data["Close"].iloc[-1]
            st.subheader("💰 Current Price")
            currency = stock.info.get("currency", "")
            st.write(f"{currency} {round(current_price, 2)}")


            # Simple moving average
            data["50MA"] = data["Close"].rolling(50).mean()

            # Plot chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Price"))
            fig.add_trace(go.Scatter(x=data.index, y=data["50MA"], name="50 Day Average"))

            fig.update_layout(title="Price Trend (Last 6 Months)",
                              xaxis_title="Date",
                              yaxis_title="Price")

            st.plotly_chart(fig)

            st.subheader("📊 Simple Explanation")

            recent_prices = data["Close"].tail(5).mean()
            recent_ma = data["50MA"].dropna().tail(5).mean()

            if recent_prices > recent_ma:
                st.success("🟢 Stock is in an UP trend.")
            elif recent_prices < recent_ma:
                st.warning("🔴 Stock is in a DOWN trend.")
            else:
                st.info("🟡 Stock is moving sideways.")


            st.write("""
            ### What does this mean?

            - If price is above average → Stock is strong 
            - If price is below average → Stock is weak 
            - Always do your own research before investing.
            """)

    except:
        st.error("Something went wrong. Please try another stock.")
