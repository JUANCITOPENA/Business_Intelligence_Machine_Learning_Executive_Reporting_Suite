# 🚀 BI & Machine Learning Executive Suite

### 📊 De Datos Crudos a Decisiones Ejecutivas

Suite analítica integral desarrollada en Python para transformar registros transaccionales masivos en inteligencia estratégica mediante **Business Intelligence, modelado financiero, Machine Learning y generación automatizada de reportes ejecutivos en PDF**.

---

## 🎯 Objetivo del Proyecto

Construir una solución empresarial integral, reproducible y orientada a la alta dirección (*C-Suite*), capaz de:

- ✅ **Consolidar y estructurar** datos transaccionales multianuales.
- ✅ **Calcular KPIs financieros y comerciales** clave: margen operativo, AOV, EBITDA y cuotas.
- ✅ **Aplicar modelos predictivos y de Machine Learning:** Forecast OLS, Clustering K-Means, clasificación logística y detección de fugas.
- ✅ **Detectar patrones, anomalías y oportunidades** de optimización de precios y cartera.
- ✅ **Generar cuatro dashboards panorámicos** de alta resolución (16:9), con narrativa de negocio integrada.
- ✅ **Automatizar un dossier ejecutivo de 10 páginas en PDF**, con análisis individualizado y matriz de decisiones.

---

## 🖼️ Dashboards Incluidos

### 📈 Dashboard #1: Diagnóstico Financiero y Comercial

- **Tendencia de Ventas vs. Metas:** evolución mensual con áreas sombreadas de superávit y déficit presupuestario.
- **Cascada de Rentabilidad:** descomposición del ingreso bruto, descuentos, costo de ventas, gastos operativos y beneficio neto.
- **Análisis por Canal:** facturación, margen neto y cumplimiento de metas.
- **Evolución Trimestral YoY:** comparativa interanual por trimestre (Q1–Q4) para 2024, 2025 y 2026.
- **Distribución Territorial:** participación regional y porcentaje de órdenes que superaron la meta.
- **Impacto de Descuentos sobre Márgenes:** evaluación de la erosión del margen operativo según los tramos de descuento comercial.

### 🤖 Dashboard #2: Machine Learning y Segmentación Estratégica

- **Forecast de Demanda:** tendencia lineal mediante mínimos cuadrados ordinarios (OLS), con intervalo de confianza del 95%.
- **Clustering de Clientes:** segmentación no supervisada mediante K-Means (clientes VIP, margen equilibrado y transacciones estándar).
- **Variables Impulsoras del Beneficio:** ponderación estandarizada (*Feature Weights*) de factores operativos asociados al EBITDA.
- **Detección de Anomalías:** auditoría estadística multivariable mediante Z-Scores sobre el ratio de gastos e ingresos.
- **Curva de Tolerancia al Descuento:** regresión logística para estimar la probabilidad de cumplimiento de metas según el descuento aplicado.
- **Matriz Prescriptiva:** mapa de calor del margen operativo por canal de distribución y categoría de producto.

### 🌎 Dashboard #3: Business Intelligence Moderno

- **Bullet Charts:** seguimiento de objetivos por canal, con rangos cualitativos y marcadores de cuota.
- **Curva de Pareto 80/20:** identificación de las plazas comerciales que concentran el 80% de la facturación acumulada.
- **Dumbbell Charts:** comparación del crecimiento y la contracción interanual por canal (2024 vs. 2026).
- **Lollipop Charts:** clasificación del ticket promedio (*Average Order Value — AOV*) por municipio.
- **Violin Plots:** análisis de la distribución y estabilidad del margen operativo por canal.
- **Índice de Concentración HHI:** evaluación del riesgo de concentración territorial mediante el índice Herfindahl-Hirschman.

### 🚀 Dashboard #4: Econometría Predictiva y Analítica Avanzada

- **Descomposición STL:** separación de tendencia, estacionalidad y residuos de la serie temporal.
- **Simulación Cuantílica Multiescenario:** proyección de demanda bajo escenarios pesimista (P10), base (P50) y optimista (P90).
- **PCA Biplot 2D:** reducción de dimensionalidad mediante análisis de componentes principales y descomposición en valores singulares (SVD).
- **Curva ROC y AUC:** evaluación del clasificador de probabilidad de éxito presupuestario.
- **Correlaciones de Pearson:** análisis de interdependencia entre unidades, precios, costos, descuentos e ingresos.
- **Elasticidad Precio-Demanda:** regresión logarítmica para estudiar la respuesta de la demanda y los ingresos ante cambios en los precios.

---

## 📄 Dossier Ejecutivo en PDF — 10 Páginas

El proyecto contempla la generación automatizada de un documento corporativo para impresión, presentación y revisión en comités directivos.

| Página | Contenido |
|:---:|---|
| 1 | Portada ejecutiva, KPIs principales y síntesis metodológica de auditoría. |
| 2 | Dashboard #1: diagnóstico financiero y comercial. |
| 3 | Análisis técnico de los seis gráficos del Dashboard #1: métricas, causas y decisiones. |
| 4 | Dashboard #2: Machine Learning clásico. |
| 5 | Análisis técnico de los seis gráficos del Dashboard #2. |
| 6 | Dashboard #3: BI moderno y concentración. |
| 7 | Análisis técnico de los seis gráficos del Dashboard #3. |
| 8 | Dashboard #4: econometría y modelos avanzados. |
| 9 | Análisis técnico de los seis gráficos del Dashboard #4. |
| 10 | Conclusiones y matriz prescriptiva de decisiones con planes de acción e impactos estimados en EBITDA. |

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Aplicación |
|---|---|
| **Python 3.10+** | Lenguaje principal del proyecto. |
| **Pandas** | Manipulación, limpieza y estructuración de datos. |
| **NumPy** | Computación vectorizada e implementaciones numéricas de modelos. |
| **Matplotlib** | Visualización, composición y renderizado de dashboards. |
| **PdfPages** | Generación de documentos PDF mediante Matplotlib. |

