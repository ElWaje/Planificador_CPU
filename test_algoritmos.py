import pytest
from algoritmos_cpu import fifo, sjf, srtf, prioridad_coop, prioridad_exprop, rr

# Datos de prueba base
procesos_base = [
    {"Proceso": "P1", "Llegada": 0, "Rafaga": 7, "Prioridad": 4},
    {"Proceso": "P2", "Llegada": 2, "Rafaga": 4, "Prioridad": 2},
    {"Proceso": "P3", "Llegada": 3, "Rafaga": 3, "Prioridad": 1},
    {"Proceso": "P4", "Llegada": 5, "Rafaga": 2, "Prioridad": 3}
]

@pytest.mark.parametrize("algoritmo", [fifo, sjf, srtf, prioridad_coop, prioridad_exprop])
def test_algoritmos_funcionan(algoritmo):
    resultados, _, _, _ = algoritmo(procesos_base)
    assert len(resultados) == 4
    for nombre, espera, respuesta in resultados:
        assert espera >= 0
        assert respuesta >= procesos_base[int(nombre[1]) - 1]["Rafaga"]

def test_rr():
    resultados, _, _, _ = rr(procesos_base, quantum=2)
    assert len(resultados) == 4
    for nombre, espera, respuesta in resultados:
        assert espera >= 0
        assert respuesta >= procesos_base[int(nombre[1]) - 1]["Rafaga"]
