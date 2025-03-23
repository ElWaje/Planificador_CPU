# app_web.py (versión final con 6 algoritmos corregidos, cálculos y cola de ejecución)
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import io

st.set_page_config(page_title='Planificador de CPU', layout='wide')

# ======================= ALGORITMOS COMPLETOS =========================
# FIFO – orden por llegada, sin expropiación
def fifo(processes):
    procesos = sorted(processes, key=lambda x: x['Llegada'])
    tiempo = 0
    resultados, gantt, detalles, cola = [], [], [], []
    for p in procesos:
        inicio = max(tiempo, p['Llegada'])
        espera = inicio - p['Llegada']
        respuesta = espera + p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        gantt.append((p['Proceso'], inicio, inicio + p['Rafaga']))
        detalles.append(
            f"{p['Proceso']}: llega en {p['Llegada']}, inicia en {inicio}\n"
            f"→ espera: {inicio} - {p['Llegada']} = {espera}\n"
            f"→ respuesta: {espera} + {p['Rafaga']} = {respuesta}\n"
        )
        cola.append(p['Proceso'])
        tiempo = inicio + p['Rafaga']
    return resultados, gantt, detalles, cola

# SJF – elige ráfaga más corta entre disponibles, no expropiativo
def sjf(processes):
    tiempo = 0
    completados = []
    resultados, gantt, detalles, cola = [], [], [], []
    while len(completados) < len(processes):
        disponibles = [p for p in processes if p['Llegada'] <= tiempo and p['Proceso'] not in completados]
        if not disponibles:
            tiempo += 1
            continue
        p = min(disponibles, key=lambda x: x['Rafaga'])
        inicio = tiempo
        espera = inicio - p['Llegada']
        respuesta = espera + p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        gantt.append((p['Proceso'], inicio, inicio + p['Rafaga']))
        detalles.append(
            f"{p['Proceso']}: llega en {p['Llegada']}, inicia en {inicio}\n"
            f"→ espera: {inicio} - {p['Llegada']} = {espera}\n"
            f"→ respuesta: {espera} + {p['Rafaga']} = {respuesta}\n"
        )
        cola.append(p['Proceso'])
        tiempo += p['Rafaga']
        completados.append(p['Proceso'])
    return resultados, gantt, detalles, cola

# SRTF – expropiativo, elige menor tiempo restante entre todos los disponibles
def srtf(processes):
    tiempo = 0
    procesos = sorted(processes, key=lambda x: x['Llegada'])
    restantes = {p['Proceso']: p['Rafaga'] for p in processes}
    gantt, completados, cola = [], [], []
    en_ejecucion = None
    ejec_inicio = 0
    tiempos_finales, detalles = {}, []

    while len(completados) < len(processes):
        disponibles = [p for p in processes if p['Llegada'] <= tiempo and restantes[p['Proceso']] > 0]
        if not disponibles:
            tiempo += 1
            continue
        actual = min(disponibles, key=lambda x: restantes[x['Proceso']])
        if en_ejecucion != actual['Proceso']:
            if en_ejecucion:
                gantt.append((en_ejecucion, ejec_inicio, tiempo))
            ejec_inicio = tiempo
            en_ejecucion = actual['Proceso']
            cola.append(en_ejecucion)
        restantes[en_ejecucion] -= 1
        if restantes[en_ejecucion] == 0:
            completados.append(en_ejecucion)
            tiempos_finales[en_ejecucion] = tiempo + 1
        tiempo += 1

    if en_ejecucion:
        gantt.append((en_ejecucion, ejec_inicio, tiempo))

    resultados = []
    for p in processes:
        fin = tiempos_finales[p['Proceso']]
        respuesta = fin - p['Llegada']
        espera = respuesta - p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        detalles.append(
            f"{p['Proceso']}: llega en {p['Llegada']}, finaliza en {fin}\n"
            f"→ espera: {respuesta} - {p['Rafaga']} = {espera}\n"
            f"→ respuesta: {respuesta}\n"
        )
    return resultados, gantt, detalles, cola

