[🇺🇸 Read in English](#-oilygiant--oil-well-prospecting-and-risk-analysis) | [🇲🇽 Leer en Español](#-oilygiant--prospección-de-pozos-petroleros-y-análisis-de-riesgo)

---

# ⛽ OilyGiant — Oil Well Prospecting and Risk Analysis

> Linear regression model and Monte Carlo simulations (Bootstrapping) to determine the region with the highest profitability and lowest financial risk for drilling 200 new oil wells.

🚀 **[Launch Interactive Streamlit App](https://oilygiant-oil-well-investment.streamlit.app/)** | 🌐 **[View Quarto Web Report](https://andagui-ds.github.io/oilygiant-oil-well-investment/)**

---

## 🎯 Business Problem

**OilyGiant** needs to decide in which of three geological regions to build 200 new oil wells. The total investment budget is **$100 million USD** (i.e., $500,000 per well). Only 500 exploration points can be sampled per region to select the top 200.

The goal is not merely to find the region with the largest reserve volume, but to maximize profit while minimizing financial loss, enforcing a strict threshold: **risk of loss must not exceed 2.5%**.

## 📊 Data

* **Sources:** `geo_data_0.csv`, `geo_data_1.csv`, `geo_data_2.csv`
* **Features:** 3 geological variables (`f0`, `f1`, `f2`) per exploration point.
* **Target Variable:** `product` (reserve volume in thousand barrels).
* **Break-Even Point:** 111.11 thousand barrels per well ($500k investment / $4,500 revenue per unit).

## 🧠 Approach and Methodology

1. **Baseline Modeling:** Trained a **Linear Regression** model to predict reserve volumes in each region (75% train / 25% validation split).
2. **Potential Profitability Calculation:** Selected the top 200 predicted wells in each region to estimate theoretical profit.
3. **Risk Simulation (Bootstrapping):**
   * Performed **1,000 iterations**.
   * In each iteration, randomly sampled 500 wells (simulating real exploration) and selected the top 200 based on model predictions.
   * Computed the profit distribution, average profit, **95% Confidence Interval (CI)**, and **Risk of Loss** (probability of negative profit).

## 🏆 Simulation Results

| Region | RMSE | Average Profit (USD) | Confidence Interval (95%) | Risk of Loss |
| :--- | :---: | :---: | :---: | :---: |
| **Region 1 🏆** | **0.89** | **$4,985,690** | **$753,155 to $9,115,036** | **1.0% (Viable)** |
| Region 0 | 37.76 | $4,359,337 | -$1,162,316 to $9,665,041 | 6.1% (Unfeasible) |
| Region 2 | 40.15 | $4,126,728 | -$1,589,395 to $9,781,912 | 7.0% (Unfeasible) |

*(Note: Regions 0 and 2 exceed the 2.5% maximum risk threshold, with confidence intervals dipping into negative values).*

## ✅ Final Recommendation

**Invest in Region 1.** Although Regions 0 and 2 show slightly higher average predicted volumes, their high variance (RMSE) pushes the risk of loss well above the 2.5% limit.

Region 1 achieves a remarkably low RMSE (0.89), indicating a near-perfect correlation between geological features and oil reserves. This enables surgical precision when selecting the top 200 wells, guaranteeing a **risk of loss of just 1.0%** and an expected average profit close to **$5 million USD**.

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:** Pandas, Scikit-learn, NumPy, Plotly, Streamlit
* **Techniques:** Linear Regression, Bootstrapping, Confidence Intervals, Risk Assessment, Decision-Making under Uncertainty.

## 🔗 Full Analysis & Production App

* 📓 [Original Jupyter Notebook with full code and simulations](notebooks/)
* 🚀 [Interactive Risk & Profit Simulator (Streamlit)](https://oilygiant-oil-well-investment.streamlit.app/)

---
---

# ⛽ OilyGiant — Prospección de Pozos Petroleros y Análisis de Riesgo

> Modelo de regresión lineal y simulaciones de Monte Carlo (Bootstrapping) para determinar la región con mayor rentabilidad y menor riesgo financiero para la perforación de 200 nuevos pozos petroleros.

🚀 **[Abrir App Interactiva en Streamlit](https://oilygiant-oil-well-investment.streamlit.app/)** | 🌐 **[Ver Reporte Web en Quarto](https://andagui-ds.github.io/oilygiant-oil-well-investment/)**

---

## 🎯 Problema de Negocio

**OilyGiant** necesita decidir en cuál de tres regiones geológicas debe construir 200 nuevos pozos de petróleo. El presupuesto de inversión es de **$100 millones de USD** (es decir, $500,000 por pozo). Solo se pueden explorar 500 puntos por región para elegir los mejores 200.

El objetivo no es solo encontrar la región con mayor volumen de reservas, sino maximizar el beneficio y minimizar el riesgo de pérdidas, estableciendo un umbral estricto: **el riesgo de pérdida no debe superar el 2.5%**.

## 📊 Datos

* **Fuentes:** `geo_data_0.csv`, `geo_data_1.csv`, `geo_data_2.csv`
* **Características:** 3 variables geológicas (`f0`, `f1`, `f2`) por cada punto de exploración.
* **Variable objetivo:** `product` (volumen de reservas en miles de barriles).
* **Punto de equilibrio (Break-even):** 111.11 miles de barriles por pozo (inversión de $500k / $4,500 por unidad).

## 🧠 Enfoque y Metodología

1. **Modelado Base:** Entrenamiento de un modelo de **Regresión Lineal** para predecir el volumen de reservas en cada región (división 75% train / 25% validación).
2. **Cálculo de Rentabilidad Potencial:** Selección de los 200 mejores pozos predichos en cada región para estimar el beneficio teórico.
3. **Simulación de Riesgo (Bootstrapping):**
   * Se realizaron **1,000 iteraciones**.
   * En cada iteración, se muestrearon aleatoriamente 500 pozos (simulando la exploración real) y se seleccionaron los mejores 200 según las predicciones.
   * Se calculó la distribución de beneficios, el beneficio promedio, el **Intervalo de Confianza (IC) del 95%** y el **Riesgo de Pérdida** (probabilidad de beneficio negativo).

## 🏆 Resultados de la Simulación

| Región | RMSE | Beneficio Promedio (USD) | Intervalo de Confianza (95%) | Riesgo de Pérdida |
| :--- | :---: | :---: | :---: | :---: |
| **Región 1 🏆** | **0.89** | **$4,985,690** | **$753,155 a $9,115,036** | **1.0% (Viable)** |
| Región 0 | 37.76 | $4,359,337 | -$1,162,316 a $9,665,041 | 6.1% (Inviable) |
| Región 2 | 40.15 | $4,126,728 | -$1,589,395 a $9,781,912 | 7.0% (Inviable) |

*(Nota: Las regiones 0 y 2 tienen un riesgo de pérdida mayor al 2.5% permitido, con intervalos de confianza que descienden a números negativos)*.

## ✅ Recomendación Final

**Se debe invertir en la Región 1.** Aunque la Región 0 y 2 tienen volúmenes medios predichos ligeramente superiores, su altísima varianza (RMSE) provoca que el riesgo de pérdida supere el umbral del 2.5%.

La Región 1 tiene un RMSE sorprendentemente bajo (0.89), lo que indica una correlación casi perfecta entre las características y las reservas. Esto permite una precisión quirúrgica al seleccionar los pozos, garantizando un **riesgo de pérdida de apenas 1.0%** y un beneficio promedio esperado cercano a los **$5 millones de USD**.

## 🛠️ Stack Técnico

* **Lenguajes:** Python
* **Librerías:** Pandas, Scikit-learn, NumPy, Plotly, Streamlit
* **Técnicas:** Regresión Lineal, Bootstrapping, Intervalos de Confianza, Evaluación de Riesgo, Toma de decisiones bajo incertidumbre.

## 🔗 Ver el Análisis Completo y App en Vivo

* 📓 [Notebook original con todo el código y las simulaciones](notebooks/)
* 🚀 [Simulador Interactivo de Riesgo y Beneficio (Streamlit)](https://oilygiant-oil-well-investment.streamlit.app/)
