
import streamlit as st

st.set_page_config(page_title="Planificador de CPU", layout='wide')

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
from fpdf import FPDF
import io
import json
from streamlit_lottie import st_lottie
import requests
from algoritmos_cpu import fifo, sjf, srtf, prioridad_coop, prioridad_exprop, rr
from i18n import TRAD
from components import simulacion_paso_a_paso, render_particle_styles, render_particle_script
from components import mostrar_decision
from components import guardar_resultados, cargar_resultados
from metricas_cpu import calcular_metricas
from recomendador import recomendar_algoritmo

# ===================== MULTILENGUAJE ========================
lang = st.sidebar.selectbox("🌐 Idioma / Language", ["es", "en"])
T = TRAD[lang]

# Estilos CSS
st.markdown(f"""
<style>
    body {{
        font-family: 'Courier New', monospace;
    }}
    .main {{
        background: linear-gradient(145deg, #f0f8ff, #e6f7ff);
        padding: 2rem;
    }}
    h1, h2, h3 {{
        color: #0ccac4 !important;
    }}
    .stButton>button {{
        background-color: #0ccac4;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.5rem 1.2rem;
    }}
    /* Ocultar texto por defecto */
    section[data-testid="stFileUploader"] div[role="button"] p {{
        visibility: hidden;
    }}

    /* Reemplazar por texto traducido + ícono */
    section[data-testid="stFileUploader"] div[role="button"]::before {{
        content: "💾 {T['subir_json']}";
        visibility: visible;
        display: block;
        font-weight: bold;
        padding-bottom: 4px;
    }}

    /* Ocultar descripción original */
    section[data-testid="stFileUploader"] small {{
        display: none;
    }}

    /* Añadir descripción traducida */
    section[data-testid="stFileUploader"]::after {{
        content: "{T['limite_json']}";
        visibility: visible;
        display: block;
        font-size: 0.8rem;
        color: gray;
        padding-top: 4px;
    }}

    /* Traducir el botón de "Browse files" */
    section[data-testid="stFileUploader"] button {{
        font-weight: bold;
    }}
    section[data-testid="stFileUploader"] button::after {{
        content: " {T['boton_subir']}";
    }}
    section[data-testid="stFileUploader"] button > span {{
        visibility: hidden;
    }}
    footer {{
        visibility: hidden;
    }}

    .custom-footer {{
        position: fixed;
        bottom: 0;
        width: 100%;
        background: linear-gradient(to right, #e0f7fa, #b2ebf2);
        color: #004d40;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        border-top: 2px solid #80deea;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        z-index: 9999;
    }}

    .custom-footer a {{
        color: #00796b;
        font-weight: bold;
        text-decoration: none;
    }}

    .custom-footer a:hover {{
        text-decoration: underline;
        color: #004d40;
    }}
    @media (prefers-color-scheme: dark) {{
        .custom-footer {{
            background: linear-gradient(to right, #263238, #37474f);
            color: #b2ebf2;
            border-top: 2px solid #4dd0e1;
        }}
        .custom-footer a {{
            color: #4dd0e1;
        }}
        .custom-footer a:hover {{
            color: #80deea;
        }}
    }}

</style>
""", unsafe_allow_html=True)

# ========== CSS Y ANIMACIONES PARTICULAS ==========
st.markdown(render_particle_styles(), unsafe_allow_html=True)
st.markdown(render_particle_script(), unsafe_allow_html=True)

# ======================== TÍTULO =========================
st.title("🧠 " + T["titulo"])
st.sidebar.header(T["config"])

quantum = st.sidebar.number_input(T["Quantum (RR)"], min_value=1, value=2, key="quantum_input")
num = st.sidebar.slider(T["N° de procesos"], 1, 10, 4, key="slider_procesos")

st.subheader("⚙️ " + T["datos_procesos"])
data = []
for i in range(num):
    cols = st.columns(4)
    nombre = cols[0].text_input(f'{T["nombre"]}_{i}', value=f'P{i+1}', key=f'nombre_{i}')
    llegada = cols[1].number_input(f'{T["llegada"]}_{i}', min_value=0, value=i, key=f'llegada_{i}')
    rafaga = cols[2].number_input(f'{T["rafaga"]}_{i}', min_value=1, value=5, key=f'rafaga_{i}')
    prioridad = cols[3].number_input(f'{T["prioridad"]}_{i}', min_value=1, value=3, key=f'prioridad_{i}')
    data.append({T["Proceso"]: nombre, T["Llegada"]: llegada, T["Rafaga"]: rafaga, T["Prioridad"]: prioridad})

# ======================== ALGORITMOS =========================
# Normalizar claves antes de pasar a los algoritmos
data_normalizada = []
for p in data:
    data_normalizada.append({
        'Proceso': p[T['Proceso']],
        'Llegada': p[T['Llegada']],
        'Rafaga': p[T['Rafaga']],
        'Prioridad': p[T['Prioridad']]
    })
    
# ======================= RECOMENDACIÓN AUTOMÁTICA =======================

