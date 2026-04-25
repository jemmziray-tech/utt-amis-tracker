import streamlit as st
import pandas as pd

# 1. Page Configuration (Browser Tab Title & Layout)
st.set_page_config(page_title="UTT AMIS Tracker", page_icon="📈", layout="wide")

# 2. Header Section
st.title("📈 UTT AMIS Investment Dashboard")
st.markdown("**The serverless financial butler tracking Tanzanian mutual funds.**")
st.divider()


# 3. Load the Data
# The @st.cache_data decorator keeps the app fast by temporarily saving the data in memory
@st.cache_data
def load_data():
    df = pd.read_csv("data/utt_amis_history.csv")
    # Convert the Date column to actual datetime objects for better graphing
    df["Date"] = pd.to_datetime(df["Date"])
    # Set the Date as the index so the charts plot correctly
    df.set_index("Date", inplace=True)
    return df


try:
    df = load_data()

    # 4. Top Row Metrics (The Big Numbers)
    st.subheader("Latest NAV (Net Asset Value)")
    latest = df.iloc[-1]

    # Create two columns side-by-side
    col1, col2 = st.columns(2)

    # Format the numbers to 2 decimal places
    col1.metric("Liquid Fund", f"{latest['Liquid_Fund_NAV']:,.2f} TZS")
    col2.metric("Wekeza Maisha", f"{latest['Wekeza_Maisha_NAV']:,.2f} TZS")

    st.divider()

    # 5. Interactive Charts
    st.subheader("Historical Growth Trends")
    # Streamlit automatically builds an interactive line chart out of the DataFrame
    st.line_chart(df[["Liquid_Fund_NAV", "Wekeza_Maisha_NAV"]])

    # 6. Raw Data Expander
    # A collapsible section for the raw numbers
    with st.expander("📂 View Raw Database"):
        st.dataframe(df.sort_index(ascending=False))  # Shows newest dates first

except Exception as e:
    st.error(f"⚠️ Could not load data. Have we scraped data yet? Error: {e}")