**Enfoques analíticos:**

- Business Intelligence (BI).
- Data Analytics.
- Machine Learning.
- Econometría.
- Analítica financiera.
- Prescriptive Analytics.
- Automatización de informes ejecutivos.

---

## 📂 Estructura del Proyecto

```text
Proyecto_BI_ML/
│
├── datos/
│   └── Reporte_Transaccional_2024_2026.csv
│
├── imagenes/
│   ├── reporte_1_bi_ejecutivo.png
│   ├── reporte_2_ml_ejecutivo.png
│   ├── reporte_3_bi_moderno.png
│   └── reporte_4_ml_econometria.png
│
├── reportes/
│   └── Dossier_Ejecutivo_BI_ML_Completo.pdf
│
├── ml_analisis.py
├── requirements.txt
└── README.md
```

> **Nota:** esta estructura representa la organización prevista del proyecto. Los nombres de archivos y carpetas deben coincidir con los que realmente existan en el repositorio.

---

## ▶️ Ejecución del Proyecto

Sigue estos pasos desde la carpeta raíz del repositorio.

### 1. Crear el entorno virtual

```bash
python -m venv .venv
```

### 2. Activar el entorno virtual

**🪟 Windows — CMD o PowerShell**

```powershell
.venv\Scripts\activate
```

**🐧 Linux / 🍎 macOS**

```bash
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Ejecutar el análisis

```bash
python ml_analisis.py
```

### ⚠️ Requisitos previos

Antes de ejecutar el proyecto, verifica que:

- Tienes instalado Python 3.10 o una versión compatible.
- El archivo `requirements.txt` contiene las dependencias necesarias.
- El archivo CSV de entrada está disponible en la ruta esperada por el script.
- Las carpetas de salida existen o el programa está preparado para crearlas automáticamente.

---

## 📁 Salidas Generadas

Al finalizar el proceso, se esperan los siguientes entregables:

- ✅ **Dashboard Ejecutivo #1:** diagnóstico financiero y comercial.
- ✅ **Dashboard Ejecutivo #2:** Machine Learning y segmentación estratégica.
- ✅ **Dashboard Ejecutivo #3:** Business Intelligence moderno.
- ✅ **Dashboard Ejecutivo #4:** econometría predictiva y analítica avanzada.
- ✅ **Dossier Ejecutivo PDF:** informe consolidado para la toma de decisiones.

Los archivos se guardarán en las ubicaciones definidas por la configuración del proyecto.

---

## 💼 Caso de Uso

La solución demuestra cómo una organización puede evolucionar desde reportes operativos tradicionales hacia una plataforma de análisis estratégico que respalde decisiones basadas en datos.

Está orientada a los siguientes perfiles:

- 👨‍💼 **CEO:** dirección estratégica y visión integral del negocio.
- 💰 **CFO:** rentabilidad, costos, márgenes y planificación financiera.
- 📈 **COO:** eficiencia operativa y seguimiento del desempeño.
- 🏢 **Directores de Negocio:** evaluación comercial y oportunidades de crecimiento.
- 📊 **Equipos de BI y Data Analytics:** análisis, visualización e interpretación de indicadores.

### 🎯 Valor empresarial

La combinación de indicadores históricos, segmentación, modelos predictivos y análisis de escenarios permite explorar preguntas como:

- ¿Qué canales comerciales generan mejores márgenes?
- ¿Dónde se concentra el riesgo financiero o territorial?
- ¿Qué descuentos pueden comprometer la rentabilidad?
- ¿Qué tendencias podrían orientar la planificación futura?
- ¿Qué acciones conviene priorizar para mejorar los resultados?

Los modelos proporcionan estimaciones y señales para apoyar el criterio directivo; sus conclusiones deben validarse con los datos y las condiciones reales del negocio.

---

## 🚀 Conclusión

Los datos por sí solos no generan valor.

El verdadero valor surge cuando se transforman en **conocimiento, contexto y decisiones estratégicas**.

Esta solución integra **Business Intelligence, Machine Learning, analítica financiera y automatización documental** para convertir información transaccional en conocimiento accionable y contribuir a una ventaja competitiva sostenible.

El objetivo no es únicamente visualizar lo que ocurrió, sino también identificar patrones, evaluar escenarios y aportar información útil para decidir qué hacer a continuación.

⭐ **¿Te resulta útil este proyecto?** Considera darle una estrella al repositorio y compartirlo con la comunidad.

---

## 📢 Tecnologías y Temáticas

`Python` · `DataScience` · `MachineLearning` · `BusinessIntelligence` · `Analytics` · `DataAnalytics` · `BI` · `ArtificialIntelligence` · `ExecutiveReporting` · `DataEngineering` · `FinancialAnalytics` · `PredictiveAnalytics` · `Econometrics`

---

**Desarrollado con Python para transformar datos en inteligencia estratégica.**
