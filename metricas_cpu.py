# metricas_cpu.py
def calcular_metricas(resultados, gantt, T):
    """
    Calcula métricas de eficiencia: cambios de contexto, uso de CPU y tiempo total de espera.
    - resultados: lista de (nombre, espera, respuesta)
    - gantt: lista de (nombre, inicio, fin)
    - T: diccionario de traducción
    """
    cambios_contexto = 0
    uso_cpu = 0
    tiempo_espera = 0

    if gantt:
        anterior = gantt[0][0]
        for actual in gantt[1:]:
            if actual[0] != anterior:
                cambios_contexto += 1
            anterior = actual[0]

    for _, ini, fin in gantt:
        uso_cpu += fin - ini

    for _, espera, _ in resultados:
        tiempo_espera += espera

    return {
        T["cambios_contexto"]: cambios_contexto,
        T["uso_cpu"]: round(uso_cpu, 2),
        T["total_espera"]: tiempo_espera
    }