# ✅ Recomendación del mejor algoritmo
recomendacion = recomendar_algoritmo(data_normalizada, T)
st.success(f"🧠 {T['recomendacion']}: {recomendacion}")

algoritmos = {
    T["FIFO"]: lambda d, T=T: fifo(d, T),
    T["SJF"]: lambda d, T=T: sjf(d, T),
    T["SRTF"]: lambda d, T=T: srtf(d, T),
    T["Prioridad Coop"]: lambda d, T=T: prioridad_coop(d, T),
    T["Prioridad Exprop"]: lambda d, T=T: prioridad_exprop(d, T),
    T["Round Robin"]: lambda d, T=T: rr(d, quantum, T)
}
selected_algo = st.selectbox(T["algoritmo"], list(algoritmos.keys()))
# Forzar recálculo si cambia el algoritmo
if 'ultimo_algo' not in st.session_state or st.session_state['ultimo_algo'] != selected_algo:
    st.session_state['ultimo_algo'] = selected_algo


resultados, gantt, detalles, cola = algoritmos[selected_algo](data_normalizada, T)
metricas = calcular_metricas(resultados, gantt, T)

# ======================== SIMULACIÓN PASO A PASO =========================
st.markdown("---")
st.subheader(T["simulacion"])
simulacion_paso_a_paso(gantt, T)

# ======================= TABLA RESULTADOS =====================
df = pd.DataFrame(resultados, columns=[T["Proceso"], T["espera"], T["respuesta"]])
st.dataframe(df)

media_espera = df[T["espera"]].mean()
media_respuesta = df[T["respuesta"]].mean()

esperas = df[T["espera"]].tolist()
respuestas = df[T["respuesta"]].tolist()

suma_espera = sum(esperas)
suma_respuesta = sum(respuestas)

st.markdown(f"""
**🧮 {T['media']}**

{T['espera']}: ({' + '.join(str(e) for e in esperas)}) / {len(esperas)} = {suma_espera}/{len(esperas)} = {media_espera:.2f}

{T['respuesta']}: ({' + '.join(str(r) for r in respuestas)}) / {len(respuestas)} = {suma_respuesta}/{len(respuestas)} = {media_respuesta:.2f}
""")

with st.expander(T["paso_paso"]):
    for d in detalles:
        st.text(d)

with st.expander(T["cola_ejecucion"]):
    st.text(' → '.join(cola))
    
fig, ax = plt.subplots(figsize=(10, 2))

# Obtener todos los nombres de procesos únicos
procesos_unicos = list({p for p, _, _ in gantt})
colormap = cm.get_cmap('nipy_spectral', len(procesos_unicos))
colores = {p: colormap(i) for i, p in enumerate(procesos_unicos)}

for p, ini, fin in gantt:
    ax.broken_barh([(ini, fin - ini)], (10, 9), facecolors=[colores[p]])
    ax.text((ini + fin) / 2, 14, p, ha='center', color='white', fontsize=8)

ax.set_xlim(0, max([fin for _, _, fin in gantt]) + 2)
ax.set_ylim(5, 25)
ax.set_xlabel(T["tiempo"])
ax.set_yticks([])
st.pyplot(fig)

# Exportar imagen del Gantt
buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button(
    label="🖼️ " + T["Descargar Gantt como imagen"],
    data=buf.getvalue(),
    file_name="gantt.png",
    mime="image/png"
)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Courier", size=12)

pdf.cell(0, 10, f"{T['resultados']} {selected_algo}", ln=True)
for fila in resultados:
    pdf.cell(0, 10, f"{fila[0]} - {T['espera']}: {fila[1]} - {T['respuesta']}: {fila[2]}", ln=True)

pdf.cell(0, 10, f"{T['media_espera']}: {media_espera:.2f}", ln=True)
pdf.cell(0, 10, f"{T['media_respuesta']}: {media_respuesta:.2f}", ln=True)

pdf_bytes = pdf.output(dest='S').encode('latin1')
st.download_button(
    T['exportar_pdf'],
    data=pdf_bytes,
    file_name=f'{selected_algo}_resultados.pdf',
    mime='application/pdf'
)

# ======================= MÉTRICAS DE EFICIENCIA ======================
st.subheader("📊 " + T["metricas"])
col1, col2, col3 = st.columns(3)
col1.metric(T["cambios_contexto"], metricas[T["cambios_contexto"]])
col2.metric(T["uso_cpu"], metricas[T["uso_cpu"]])
col3.metric(T["total_espera"], metricas[T["total_espera"]])

# ======================= GRAFICAS COMPARATIVAS ======================
# Cargamos métricas de todos los algoritmos
metricas_todos = {}
for nombre, func in algoritmos.items():
    r, g, _, _ = func(data_normalizada, T)
    m = calcular_metricas(r, g,T)
    metricas_todos[nombre] = m

st.subheader("📈 " + T["comparativa"])
abreviaturas = {
    T["FIFO"]: "FIFO",
    T["SJF"]: "SJF",
    T["SRTF"]: "SRTF",
    T["PC"]: T["Prioridad Coop"],
    T["PE"]: T["Prioridad Exprop"],
    T["RR"]: T["Round Robin"]
}

