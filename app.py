import numpy as np  # Operaciones numéricas, percentiles y generación de números aleatorios
import pandas as pd  # Lectura de datos geológicos y construcción de tablas comparativas
import plotly.express as px  # Gráfica interactiva de distribución de ganancias
# Modelo predictivo de volumen de reservas
from sklearn.linear_model import LinearRegression
# Cálculo del error cuadrático medio (RMSE)
from sklearn.metrics import root_mean_squared_error
# División entrenamiento/validación (75% / 25%)
from sklearn.model_selection import train_test_split
import streamlit as st  # Interfaz web nativa 100% en Python sin CSS

st.set_page_config(  # Configura el título de la pestaña y el ancho completo de pantalla
    page_title="OilyGiant - Risk & Profit Analysis",
    page_icon="🛢️",
    layout="wide",
)

# Título compacto nativo sin CSS
st.header("🛢️ OilyGiant - Oil Well Investment & Risk Analysis")
st.caption(  # Subtítulo explicativo de la metodología de simulación
    "Linear Regression on geological survey data + 1,000 Bootstrapping"
    " simulations (top 200 wells out of 500 sampled points)."
)


@st.cache_data  # Guarda en caché los CSV geológicos para evitar recargas repetidas
def load_data():
    files = {  # Diccionario con las rutas de los 3 archivos en la raíz del repositorio
        "Region 0": "geo_data_0.csv",
        "Region 1": "geo_data_1.csv",
        "Region 2": "geo_data_2.csv",
    }
    return {name: pd.read_csv(path) for name, path in files.items()}


regions_data = load_data()  # Carga los datos de las tres regiones disponibles


@st.cache_data  # Guarda en caché los resultados del bootstrapping según región y presupuesto
def run_simulation(df, budget_usd, n_simulations=1000):
    X = df[["f0", "f1", "f2"]]  # Características geológicas de entrada
    y = df["product"]  # Volumen de reservas en miles de barriles

    X_train, X_valid, y_train, y_valid = train_test_split(  # Partición estándar 75/25
        X, y, test_size=0.25, random_state=12345
    )

    model = LinearRegression()  # Inicializa la regresión lineal
    # Entrena el modelo con los datos de entrenamiento
    model.fit(X_train, y_train)
    # Predicciones alineadas por índice
    predictions = pd.Series(model.predict(X_valid), index=y_valid.index)

    rmse = root_mean_squared_error(
        y_valid, predictions)  # Error RMSE en validación

    revenue_per_unit = 4500  # Ingreso en USD por cada unidad (1,000 barriles)
    state = np.random.RandomState(12345)  # Semilla fija para reproducibilidad
    profits = []  # Lista para almacenar la ganancia neta de cada iteración

    for _ in range(n_simulations):  # Ejecuta las 1,000 muestras bootstrap
        target_sample = y_valid.sample(
            n=500, replace=True, random_state=state)  # Explora 500 puntos
        # Obtiene las predicciones de esos 500 puntos
        preds_sample = predictions[target_sample.index]
        top_200 = target_sample[preds_sample.sort_values(
            ascending=False).index][:200]  # Elige los 200 mejores
        # Calcula beneficio neto descontando inversión
        profit = (top_200.sum() * revenue_per_unit) - budget_usd
        profits.append(profit)

    return rmse, np.array(profits)


# Controles en la barra lateral
st.sidebar.header("Project Parameters")  # Encabezado del panel izquierdo
selected_region = st.sidebar.selectbox(  # Selector de región para el desglose detallado
    "Select Region", ["Region 1", "Region 0", "Region 2"]
)
budget = st.sidebar.number_input(  # Control numérico para simular distintos presupuestos de inversión
    "Budget (USD)",
    min_value=10_000_000,
    max_value=500_000_000,
    value=100_000_000,
    step=5_000_000,
)

# Cálculo de tabla resumen para las 3 regiones
summary_rows = []  # Filas de la tabla comparativa
all_results = {}  # Almacena métricas y arreglos de ganancias por región

for reg_name in ["Region 1", "Region 0", "Region 2"]:
    rmse_val, profits_arr = run_simulation(
        regions_data[reg_name], budget)  # Ejecuta simulación por región
    all_results[reg_name] = (rmse_val, profits_arr)

    avg_p = profits_arr.mean()  # Beneficio promedio esperado
    # Límite inferior del intervalo de confianza al 95%
    ci_l = np.percentile(profits_arr, 2.5)
    # Límite superior del intervalo de confianza al 95%
    ci_u = np.percentile(profits_arr, 97.5)
    # Porcentaje de escenarios con pérdida económica
    risk_p = (profits_arr < 0).mean() * 100
    # Regla de negocio: riesgo menor a 2.5%
    status = "Viable" if risk_p < 2.5 else "Unfeasible"
    label = f"{reg_name} 🏆" if reg_name == "Region 1" and risk_p < 2.5 else reg_name

    summary_rows.append({
        "Region": label,
        "RMSE": round(rmse_val, 2),
        "Average Profit (USD)": f"${avg_p:,.0f}",
        "Confidence Interval (95%)": f"${ci_l:,.0f} to ${ci_u:,.0f}",
        "Risk of Loss": f"{risk_p:.1f}% ({status})",
    })

# Distribución en 2 columnas para mantener todo visible en una pantalla
left_col, right_col = st.columns([1.1, 1], gap="medium")

with left_col:
    # Subtítulo de la tabla comparativa
    st.subheader("🏆 Simulation Results (All Regions)")
    st.dataframe(  # Tabla interactiva nativa sin bordes ni estilos externos
        pd.DataFrame(summary_rows),
        use_container_width=True,
        hide_index=True,
        height=142,
    )

    # Extrae los resultados de la región elegida
    rmse_sel, profits_sel = all_results[selected_region]
    avg_profit = profits_sel.mean()
    risk_of_loss = (profits_sel < 0).mean() * 100
    ci_low = np.percentile(profits_sel, 2.5)
    ci_high = np.percentile(profits_sel, 97.5)
    is_viable = risk_of_loss < 2.5

    # Subtítulo de métricas individuales
    st.subheader(f"Detailed Breakdown — {selected_region}")
    m1, m2 = st.columns(2)  # Primera fila de tarjetas KPI
    m1.metric("RMSE", f"{rmse_sel:.2f}")
    m2.metric("Average Profit (USD)", f"${avg_profit:,.0f}")

    m3, m4 = st.columns(2)  # Segunda fila de tarjetas KPI
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
    # Subtítulo del histograma
    st.subheader(f"Profit Distribution — {selected_region}")
    fig = px.histogram(  # Histograma nativo de Plotly con la distribución de ganancias
        profits_sel,
        nbins=45,
        labels={"value": "Net Profit (USD)", "count": "Frequency"},
    )
    fig.update_layout(  # Ajusta altura y márgenes compactos
        showlegend=False,
        height=355,
        margin=dict(l=10, r=10, t=15, b=10),
    )
    fig.add_vline(  # Línea vertical punteada marcando el punto de equilibrio ($0)
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Break-Even ($0)",
    )
    # Renderiza la gráfica responsiva
    st.plotly_chart(fig, use_container_width=True)
