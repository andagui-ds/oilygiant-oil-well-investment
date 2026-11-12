import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("⛽ OilyGiant - Análisis de Riesgo")

st.markdown("""
Esta herramienta simula la selección de los **200 mejores pozos** 
de una muestra de 500 para calcular la distribución de ganancias.
""")

# Simulamos datos de ganancias (en lugar de correr el bootstrapping real)
@st.cache_data
def simular_ganancias():
    np.random.seed(42)
    return np.random.normal(loc=4_500_000, scale=2_500_000, size=1000)

ganancias = simular_ganancias()

st.sidebar.header("Parámetros del Proyecto")
region = st.sidebar.selectbox("Selecciona la Región", ["Región 0", "Región 1", "Región 2"])
presupuesto = st.sidebar.number_input("Presupuesto (USD)", value=100_000_000, step=10_000_000)

if st.sidebar.button("Evaluar Riesgo"):
    st.subheader(f"Resultados para {region}")
    
    # Mostrar métricas clave
    col1, col2, col3 = st.columns(3)
    col1.metric("Ganancia Promedio", f"${ganancias.mean():,.0f}")
    col2.metric("Riesgo de Pérdida", f"{(ganancias < 0).mean() * 100:.1f}%")
    col3.metric("Intervalo de Confianza (95%)", f"${np.percentile(ganancias, 2.5):,.0f} - ${np.percentile(ganancias, 97.5):,.0f}")
    
    # Gráfico interactivo
    fig = px.histogram(ganancias, nbins=50, title="Distribución de Ganancias (1000 Simulaciones)")
    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Umbral de Pérdida")
    st.plotly_chart(fig)