for key in [T["cambios_contexto"], T["uso_cpu"], T["total_espera"]]:
    fig, ax = plt.subplots()
    nombres = list(abreviaturas.keys())  # Siglas traducidas
    valores = [metricas_todos[abreviaturas[n]][key] for n in nombres]
    ax.bar(nombres, valores)
    ax.set_ylabel(key)
    ax.set_title(f"{T['comparativa']} - {key}")
    ax.tick_params(axis='x', labelrotation=15)  # Evita superposición de texto
    st.pyplot(fig)
# Función para cargar animación desde URL
def cargar_animacion(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# ========== GUARDAR CONFIGURACIÓN COMO JSON ==========
config_actual = {
    "idioma": lang,
    "algoritmo": st.session_state.get('ultimo_algo', selected_algo),
    "num_procesos": num,
    "quantum": quantum
}

try:
    config_json = json.dumps(config_actual, indent=4)
    st.download_button(
        label="💾 " + T["descargar_config"],
        data=config_json,
        file_name="configuracion_cpu.json",
        mime="application/json"
    )
    st.toast(T["config_guardada"], icon="✅")
except Exception as e:
    st.toast(T["error_guardado"] + str(e), icon="❌")

# ========== CARGAR CONFIGURACIÓN DESDE JSON ==========
st.markdown("---")

# Animación + carga de configuración
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        animacion = cargar_animacion("https://lottie.host/1b2ab028-3e5b-41a0-8a5e-083c5cbf3b35/Zpj7LZJH93.json")
        if animacion:
            st_lottie(animacion, height=140)
    with col2:
        st.subheader("⚙️ " + T["cargar_config"])
        archivo_json = st.file_uploader("📤 " + T["subir_json"], type="json")

if archivo_json is not None:
    try:
        contenido = json.load(archivo_json)
        st.session_state['idioma'] = contenido.get("idioma", lang)
        st.session_state['ultimo_algo'] = contenido.get("algoritmo", selected_algo)
        st.session_state['quantum_input'] = contenido.get("quantum", quantum)
        st.session_state['slider_procesos'] = contenido.get("num_procesos", num)
        st.success(T["config_cargada"])

        # Forzar recarga si cambia idioma
        if contenido.get("idioma") and contenido["idioma"] != lang:
            st.session_state["idioma"] = contenido["idioma"]
            st.rerun()
    except Exception as e:
        st.error(T["error_config"] + str(e))

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Diccionario con configuración actual
config_actual = {
    "idioma": lang,
    "algoritmo": selected_algo,
    "num_procesos": num,
    "quantum": quantum
}

# Guardar resultados completos
guardar_resultados(data_normalizada, resultados, gantt, metricas, recomendacion, config_actual, T)

# Cargar resultados (esto puede ir antes si querés que se ejecute primero)
cargar_resultados(T)
# ==== MOSTRAR RESULTADOS CARGADOS DESDE JSON ====
if "resultado_json" in st.session_state:
    rjson = st.session_state["resultado_json"]

    st.markdown("## ✅ " + T["vista_resultados_json"])
    
    # Tabla de resultados
    st.subheader(T["resultados"])
    df = pd.DataFrame(rjson["resultados"], columns=[T["Proceso"], T["espera"], T["respuesta"]])
    st.dataframe(df)

    # Gantt
    gantt = rjson["gantt"]
    fig, ax = plt.subplots(figsize=(10, 2))
    procesos_unicos = list({p for p, _, _ in gantt})
    colormap = cm.get_cmap('nipy_spectral', len(procesos_unicos))
    colores = {p: colormap(i) for i, p in enumerate(procesos_unicos)}
    for p, ini, fin in gantt:
        ax.broken_barh([(ini, fin - ini)], (10, 9), facecolors=[colores[p]])
        ax.text((ini + fin) / 2, 14, p, ha='center', color='white', fontsize=8)
    ax.set_xlim(0, max([fin for _, _, fin in gantt]) + 2)
    ax.set_ylim(5, 25)
    ax.set_xlabel(T["tiempo"])
    ax.set_yticks([])
    st.pyplot(fig)

    # Métricas
    st.subheader("📊 " + T["metricas"])
    met = rjson["metricas"]
    col1, col2, col3 = st.columns(3)
    col1.metric(T["cambios_contexto"], met[T["cambios_contexto"]])
    col2.metric(T["uso_cpu"], met[T["uso_cpu"]])
    col3.metric(T["total_espera"], met[T["total_espera"]])

    # Recomendación
    st.info("🧠 " + T["recomendacion"] + ": " + rjson["recomendacion"])

    # Limpiar resultados
    if st.button("🧹 " + T["limpiar_resultados"]):
        del st.session_state["resultado_json"]
        st.rerun()


# ======================= FOOTER =======================
from datetime import datetime
año_actual = datetime.now().year

st.markdown(f"""
<div class="custom-footer">
    🧠 © {año_actual} <a href="https://github.com/ElWaje/Planificador_CPU" target="_blank">{T['footer_app']}</a> — {T['footer_powered']}
</div>
""", unsafe_allow_html=True)
