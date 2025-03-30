'''Algoritmos de planificación de CPU'''
from components.panel_decision import mostrar_decision

# FIFO – orden por llegada, sin expropiación
def fifo(processes, T):
    procesos = sorted(processes, key=lambda x: x['Llegada'])
    tiempo = 0
    resultados, gantt, detalles, cola = [], [], [], []
    for p in procesos:
        mostrar_decision([p], "Llegada", p['Proceso'], T)
        inicio = max(tiempo, p['Llegada'])
        espera = inicio - p['Llegada']
        respuesta = espera + p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        gantt.append((p['Proceso'], inicio, inicio + p['Rafaga']))
        detalles.append(
            f"{p['Proceso']}: {T['llega_en']} {p['Llegada']},  {T['inicia_en']} {inicio}\n"
            f"{T['espera_']} {inicio} - {p['Llegada']} = {espera}\n"
            f"{T['respuesta_']} {espera} + {p['Rafaga']} = {respuesta}\n"
        )
        cola.append(p['Proceso'])
        tiempo = inicio + p['Rafaga']
    return resultados, gantt, detalles, cola

# SJF – elige ráfaga más corta entre disponibles, no expropiativo
def sjf(processes, T):
    tiempo = 0
    completados = []
    resultados, gantt, detalles, cola = [], [], [], []
    while len(completados) < len(processes):
        disponibles = [p for p in processes if p['Llegada'] <= tiempo and p['Proceso'] not in completados]
        if not disponibles:
            tiempo += 1
            continue
        p = min(disponibles, key=lambda x: x['Rafaga'])
        mostrar_decision(disponibles, "Rafaga", p['Proceso'], T)
        inicio = tiempo
        espera = inicio - p['Llegada']
        respuesta = espera + p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        gantt.append((p['Proceso'], inicio, inicio + p['Rafaga']))
        detalles.append(
            f"{p['Proceso']}: {T['llega_en']} {p['Llegada']},  {T['inicia_en']} {inicio}\n"
            f"{T['espera_']} {inicio} - {p['Llegada']} = {espera}\n"
            f"{T['respuesta_']} {espera} + {p['Rafaga']} = {respuesta}\n"
        )
        cola.append(p['Proceso'])
        tiempo += p['Rafaga']
        completados.append(p['Proceso'])
    return resultados, gantt, detalles, cola

# SRTF – expropiativo, elige menor tiempo restante entre todos los disponibles
def srtf(processes, T):
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
        mostrar_decision(disponibles, "Rafaga", actual['Proceso'], T)
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
            f"{p['Proceso']}: {T['llega_en']} {p['Llegada']}, {T['finaliza_en']} {fin}\n"
            f"{T['espera_']} {respuesta} - {p['Rafaga']} = {espera}\n"
            f"{T['respuesta_']} {respuesta}\n"
        )
    return resultados, gantt, detalles, cola

# Prioridad cooperativa – no interrumpe, ejecuta proceso con menor prioridad entre disponibles
def prioridad_coop(processes, T):
    tiempo = 0
    completados = []
    resultados, gantt, detalles, cola = [], [], [], []
    while len(completados) < len(processes):
        disponibles = [p for p in processes if p['Llegada'] <= tiempo and p not in completados]
        if not disponibles:
            tiempo += 1
            continue
        p = min(disponibles, key=lambda x: x['Prioridad'])
        mostrar_decision(disponibles, "Prioridad", p['Proceso'], T)
        inicio = tiempo
        espera = inicio - p['Llegada']
        respuesta = espera + p['Rafaga']
        resultados.append((p['Proceso'], espera, respuesta))
        gantt.append((p['Proceso'], inicio, inicio + p['Rafaga']))
        detalles.append(
            f"{p['Proceso']}: {T['llega_en']}n {p['Llegada']},  {T['inicia_en']} {inicio}\n"
            f"{T['espera_']} {espera}\n"
            f"{T['respuesta_']} {respuesta}\n"
        )
        cola.append(p['Proceso'])
        tiempo += p['Rafaga']
        completados.append(p)
    return resultados, gantt, detalles, cola

# Prioridad expropiativa – interrumpe si llega proceso con mejor prioridad
def prioridad_exprop(processes, T):
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
        mostrar_decision(disponibles, "Prioridad", actual['Proceso'], T)
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
            f"{p['Proceso']}: {T['llega_en']} {p['Llegada']}, {T['finaliza_en']} {fin}\n"
            f"{T['espera_']} {espera}\n"
            f"{T['respuesta_']} {respuesta}\n"
        )
    return resultados, gantt, detalles, cola

# Round Robin – con quantum definido por usuario
def rr(processes, quantum, T):
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
        mostrar_decision([p], "Cola", nombre, T)
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
            f"{p['Proceso']}: {T['llega_en']} {p['Llegada']}, {T['finaliza_en']} {tiempos_finales[p['Proceso']]}\n"
            f"{T['espera_']} {espera}\n"
            f"{T['respuesta_']} {respuesta}\n"
        )
    return resultados, gantt, detalles, cola

