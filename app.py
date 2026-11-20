import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import streamlit as st

st.set_page_config(page_title="OilyGiant - Análisis de Riesgo", layout="wide")

st.title("🛢️ OilyGiant - Análisis de Riesgo y Rentabilidad")
st.markdown(
    "Esta herramienta entrena un modelo de **Regresión Lineal** sobre los"
    " estudios geológicos reales y ejecuta **1,000 simulaciones de"
    " Bootstrapping** (seleccionando los **200 mejores pozos** de una muestra"
    " de 500)."
)


# 1. Cargar los datasets reales desde la raíz del repositorio
@st.cache_data
def cargar_datos():
  archivos = {
      "Región 0": "geo_data_0.csv",
      "Región 1": "geo_data_1.csv",
      "Región 2": "geo_data_2.csv",
  }
  return {nombre: pd.read_csv(ruta) for nombre, ruta in archivos.items()}


datos_regiones = cargar_datos()


# 2. Entrenar modelo y ejecutar Bootstrapping real (cacheado por región y presupuesto)
@st.cache_data
def ejecutar_analisis(df, presupuesto_usd, n_simulaciones=1000):
  X = df[["f0", "f1", "f2"]]
  y = df["product"]

  X_train, X_valid, y_train, y_valid = train_test_split(
      X, y, test_size=0.25, random_state=12345
  )

  model = LinearRegression()
  model.fit(X_train, y_train)
  predicciones = pd.Series(model.predict(X_valid), index=y_valid.index)

  # Parámetros financieros del proyecto OilyGiant
  ingreso_por_unidad = 4500  # 4,500 USD por cada mil barriles
  state = np.random.RandomState(12345)
  ganancias = []

  for _ in range(n_simulaciones):
    muestra_target = y_valid.sample(n=500, replace=True, random_state=state)
    muestra_preds = predicciones[muestra_target.index]

    # Seleccionar los 200 mejores pozos según la predicción del modelo
    mejores_200 = muestra_target[
        muestra_preds.sort_values(ascending=False).index
    ][:200]
    ganancia = (mejores_200.sum() * ingreso_por_unidad) - presupuesto_usd
    ganancias.append(ganancia)

  return np.array(ganancias)


# Barra lateral con parámetros interactivos
st.sidebar.header("Parámetros del Proyecto")
region = st.sidebar.selectbox(
    "Selecciona la Región", ["Región 0", "Región 1", "Región 2"]
)
presupuesto = st.sidebar.number_input(
    "Presupuesto (USD)",
    min_value=10_000_000,
    max_value=500_000_000,
    value=100_000_000,
    step=5_000_000,
)

if st.sidebar.button("Evaluar Riesgo"):
  df_seleccionado = datos_regiones[region]
  ganancias = ejecutar_analisis(df_seleccionado, presupuesto)

  ganancia_media = ganancias.mean()
  riesgo_perdida = (ganancias < 0).mean() * 100
  ic_inf = np.percentile(ganancias, 2.5)
  ic_sup = np.percentile(ganancias, 97.5)

  st.subheader(f"Resultados Reales para {region}")

  col1, col2, col3 = st.columns(3)
  col1.metric("Ganancia Promedio", f"${ganancia_media:,.0f}")
  col2.metric(
      "Riesgo de Pérdida",
      f"{riesgo_perdida:.1f}%",
      delta="Apto (< 2.5%)" if riesgo_perdida < 2.5 else "Riesgo Alto (≥ 2.5%)",
      delta_color="normal" if riesgo_perdida < 2.5 else "inverse",
  )
  col3.metric("Intervalo de Confianza (95%)", f"${ic_inf:,.0f} a ${ic_sup:,.0f}")

  fig = px.histogram(
      ganancias,
      nbins=50,
      title=(
          f"Distribución Real de Ganancias - {region} (1,000 Simulaciones)"
      ),
      labels={"value": "Ganancia Neta (USD)", "count": "Frecuencia"},
  )
  fig.update_layout(showlegend=False)
  fig.add_vline(
      x=0, line_dash="dash", line_color="red", annotation_text="Punto de Equilibrio ($0)"
  )
  st.plotly_chart(fig, use_container_width=True)
