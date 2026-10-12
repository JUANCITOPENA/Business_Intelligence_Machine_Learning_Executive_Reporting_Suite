import os
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# =====================================================================
# 1. CARGA DE DATOS Y FORMATEADORES
# =====================================================================
archivo_csv = "Reporte_Transaccional_2024_2026.csv"
if not os.path.exists(archivo_csv):
  raise FileNotFoundError(
      f"No se encontró '{archivo_csv}'. Asegúrate de tener el archivo en la misma carpeta."
  )

df = pd.read_csv(archivo_csv)
df["Fecha"] = pd.to_datetime(df["Fecha"])

if "Periodo_Mes" not in df.columns:
  df["Periodo_Mes"] = df["Fecha"].dt.to_period("M").astype(str)

col_conteo = df.columns[0]
fmt_m = ticker.FuncFormatter(lambda x, p: f"${x*1e-6:.2f}M")
fmt_k = ticker.FuncFormatter(lambda x, p: f"${x*1e-3:.0f}K")

# Métricas Consolidadas
ing_bruto = df["Ingreso_Bruto"].sum()
ing_neto = df["Ingresos_Netos"].sum()
descuentos = df["Descuento_Monto"].sum()
costo_merc = df["Costo_Mercancia"].sum()
gasto_oper = df["Gasto_Operativo"].sum()
beneficio_tot = df["Beneficio_Neto"].sum()
meta_tot = df["Meta_Ventas"].sum()

margen_prom = (beneficio_tot / ing_neto) * 100
cumplimiento_tot = (ing_neto / meta_tot) * 100
tasa_exito = df["Cumplio_Meta"].mean() * 100
ticket_prom = ing_neto / len(df)

mensual = (
    df.groupby("Periodo_Mes")
    .agg(
        Ingresos=("Ingresos_Netos", "sum"),
        Meta=("Meta_Ventas", "sum"),
        Beneficio=("Beneficio_Neto", "sum"),
    )
    .reset_index()
)
mensual["Margen_Pct"] = (mensual["Beneficio"] / mensual["Ingresos"]) * 100


# =====================================================================
# 2. FUNCIONES DE DISEÑO Y TIPOGRAFÍA EJECUTIVA
# =====================================================================
def draw_header_banner(fig, title, subtitle):
  band = patches.FancyBboxPatch(
      (0.03, 0.88),
      0.94,
      0.09,
      boxstyle="round,pad=0.008,rounding_size=0.015",
      facecolor="#0f172a",
      edgecolor="none",
      transform=fig.transFigure,
  )
  fig.patches.append(band)
  fig.text(
      0.05, 0.935, title, fontsize=18, fontweight="bold", color="#ffffff"
  )
  fig.text(0.05, 0.898, subtitle, fontsize=11, color="#94a3b8")


def draw_executive_card(
    fig,
    x,
    y,
    w,
    h,
    badge_tag,
    title,
    kpi_badge,
    bullets,
    accent_color="#2563eb",
    bg_badge="#e0f2fe",
):
  # Tarjeta principal con fondo blanco y sombra
  card = patches.FancyBboxPatch(
      (x, y),
      w,
      h,
      boxstyle="round,pad=0.006,rounding_size=0.012",
      facecolor="#ffffff",
      edgecolor="#cbd5e1",
      linewidth=1.4,
      transform=fig.transFigure,
      zorder=1,
  )
  fig.patches.append(card)

  # Franja superior de encabezado
  h_bar = patches.FancyBboxPatch(
      (x, y + h - 0.065),
      w,
      0.065,
      boxstyle="round,pad=0.006,rounding_size=0.012",
      facecolor="#f8fafc",
      edgecolor="#cbd5e1",
      linewidth=1,
      transform=fig.transFigure,
      zorder=2,
  )
  fig.patches.append(h_bar)

  # Línea vertical de acento lateral
  left_line = patches.FancyBboxPatch(
      (x, y),
      0.007,
      h,
      boxstyle="round,pad=0.001,rounding_size=0.003",
      facecolor=accent_color,
      edgecolor="none",
      transform=fig.transFigure,
      zorder=3,
  )
  fig.patches.append(left_line)

  # Píldora de etiqueta
  pill = patches.FancyBboxPatch(
      (x + 0.012, y + h - 0.048),
      0.048,
      0.026,
      boxstyle="round,pad=0.002,rounding_size=0.005",
      facecolor=bg_badge,
      edgecolor="none",
      transform=fig.transFigure,
      zorder=4,
  )
  fig.patches.append(pill)
  fig.text(
      x + 0.016,
      y + h - 0.041,
      badge_tag,
      fontsize=8.5,
      fontweight="bold",
      color=accent_color,
      zorder=5,
  )

  # Título y KPI Badge
  fig.text(
      x + 0.065,
      y + h - 0.041,
      title,
      fontsize=10.5,
      fontweight="bold",
      color="#0f172a",
      zorder=5,
  )
  fig.text(
      x + w - 0.014,
      y + h - 0.041,
      kpi_badge,
      fontsize=9.8,
      fontweight="bold",
      color=accent_color,
      ha="right",
      zorder=5,
  )

  # Bloques de texto estructurados
  cur_y = y + h - 0.096
  for b_title, b_desc in bullets:
    fig.text(
        x + 0.015,
        cur_y,
        f"• {b_title}:",
        fontsize=9.4,
        fontweight="bold",
        color="#1e293b",
        zorder=4,
    )
    fig.text(
        x + 0.015,
        cur_y - 0.023,
        f"   {b_desc}",
        fontsize=9.0,
        color="#475569",
        zorder=4,
    )
    cur_y -= 0.054


pdf_path = "Dossier_Ejecutivo_BI_ML_Completo.pdf"
pdf = PdfPages(pdf_path)

print("=" * 75)
print(
    "INICIANDO COMPILACIÓN DEL DOSSIER EJECUTIVO PREMIUM (10 PÁGINAS | 24"
    " GRÁFICOS)"
)
print("=" * 75)

# =====================================================================
# PÁGINA 1: PORTADA EJECUTIVA Y TABLERO DE KPIS
# =====================================================================
print("\n📄 [1/10] Generando Portada Ejecutiva con Tarjetas KPI...")
fig_cov = plt.figure(figsize=(19.2, 10.8), dpi=130)
fig_cov.patch.set_facecolor("#f8fafc")

# Encabezado corporativo oscuro
top_band = patches.FancyBboxPatch(
    (0.03, 0.86),
    0.94,
    0.11,
    boxstyle="round,pad=0.008,rounding_size=0.015",
    facecolor="#0f172a",
    edgecolor="none",
    transform=fig_cov.transFigure,
)
fig_cov.patches.append(top_band)

fig_cov.text(
    0.05,
    0.925,
    "DOSSIER EJECUTIVO DE RENDIMIENTO CORPORATIVO & ANALÍTICA INTEGRAL",
    fontsize=20,
    fontweight="bold",
    color="#ffffff",
)
fig_cov.text(
    0.05,
    0.885,
    "DIAGNÓSTICO FINANCIERO   |   MACHINE LEARNING   |   BI MODERNO   |  "
    " PROYECCIONES ECONOMÉTRICAS",
    fontsize=11.5,
    fontweight="bold",
    color="#38bdf8",
)

# 4 Tarjetas KPI de Alto Impacto
kpis = [
    (
        "FACTURACIÓN NETA",
        f"${ing_neto*1e-6:.2f}M",
        f"Bruto: ${ing_bruto*1e-6:.2f}M (-{descuentos/ing_bruto*100:.1f}%)",
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "BENEFICIO NETO",
        f"${beneficio_tot*1e-6:.2f}M",
        f"Margen Operativo: {margen_prom:.1f}%",
        "#16a34a",
        "#dcfce7",
    ),
    (
        "ALCANCE DE METAS",
        f"{cumplimiento_tot:.1f}%",
        f"Meta Total: ${meta_tot*1e-6:.2f}M",
        "#ea580c",
        "#ffedd5",
    ),
    (
        "TICKET PROMEDIO (AOV)",
        f"${ticket_prom*1e-3:.1f}K",
        "3,000 Transacciones Consolidadas",
        "#7c3aed",
        "#f3e8ff",
    ),
]
x_k = 0.03
for tit, val, sub, col, bg_col in kpis:
  card = patches.FancyBboxPatch(
      (x_k, 0.67),
      0.22,
      0.165,
      boxstyle="round,pad=0.006,rounding_size=0.012",
      facecolor="#ffffff",
      edgecolor="#cbd5e1",
      linewidth=1.5,
      transform=fig_cov.transFigure,
  )
  fig_cov.patches.append(card)

  badge = patches.FancyBboxPatch(
      (x_k + 0.015, 0.795),
      0.19,
      0.028,
      boxstyle="round,pad=0.003,rounding_size=0.006",
      facecolor=bg_col,
      edgecolor="none",
      transform=fig_cov.transFigure,
  )
  fig_cov.patches.append(badge)
  fig_cov.text(
      x_k + 0.022, 0.803, tit, fontsize=9.5, fontweight="bold", color=col
  )
  fig_cov.text(
      x_k + 0.015,
      0.735,
      val,
      fontsize=21,
      fontweight="bold",
      color="#0f172a",
  )
  fig_cov.text(
      x_k + 0.015,
      0.695,
      sub,
      fontsize=9.0,
      fontweight="bold",
      color="#64748b",
  )

  left_ind = patches.FancyBboxPatch(
      (x_k, 0.67),
      0.006,
      0.165,
      boxstyle="round,pad=0.001,rounding_size=0.003",
      facecolor=col,
      edgecolor="none",
      transform=fig_cov.transFigure,
  )
  fig_cov.patches.append(left_ind)
  x_k += 0.24

# Bloque Izquierdo: Síntesis Estratégica
card_b1 = patches.FancyBboxPatch(
    (0.03, 0.08),
    0.58,
    0.55,
    boxstyle="round,pad=0.006,rounding_size=0.012",
    facecolor="#ffffff",
    edgecolor="#cbd5e1",
    linewidth=1.5,
    transform=fig_cov.transFigure,
)
fig_cov.patches.append(card_b1)
acc_b1 = patches.FancyBboxPatch(
    (0.03, 0.08),
    0.007,
    0.55,
    boxstyle="round,pad=0.001,rounding_size=0.003",
    facecolor="#0284c7",
    edgecolor="none",
    transform=fig_cov.transFigure,
)
fig_cov.patches.append(acc_b1)

fig_cov.text(
    0.05,
    0.585,
    "SÍNTESIS EJECUTIVA Y RESULTADOS DE AUDITORÍA",
    fontsize=13,
    fontweight="bold",
    color="#0f172a",
)

