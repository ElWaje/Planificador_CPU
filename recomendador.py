# recomendador.py

def recomendar_algoritmo(processes, T):
    if not processes:
        return T["sin_recomendacion"]

    n = len(processes)
    rafagas = [p["Rafaga"] for p in processes]
    llegadas = [p["Llegada"] for p in processes]
    prioridades = [p["Prioridad"] for p in processes]

    prom_rafaga = sum(rafagas) / n
    dispersion_llegadas = max(llegadas) - min(llegadas) if n > 1 else 0
    hay_prioridades = len(set(prioridades)) > 1

    if prom_rafaga <= 4 and dispersion_llegadas > 2:
        return T["recom_srtf"]
    elif hay_prioridades:
        return T["recom_prioridad"]
    elif dispersion_llegadas == 0:
        return T["recom_rr"]
    elif prom_rafaga > 6:
        return T["recom_sjf"]
    else:
        return T["recom_fifo"]