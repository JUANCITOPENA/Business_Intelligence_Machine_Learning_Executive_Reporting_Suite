# 🚀 BI & Machine Learning Executive Suite
### 📊 De Datos Crudos a Decisiones Ejecutivas

Suite analítica integral desarrollada en Python para transformar registros transaccionales masivos en inteligencia estratégica mediante **Business Intelligence**, **Modelado Financiero**, **Machine Learning nativo** y **Generación Automatizada de Reportes Ejecutivos en PDF**.

---

## 🎯 Objetivo del Proyecto

Construir una solución empresarial integral, reproducible y de nivel directivo (C-Suite) capaz de:

* ✅ **Consolidar y estructurar** datos transaccionales multianuales.
* ✅ **Calcular KPIs financieros y comerciales** clave (Margen Operativo, AOV, EBITDA, Cuotas).
* ✅ **Aplicar modelos predictivos y de Machine Learning** (Forecast OLS, Clustering K-Means, Clasificación Logística, Detección de Fugas).
* ✅ **Detectar patrones, anomalías y oportunidades** de optimización de precios y cartera.
* ✅ **Generar 4 dashboards panorámicos de alta resolución (16:9)** con narrativa de negocio integrada.
* ✅ **Automatizar la creación de un dossier ejecutivo en PDF de 10 páginas** con análisis individualizado y matriz de decisiones.

---

## 🖼️ Dashboards Incluidos

### 📈 Dashboard #1: Diagnóstico Financiero y Comercial
* **Tendencia de Ventas vs. Metas:** Evolución mensual con áreas sombreadas de superávit y déficit presupuestario.
* **Cascada de Rentabilidad:** Deconstrucción del Ingreso Bruto restando descuentos, costo de ventas y gastos operativos.
* **Análisis por Canal:** Volumen de facturación, porcentaje de margen neto y tasa de alcance de metas.
* **Evolución Trimestral YoY:** Comparativa interanual estacional por trimestres (Q1 a Q4) para 2024, 2025 y 2026.
* **Distribución Territorial:** Participación por regiones y porcentaje de órdenes que superaron la meta.
* **Impacto de Descuentos sobre Márgenes:** Evaluación de erosión de margen operativo según tramos de rebaja comercial.

### 🤖 Dashboard #2: Machine Learning y Segmentación Estratégica
* **Forecast de Demanda:** Tendencia lineal por mínimos cuadrados ordinarios (OLS) con intervalo de confianza al 95%.
* **Clustering de Clientes:** Segmentación K-Means no supervisada (Clientes VIP, Margen Equilibrado, Transacciones Estándar).
* **Variables Impulsoras del Beneficio:** Ponderación estandarizada (*Feature Weights*) de factores operativos sobre el EBITDA.
* **Detección de Anomalías:** Auditoría estadística multivariable con Z-Scores sobre el ratio de gastos/ingresos.
* **Curva de Tolerancia al Descuento:** Regresión logística que calcula la frontera exacta de quiebre comercial ($P(\text{Meta}) < 50\%$).
* **Matriz Prescriptiva:** Mapa de calor de margen operativo cruzando canales de distribución vs. categorías de producto.

### 🌎 Dashboard #3: Business Intelligence Moderno
* **Bullet Charts:** Seguimiento de metas por canal con rangos cualitativos (deficiente, aceptable, excelente) y marcador de cuota.
* **Curva de Pareto 80/20:** Identificación de plazas urbanas clave que concentran el 80% de la facturación acumulada.
* **Dumbbell Charts:** Brecha de crecimiento y contracción interanual (2024 vs. 2026) por canal comercial.
* **Lollipop Charts:** Ranking de Ticket Promedio (*Average Order Value* - AOV) por municipio.
* **Violin Plots:** Distribución de densidad de probabilidad y estabilidad del margen operativo por canal.
* **Índice de Concentración HHI:** Medición del riesgo de concentración territorial mediante el Índice Herfindahl-Hirschman.

### 🚀 Dashboard #4: Econometría Predictiva y Analítica Avanzada
* **Descomposición STL:** Aislamiento de la tendencia central móvil (MA-3) frente a componentes estacionales y residuales.
* **Simulación Cuantílica Multiescenario:** Proyección de demanda bajo estrés macroeconómico (P10 Pesimista, P50 Base, P90 Optimista).
* **PCA Biplot 2D:** Reducción de dimensionalidad por descomposición en valores singulares (SVD) para mapear vectores financieros.
* **Curva ROC y AUC:** Evaluación del clasificador de probabilidad de éxito presupuestario.
* **Correlaciones de Pearson:** Matriz numérica de interdependencia entre unidades, precios, costos, descuentos e ingresos.
* **Elasticidad Precio-Demanda:** Regresión logarítmica para determinar la respuesta de la demanda e ingresos ante ajustes de precio base.