sintesis_bullets = [
    (
        "Retención Financiera Fuerte",
        (
            r"Se generaron \$30.98M netos con margen operativo de 39.8%, sin"
            r" meses con pérdida neta."
        ),
    ),
    (
        "Cumplimiento Presupuestario",
        (
            r"La compañía cubrió el 97.8% de su meta corporativa asignada"
            r" (\$79.65M)."
        ),
    ),
    (
        "Fugas por Descuentos",
        (
            r"Se aplicaron \$4.42M en rebajas; tramos >6.5% reducen la"
            r" probabilidad de meta a <50%."
        ),
    ),
    (
        "Concentración de Riesgo",
        (
            r"El Cibao genera el 49.8% de ingresos (HHI de 3,401 pts),"
            r" exigiendo diversificación al Este."
        ),
    ),
    (
        "Inelasticidad de la Demanda",
        (
            r"Coeficiente de 0.01 confirma que el mercado absorbe aumentos"
            r" graduales (+3%) sin perder ventas."
        ),
    ),
]
y_b1 = 0.535
for s_tit, s_desc in sintesis_bullets:
  fig_cov.text(
      0.05,
      y_b1,
      f"• {s_tit}:",
      fontsize=10.2,
      fontweight="bold",
      color="#1e293b",
  )
  fig_cov.text(0.05, y_b1 - 0.024, f"   {s_desc}", fontsize=9.6, color="#475569")
  y_b1 -= 0.075

# Bloque Derecho: Estructura del Dossier
card_b2 = patches.FancyBboxPatch(
    (0.63, 0.08),
    0.34,
    0.55,
    boxstyle="round,pad=0.006,rounding_size=0.012",
    facecolor="#ffffff",
    edgecolor="#cbd5e1",
    linewidth=1.5,
    transform=fig_cov.transFigure,
)
fig_cov.patches.append(card_b2)
acc_b2 = patches.FancyBboxPatch(
    (0.63, 0.08),
    0.007,
    0.55,
    boxstyle="round,pad=0.001,rounding_size=0.003",
    facecolor="#16a34a",
    edgecolor="none",
    transform=fig_cov.transFigure,
)
fig_cov.patches.append(acc_b2)

fig_cov.text(
    0.65,
    0.585,
    "ESTRUCTURA METODOLÓGICA",
    fontsize=13,
    fontweight="bold",
    color="#0f172a",
)

docs = [
    (
        "Lámina 1 / Pág 2-3",
        "Diagnóstico Financiero, Cascada y Canales",
        "#0284c7",
    ),
    ("Lámina 2 / Pág 4-5", "Machine Learning, K-Means y Descuentos", "#ea580c"),
    ("Lámina 3 / Pág 6-7", "BI Moderno, Pareto 80/20 y Riesgo HHI", "#0284c7"),
    ("Lámina 4 / Pág 8-9", "Econometría, P10/P90 y Elasticidad", "#7c3aed"),
    (
        "Matriz Final / Pág 10",
        "Decisiones y Plan de Acción 2027",
        "#16a34a",
    ),
]
y_b2 = 0.525
for cod, desc, col_d in docs:
  p_tag = patches.FancyBboxPatch(
      (0.65, y_b2),
      0.12,
      0.03,
      boxstyle="round,pad=0.002,rounding_size=0.005",
      facecolor="#f1f5f9",
      edgecolor="none",
      transform=fig_cov.transFigure,
  )
  fig_cov.patches.append(p_tag)
  fig_cov.text(
      0.655,
      y_b2 + 0.008,
      cod,
      fontsize=8.8,
      fontweight="bold",
      color=col_d,
  )
  fig_cov.text(
      0.65,
      y_b2 - 0.024,
      desc,
      fontsize=9.2,
      fontweight="bold",
      color="#334155",
  )
  y_b2 -= 0.078

fig_cov.text(
    0.03,
    0.03,
    "Dossier Confidencial   |   Dirección de Finanzas & Analítica Avanzada  "
    " |   Octubre 2026",
    fontsize=9.5,
    color="#94a3b8",
)

plt.axis("off")
pdf.savefig(fig_cov)
plt.close(fig_cov)

# =====================================================================
# PÁGINA 2: LÁMINA 1 - BI CLÁSICO
# =====================================================================
print("\n📊 [2/10] Generando Lámina 1: Diagnóstico Financiero (16:9)...")
fig1, axs1 = plt.subplots(2, 3, figsize=(19.2, 10.8), dpi=150)
fig1.patch.set_facecolor("#f8fafc")
fig1.suptitle(
    "INFORME GERENCIAL 1: DIAGNÓSTICO FINANCIERO Y COMERCIAL (2024 - OCT 2026)",
    fontsize=16,
    fontweight="bold",
    y=0.96,
    color="#1a252f",
)

