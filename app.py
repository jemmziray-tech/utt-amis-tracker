import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(page_title="UTT AMIS Tracker", page_icon="🏦", layout="wide")

# Injecting subtle CSS to polish whitespace, typography, and buttons
st.markdown(
    """
    <style>
        .big-wealth-text {
            font-size: 3rem !important;
            font-weight: 800;
            color: #00E396;
            margin-bottom: 0px;
        }
        hr {
            border-color: rgba(255, 255, 255, 0.1) !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


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

st.markdown(
    "**Automated wealth tracking and forecasting for the modern investor.**",
    help="Data is scraped daily directly from the official UTT AMIS portals.",
)
st.divider()


# --- 3. Load the Data & Calculate Metrics ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/utt_amis_history.csv")
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df.set_index("Date", inplace=True)
    return df


try:
    df = load_data()
    latest = df.iloc[-1]

    # Calculate absolute delta and percentage yield
    if len(df) > 1:
        prev_liquid = df["Liquid_Fund_NAV"].iloc[-2]
        prev_wekeza = df["Wekeza_Maisha_NAV"].iloc[-2]

        liquid_delta = latest["Liquid_Fund_NAV"] - prev_liquid
        liquid_pct = (liquid_delta / prev_liquid) * 100

        wekeza_delta = latest["Wekeza_Maisha_NAV"] - prev_wekeza
        wekeza_pct = (wekeza_delta / prev_wekeza) * 100
    else:
        liquid_delta, wekeza_delta, liquid_pct, wekeza_pct = 0, 0, 0, 0

    # --- 4. Personal Portfolio Sidebar ---
    with st.sidebar:
        sidebar_col1, sidebar_col2 = st.columns([1, 4])
        with sidebar_col1:
            render_animated_icon("https://cdn.lordicon.com/yeallgsa.json", size=45)
        with sidebar_col2:
            st.header("My Portfolio")

        st.markdown("Enter your units to calculate your current value:")

        liquid_units = st.number_input(
            "Liquid Fund Units", min_value=0.0, value=0.0, step=10.0
        )
        wekeza_units = st.number_input(
            "Wekeza Maisha Units", min_value=0.0, value=0.0, step=10.0
        )

        total_portfolio = 0
        if liquid_units > 0 or wekeza_units > 0:
            total_liquid = liquid_units * latest["Liquid_Fund_NAV"]
            total_wekeza = wekeza_units * latest["Wekeza_Maisha_NAV"]
            total_portfolio = total_liquid + total_wekeza

            st.divider()
            st.subheader("Current Market Value")

            st.metric("Liquid Fund Value", f"{total_liquid:,.2f} TZS")
            st.metric("Wekeza Maisha Value", f"{total_wekeza:,.2f} TZS")

            st.success(f"**Total Portfolio:**\n### {total_portfolio:,.2f} TZS")

            # Asset Allocation Donut Chart
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Asset Allocation")

            pie_df = pd.DataFrame(
                {
                    "Fund": ["Liquid Fund", "Wekeza Maisha"],
                    "Value": [total_liquid, total_wekeza],
                }
            )
            pie_df = pie_df[pie_df["Value"] > 0]

            pie_fig = px.pie(
                pie_df,
                values="Value",
                names="Fund",
                hole=0.75,
                color="Fund",
                color_discrete_map={
                    "Liquid Fund": "#00E396",
                    "Wekeza Maisha": "#008FFB",
                },
            )
            pie_fig.update_layout(
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=180,
            )
            pie_fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color="#000000", width=2)),
            )
            st.plotly_chart(pie_fig, use_container_width=True)

            if st.button("Celebrate Growth 🎉", use_container_width=True):
                st.balloons()

    # --- 5. Main Content Tabs ---
    tab1, tab2, tab3 = st.tabs(
        ["📊 Market Overview", "🔮 Wealth Forecaster", "📂 Raw Data"]
    )

    # TAB 1: Market Overview
    with tab1:
        with st.container(border=True):
            st.subheader("Latest NAV")
            col1, col2 = st.columns(2)

            col1.metric(
                "Liquid Fund",
                f"{latest['Liquid_Fund_NAV']:,.2f} TZS",
                delta=(
                    f"{liquid_delta:,.2f} TZS ({liquid_pct:,.3f}%)"
                    if liquid_delta
                    else None
                ),
            )
            col2.metric(
                "Wekeza Maisha",
                f"{latest['Wekeza_Maisha_NAV']:,.2f} TZS",
                delta=(
                    f"{wekeza_delta:,.2f} TZS ({wekeza_pct:,.3f}%)"
                    if wekeza_delta
                    else None
                ),
            )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("Historical Growth Trends")

            df_long = df.reset_index().melt(
                id_vars="Date",
                value_vars=["Liquid_Fund_NAV", "Wekeza_Maisha_NAV"],
                var_name="Fund",
                value_name="NAV (TZS)",
            )
            df_long["Fund"] = df_long["Fund"].str.replace("_", " ")

            # The "Neon Institutional" Line Chart (Auto-Scaling Fix)
            fig = px.line(
                df_long,
                x="Date",
                y="NAV (TZS)",
                color="Fund",
                facet_row="Fund",
                template="plotly_dark",
                markers=True,  # Shows the exact daily points
                color_discrete_map={
                    "Liquid Fund NAV": "#00E396",
                    "Wekeza Maisha NAV": "#008FFB",
                },
            )

            # Thick lines and distinct markers
            fig.update_traces(line=dict(width=3), marker=dict(size=6))

            # Unlinked Y-axes for micro-volatility visibility
            fig.update_yaxes(
                matches=None, showgrid=True, gridcolor="rgba(255,255,255,0.05)"
            )
            fig.update_xaxes(showgrid=False)

            fig.update_layout(
                hovermode="x unified",
                showlegend=False,
                height=650,
                margin=dict(t=40, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            fig.for_each_annotation(
                lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>")
            )
            st.plotly_chart(fig, use_container_width=True)

    # TAB 2: The Wealth Forecaster
    with tab2:
        with st.container(border=True):
            st.subheader("The Wealth Time Machine")
            st.markdown(
                "Play with the sliders to see how your money could grow over time assuming an average 10% annual return."
            )

            calc_col1, calc_col2 = st.columns([1, 2], gap="large")

            with calc_col1:
                monthly_contribution = st.slider(
                    "Monthly Contribution (TZS)",
                    min_value=10000,
                    max_value=1000000,
                    step=10000,
                    value=50000,
                )
                years = st.slider("Years to Grow", min_value=1, max_value=30, value=10)

                annual_rate = 0.10
                months = years * 12
                monthly_rate = annual_rate / 12

                fv_current = total_portfolio * (1 + annual_rate) ** years
                fv_contributions = monthly_contribution * (
                    ((1 + monthly_rate) ** months - 1) / monthly_rate
                )
                total_future_wealth = fv_current + fv_contributions

                st.markdown("<br>", unsafe_allow_html=True)
                st.caption(f"Projected Wealth in {years} years:")
                st.markdown(
                    f'<p class="big-wealth-text">{total_future_wealth:,.0f} TZS</p>',
                    unsafe_allow_html=True,
                )

            with calc_col2:
                projection_data = []
                current_balance = total_portfolio
                for year in range(1, years + 1):
                    current_balance = (
                        current_balance + (monthly_contribution * 12)
                    ) * (1 + annual_rate)
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
                )
                bar_fig.update_traces(
                    marker_color="#00E396",
                    marker_line_color="#000000",
                    marker_line_width=1.5,
                    opacity=0.9,
                )
                bar_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=10, l=10, r=10),
                )
                st.plotly_chart(bar_fig, use_container_width=True)

    # TAB 3: Raw Data & Export
    with tab3:
        with st.container(border=True):
            data_col1, data_col2 = st.columns([4, 1])
            with data_col1:
                st.subheader("Historical Ledger")
            with data_col2:
                # One-Click Data Export
                csv_export = df.to_csv().encode("utf-8")
                st.download_button(
                    label="📥 Download Data (CSV)",
                    data=csv_export,
                    file_name="utt_amis_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            st.dataframe(
                df.sort_index(ascending=False), use_container_width=True, height=500
            )

except Exception as e:
    st.error(f"⚠️ Could not load data. Error: {e}")