# Prioridad cooperativa – no interrumpe, ejecuta proceso con menor prioridad entre disponibles
def prioridad_coop(processes):
    tiempo = 0
    completados = []
    resultados, gantt, detalles, cola = [], [], [], []
    while len(completados) < len(processes):
        disponibles = [p for p in processes if p['Llegada'] <= tiempo and p not in completados]
        if not disponibles:
            tiempo += 1
            continue
        p = min(disponibles, key=lambda x: x['Prioridad'])
        inicio = tiempo
        espera = inicio - p['Llegada']
        respuesta = espera + p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        gantt.append((p['Proceso'], inicio, inicio + p['Rafaga']))
        detalles.append(
            f"{p['Proceso']}: llega en {p['Llegada']}, inicia en {inicio}\n"
            f"→ espera: {espera}\n"
            f"→ respuesta: {respuesta}\n"
        )
        cola.append(p['Proceso'])
        tiempo += p['Rafaga']
        completados.append(p)
    return resultados, gantt, detalles, cola

# Prioridad expropiativa – interrumpe si llega proceso con mejor prioridad
def prioridad_exprop(processes):
    tiempo = 0
    restantes = {p['Proceso']: p['Rafaga'] for p in processes}
    gantt, completados, cola = [], [], []
    en_ejecucion = None
    ejec_inicio = 0
    tiempos_finales, detalles = {}, []

    while len(completados) < len(processes):
        disponibles = [p for p in processes if p['Llegada'] <= tiempo and restantes[p['Proceso']] > 0]
        if not disponibles:
            tiempo += 1
            continue
        actual = min(disponibles, key=lambda x: x['Prioridad'])
        if en_ejecucion != actual['Proceso']:
            if en_ejecucion:
                gantt.append((en_ejecucion, ejec_inicio, tiempo))
            ejec_inicio = tiempo
            en_ejecucion = actual['Proceso']
            cola.append(en_ejecucion)
        restantes[en_ejecucion] -= 1
        if restantes[en_ejecucion] == 0:
            completados.append(en_ejecucion)
            tiempos_finales[en_ejecucion] = tiempo + 1
        tiempo += 1

    if en_ejecucion:
        gantt.append((en_ejecucion, ejec_inicio, tiempo))

    resultados = []
    for p in processes:
        fin = tiempos_finales[p['Proceso']]
        respuesta = fin - p['Llegada']
        espera = respuesta - p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        detalles.append(
            f"{p['Proceso']}: llega en {p['Llegada']}, finaliza en {fin}\n"
            f"→ espera: {espera}\n"
            f"→ respuesta: {respuesta}\n"
        )
    return resultados, gantt, detalles, cola

# Round Robin – con quantum definido por usuario
def rr(processes, quantum):
    tiempo = 0
    queue = []
    pendientes = sorted(processes, key=lambda x: x['Llegada'])
    restantes = {p['Proceso']: p['Rafaga'] for p in processes}
    gantt, resultados, detalles, cola = [], [], [], []
    tiempos_finales = {}

    while pendientes or queue:
        while pendientes and pendientes[0]['Llegada'] <= tiempo:
            queue.append(pendientes.pop(0))
        if not queue:
            tiempo += 1
            continue
        p = queue.pop(0)
        nombre = p['Proceso']
        ejec = min(quantum, restantes[nombre])
        inicio = tiempo
        tiempo += ejec
        gantt.append((nombre, inicio, tiempo))
        cola.append(nombre)
        restantes[nombre] -= ejec
        while pendientes and pendientes[0]['Llegada'] <= tiempo:
            queue.append(pendientes.pop(0))
        if restantes[nombre] > 0:
            queue.append(p)
        else:
            tiempos_finales[nombre] = tiempo

    for p in processes:
        respuesta = tiempos_finales[p['Proceso']] - p['Llegada']
        espera = respuesta - p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        detalles.append(
            f"{p['Proceso']}: llega en {p['Llegada']}, finaliza en {tiempos_finales[p['Proceso']]}\n"
            f"→ espera: {espera}\n"
            f"→ respuesta: {respuesta}\n"
        )
    return resultados, gantt, detalles, cola

