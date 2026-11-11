# ⛽ OilyGiant — Prospección de Pozos Petroleros y Análisis de Riesgo

> Modelo de regresión lineal y simulaciones de Monte Carlo (Bootstrapping) para determinar la región con mayor rentabilidad y menor riesgo financiero para la perforación de 200 nuevos pozos petroleros.

## 🎯 Problema de Negocio

**OilyGiant** necesita decidir en cuál de tres regiones geológicas debe construir 200 nuevos pozos de petróleo. 
El presupuesto de inversión es de **$100 millones de USD** (es decir, $500,000 por pozo). Solo se pueden explorar 500 puntos por región para elegir los mejores 200.

El objetivo no es solo encontrar la región con mayor volumen de reservas, sino **maximizar el beneficio y minimizar el riesgo de pérdidas**, estableciendo un umbral estricto: el riesgo de pérdida no debe superar el **2.5%**.

## 📊 Datos

- **Fuentes:** `geo_data_0.csv`, `geo_data_1.csv`, `geo_data_2.csv`
- **Características:** 3 variables geológicas (f0, f1, f2) por cada punto de exploración.
- **Variable objetivo:** `product` (volumen de reservas en miles de barriles).
- **Punto de equilibrio (Break-even):** 111.11 miles de barriles por pozo (inversión de $500k / $4,500 por unidad).

## 🧠 Enfoque y Metodología

1. **Modelado Base:** Entrenamiento de un modelo de **Regresión Lineal** para predecir el volumen de reservas en cada región (división 75% train / 25% validación).
2. **Cálculo de Rentabilidad Potencial:** Selección de los 200 mejores pozos predichos en cada región para estimar el beneficio teórico.
3. **Simulación de Riesgo (Bootstrapping):**
   - Se realizaron **1,000 iteraciones**.
   - En cada iteración, se muestrearon aleatoriamente 500 pozos (simulando la exploración real) y se seleccionaron los mejores 200 según las predicciones.
   - Se calculó la distribución de beneficios, el beneficio promedio, el **Intervalo de Confianza (IC) del 95%** y el **Riesgo de Pérdida** (probabilidad de beneficio negativo).

## 🏆 Resultados de la Simulación

| Región | RMSE | Beneficio Promedio (USD) | Intervalo de Confianza (95%) | Riesgo de Pérdida |
| :--- | ---: | ---: | :--- | ---: |
| **Región 1** 🏆 | **0.89** | **$4,985,690** | $753,155 a $9,115,036 | **1.0%** (Viable) |
| Región 0 | 37.76 | $4,359,337 | -$1,162,316 a $9,665,041 | 6.1% (Inviable) |
| Región 2 | 40.15 | $4,126,728 | -$1,589,395 a $9,781,912 | 7.0% (Inviable) |

*(Nota: Las regiones 0 y 2 tienen un riesgo de pérdida mayor al 2.5% permitido, con intervalos de confianza que descienden a números negativos).*

## ✅ Recomendación Final

**Se debe invertir en la Región 1.**
Aunque la Región 0 y 2 tienen volúmenes medios predichos ligeramente superiores, su altísima varianza (RMSE) provoca que el riesgo de pérdida supere el umbral del 2.5%. 

La Región 1 tiene un RMSE sorprendentemente bajo (0.89), lo que indica una correlación casi perfecta entre las características y las reservas. Esto permite una precisión quirúrgica al seleccionar los pozos, garantizando un **riesgo de pérdida de apenas 1.0%** y un beneficio promedio esperado cercano a los **$5 millones de USD**.

## 🛠️ Stack Técnico
- **Lenguajes:** Python
- **Librerías:** Pandas, Scikit-learn, NumPy, Math
- **Técnicas:** Regresión Lineal, Bootstrapping, Intervalos de Confianza, Evaluación de Riesgo, Toma de decisiones bajo incertidumbre.

## 🔗 Ver el Análisis Completo
- 📓 [Notebook original con todo el código y las simulaciones](notebooks/analisis-oilygiant.ipynb)
