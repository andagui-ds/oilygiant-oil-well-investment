import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
import streamlit as st

st.set_page_config(page_title="OilyGiant - Risk & Profit Analysis", layout="wide")

# Reducir espacios vacíos superiores e inferiores para que quepa en una pantalla
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 0.5rem;
        }
        h1 {
            font-size: 1.85rem !important;
            margin-bottom: 0.2rem !important;
        }
        h3 {
            font-size: 1.15rem !important;
            margin-top: 0.4rem !important;
            margin-bottom: 0.4rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛢️ OilyGiant - Oil Well Investment & Risk Analysis")
st.caption(
    "Linear Regression on geological survey data + 1,000 Bootstrapping"
    " simulations (top 200 wells out of 500 sampled points)."
)


@st.cache_data
def load_data():
  files = {
      "Region 0": "geo_data_0.csv",
      "Region 1": "geo_data_1.csv",
      "Region 2": "geo_data_2.csv",
  }
  return {name: pd.read_csv(path) for name, path in files.items()}


regions_data = load_data()


@st.cache_data
def run_simulation(df, budget_usd, n_simulations=1000):
  X = df[["f0", "f1", "f2"]]
  y = df["product"]

  X_train, X_valid, y_train, y_valid = train_test_split(
      X, y, test_size=0.25, random_state=12345
  )

  model = LinearRegression()
  model.fit(X_train, y_train)
  predictions = pd.Series(model.predict(X_valid), index=y_valid.index)

  rmse = root_mean_squared_error(y_valid, predictions)

  revenue_per_unit = 4500
  state = np.random.RandomState(12345)
  profits = []

  for _ in range(n_simulations):
    target_sample = y_valid.sample(n=500, replace=True, random_state=state)
    preds_sample = predictions[target_sample.index]
    top_200 = target_sample[preds_sample.sort_values(ascending=False).index][
        :200
    ]
    profit = (top_200.sum() * revenue_per_unit) - budget_usd
    profits.append(profit)

  return rmse, np.array(profits)


# Sidebar controls
st.sidebar.header("Project Parameters")
selected_region = st.sidebar.selectbox(
    "Select Region", ["Region 1", "Region 0", "Region 2"]
)
budget = st.sidebar.number_input(
    "Budget (USD)",
    min_value=10_000_000,
    max_value=500_000_000,
    value=100_000_000,
    step=5_000_000,
)

# Compute summary for all 3 regions
summary_rows = []
all_results = {}

for reg_name in ["Region 1", "Region 0", "Region 2"]:
  rmse_val, profits_arr = run_simulation(regions_data[reg_name], budget)
  all_results[reg_name] = (rmse_val, profits_arr)

  avg_p = profits_arr.mean()
  ci_l = np.percentile(profits_arr, 2.5)
  ci_u = np.percentile(profits_arr, 97.5)
  risk_p = (profits_arr < 0).mean() * 100
  status = "Viable" if risk_p < 2.5 else "Unfeasible"
  label = (
      f"{reg_name} 🏆" if reg_name == "Region 1" and risk_p < 2.5 else reg_name
  )

  summary_rows.append({
      "Region": label,
      "RMSE": round(rmse_val, 2),
      "Average Profit (USD)": f"${avg_p:,.0f}",
      "Confidence Interval (95%)": f"${ci_l:,.0f} to ${ci_u:,.0f}",
      "Risk of Loss": f"{risk_p:.1f}% ({status})",
  })

# Layout en 2 columnas para que todo quepa sin scroll
left_col, right_col = st.columns([1.1, 1], gap="medium")

with left_col:
  st.subheader("🏆 Simulation Results (All Regions)")
  st.dataframe(
      pd.DataFrame(summary_rows),
      use_container_width=True,
      hide_index=True,
      height=142,
  )

  rmse_sel, profits_sel = all_results[selected_region]
  avg_profit = profits_sel.mean()
  risk_of_loss = (profits_sel < 0).mean() * 100
  ci_low = np.percentile(profits_sel, 2.5)
  ci_high = np.percentile(profits_sel, 97.5)
  is_viable = risk_of_loss < 2.5

  st.subheader(f"Detailed Breakdown — {selected_region}")
  m1, m2 = st.columns(2)
  m1.metric("RMSE", f"{rmse_sel:.2f}")
  m2.metric("Average Profit (USD)", f"${avg_profit:,.0f}")

  m3, m4 = st.columns(2)
  m3.metric(
      "Confidence Interval (95%)",
      f"${ci_low/1e6:.2f}M to ${ci_high/1e6:.2f}M",
  )
  m4.metric(
      "Risk of Loss",
      f"{risk_of_loss:.1f}%",
      delta="Viable (< 2.5%)" if is_viable else "Unfeasible (≥ 2.5%)",
      delta_color="normal" if is_viable else "inverse",
  )

with right_col:
  st.subheader(f"Profit Distribution — {selected_region}")
  fig = px.histogram(
      profits_sel,
      nbins=45,
      labels={"value": "Net Profit (USD)", "count": "Frequency"},
  )
  fig.update_layout(
      showlegend=False,
      height=355,
      margin=dict(l=10, r=10, t=15, b=10),
  )
  fig.add_vline(
      x=0,
      line_dash="dash",
      line_color="red",
      annotation_text="Break-Even ($0)",
  )
  st.plotly_chart(fig, use_container_width=True)