---

## 📄 Dossier Ejecutivo en PDF (10 Páginas)

El script genera automáticamente un documento corporativo listo para impresión y comités directivos, estructurado de la siguiente forma:

1. **Página 1:** Portada ejecutiva, tarjetas de KPIs principales y síntesis metodológica de auditoría.
2. **Página 2:** Lámina 1 completa en alta resolución (Diagnóstico Financiero).
3. **Página 3:** Análisis técnico individualizado de los 6 cuadrantes de la Lámina 1 (Métricas, Causas y Decisiones).
4. **Página 4:** Lámina 2 completa en alta resolución (Machine Learning Clásico).
5. **Página 5:** Análisis técnico individualizado de los 6 cuadrantes de la Lámina 2.
6. **Página 6:** Lámina 3 completa en alta resolución (BI Moderno y Concentración).
7. **Página 7:** Análisis técnico individualizado de los 6 cuadrantes de la Lámina 3.
8. **Página 8:** Lámina 4 completa en alta resolución (Econometría y Modelos Avanzados).
9. **Página 9:** Análisis técnico individualizado de los 6 cuadrantes de la Lámina 4.
10. **Página 10:** Conclusiones finales y **Matriz Prescriptiva de Decisiones** con planes de acción e impactos estimados en EBITDA.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Manipulación de Datos:** Pandas
* **Computación Vectorizada y ML:** NumPy (implementaciones vectorizadas de OLS, K-Means, SVD y Regresión Logística)
* **Visualización y Renderizado:** Matplotlib
* **Generación Documental:** Matplotlib PDF Backend (`PdfPages`)
* **Enfoques:** Business Intelligence, Data Analytics, Econometría, Prescriptive Analytics

---

## 📂 Estructura del Proyecto

```text
📦 Proyecto_BI_ML
│
├── 📂 datos
│   └── 📄 Reporte_Transaccional_2024_2026.csv
│
├── 📂 imagenes
│   ├── 🖼️ reporte_1_bi_ejecutivo.png
│   ├── 🖼️ reporte_2_ml_ejecutivo.png
│   ├── 🖼️ reporte_3_bi_moderno.png
│   └── 🖼️ reporte_4_ml_econometria.png
│
├── 📂 reportes
│   └── 📄 Dossier_Ejecutivo_BI_ML_Completo.pdf
│
├── 🐍 ml_analisis.py
├── 📜 requirements.txt
└── 📘 README.md

▶️ Instalación y Ejecución
1️⃣ Crear entorno virtual
Bash
python -m venv .venv
2️⃣ Activar entorno virtual
Windows (PowerShell):

PowerShell
.venv\Scripts\Activate.ps1
Windows (CMD):

DOS
.venv\Scripts\activate.bat
Linux / macOS:

Bash
source .venv/bin/activate
3️⃣ Instalar dependencias
Bash
pip install -r requirements.txt
Contenido de requirements.txt:

Plaintext
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
4️⃣ Ejecutar la Suite Analítica
Bash
python ml_analisis.py
📁 Salidas Generadas
Al finalizar el proceso, se crearán de manera automática:

reporte_1_bi_ejecutivo.png (Dashboard Financiero 16:9)

reporte_2_ml_ejecutivo.png (Dashboard Machine Learning 16:9)

reporte_3_bi_moderno.png (Dashboard BI Moderno 16:9)

reporte_4_ml_econometria.png (Dashboard Econometría 16:9)

Dossier_Ejecutivo_BI_ML_Completo.pdf (Informe Ejecutivo Consolidado de 10 páginas)

💡 Casos de Uso y Audiencia
Diseñado para respaldar la toma de decisiones basada en datos para:

👨‍💼 CEO / Dirección General: Supervisión integral de rentabilidad, balance regional y posicionamiento comercial.

💰 CFO / Dirección de Finanzas: Control de retención neta, auditoría de fugas por descuentos y proyecciones de estrés (P10/P50/P90).

📈 COO / Dirección de Operaciones: Diagnóstico de costos de flete, logística y rendimiento por canal de distribución.

🏢 Dirección Comercial: Fijación de topes estrictos de descuento y programas de lealtad para clientes de gran volumen.

📊 Equipos de Data Science y BI: Plantilla reproducible de código limpio sin dependencias propietarias complejas.

🚀 Conclusión
Los datos por sí solos no generan valor. El verdadero valor surge cuando se transforman en conocimiento, contexto y decisiones estratégicas cuantitativas.

Esta suite demuestra cómo integrar Business Intelligence, Machine Learning, Analítica Financiera y Automatización Documental para transformar registros transaccionales en una ventaja competitiva sostenible.

⭐ Si este proyecto te resulta útil, considera darle una estrella al repositorio.