st.title('🧠 Simulador de Planificación de CPU')
st.sidebar.header('Configuración')
quantum = st.sidebar.number_input('Quantum (RR)', min_value=1, value=2)
num = st.sidebar.slider('N° de procesos', 1, 10, 4)

st.subheader('⚙️ Datos de procesos')
data = []
for i in range(num):
    cols = st.columns(4)
    nombre = cols[0].text_input(f'Nombre_{i}', value=f'P{i+1}')
    llegada = cols[1].number_input(f'Llegada_{i}', min_value=0, value=i)
    rafaga = cols[2].number_input(f'Ráfaga_{i}', min_value=1, value=5)
    prioridad = cols[3].number_input(f'Prioridad_{i}', min_value=1, value=3)
    data.append({'Proceso': nombre, 'Llegada': llegada, 'Rafaga': rafaga, 'Prioridad': prioridad})

algoritmos = {
    "FIFO": lambda d: fifo(d),
    "SJF": lambda d: sjf(d),
    "SRTF": lambda d: srtf(d),
    "Prioridad Coop": lambda d: prioridad_coop(d),
    "Prioridad Exprop": lambda d: prioridad_exprop(d),
    "Round Robin": lambda d: rr(d, quantum)
}

algo = st.selectbox("Selecciona algoritmo", list(algoritmos.keys()), key="algoritmo")
# Forzar recálculo si cambia el algoritmo
if 'ultimo_algo' not in st.session_state or st.session_state['ultimo_algo'] != algo:
    st.session_state['ultimo_algo'] = algo
resultados, gantt, detalles, cola = algoritmos[algo](data)

df = pd.DataFrame(resultados, columns=['Proceso', 'Espera', 'Respuesta'])
st.dataframe(df)

media_espera = df['Espera'].mean()
media_respuesta = df['Respuesta'].mean()

st.markdown(f"**🧮 Medias:**\n\nEspera: ({' + '.join(str(e) for e in df['Espera'])}) / {len(df)} = {media_espera:.2f}\n\nRespuesta: ({' + '.join(str(r) for r in df['Respuesta'])}) / {len(df)} = {media_respuesta:.2f}")

with st.expander("📋 Cálculos paso a paso"):
    for d in detalles:
        st.text(d)

with st.expander("📥 Cola de ejecución"):
    st.text(' → '.join(cola))

fig, ax = plt.subplots(figsize=(10, 1.8))
for p, ini, fin in gantt:
    ax.broken_barh([(ini, fin - ini)], (10, 9), facecolors='tab:blue')
    ax.text((ini + fin) / 2, 14, p, ha='center', color='white')
ax.set_xlim(0, max([fin for _, _, fin in gantt]) + 2)
ax.set_ylim(5, 25)
ax.set_xlabel('Tiempo')
ax.set_yticks([])
st.pyplot(fig)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Courier", size=12)
pdf.cell(0, 10, f'Resultados {algo}', ln=True)
for fila in resultados:
    pdf.cell(0, 10, f'{fila[0]} - Espera: {fila[1]} - Respuesta: {fila[2]}', ln=True)
pdf.cell(0, 10, f'Media Espera: {media_espera:.2f}', ln=True)
pdf.cell(0, 10, f'Media Respuesta: {media_respuesta:.2f}', ln=True)
pdf_bytes = pdf.output(dest='S').encode('latin1')
st.download_button(
    '📄 Exportar PDF',
    data=pdf_bytes,
    file_name=f'{algo}_resultados.pdf',
    mime='application/pdf'
)