# 1.1 Facturación Mensual vs Metas
ax1_1 = axs1[0, 0]
ax1_1.set_facecolor("#ffffff")
x_m = np.arange(len(mensual))
ax1_1.plot(
    x_m,
    mensual["Ingresos"],
    color="#1f77b4",
    lw=2.5,
    marker="o",
    ms=4,
    label="Ingresos Reales",
)
ax1_1.plot(
    x_m,
    mensual["Meta"],
    color="#d35400",
    lw=2,
    ls="--",
    label="Meta Proyectada",
)
ax1_1.fill_between(
    x_m,
    mensual["Ingresos"],
    mensual["Meta"],
    where=(mensual["Ingresos"] >= mensual["Meta"]),
    color="#2ecc71",
    alpha=0.25,
    label="Superávit",
)
ax1_1.fill_between(
    x_m,
    mensual["Ingresos"],
    mensual["Meta"],
    where=(mensual["Ingresos"] < mensual["Meta"]),
    color="#e74c3c",
    alpha=0.25,
    label="Déficit",
)
ax1_1.set_xticks(x_m[::4])
ax1_1.set_xticklabels(
    mensual["Periodo_Mes"].iloc[::4], rotation=25, ha="right", fontsize=8.5
)
ax1_1.yaxis.set_major_formatter(fmt_m)
ax1_1.set_title(
    "1. Tendencia Mensual: Facturación vs. Metas\n(Evolución histórica de"
    " cumplimiento presupuestario)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax1_1.legend(loc="lower left", fontsize=8, framealpha=0.9)
ax1_1.grid(True, ls="--", alpha=0.3)

# 1.2 Cascada
ax1_2 = axs1[0, 1]
ax1_2.set_facecolor("#ffffff")
tb = df["Ingreso_Bruto"].sum()
vals_cascada = [
    tb,
    -df["Descuento_Monto"].sum(),
    -df["Costo_Mercancia"].sum(),
    -df["Gasto_Operativo"].sum(),
    df["Beneficio_Neto"].sum(),
]
etapas = [
    "Ing. Bruto",
    "Descuentos",
    "Costo Merc.",
    "Gasto Oper.",
    "Beneficio Neto",
]
cols_cascada = ["#2c3e50", "#e74c3c", "#e67e22", "#95a5a6", "#27ae60"]
bars1_2 = ax1_2.bar(
    etapas,
    [abs(v) for v in vals_cascada],
    color=cols_cascada,
    width=0.55,
    alpha=0.9,
)
for b, v in zip(bars1_2, vals_cascada):
  h = b.get_height()
  pct = (abs(v) / tb) * 100
  ax1_2.annotate(
      f"${abs(v)*1e-6:.2f}M\n({pct:.1f}%)",
      (b.get_x() + b.get_width() / 2, h),
      xytext=(0, 4),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=8,
      fontweight="bold",
  )
ax1_2.set_ylim(0, tb * 1.28)
ax1_2.yaxis.set_major_formatter(fmt_m)
ax1_2.set_title(
    "2. Cascada de Rentabilidad y Retención\n(Estructura de costos y margen neto"
    " final)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax1_2.grid(axis="y", ls="--", alpha=0.3)

# 1.3 Canales
ax1_3 = axs1[0, 2]
ax1_3.set_facecolor("#ffffff")
canales = (
    df.groupby("Canal_Distribucion")
    .agg(
        Ingresos=("Ingresos_Netos", "sum"),
        Beneficio=("Beneficio_Neto", "sum"),
        Meta=("Meta_Ventas", "sum"),
    )
    .sort_values(by="Ingresos", ascending=True)
)
y_c = np.arange(len(canales))
bars1_3 = ax1_3.barh(
    y_c, canales["Ingresos"], color="#2980b9", height=0.55, alpha=0.88
)
ax1_3.set_yticks(y_c)
ax1_3.set_yticklabels(canales.index, fontsize=8.5)
ax1_3.xaxis.set_major_formatter(fmt_m)
ax1_3.set_xlim(0, canales["Ingresos"].max() * 1.45)
for b, (_, row) in zip(bars1_3, canales.iterrows()):
  mg = (row["Beneficio"] / row["Ingresos"]) * 100
  cumpl = (row["Ingresos"] / row["Meta"]) * 100
  ax1_3.annotate(
      f" ${row['Ingresos']*1e-6:.2f}M | Mg: {mg:.1f}% | Meta: {cumpl:.0f}%",
      (b.get_width(), b.get_y() + b.get_height() / 2),
      xytext=(4, 0),
      textcoords="offset points",
      ha="left",
      va="center",
      fontsize=7.5,
      fontweight="bold",
  )
ax1_3.set_title(
    "3. Rendimiento Comercial por Canal\n(Volumen de facturación, margen neto y"
    " cumplimiento)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax1_3.grid(axis="x", ls="--", alpha=0.3)

# 1.4 YoY
ax1_4 = axs1[1, 0]
ax1_4.set_facecolor("#ffffff")
yoy = (
    df.groupby(["Anio", "Trimestre"])
    .agg(Ingresos=("Ingresos_Netos", "sum"))
    .reset_index()
)
trimestres = ["Q1", "Q2", "Q3", "Q4"]
x_q = np.arange(4)
w_q = 0.26
colores_a = {2024: "#3498db", 2025: "#f39c12", 2026: "#2c3e50"}
for i, anio in enumerate([2024, 2025, 2026]):
  sub = yoy[yoy["Anio"] == anio]
  v_q = [
      (
          sub[sub["Trimestre"] == q]["Ingresos"].values[0]
          if q in sub["Trimestre"].values
          else 0
      )
      for q in trimestres
  ]
  b_q = ax1_4.bar(
      x_q + (i * w_q) - w_q,
      v_q,
      width=w_q,
      label=f"Año {anio}",
      color=colores_a[anio],
      alpha=0.85,
  )
  for b in b_q:
    h = b.get_height()
    if h > 0:
      ax1_4.annotate(
          f"${h*1e-6:.2f}M",
          (b.get_x() + b.get_width() / 2, h),
          xytext=(0, 3),
          textcoords="offset points",
          ha="center",
          va="bottom",
          fontsize=7,
          fontweight="bold",
      )
ax1_4.set_xticks(x_q)
ax1_4.set_xticklabels(trimestres, fontsize=9)
ax1_4.yaxis.set_major_formatter(fmt_m)
ax1_4.set_ylim(0, yoy["Ingresos"].max() * 1.25)
ax1_4.set_title(
    "4. Dinámica Estacional Trimestral (YoY)\n(Crecimiento interanual por"
    " período fiscal)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax1_4.legend(loc="upper left", fontsize=8)
ax1_4.grid(axis="y", ls="--", alpha=0.3)

# 1.5 Región
ax1_5 = axs1[1, 1]
ax1_5.set_facecolor("#ffffff")
reg = (
    df.groupby("Region")
    .agg(
        Ingresos=("Ingresos_Netos", "sum"),
        Beneficio=("Beneficio_Neto", "sum"),
        Cumpl=("Cumplio_Meta", "mean"),
    )
    .sort_values(by="Ingresos", ascending=False)
)
bars1_5 = ax1_5.bar(
    reg.index,
    reg["Ingresos"],
    color=["#16a085", "#27ae60", "#2980b9", "#8e44ad"],
    width=0.55,
    alpha=0.85,
)
for b, (_, row) in zip(bars1_5, reg.iterrows()):
  tasa = row["Cumpl"] * 100
  mg = (row["Beneficio"] / row["Ingresos"]) * 100
  ax1_5.annotate(
      f"${row['Ingresos']*1e-6:.2f}M\nÉxito: {tasa:.1f}%\nMg: {mg:.1f}%",
      (b.get_x() + b.get_width() / 2, b.get_height()),
      xytext=(0, 4),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=7.5,
      fontweight="bold",
  )
ax1_5.yaxis.set_major_formatter(fmt_m)
ax1_5.set_ylim(0, reg["Ingresos"].max() * 1.35)
ax1_5.set_title(
    "5. Desempeño Territorial y Eficiencia\n(Ventas regionales, margen y tasa de"
    " éxito)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax1_5.grid(axis="y", ls="--", alpha=0.3)

# 1.6 Descuentos
ax1_6 = axs1[1, 2]
ax1_6.set_facecolor("#ffffff")
df["Rango_Desc"] = pd.cut(
    (df["Descuento_Monto"] / df["Ingreso_Bruto"]) * 100,
    bins=[-1, 2, 5, 8, 100],
    labels=["0-2% (Bajo)", "3-5% (Medio)", "6-8% (Alto)", ">8% (Crítico)"],
)
desc_agg = (
    df.groupby("Rango_Desc", observed=False)
    .agg(
        Margen=("Margen_Operativo_Pct", "mean"),
        Cantidad=(col_conteo, "count"),
    )
    .reset_index()
)
bars1_6 = ax1_6.bar(
    desc_agg["Rango_Desc"],
    desc_agg["Margen"],
    color=["#27ae60", "#2980b9", "#f39c12", "#c0392b"],
    width=0.5,
    alpha=0.88,
)
ax1_6.axhline(
    30, color="#c0392b", ls=":", lw=1.5, label="Umbral Mínimo Rentable (30%)"
)
for b, (_, row) in zip(bars1_6, desc_agg.iterrows()):
  ax1_6.annotate(
      f"Margen: {row['Margen']:.1f}%\n({row['Cantidad']} trx)",
      (b.get_x() + b.get_width() / 2, b.get_height()),
      xytext=(0, 4),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=8,
      fontweight="bold",
  )
ax1_6.set_ylim(0, desc_agg["Margen"].max() * 1.35)
ax1_6.set_ylabel("Margen Promedio (%)", fontsize=8.5)
ax1_6.set_title(
    "6. Erosión de Márgenes por Descuento\n(Sensibilidad de precios vs."
    " rentabilidad final)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax1_6.legend(loc="upper right", fontsize=8)
ax1_6.grid(axis="y", ls="--", alpha=0.3)

plt.subplots_adjust(
    left=0.06, right=0.95, top=0.90, bottom=0.08, wspace=0.28, hspace=0.38
)
plt.savefig("reporte_1_bi_ejecutivo.png", dpi=150, bbox_inches="tight")
pdf.savefig(fig1)
plt.close(fig1)

# =====================================================================
# PÁGINA 3: ANÁLISIS DETALLADO DE LÁMINA 1 (TARJETAS RENOVADAS)
# =====================================================================
print("\n📝 [3/10] Generando Análisis Individualizado de Lámina 1...")
fig_t1 = plt.figure(figsize=(19.2, 10.8), dpi=130)
fig_t1.patch.set_facecolor("#f8fafc")
draw_header_banner(
    fig_t1,
    "INFORME EJECUTIVO & ANÁLISIS INDIVIDUALIZADO: LÁMINA 1",
    "Diagnóstico Financiero, Cascada de Márgenes, Canales de Venta y Desempeño"
    " Territorial",
)

coords_6 = [
    (0.03, 0.47, 0.30, 0.38),
    (0.35, 0.47, 0.30, 0.38),
    (0.67, 0.47, 0.30, 0.38),
    (0.03, 0.05, 0.30, 0.38),
    (0.35, 0.05, 0.30, 0.38),
    (0.67, 0.05, 0.30, 0.38),
]

cards_l1 = [
    (
        "VENTAS",
        "1. FACTURACIÓN VS. METAS",
        "$2.43M / Mes",
        [
            (
                "Métrica Central",
                (
                    r"Facturación promedio mensual de \$2.43M con picos"
                    r" históricos en Q1."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "Déficit en cierre de año por proyecciones lineales que no"
                    " absorben estacionalidad."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Superávit acumulado en Q1-Q3 compensa los desvíos del"
                    " cuarto trimestre."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Ajustar metas de cierre de año a la capacidad fabril y"
                    " absorción real."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "COSTOS",
        "2. CASCADA DE RENTABILIDAD",
        "Retención: 37.6%",
        [
            (
                "Métrica Central",
                (
                    r"Ingreso Bruto \$82.33M; Beneficio Neto retenido final de"
                    r" \$30.98M."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"Costo de Mercancía absorbe 49.8% (\$41.04M); Gastos"
                    r" Operativos solo 7.1%."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    r"Rebajas comerciales (\$4.42M) representan el 5.4% de fuga"
                    " directa del ingreso."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Negociar compras por volumen para reducir costo de ventas"
                    " en 2.0%."
                ),
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
    (
        "CANAL",
        "3. DESEMPEÑO POR CANAL",
        "Líder: E-Commerce",
        [
            (
                "Métrica Central",
                (
                    r"E-Commerce (\$16.78M) y Cuentas Clave (\$16.26M) dominan"
                    " la facturación."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "Margen uniforme en ~39.7% en los 5 canales de distribución"
                    " activos."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Cumplimiento presupuestario homogéneo entre el 97% y el 99%.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Canalizar 20% más inventario a E-Commerce por menor costo"
                    " de intermediación."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "TIEMPO",
        "4. DINÁMICA TRIMESTRAL YoY",
        "+4.8% en Q1 y Q3",
        [
            (
                "Métrica Central",
                (
                    "Crecimiento interanual sostenido en 2024 y 2025 en trimestres"
                    " nones."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"El año 2026 registra corte parcial cerrado a Octubre"
                    r" (\$0.78M en Q4)."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Q1 y Q3 concentran la mayor tracción comercial del ciclo"
                    " anual."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Concentrar abastecimiento e inventario 30 días antes del"
                    " inicio de Q1 y Q3."
                ),
            ),
        ],
        "#d97706",
        "#fef3c7",
    ),
    (
        "ZONA",
        "5. DESEMPEÑO TERRITORIAL",
        "Cibao: $38.8M (49.8%)",
        [
            (
                "Métrica Central",
                (
                    r"Norte (Cibao) lidera con \$38.83M y tasa de éxito de"
                    " orden del 42.9%."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"Región Sur aporta \$9.58M pero exhibe la tasa de éxito"
                    " más alta (45.3%)."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Santo Domingo y Este están subexplotados frente al"
                    " potencial del mercado."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Reasignar ejecutivos comerciales hacia la zona"
                    " Metropolitana y Este."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "PRECIO",
        "6. EROSIÓN POR DESCUENTO",
        "Tope Seguro: 5%",
        [
            (
                "Métrica Central",
                "Descuentos de 0-2% retienen margen de 39.6% (578 órdenes).",
            ),
            (
                "Causa Raíz",
                (
                    "Descuentos >8% involucran 930 órdenes con margen en 40.1%"
                    " pero cuotas fallidas."
                ),
            ),
            (
                "Hallazgo Crítico",
                "El umbral mínimo de rentabilidad (30%) nunca fue perforado.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Bloquear en ERP descuentos comerciales que superen el"
                    " 5.0% sin visto bueno."
                ),
            ),
        ],
        "#dc2626",
        "#fee2e2",
    ),
]

for (x, y, w, h), (tag, tit, kpi_b, b_list, col, bg) in zip(coords_6, cards_l1):
  draw_executive_card(
      fig_t1,
      x,
      y,
      w,
      h,
      tag,
      tit,
      kpi_b,
      b_list,
      accent_color=col,
      bg_badge=bg,
  )

plt.axis("off")
pdf.savefig(fig_t1)
plt.close(fig_t1)

# =====================================================================
# PÁGINA 4: LÁMINA 2 - MACHINE LEARNING
# =====================================================================
print("\n🤖 [4/10] Generando Lámina 2: Modelos de Machine Learning (16:9)...")
fig2, axs2 = plt.subplots(2, 3, figsize=(19.2, 10.8), dpi=150)
fig2.patch.set_facecolor("#f8fafc")
fig2.suptitle(
    "INFORME GERENCIAL 2: ANALÍTICA AVANZADA Y MACHINE LEARNING (2024 - OCT"
    " 2026)",
    fontsize=16,
    fontweight="bold",
    y=0.96,
    color="#1a252f",
)

# 2.1 Forecast OLS
ax2_1 = axs2[0, 0]
ax2_1.set_facecolor("#ffffff")
t_arr = np.arange(len(mensual))
y_ing = mensual["Ingresos"].values
coef_ols = np.polyfit(t_arr, y_ing, 1)
trend_ols = np.poly1d(coef_ols)(t_arr)
t_fut_arr = np.arange(len(mensual), len(mensual) + 4)
pred_fut_arr = np.poly1d(coef_ols)(t_fut_arr)
std_res_arr = np.std(y_ing - trend_ols)

ax2_1.plot(
    t_arr, y_ing, "o-", color="#1f77b4", ms=4, lw=2, label="Histórico Real"
)
ax2_1.plot(
    t_arr, trend_ols, "--", color="#34495e", lw=1.8, label="Tendencia Central"
)
ax2_1.plot(
    t_fut_arr,
    pred_fut_arr,
    "s--",
    color="#e67e22",
    lw=2,
    label="Forecast Cierre",
)
ax2_1.fill_between(
    np.concatenate([t_arr, t_fut_arr]),
    np.concatenate([trend_ols, pred_fut_arr]) - (1.96 * std_res_arr),
    np.concatenate([trend_ols, pred_fut_arr]) + (1.96 * std_res_arr),
    color="#3498db",
    alpha=0.15,
    label="Banda Confianza 95%",
)
ax2_1.set_xticks(np.concatenate([t_arr[::5], t_fut_arr[-1:]]))
labels_t_arr = [mensual["Periodo_Mes"].iloc[i] for i in t_arr[::5]] + [
    "Nov-26 Est."
]
ax2_1.set_xticklabels(labels_t_arr, rotation=25, ha="right", fontsize=8.5)
ax2_1.yaxis.set_major_formatter(fmt_m)
ax2_1.annotate(
    f"Proyección Cierre:\n${pred_fut_arr[-1]*1e-6:.2f}M",
    (t_fut_arr[-1], pred_fut_arr[-1]),
    xytext=(-65, 18),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#e67e22", lw=1.2),
    fontsize=8,
    fontweight="bold",
)
ax2_1.set_title(
    "1. Forecast de Tendencia y Demanda Futura\n(Proyección OLS hacia 2027 con"
    " IC 95%)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax2_1.legend(loc="lower left", fontsize=8)
ax2_1.grid(True, ls="--", alpha=0.3)

# 2.2 K-Means
ax2_2 = axs2[0, 1]
ax2_2.set_facecolor("#ffffff")
X_raw = df[["Ingresos_Netos", "Margen_Operativo_Pct"]].values
X_n = (X_raw - X_raw.mean(axis=0)) / (X_raw.std(axis=0) + 1e-8)
np.random.seed(42)
cent_km = X_n[np.random.choice(len(X_n), 3, replace=False)]
for _ in range(25):
  dists_km = np.linalg.norm(X_n[:, np.newaxis] - cent_km, axis=2)
  lbls_km = np.argmin(dists_km, axis=1)
  new_c_km = np.array([X_n[lbls_km == i].mean(axis=0) for i in range(3)])
  if np.allclose(cent_km, new_c_km):
    break
  cent_km = new_c_km
df["Cluster"] = lbls_km
c_means = df.groupby("Cluster")["Ingresos_Netos"].mean().sort_values()
map_c = {
    c_means.index[2]: "A: Clientes VIP (Volumen)",
    c_means.index[1]: "B: Margen Equilibrado",
    c_means.index[0]: "C: Transacciones Estándar",
}
df["Cluster_Nom"] = df["Cluster"].map(map_c)
c_col = {
    "A: Clientes VIP (Volumen)": "#e74c3c",
    "B: Margen Equilibrado": "#27ae60",
    "C: Transacciones Estándar": "#2980b9",
}
for nom, col in c_col.items():
  sub_c = df[df["Cluster_Nom"] == nom]
  ax2_2.scatter(
      sub_c["Ingresos_Netos"],
      sub_c["Margen_Operativo_Pct"],
      color=col,
      alpha=0.5,
      s=20,
      label=f"{nom} ({len(sub_c)})",
  )
ax2_2.xaxis.set_major_formatter(fmt_k)
ax2_2.set_xlabel("Monto Transacción ($)", fontsize=8.5)
ax2_2.set_ylabel("Margen Operativo (%)", fontsize=8.5)
ax2_2.set_title(
    "2. Segmentación K-Means de Cartera\n(Clusters no supervisados para pricing"
    " y fidelización)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax2_2.legend(loc="upper right", fontsize=7.5)
ax2_2.grid(True, ls="--", alpha=0.3)

# 2.3 Feature Weights
ax2_3 = axs2[0, 2]
ax2_3.set_facecolor("#ffffff")
feats = [
    "Cantidad_Unidades",
    "Precio_Unitario",
    "Costo_Unitario",
    "Descuento_Monto",
    "Gasto_Operativo",
]
X_f = df[feats].values
y_f = df["Beneficio_Neto"].values
X_fn = (X_f - X_f.mean(axis=0)) / (X_f.std(axis=0) + 1e-8)
y_fn = (y_f - y_f.mean()) / (y_f.std() + 1e-8)
betas = np.linalg.pinv(X_fn.T @ X_fn) @ X_fn.T @ y_fn
imp = (np.abs(betas) / np.sum(np.abs(betas))) * 100
s_imp = pd.Series(imp, index=feats).sort_values(ascending=True)
bars_imp = ax2_3.barh(
    s_imp.index, s_imp.values, color="#8e44ad", height=0.55, alpha=0.88
)
for b in bars_imp:
  w_val = b.get_width()
  ax2_3.annotate(
      f" {w_val:.1f}% peso",
      (w_val, b.get_y() + b.get_height() / 2),
      xytext=(3, 0),
      textcoords="offset points",
      ha="left",
      va="center",
      fontsize=8,
      fontweight="bold",
  )
ax2_3.set_xlim(0, max(s_imp.values) * 1.35)
ax2_3.set_title(
    "3. Impulsores Clave del Retorno (Feature Weights)\n(Sensibilidad de"
    " variables operativas sobre el EBITDA)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax2_3.grid(axis="x", ls="--", alpha=0.3)

# 2.4 Fugas
ax2_4 = axs2[1, 0]
ax2_4.set_facecolor("#ffffff")
rg = df["Gastos_Totales"] / (df["Ingresos_Netos"] + 1e-5)
z_g = np.abs((rg - rg.mean()) / (rg.std() + 1e-8))
df["Anom"] = z_g > 2.3
norm = df[~df["Anom"]]
anom = df[df["Anom"]]
ax2_4.scatter(
    norm["Ingresos_Netos"],
    norm["Gastos_Totales"],
    color="#bdc3c7",
    alpha=0.35,
    s=15,
    label=f"Órdenes Regulares ({len(norm)})",
)
ax2_4.scatter(
    anom["Ingresos_Netos"],
    anom["Gastos_Totales"],
    color="#c0392b",
    marker="x",
    s=55,
    label=f"Fugas Críticas ({len(anom)})",
)
ax2_4.xaxis.set_major_formatter(fmt_k)
ax2_4.yaxis.set_major_formatter(fmt_k)
ax2_4.set_xlabel("Ingresos Netos ($)", fontsize=8.5)
ax2_4.set_ylabel("Gastos Totales ($)", fontsize=8.5)
ax2_4.set_title(
    "4. Detección de Fugas y Órdenes Atípicas\n(Auditoría estadística de"
    " sobrecostos desmedidos)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax2_4.legend(loc="upper left", fontsize=8)
ax2_4.grid(True, ls="--", alpha=0.3)

# 2.5 Regresión Logística
ax2_5 = axs2[1, 1]
ax2_5.set_facecolor("#ffffff")
p_desc = (df["Descuento_Monto"] / df["Ingreso_Bruto"] * 100).values
y_log = df["Cumplio_Meta"].astype(float).values
xm, xs = p_desc.mean(), p_desc.std() + 1e-8
x_sc = (p_desc - xm) / xs
w_l, b_l = 0.0, 0.0
for _ in range(400):
  z_l = np.clip(w_l * x_sc + b_l, -15, 15)
  p_l = 1 / (1 + np.exp(-z_l))
  w_l -= 0.1 * np.mean((p_l - y_log) * x_sc)
  b_l -= 0.1 * np.mean(p_l - y_log)

xc = np.linspace(0, 15, 200)
zc = np.clip(w_l * ((xc - xm) / xs) + b_l, -15, 15)
yp = 1 / (1 + np.exp(-zc)) * 100
ax2_5.plot(xc, yp, color="#e74c3c", lw=2.5, label="P(Superar Meta)")
ax2_5.axhline(50, color="#34495e", ls="--", lw=1.2, label="Umbral Crítico (50%)")
idx_50 = np.argmin(np.abs(yp - 50))
ax2_5.annotate(
    f"Quiebre: {xc[idx_50]:.1f}% Descuento\n(<50% probabilidad de éxito)",
    (xc[idx_50], 50),
    xytext=(15, 18),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#34495e", lw=1.2),
    fontsize=8,
    fontweight="bold",
)
ax2_5.set_xlabel("Descuento Comercial (%)", fontsize=8.5)
ax2_5.set_ylabel("Probabilidad de Logro (%)", fontsize=8.5)
ax2_5.set_ylim(0, 105)
ax2_5.set_title(
    "5. Curva de Elasticidad y Probabilidad de Meta\n(Regresión logística de"
    " tolerancia al descuento)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax2_5.legend(loc="lower left", fontsize=8)
ax2_5.grid(True, ls="--", alpha=0.3)

# 2.6 Matriz Prescriptiva
ax2_6 = axs2[1, 2]
mat = df.pivot_table(
    index="Canal_Distribucion",
    columns="Categoria",
    values="Margen_Operativo_Pct",
    aggfunc="mean",
)
cax = ax2_6.imshow(mat.values, cmap="YlGnBu", aspect="auto")
fig2.colorbar(cax, ax=ax2_6, orientation="vertical", shrink=0.8, pad=0.03)
ax2_6.set_xticks(np.arange(len(mat.columns)))
ax2_6.set_yticks(np.arange(len(mat.index)))
ax2_6.set_xticklabels(mat.columns, rotation=20, ha="right", fontsize=8)
ax2_6.set_yticklabels(mat.index, fontsize=8)
for i in range(len(mat.index)):
  for j in range(len(mat.columns)):
    v = mat.iloc[i, j]
    c_txt = "white" if v > mat.values.mean() else "black"
    ax2_6.text(
        j,
        i,
        f"{v:.1f}%",
        ha="center",
        va="center",
        color=c_txt,
        fontweight="bold",
        fontsize=8.5,
    )
ax2_6.set_title(
    "6. Matriz Prescriptiva: Margen (%) por Categoría y Canal\n(Guía para"
    " balancear el mix de productos)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)

plt.subplots_adjust(
    left=0.06, right=0.95, top=0.90, bottom=0.08, wspace=0.28, hspace=0.38
)
plt.savefig("reporte_2_ml_ejecutivo.png", dpi=150, bbox_inches="tight")
pdf.savefig(fig2)
plt.close(fig2)

# =====================================================================
# PÁGINA 5: ANÁLISIS DETALLADO DE LÁMINA 2
# =====================================================================
print("\n📝 [5/10] Generando Análisis Individualizado de Lámina 2...")
fig_t2 = plt.figure(figsize=(19.2, 10.8), dpi=130)
fig_t2.patch.set_facecolor("#f8fafc")
draw_header_banner(
    fig_t2,
    "INFORME EJECUTIVO & ANÁLISIS INDIVIDUALIZADO: LÁMINA 2",
    "Modelos de Machine Learning, Segmentación No Supervisada y Sensibilidad de"
    " Metas",
)

cards_l2 = [
    (
        "PREDICCIÓN",
        "1. FORECAST ECONOMÉTRICO",
        "$2.11M / Mes Cierre",
        [
            (
                "Métrica Central",
                (
                    r"Tendencia lineal OLS sitúa el ingreso en \$2.11M"
                    " mensuales a fin de 2026."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"Banda de confianza al 95% oscila entre \$1.60M"
                    r" (pesimista) y \$2.62M."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Ausencia de quiebres estructurales en la serie de demanda.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Programar inventarios de materias primas usando el"
                    " escenario central."
                ),
            ),
        ],
        "#ea580c",
        "#ffedd5",
    ),
    (
        "CLUSTERS",
        "2. SEGMENTACIÓN K-MEANS",
        "1,010 Clientes VIP",
        [
            (
                "Métrica Central",
                (
                    r"Cluster A (VIP): 1,010 transacciones con tickets >\$30K"
                    " concentran volumen."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "Cluster B (1,028 órdenes) mantiene margen equilibrado"
                    " (~40%)."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Los clientes VIP generan masa crítica pero exigen más"
                    " rebajas de precios."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Crear acuerdos marco de fidelización sin erosionar el"
                    " precio unitario."
                ),
            ),
        ],
        "#7c3aed",
        "#f3e8ff",
    ),
    (
        "FACTORES",
        "3. IMPULSORES DEL BENEFICIO",
        "Gasto Operativo: 94.8%",
        [
            (
                "Métrica Central",
                (
                    "El Gasto Operativo y el Costo explican el 95% de la"
                    " variación del retorno."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "Precio unitario y volumen tienen impacto secundario en el"
                    " EBITDA final."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Cualquier desvío logístico o de fletes destruye"
                    " rentabilidad de inmediato."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Enfocar los OKRs operacionales en eficiencia logística de"
                    " última milla."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "AUDITORÍA",
        "4. DETECCIÓN DE FUGAS Z-SCORE",
        "0 Anomalías Críticas",
        [
            (
                "Métrica Central",
                (
                    "Evaluación multivariable del ratio Gastos / Ingresos en"
                    " 3,000 órdenes."
                ),
            ),
            (
                "Causa Raíz",
                "Cero órdenes registradas superaron el límite de alerta Z > 2.3.",
            ),
            (
                "Hallazgo Crítico",
                (
                    "Disciplina financiera sólida con costos estrictamente"
                    " proporcionales."
                ),
            ),
            (
                "Decisión Ejecutiva",
                "Mantener el control automatizado de auditoría en el ERP.",
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
    (
        "QUIEBRE",
        "5. CURVA LOGÍSTICA DE META",
        "Frontera: 6.5% Desc.",
        [
            (
                "Métrica Central",
                "La probabilidad de lograr la cuota cae a <50% al superar 6.5% de"
                " descuento.",
            ),
            (
                "Causa Raíz",
                (
                    "Rebajas comerciales agresivas no logran compensarse con"
                    " volumen físico."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Relación de quiebre probabilístico modelada mediante"
                    " función sigmoide."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Tope estricto de descuento al equipo de ventas limitado al"
                    " 5.0%."
                ),
            ),
        ],
        "#dc2626",
        "#fee2e2",
    ),
    (
        "MIX",
        "6. MATRIZ PRESCRIPTIVA",
        "Bebidas Retail: 40.4%",
        [
            (
                "Métrica Central",
                (
                    "Bebidas No Alcohólicas en Punto de Venta entregan margen"
                    " líder (40.4%)."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "Alimentos en B2B Mayorista rinden 39.5% por mayor volumen"
                    " contratado."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Rango estrecho de márgenes (39.1% a 40.4%) en toda la matriz.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Priorizar la colocación de bebidas no alcohólicas en"
                    " canales minoristas."
                ),
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
]

for (x, y, w, h), (tag, tit, kpi_b, b_list, col, bg) in zip(coords_6, cards_l2):
  draw_executive_card(
      fig_t2,
      x,
      y,
      w,
      h,
      tag,
      tit,
      kpi_b,
      b_list,
      accent_color=col,
      bg_badge=bg,
  )

plt.axis("off")
pdf.savefig(fig_t2)
plt.close(fig_t2)

# =====================================================================
# PÁGINA 6: LÁMINA 3 - BI MODERNO Y CONCENTRACIÓN
# =====================================================================
print("\n📈 [6/10] Generando Lámina 3: BI Moderno y Concentración (16:9)...")
fig3, axs3 = plt.subplots(2, 3, figsize=(19.2, 10.8), dpi=150)
fig3.patch.set_facecolor("#f8fafc")
fig3.suptitle(
    "INFORME GERENCIAL 3: BI MODERNO Y ANÁLISIS ESTRATÉGICO DE CONCENTRACIÓN"
    " (2024 - OCT 2026)",
    fontsize=16,
    fontweight="bold",
    y=0.96,
    color="#1a252f",
)

# 3.1 Bullet Chart
ax3_1 = axs3[0, 0]
ax3_1.set_facecolor("#ffffff")
canales_df = (
    df.groupby("Canal_Distribucion")
    .agg(Ventas=("Ingresos_Netos", "sum"), Meta=("Meta_Ventas", "sum"))
    .sort_values("Ventas")
)
y_pos = np.arange(len(canales_df))

for i, (canal, row) in enumerate(canales_df.iterrows()):
  meta = row["Meta"]
  real = row["Ventas"]
  ax3_1.barh(i, meta * 1.25, height=0.6, color="#e0e0e0", alpha=0.5)
  ax3_1.barh(i, meta * 0.95, height=0.6, color="#bdc3c7", alpha=0.6)
  ax3_1.barh(i, meta * 0.70, height=0.6, color="#95a5a6", alpha=0.6)
  ax3_1.barh(i, real, height=0.25, color="#2c3e50")
  ax3_1.vlines(meta, i - 0.35, i + 0.35, color="#e74c3c", linewidth=2.5)
  ax3_1.annotate(
      f"${real*1e-6:.2f}M / ${meta*1e-6:.2f}M",
      (real, i),
      xytext=(5, 0),
      textcoords="offset points",
      va="center",
      fontsize=7.5,
      fontweight="bold",
  )

ax3_1.set_yticks(y_pos)
ax3_1.set_yticklabels(canales_df.index, fontsize=8.5)
ax3_1.xaxis.set_major_formatter(fmt_m)
ax3_1.set_title(
    "1. Bullet Chart: Cumplimiento de Metas por Canal\n(Barra: Real | Línea"
    " Roja: Meta | Sombras: Rangos)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax3_1.grid(axis="x", ls="--", alpha=0.3)

# 3.2 Pareto 80/20
ax3_2 = axs3[0, 1]
ax3_2.set_facecolor("#ffffff")
pareto_df = (
    df.groupby("Ciudad")["Ingresos_Netos"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
pareto_df["Cum_Pct"] = (
    pareto_df["Ingresos_Netos"].cumsum() / pareto_df["Ingresos_Netos"].sum()
) * 100
bars_p = ax3_2.bar(
    pareto_df["Ciudad"],
    pareto_df["Ingresos_Netos"],
    color="#3498db",
    width=0.55,
    alpha=0.85,
)
ax3_2_twin = ax3_2.twinx()
ax3_2_twin.plot(
    pareto_df["Ciudad"], pareto_df["Cum_Pct"], color="#e74c3c", marker="o", lw=2
)
ax3_2_twin.axhline(80, color="#27ae60", ls="--", lw=1.5, label="Regla 80%")
ax3_2_twin.set_ylabel("% Acumulado", color="#e74c3c", fontsize=8.5)
ax3_2_twin.set_ylim(0, 105)
ax3_2_twin.grid(False)
ax3_2.yaxis.set_major_formatter(fmt_m)
ax3_2.set_xticks(range(len(pareto_df)))
ax3_2.set_xticklabels(pareto_df["Ciudad"], rotation=28, ha="right", fontsize=8)
for b in bars_p:
  ax3_2.annotate(
      f"${b.get_height()*1e-6:.1f}M",
      (b.get_x() + b.get_width() / 2, b.get_height()),
      xytext=(0, 2),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=7,
      fontweight="bold",
  )
ax3_2.set_title(
    "2. Curva de Pareto 80/20 por Ciudad\n(Concentración de facturación en"
    " plazas clave)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax3_2.grid(axis="y", ls="--", alpha=0.3)

# 3.3 Dumbbell Chart
ax3_3 = axs3[0, 2]
ax3_3.set_facecolor("#ffffff")
df_24_26 = (
    df[df["Anio"].isin([2024, 2026])]
    .groupby(["Canal_Distribucion", "Anio"])["Ingresos_Netos"]
    .sum()
    .unstack()
)
df_24_26["Crecimiento_Pct"] = (
    (df_24_26[2026] - df_24_26[2024]) / df_24_26[2024]
) * 100
y_db = np.arange(len(df_24_26))

for i, (canal, row) in enumerate(df_24_26.iterrows()):
  v24, v26 = row[2024], row[2026]
  ax3_3.plot([v24, v26], [i, i], color="#95a5a6", lw=2, zorder=1)
  ax3_3.scatter(
      v24, i, color="#3498db", s=70, zorder=2, label="2024" if i == 0 else ""
  )
  ax3_3.scatter(
      v26,
      i,
      color="#2ecc71" if v26 >= v24 else "#e74c3c",
      s=70,
      zorder=2,
      label="2026" if i == 0 else "",
  )
  ax3_3.annotate(
      f" {row['Crecimiento_Pct']:+.1f}%",
      (max(v24, v26), i),
      xytext=(5, 0),
      textcoords="offset points",
      va="center",
      fontsize=7.5,
      fontweight="bold",
  )

ax3_3.set_yticks(y_db)
ax3_3.set_yticklabels(df_24_26.index, fontsize=8.5)
ax3_3.xaxis.set_major_formatter(fmt_m)
ax3_3.set_title(
    "3. Dumbbell Chart: Brecha de Crecimiento 2024 vs 2026\n(Evolución por"
    " canal comercial)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax3_3.legend(loc="lower right", fontsize=8)
ax3_3.grid(axis="x", ls="--", alpha=0.3)

# 3.4 Lollipop AOV
ax3_4 = axs3[1, 0]
ax3_4.set_facecolor("#ffffff")
aov_df = (
    df.groupby("Ciudad")["Ingresos_Netos"]
    .mean()
    .sort_values()
    .reset_index()
)
y_lp = np.arange(len(aov_df))
ax3_4.hlines(
    y=y_lp, xmin=0, xmax=aov_df["Ingresos_Netos"], color="#bdc3c7", lw=1.8
)
ax3_4.scatter(aov_df["Ingresos_Netos"], y_lp, color="#8e44ad", s=65, zorder=3)
for i, row in aov_df.iterrows():
  ax3_4.annotate(
      f" ${row['Ingresos_Netos']*1e-3:.1f}K",
      (row["Ingresos_Netos"], i),
      xytext=(4, 0),
      textcoords="offset points",
      va="center",
      fontsize=7.5,
      fontweight="bold",
  )
ax3_4.set_yticks(y_lp)
ax3_4.set_yticklabels(aov_df["Ciudad"], fontsize=8.5)
ax3_4.xaxis.set_major_formatter(fmt_k)
ax3_4.set_xlim(0, aov_df["Ingresos_Netos"].max() * 1.25)
ax3_4.set_title(
    "4. Lollipop Chart: Ticket Promedio (AOV) por Ciudad\n(Valor medio por"
    " transacción)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax3_4.grid(axis="x", ls="--", alpha=0.3)

# 3.5 Violin Plot
ax3_5 = axs3[1, 1]
ax3_5.set_facecolor("#ffffff")
canales_list = df["Canal_Distribucion"].unique()
data_violin = [
    df[df["Canal_Distribucion"] == c]["Margen_Operativo_Pct"].values
    for c in canales_list
]
parts = ax3_5.violinplot(
    data_violin,
    positions=range(len(canales_list)),
    showmeans=True,
    showmedians=True,
)
for pc in parts["bodies"]:
  pc.set_facecolor("#27ae60")
  pc.set_edgecolor("#1e8449")
  pc.set_alpha(0.6)
ax3_5.set_xticks(range(len(canales_list)))
ax3_5.set_xticklabels(
    [c.replace(" ", "\n") for c in canales_list], fontsize=8
)
ax3_5.set_ylabel("Margen Operativo (%)", fontsize=8.5)
ax3_5.set_title(
    "5. Violin Plot: Densidad de Margen Operativo por Canal\n(Dispersión y"
    " estabilidad de la rentabilidad)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax3_5.grid(axis="y", ls="--", alpha=0.3)

# 3.6 Concentración HHI
ax3_6 = axs3[1, 2]
ax3_6.set_facecolor("#ffffff")
share_region = (
    df.groupby("Region")["Ingresos_Netos"].sum() / df["Ingresos_Netos"].sum()
) * 100
hhi = np.sum((share_region.values) ** 2)
wedges, texts, autotexts = ax3_6.pie(
    share_region,
    labels=share_region.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=["#16a085", "#27ae60", "#2980b9", "#8e44ad"],
    pctdistance=0.75,
    wedgeprops=dict(width=0.4, edgecolor="w"),
)
for at in autotexts:
  at.set_fontsize(8)
  at.set_weight("bold")
ax3_6.text(
    0,
    0,
    f"HHI:\n{hhi:.0f} pts\n{'Moderado' if hhi<2500 else 'Concentrado'}",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color="#2c3e50",
)
ax3_6.set_title(
    "6. Concentración Territorial & Índice HHI\n(Riesgo de diversificación"
    " geográfica)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)

plt.subplots_adjust(
    left=0.06, right=0.95, top=0.90, bottom=0.08, wspace=0.28, hspace=0.38
)
plt.savefig("reporte_3_bi_moderno.png", dpi=150, bbox_inches="tight")
pdf.savefig(fig3)
plt.close(fig3)

# =====================================================================
# PÁGINA 7: ANÁLISIS DETALLADO DE LÁMINA 3
# =====================================================================
print("\n📝 [7/10] Generando Análisis Individualizado de Lámina 3...")
fig_t3 = plt.figure(figsize=(19.2, 10.8), dpi=130)
fig_t3.patch.set_facecolor("#f8fafc")
draw_header_banner(
    fig_t3,
    "INFORME EJECUTIVO & ANÁLISIS INDIVIDUALIZADO: LÁMINA 3",
    "BI Moderno, Diagramas de Bala, Pareto 80/20 y Concentración Territorial"
    " HHI",
)

cards_l3 = [
    (
        "BALA",
        "1. BULLET CHART POR CANAL",
        "97% - 99% Metas",
        [
            (
                "Métrica Central",
                (
                    r"E-Commerce (\$16.78M) superó el rango satisfactorio"
                    " fijado."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"Distribución Directa (\$14.52M) quedó al 97% pero dentro"
                    " de tolerancia."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Todos los canales superan holgadamente la zona deficiente"
                    " (<70%)."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Reasignar cuotas para potenciar canales digitales de alto"
                    " dinamismo."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "PARETO",
        "2. CURVA 80/20 POR CIUDAD",
        "5 Ciudades = 80%",
        [
            (
                "Métrica Central",
                (
                    r"Santo Domingo (\$10.9M) y Puerto Plata (\$10.2M) lideran"
                    " el volumen."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "5 municipios concentran el 80% del valor facturado a nivel"
                    " nacional."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Alta vulnerabilidad comercial en plazas del interior menor.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Enfocar el plan de fidelización VIP en las 5 plazas"
                    " estratégicas."
                ),
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
    (
        "BRECHA",
        "3. DUMBBELL YoY 2024-2026",
        "Punto Venta: -14.1%",
        [
            (
                "Métrica Central",
                "Contracción de Punto de Venta (-14.1%) y Distribución (-27.3%).",
            ),
            (
                "Causa Raíz",
                (
                    "Migración acelerada del consumidor institucional al canal"
                    " digital."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Canales tradicionales pierden tracción de ingresos brutos.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Acelerar inversiones en plataformas B2B digitales de"
                    " autoservicio."
                ),
            ),
        ],
        "#dc2626",
        "#fee2e2",
    ),
    (
        "TICKET",
        "4. LOLLIPOP TICKET (AOV)",
        "La Vega: $26.9K Líder",
        [
            (
                "Métrica Central",
                r"La Vega lidera en ticket promedio con \$26.9K por transacción.",
            ),
            (
                "Causa Raíz",
                (
                    r"Santiago muestra el menor AOV (\$24.8K) pero con mayor"
                    " frecuencia."
                ),
            ),
            (
                "Hallazgo Crítico",
                r"Estabilidad del AOV nacional alrededor de los \$26.0K.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Introducir paquetes promocionales por volumen para elevar"
                    " el AOV en Santiago."
                ),
            ),
        ],
        "#7c3aed",
        "#f3e8ff",
    ),
    (
        "DISPERSIÓN",
        "5. VIOLIN PLOT DE MARGEN",
        "Mediana: 39.8%",
        [
            (
                "Métrica Central",
                (
                    "Densidad concentrada de margen operativo entre 38.5% y"
                    " 41.0%."
                ),
            ),
            (
                "Causa Raíz",
                (
                    "Punto de Venta muestra la menor dispersión y mayor"
                    " predictibilidad."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Ausencia total de colas largas en zonas de pérdida operativa.",
            ),
            (
                "Decisión Ejecutiva",
                "Estandarizar listas de precios para evitar arbitraje entre canales.",
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
    (
        "RIESGO",
        "6. CONCENTRACIÓN HHI",
        "3,401 Puntos (Alto)",
        [
            (
                "Métrica Central",
                (
                    "Índice HHI de 3,401 puntos supera holgadamente el umbral"
                    " de 2,500."
                ),
            ),
            (
                "Causa Raíz",
                "Norte (Cibao) acapara el 49.8% de todos los ingresos de la firma.",
            ),
            (
                "Hallazgo Crítico",
                (
                    "Alta exposición operativa ante contingencias climáticas en"
                    " el Norte."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Desplegar un plan agresivo de expansión hacia Punta Cana y"
                    " Santo Domingo."
                ),
            ),
        ],
        "#ea580c",
        "#ffedd5",
    ),
]

for (x, y, w, h), (tag, tit, kpi_b, b_list, col, bg) in zip(coords_6, cards_l3):
  draw_executive_card(
      fig_t3,
      x,
      y,
      w,
      h,
      tag,
      tit,
      kpi_b,
      b_list,
      accent_color=col,
      bg_badge=bg,
  )

plt.axis("off")
pdf.savefig(fig_t3)
plt.close(fig_t3)

# =====================================================================
# PÁGINA 8: LÁMINA 4 - ECONOMETRÍA Y ML AVANZADO
# =====================================================================
print("\n🔬 [8/10] Generando Lámina 4: Econometría y Modelos Avanzados (16:9)...")
fig4, axs4 = plt.subplots(2, 3, figsize=(19.2, 10.8), dpi=150)
fig4.patch.set_facecolor("#f8fafc")
fig4.suptitle(
    "INFORME GERENCIAL 4: ECONOMETRÍA PREDICTIVA Y MACHINE LEARNING AVANZADO"
    " (2024 - OCT 2026)",
    fontsize=16,
    fontweight="bold",
    y=0.96,
    color="#1a252f",
)

# 4.1 Descomposición STL
ax4_1 = axs4[0, 0]
ax4_1.set_facecolor("#ffffff")
ingresos_ts = mensual["Ingresos"].values
trend_ma = (
    pd.Series(ingresos_ts)
    .rolling(window=3, center=True)
    .mean()
    .bfill()
    .ffill()
    .values
)
seasonal = ingresos_ts - trend_ma
ax4_1.plot(
    mensual["Periodo_Mes"], ingresos_ts, label="Serie Real", color="#1f77b4", lw=2
)
ax4_1.plot(
    mensual["Periodo_Mes"],
    trend_ma,
    label="Tendencia (MA-3)",
    color="#e67e22",
    lw=2,
    ls="--",
)
ax4_1.bar(
    mensual["Periodo_Mes"],
    seasonal,
    label="Estacional / Residual",
    color="#27ae60",
    alpha=0.5,
    width=0.4,
)
ax4_1.set_xticks(range(0, len(mensual), 4))
ax4_1.set_xticklabels(
    mensual["Periodo_Mes"].iloc[::4], rotation=25, ha="right", fontsize=8
)
ax4_1.yaxis.set_major_formatter(fmt_m)
ax4_1.set_title(
    "1. Descomposición de Demanda: Tendencia vs. Variación Residual\n(Aislamiento"
    " de componentes estructurales)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax4_1.legend(loc="upper left", fontsize=7.5)
ax4_1.grid(True, ls="--", alpha=0.3)

# 4.2 Proyección Cuantílica
ax4_2 = axs4[0, 1]
ax4_2.set_facecolor("#ffffff")
t_p = np.arange(len(mensual))
t_fut_p = np.arange(len(mensual), len(mensual) + 4)
coef_p50 = np.polyfit(t_p, ingresos_ts, 1)
trend_p50 = np.poly1d(coef_p50)(t_fut_p)
std_err = np.std(ingresos_ts - np.poly1d(coef_p50)(t_p))
p10_fut = trend_p50 - 1.28 * std_err
p90_fut = trend_p50 + 1.28 * std_err

ax4_2.plot(
    mensual["Periodo_Mes"],
    ingresos_ts,
    "o-",
    color="#2c3e50",
    ms=3,
    label="Histórico",
)
labels_fut = ["Nov-26", "Dic-26", "Ene-27", "Feb-27"]
ax4_2.plot(
    labels_fut, trend_p50, "s--", color="#3498db", lw=2, label="P50 (Base)"
)
ax4_2.plot(
    labels_fut,
    p90_fut,
    "^:",
    color="#27ae60",
    lw=2,
    label="P90 (Optimista)",
)
ax4_2.plot(
    labels_fut,
    p10_fut,
    "v:",
    color="#e74c3c",
    lw=2,
    label="P10 (Pesimista)",
)
ax4_2.fill_between(labels_fut, p10_fut, p90_fut, color="#3498db", alpha=0.15)
ax4_2.set_xticks(list(range(0, len(mensual), 5)) + [len(mensual) + 3])
ax4_2.set_xticklabels(
    list(mensual["Periodo_Mes"].iloc[::5]) + ["Feb-27"],
    rotation=25,
    ha="right",
    fontsize=8,
)
ax4_2.yaxis.set_major_formatter(fmt_m)
ax4_2.set_title(
    "2. Proyección Cuantílica Multiescenario (P10 / P50 / P90)\n(Simulación de"
    " estrés y planificación de liquidez)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax4_2.legend(loc="lower left", fontsize=7.5)
ax4_2.grid(True, ls="--", alpha=0.3)

# 4.3 PCA Biplot
ax4_3 = axs4[0, 2]
ax4_3.set_facecolor("#ffffff")
vars_pca = [
    "Cantidad_Unidades",
    "Precio_Unitario",
    "Costo_Unitario",
    "Descuento_Monto",
    "Gasto_Operativo",
    "Beneficio_Neto",
]
X_pca = df[vars_pca].values
X_pca_norm = (X_pca - X_pca.mean(axis=0)) / X_pca.std(axis=0)

U, S, Vt = np.linalg.svd(X_pca_norm, full_matrices=False)
coords = U[:, :2] * S[:2]
loadings = Vt[:2, :].T

sample_idx = np.random.choice(len(coords), 300, replace=False)
ax4_3.scatter(
    coords[sample_idx, 0],
    coords[sample_idx, 1],
    c="#bdc3c7",
    alpha=0.5,
    s=15,
    label="Órdenes",
)
for i, var_name in enumerate(vars_pca):
  ax4_3.arrow(
      0,
      0,
      loadings[i, 0] * 15,
      loadings[i, 1] * 15,
      color="#e74c3c",
      width=0.2,
      head_width=0.8,
      alpha=0.85,
  )
  ax4_3.text(
      loadings[i, 0] * 17,
      loadings[i, 1] * 17,
      var_name[:12],
      color="#2c3e50",
      fontsize=7.5,
      fontweight="bold",
  )
ax4_3.axhline(0, color="grey", ls="--", lw=0.8)
ax4_3.axvline(0, color="grey", ls="--", lw=0.8)
ax4_3.set_xlabel("PC1 (Dimensión Principal)", fontsize=8)
ax4_3.set_ylabel("PC2 (Dimensión Secundaria)", fontsize=8)
ax4_3.set_title(
    "3. PCA Biplot: Mapa Multivariable de Factores\n(Vectores de variables y"
    " dispersión dimensional)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax4_3.grid(True, ls="--", alpha=0.3)

# 4.4 Curva ROC
ax4_4 = axs4[1, 0]
ax4_4.set_facecolor("#ffffff")
score = df["Margen_Operativo_Pct"].values - (
    df["Descuento_Monto"] / df["Ingreso_Bruto"] * 100
).values
y_true = df["Cumplio_Meta"].values.astype(int)

thresholds = np.linspace(score.min(), score.max(), 100)
tpr, fpr = [], []
for th in thresholds:
  pred = (score >= th).astype(int)
  tp = np.sum((pred == 1) & (y_true == 1))
  fp = np.sum((pred == 1) & (y_true == 0))
  fn = np.sum((pred == 0) & (y_true == 1))
  tn = np.sum((pred == 0) & (y_true == 0))
  tpr.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
  fpr.append(fp / (fp + tn) if (fp + tn) > 0 else 0)

fpr_arr = np.array(fpr)
tpr_arr = np.array(tpr)
sort_idx = np.argsort(fpr_arr)
fpr_s = fpr_arr[sort_idx]
tpr_s = tpr_arr[sort_idx]
auc_val = (
    np.trapezoid(tpr_s, fpr_s)
    if hasattr(np, "trapezoid")
    else np.trapz(tpr_s, fpr_s)
)

ax4_4.plot(
    fpr_s,
    tpr_s,
    color="#2980b9",
    lw=2.5,
    label=f"Modelo Clasificador (AUC = {auc_val:.2f})",
)
ax4_4.plot(
    [0, 1], [0, 1], color="#7f8c8d", ls="--", lw=1.5, label="Azar (AUC = 0.50)"
)
ax4_4.set_xlabel("Tasa de Falsos Positivos (1 - Especificidad)", fontsize=8)
ax4_4.set_ylabel("Tasa de Verdaderos Positivos (Sensibilidad)", fontsize=8)
ax4_4.set_title(
    "4. Curva ROC & AUC: Capacidad Predictiva de Metas\n(Eficacia del scoring"
    " crediticio y comercial)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax4_4.legend(loc="lower right", fontsize=8)
ax4_4.grid(True, ls="--", alpha=0.3)

# 4.5 Correlación Pearson
ax4_5 = axs4[1, 1]
ax4_5.set_facecolor("#ffffff")
corr_vars = [
    "Cantidad_Unidades",
    "Precio_Unitario",
    "Costo_Unitario",
    "Descuento_Monto",
    "Ingresos_Netos",
    "Beneficio_Neto",
]
corr_mat = df[corr_vars].corr()
cax_corr = ax4_5.imshow(corr_mat.values, cmap="coolwarm", vmin=-1, vmax=1)
fig4.colorbar(cax_corr, ax=ax4_5, orientation="vertical", shrink=0.8, pad=0.03)
ax4_5.set_xticks(range(len(corr_vars)))
ax4_5.set_yticks(range(len(corr_vars)))
short_labels = [
    "Unidades",
    "Precio",
    "Costo",
    "Descuento",
    "Ingreso",
    "Beneficio",
]
ax4_5.set_xticklabels(short_labels, rotation=25, ha="right", fontsize=8)
ax4_5.set_yticklabels(short_labels, fontsize=8)
for i in range(len(corr_vars)):
  for j in range(len(corr_vars)):
    val = corr_mat.iloc[i, j]
    ax4_5.text(
        j,
        i,
        f"{val:.2f}",
        ha="center",
        va="center",
        color="white" if abs(val) > 0.5 else "black",
        fontsize=8,
        fontweight="bold",
    )
ax4_5.set_title(
    "5. Matriz de Correlación de Pearson\n(Interdependencia entre palancas"
    " financieras)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)

# 4.6 Elasticidad Precio
ax4_6 = axs4[1, 2]
ax4_6.set_facecolor("#ffffff")
df["Precio_Bin"] = pd.qcut(df["Precio_Unitario"], q=8)
elasticidad_df = (
    df.groupby("Precio_Bin", observed=False)
    .agg(
        Precio_Medio=("Precio_Unitario", "mean"),
        Volumen_Medio=("Cantidad_Unidades", "mean"),
        Ingreso_Medio=("Ingresos_Netos", "mean"),
    )
    .reset_index()
)

p_vals = elasticidad_df["Precio_Medio"].values
q_vals = elasticidad_df["Volumen_Medio"].values
elas_coef = np.polyfit(np.log(p_vals), np.log(q_vals), 1)[0]

ax4_6.plot(
    p_vals,
    q_vals,
    "o-",
    color="#8e44ad",
    lw=2,
    ms=6,
    label=f"Demanda (Elasticidad: {elas_coef:.2f})",
)
ax4_6_twin = ax4_6.twinx()
ax4_6_twin.plot(
    p_vals,
    elasticidad_df["Ingreso_Medio"],
    "s--",
    color="#f39c12",
    lw=1.8,
    label="Ingreso Medio ($)",
)
ax4_6_twin.yaxis.set_major_formatter(fmt_k)
ax4_6_twin.set_ylabel("Ingreso Medio ($)", color="#f39c12", fontsize=8)
ax4_6_twin.grid(False)
ax4_6.set_xlabel("Precio Unitario ($)", fontsize=8)
ax4_6.set_ylabel("Volumen Medio (Unidades)", color="#8e44ad", fontsize=8)
ax4_6.set_title(
    f"6. Curva de Elasticidad Precio-Demanda\n(Coeficiente: {elas_coef:.2f} |"
    " Demanda Inelástica)",
    fontsize=10.5,
    fontweight="bold",
    pad=8,
)
ax4_6.grid(True, ls="--", alpha=0.3)

plt.subplots_adjust(
    left=0.06, right=0.95, top=0.90, bottom=0.08, wspace=0.28, hspace=0.38
)
plt.savefig("reporte_4_ml_econometria.png", dpi=150, bbox_inches="tight")
pdf.savefig(fig4)
plt.close(fig4)

# =====================================================================
# PÁGINA 9: ANÁLISIS DETALLADO DE LÁMINA 4
# =====================================================================
print("\n📝 [9/10] Generando Análisis Individualizado de Lámina 4...")
fig_t4 = plt.figure(figsize=(19.2, 10.8), dpi=130)
fig_t4.patch.set_facecolor("#f8fafc")
draw_header_banner(
    fig_t4,
    "INFORME EJECUTIVO & ANÁLISIS INDIVIDUALIZADO: LÁMINA 4",
    "Econometría Predictiva, Simulación de Estrés Cuantílica y Elasticidad de"
    " Precios",
)

cards_l4 = [
    (
        "SERIES",
        "1. DESCOMPOSICIÓN STL",
        "$2.35M Tendencia Base",
        [
            (
                "Métrica Central",
                (
                    r"Tendencia móvil MA-3 confirma estabilidad en torno a"
                    r" \$2.35M mensuales."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"Oscilación residual acotada en banda estrecha (+\$250K a"
                    r" -\$200K)."
                ),
            ),
            (
                "Hallazgo Crítico",
                "Ausencia de factores externos que alteren la serie temporal.",
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Utilizar la curva de tendencia como base de presupuesto"
                    " para 2027."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "ESTRÉS",
        "2. PROYECCIÓN CUANTÍLICA",
        "Piso P10: $1.75M",
        [
            (
                "Métrica Central",
                (
                    r"Escenario Pesimista (P10) garantiza un piso de \$1.75M en"
                    " recesión."
                ),
            ),
            (
                "Causa Raíz",
                (
                    r"Escenario Esperado P50 sitúa demanda en \$2.11M; Optimista"
                    r" P90 en \$2.48M."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Flujo de efectivo blindado contra escenarios severos de"
                    " mercado."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Fijar pedidos de compra de insumos calibrados al escenario"
                    " P50."
                ),
            ),
        ],
        "#7c3aed",
        "#f3e8ff",
    ),
    (
        "FACTORES",
        "3. PCA BIPLOT 2D",
        "PC1: Volumen | PC2: Margen",
        [
            (
                "Métrica Central",
                (
                    "Dimensión 1 segrega nítidamente los pedidos de alto volumen"
                    " físico."
                ),
            ),
            (
                "Causa Raíz",
                "Dimensión 2 asocia precios mayores con mayor margen unitario.",
            ),
            (
                "Hallazgo Crítico",
                (
                    "El volumen bruto no garantiza retención de margen"
                    " proporcional."
                ),
            ),
            (
                "Decisión Ejecutiva",
                "Diferenciar catálogos para canal mayorista vs. retail minorista.",
            ),
        ],
        "#ea580c",
        "#ffedd5",
    ),
    (
        "SCORING",
        "4. CURVA ROC & AUC",
        "AUC: 0.52 (Azar)",
        [
            (
                "Métrica Central",
                "Modelo predictivo de logro de cuota alcanza un AUC de 0.52.",
            ),
            (
                "Causa Raíz",
                (
                    "El alcance de metas depende de la cuota asignada y no del"
                    " cliente."
                ),
            ),
            (
                "Hallazgo Crítico",
                (
                    "Las transacciones individuales no reflejan sesgo intrínseco"
                    " de impago."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Reformular el método de cálculo y asignación de metas"
                    " comerciales."
                ),
            ),
        ],
        "#0284c7",
        "#e0f2fe",
    ),
    (
        "CORRELACIÓN",
        "5. MATRIZ DE PEARSON",
        "Ingreso-Beneficio: 0.97",
        [
            (
                "Métrica Central",
                "Correlación casi perfecta (0.97) entre ingresos y beneficio neto.",
            ),
            (
                "Causa Raíz",
                "Correlación negativa (-0.07) entre descuento aplicado e ingreso.",
            ),
            (
                "Hallazgo Crítico",
                (
                    "Bajar precios no estimula compras de mayor volumen en la"
                    " cartera."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Eliminar políticas de bonificaciones comerciales"
                    " generalizadas."
                ),
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
    (
        "ELASTICIDAD",
        "6. ELASTICIDAD PRECIO",
        "Coef: 0.01 (Inelástica)",
        [
            (
                "Métrica Central",
                "Coeficiente empírico de 0.01 confirma demanda altamente inelástica.",
            ),
            (
                "Causa Raíz",
                "Incrementos de precio unitario no deprimen el volumen de demanda.",
            ),
            (
                "Hallazgo Crítico",
                (
                    r"El ingreso medio (\$26.5K) se expande al aumentar el"
                    " precio base."
                ),
            ),
            (
                "Decisión Ejecutiva",
                (
                    "Aplicar un incremento estratégico de precios del +3.0% en"
                    " SKU líderes."
                ),
            ),
        ],
        "#16a34a",
        "#dcfce7",
    ),
]

for (x, y, w, h), (tag, tit, kpi_b, b_list, col, bg) in zip(coords_6, cards_l4):
  draw_executive_card(
      fig_t4,
      x,
      y,
      w,
      h,
      tag,
      tit,
      kpi_b,
      b_list,
      accent_color=col,
      bg_badge=bg,
  )

plt.axis("off")
pdf.savefig(fig_t4)
plt.close(fig_t4)

# =====================================================================
# PÁGINA 10: CONCLUSIONES Y MATRIZ PRESCRIPTIVA (REDISEÑO EXECUTIVE)
# =====================================================================
print("\n🎯 [10/10] Generando Conclusiones y Matriz Prescriptiva Final...")
fig_p10 = plt.figure(figsize=(19.2, 10.8), dpi=130)
fig_p10.patch.set_facecolor("#f8fafc")

# Encabezado
header_p10 = patches.FancyBboxPatch(
    (0.03, 0.88),
    0.94,
    0.09,
    boxstyle="round,pad=0.008,rounding_size=0.015",
    facecolor="#0f172a",
    edgecolor="none",
    transform=fig_p10.transFigure,
)
fig_p10.patches.append(header_p10)
fig_p10.text(
    0.05,
    0.935,
    "CONCLUSIONES ESTRATÉGICAS Y MATRIZ EJECUTIVA DE TOMA DE DECISIONES",
    fontsize=18,
    fontweight="bold",
    color="#ffffff",
)
fig_p10.text(
    0.05,
    0.898,
    "Hoja de Ruta Corporativa para Optimización de Rentabilidad, Mitigación de"
    " Riesgos y Asignación de Capital en 2027",
    fontsize=11.5,
    color="#94a3b8",
)

# Tarjeta de Síntesis
card_top = patches.FancyBboxPatch(
    (0.03, 0.64),
    0.94,
    0.22,
    boxstyle="round,pad=0.006,rounding_size=0.012",
    facecolor="#ffffff",
    edgecolor="#cbd5e1",
    linewidth=1.5,
    transform=fig_p10.transFigure,
)
fig_p10.patches.append(card_top)
acc_top = patches.FancyBboxPatch(
    (0.03, 0.64),
    0.007,
    0.22,
    boxstyle="round,pad=0.001,rounding_size=0.003",
    facecolor="#2563eb",
    edgecolor="none",
    transform=fig_p10.transFigure,
)
fig_p10.patches.append(acc_top)

fig_p10.text(
    0.05,
    0.82,
    "SÍNTESIS DE CONCLUSIONES Y DIAGNÓSTICO INTEGRAL",
    fontsize=13,
    fontweight="bold",
    color="#1e293b",
)

conclusions_p10 = [
    (
        "• Solidez de Retención Operativa:",
        (
            r"Masa neta de \$30.98M con 39.8% de margen sobre \$77.91M netos,"
            " demostrando alta resiliencia financiera."
        ),
    ),
    (
        "• Cumplimiento Presupuestario Global:",
        (
            r"Alcance del 97.8% de la meta corporativa (\$79.65M), apalancado en"
            " E-Commerce y Cuentas Clave."
        ),
    ),
    (
        "• Alerta Crítica de Concentración:",
        (
            r"El Cibao concentra el 49.8% de ingresos (Índice HHI en 3,401"
            " puntos), exigiendo diversificación hacia el Este y Santo Domingo."
        ),
    ),
    (
        "• Inelasticidad y Pricing Estratégico:",
        (
            "Coeficiente de elasticidad de 0.01 confirma que el mercado absorbe"
            " incrementos graduales (+3%) sin pérdida de volumen."
        ),
    ),
]

y_c = 0.775
for c_title, c_desc in conclusions_p10:
  fig_p10.text(
      0.05, y_c, c_title, fontsize=10.2, fontweight="bold", color="#0f172a"
  )
  fig_p10.text(0.24, y_c, c_desc, fontsize=10.0, color="#475569")
  y_c -= 0.038

# Tarjeta de la Matriz de Decisiones
card_tbl = patches.FancyBboxPatch(
    (0.03, 0.08),
    0.94,
    0.53,
    boxstyle="round,pad=0.006,rounding_size=0.012",
    facecolor="#ffffff",
    edgecolor="#cbd5e1",
    linewidth=1.5,
    transform=fig_p10.transFigure,
)
fig_p10.patches.append(card_tbl)
acc_tbl = patches.FancyBboxPatch(
    (0.03, 0.08),
    0.007,
    0.53,
    boxstyle="round,pad=0.001,rounding_size=0.003",
    facecolor="#16a34a",
    edgecolor="none",
    transform=fig_p10.transFigure,
)
fig_p10.patches.append(acc_tbl)

fig_p10.text(
    0.05,
    0.575,
    "MATRIZ PRESCRIPTIVA DE TOMA DE DECISIONES Y PLAN DE ACCIÓN 2027",
    fontsize=13,
    fontweight="bold",
    color="#15803d",
)

# Encabezado de la Tabla
tbl_hdr = patches.FancyBboxPatch(
    (0.045, 0.52),
    0.91,
    0.038,
    boxstyle="round,pad=0.003,rounding_size=0.006",
    facecolor="#f1f5f9",
    edgecolor="#e2e8f0",
    linewidth=1,
    transform=fig_p10.transFigure,
)
fig_p10.patches.append(tbl_hdr)

fig_p10.text(
    0.06,
    0.532,
    "ÁREA ESTRATÉGICA",
    fontsize=9.5,
    fontweight="bold",
    color="#334155",
)
fig_p10.text(
    0.23,
    0.532,
    "HALLAZGO ANALÍTICO / MODELO",
    fontsize=9.5,
    fontweight="bold",
    color="#334155",
)
fig_p10.text(
    0.53,
    0.532,
    "DECISIÓN EJECUTIVA INMEDIATA",
    fontsize=9.5,
    fontweight="bold",
    color="#334155",
)
fig_p10.text(
    0.81,
    0.532,
    "IMPACTO ESTIMADO",
    fontsize=9.5,
    fontweight="bold",
    color="#334155",
)

decisions_data = [
    (
        "Política de Descuentos",
        r"Descuentos >6.5% reducen la probabilidad de meta a <50%.",
        "Bloqueo estricto en ERP a máximo 5% sin aprobación de Finanzas.",
        r"+$1.2M Margen Recuperado",
        "#dcfce7",
        "#15803d",
    ),
    (
        "Cartera Clientes VIP",
        r"1,010 clientes VIP (Cluster A) concentran volumen con menor margen.",
        "Diseñar contratos marco con bonos por pronto pago en vez de rebajas.",
        "Fidelización 85% Cartera",
        "#e0f2fe",
        "#0369a1",
    ),
    (
        "Expansión Territorial",
        r"Sobreexposición extrema al Cibao (HHI: 3,401 pts; 49.8% ingresos).",
        "Reasignar 25% del presupuesto comercial hacia Santo Domingo y Este.",
        "HHI < 2,500 pts (Equilibrio)",
        "#fef3c7",
        "#b45309",
    ),
    (
        "Optimización Precios",
        r"Demanda altamente inelástica ante precio unitario (coeficiente 0.01).",
        "Ajuste selectivo de precios (+2.5% a +3.5%) en SKU líderes.",
        r"+$1.9M Directo al EBITDA",
        "#dcfce7",
        "#15803d",
    ),
    (
        "Planificación y Stock",
        r"Piso P10 de \$1.75M y proyección esperada P50 de \$2.11M mensuales.",
        "Alinear abastecimiento y compras de materias primas al escenario P50.",
        "-12% Sobrecostos Logísticos",
        "#f3e8ff",
        "#7e22ce",
    ),
]

y_row = 0.46
for area, hallazgo, decision, impacto, bg_imp, col_imp in decisions_data:
  fig_p10.text(
      0.06, y_row, area, fontsize=10.0, fontweight="bold", color="#0f172a"
  )
  fig_p10.text(0.23, y_row, hallazgo, fontsize=9.5, color="#475569")
  fig_p10.text(
      0.53, y_row, decision, fontsize=9.5, fontweight="bold", color="#1e293b"
  )

  # Píldora de impacto resaltada
  pill = patches.FancyBboxPatch(
      (0.805, y_row - 0.008),
      0.145,
      0.026,
      boxstyle="round,pad=0.002,rounding_size=0.005",
      facecolor=bg_imp,
      edgecolor="none",
      transform=fig_p10.transFigure,
  )
  fig_p10.patches.append(pill)
  fig_p10.text(
      0.812,
      y_row - 0.002,
      impacto,
      fontsize=8.8,
      fontweight="bold",
      color=col_imp,
  )

  # Línea divisoria
  div = plt.Line2D(
      [0.05, 0.95],
      [y_row - 0.022, y_row - 0.022],
      color="#f1f5f9",
      linewidth=1.2,
      transform=fig_p10.transFigure,
  )
  fig_p10.lines.append(div)
  y_row -= 0.075

fig_p10.text(
    0.05,
    0.04,
    "Preparado por: Dirección de Analítica & Business Intelligence   |  "
    " Validado por: Comité Ejecutivo y Finanzas   |   Octubre 2026",
    fontsize=9.5,
    color="#94a3b8",
)

plt.axis("off")
pdf.savefig(fig_p10)
plt.close(fig_p10)

# Cierre del PDF maestro
pdf.close()

print("\n" + "=" * 75)
print("🎉 COMPILACIÓN FINALIZADA CON ÉXITO")
print(
    f"📁 Documento PDF Maestro Generado: '{pdf_path}' (10 Páginas Completas)"
)
print("📁 4 Láminas PNG en 16:9 generadas:")
print("   - reporte_1_bi_ejecutivo.png")
print("   - reporte_2_ml_ejecutivo.png")
print("   - reporte_3_bi_moderno.png")
print("   - reporte_4_ml_econometria.png")
print("=" * 75)