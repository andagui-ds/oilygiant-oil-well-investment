# 🏗️ ¿Dónde perforar? Decisión de inversión de $100M con Machine Learning

**Problema de negocio:** OilyGiant debía elegir entre 3 regiones para perforar 200 pozos petrolíferos con un presupuesto de **$100 millones**. La decisión implicaba analizar el volumen esperado de reservas y, sobre todo, el **riesgo de pérdida** en cada región.

**Objetivo:** seleccionar la región con mayor beneficio esperado manteniendo un **riesgo de pérdida inferior al 2.5%**.

---

## 📊 Resultado principal

| Región | Beneficio esperado | IC 95% (inferior) | IC 95% (superior) | Riesgo de pérdida | ¿Viable? |
|---|---|---|---|---|---|
| Región 0 | $4.28M | -$0.97M | $9.54M | 5.5% | ❌ |
| **Región 1** | **$5.12M** | **$0.92M** | **$9.21M** | **0.6%** | ✅ |
| Región 2 | $4.09M | -$1.21M | $9.61M | 7.5% | ❌ |

> **Recomendación:** perforar en la **Región 1**. Es la única que cumple con todos los criterios: beneficio esperado alto, IC 95% completamente positivo y riesgo de pérdida muy por debajo del umbral del 2.5%.

---

## 🛠️ Metodología

1. **Exploración de datos:** 3 datasets geológicos independientes (uno por región) con ~10,000 registros cada uno.
2. **Modelado:** regresión lineal para predecir el volumen de reservas de cada pozo (requisito del negocio por interpretabilidad).
3. **Selección:** de los 500 pozos explorados, elegir los 200 con mayor predicción de reservas.
4. **Evaluación de riesgo:** 1,000 simulaciones de **bootstrapping** (muestreo con reemplazo de 500 pozos) para estimar la distribución de beneficios, el IC 95% y la probabilidad de pérdida.
5. **Punto de equilibrio:** 111.11 miles de barriles por pozo (ingreso de $4,500 por unidad vs. costo de $500,000 por pozo).

---

## 📁 Contenido del repositorio

- `notebooks/01-analisis-principal.ipynb`: análisis completo (EDA, modelado, bootstrapping y visualizaciones).
- `requirements.txt`: dependencias para reproducir el análisis.
- `images/`: gráficos exportados para el README.

---

## ▶️ Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01-analisis-principal.ipynb