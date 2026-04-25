import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="UTT AMIS Tracker", page_icon="🏦", layout="wide")


def render_animated_icon(url, size=55):
    components.html(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
            <script src="https://cdn.lordicon.com/lordicon.js"></script>
            <lord-icon
                src="{url}"
                trigger="loop"
                delay="1500"
                colors="primary:#ffffff,secondary:#2088ff"
                style="width:{size}px;height:{size}px;">
            </lord-icon>
        </div>
        """,
        height=size + 10,
    )


# --- 2. Header Section ---
head_col1, head_col2 = st.columns([1, 20])
with head_col1:
    render_animated_icon("https://cdn.lordicon.com/qwwyqyyg.json", size=50)
with head_col2:
    st.title("UTT AMIS Executive Dashboard")

st.markdown("**Automated wealth tracking and forecasting for the modern investor.**")
st.divider()


# --- 3. Load the Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/utt_amis_history.csv")
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df.set_index("Date", inplace=True)
    return df


try:
    df = load_data()
    latest = df.iloc[-1]

    if len(df) > 1:
        liquid_delta = df["Liquid_Fund_NAV"].iloc[-1] - df["Liquid_Fund_NAV"].iloc[-2]
        wekeza_delta = (
            df["Wekeza_Maisha_NAV"].iloc[-1] - df["Wekeza_Maisha_NAV"].iloc[-2]
        )
    else:
        liquid_delta = None
        wekeza_delta = None

    # --- 4. Personal Portfolio Sidebar ---
    sidebar_col1, sidebar_col2 = st.sidebar.columns([1, 4])
    with sidebar_col1:
        render_animated_icon("https://cdn.lordicon.com/yeallgsa.json", size=45)
    with sidebar_col2:
        st.sidebar.header("My Portfolio")

    st.sidebar.markdown("Enter your units to calculate your current value:")

    liquid_units = st.sidebar.number_input(
        "Liquid Fund Units", min_value=0.0, value=0.0, step=10.0
    )
    wekeza_units = st.sidebar.number_input(
        "Wekeza Maisha Units", min_value=0.0, value=0.0, step=10.0
    )

    total_portfolio = 0
    if liquid_units > 0 or wekeza_units > 0:
        total_liquid = liquid_units * latest["Liquid_Fund_NAV"]
        total_wekeza = wekeza_units * latest["Wekeza_Maisha_NAV"]
        total_portfolio = total_liquid + total_wekeza

        st.sidebar.divider()
        st.sidebar.subheader("Current Market Value")
        st.sidebar.write(f"**Liquid:** {total_liquid:,.2f} TZS")
        st.sidebar.write(f"**Wekeza:** {total_wekeza:,.2f} TZS")
        st.sidebar.success(f"**Total Portfolio:** {total_portfolio:,.2f} TZS")

        # A fun dopamine hit for the user
        if st.sidebar.button("Celebrate Growth 🎉"):
            st.balloons()

    # --- 5. Main Content Tabs ---
    # Tabs keep the user clicking and exploring without overwhelming the screen
    tab1, tab2, tab3 = st.tabs(
        ["📊 Market Overview", "🔮 Wealth Forecaster", "📂 Raw Data"]
    )

    # TAB 1: Market Overview
    with tab1:
        st.subheader("Latest NAV (Net Asset Value)")
        col1, col2 = st.columns(2)
        col1.metric(
            "Liquid Fund",
            f"{latest['Liquid_Fund_NAV']:,.2f} TZS",
            delta=f"{liquid_delta:,.2f} TZS" if liquid_delta else None,
        )
        col2.metric(
            "Wekeza Maisha",
            f"{latest['Wekeza_Maisha_NAV']:,.2f} TZS",
            delta=f"{wekeza_delta:,.2f} TZS" if wekeza_delta else None,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Historical Growth Trends")

        # Upgraded Plotly Chart
        fig = px.line(
            df,
            x=df.index,
            y=["Liquid_Fund_NAV", "Wekeza_Maisha_NAV"],
            labels={"value": "NAV (TZS)", "variable": "Fund"},
            template="plotly_dark",
        )  # Matches the sleek UI
        fig.update_layout(
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    # TAB 2: The Wealth Forecaster (The highly addictive feature)
    with tab2:
        st.subheader("The Wealth Time Machine")
        st.markdown(
            "Play with the sliders to see how your money could grow over time assuming an average 10% annual return."
        )

        calc_col1, calc_col2 = st.columns([1, 2])

        with calc_col1:
            monthly_contribution = st.slider(
                "Monthly Contribution (TZS)",
                min_value=10000,
                max_value=1000000,
                step=10000,
                value=50000,
            )
            years = st.slider("Years to Grow", min_value=1, max_value=30, value=10)

            # Simple Compound Interest Math
            annual_rate = 0.10
            months = years * 12
            monthly_rate = annual_rate / 12

            # Future Value of current portfolio + Future Value of monthly contributions
            fv_current = total_portfolio * (1 + annual_rate) ** years
            fv_contributions = monthly_contribution * (
                ((1 + monthly_rate) ** months - 1) / monthly_rate
            )
            total_future_wealth = fv_current + fv_contributions

            st.info(
                f"Projected Wealth in {years} years:\n### **{total_future_wealth:,.0f} TZS**"
            )

        with calc_col2:
            # Generate a quick projection dataframe to chart the growth
            projection_data = []
            current_balance = total_portfolio
            for year in range(1, years + 1):
                current_balance = (current_balance + (monthly_contribution * 12)) * (
                    1 + annual_rate
                )
                projection_data.append(
                    {"Year": f"Year {year}", "Projected Value": current_balance}
                )

            proj_df = pd.DataFrame(projection_data)
            bar_fig = px.bar(
                proj_df,
                x="Year",
                y="Projected Value",
                text_auto=".2s",
                template="plotly_dark",
                color_discrete_sequence=["#2088ff"],
            )
            st.plotly_chart(bar_fig, use_container_width=True)

    # TAB 3: Raw Data
    with tab3:
        st.subheader("Historical Ledger")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Could not load data. Error: {e}")
