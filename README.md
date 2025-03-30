# 🧠 Planificador de CPU - Proyecto Interactivo

Este proyecto permite visualizar, comparar y simular diferentes algoritmos de planificación de procesos de CPU en una interfaz web interactiva utilizando **Streamlit**.

---

## 🚀 Funcionalidades

- Simulación de algoritmos: FIFO, SJF, SRTF, Round Robin, Prioridad (Cooperativa y Expropiativa)
- Cálculo automático de métricas: espera, respuesta, uso de CPU, cambios de contexto, etc.
- Exportación de resultados como PDF o imagen
- Comparación gráfica entre algoritmos
- Soporte **multilenguaje**: Español 🇪🇸 e Inglés 🇬🇧
- Carga y guardado de configuración como JSON
- Simulación paso a paso animada
- Panel de decisiones explicativas para el planificador
- Exportación y carga completa de resultados como JSON

---

## 🧩 Fases del Proyecto

### ✅ Fase 1: Interfaz interactiva

- Parámetros configurables (procesos, quantum)
- Visualización de resultados y métricas

### ✅ Fase 2: Algoritmos de planificación

- FIFO, SJF, SRTF, RR, Prioridad Coop y Exprop

### ✅ Fase 3: Visualización de Gantt

- Colores automáticos por proceso
- Exportación como imagen

### ✅ Fase 4: Pruebas automáticas y CI/CD

- `pytest` integrado
- GitHub Actions configurado

### ✅ Fase 5: Métricas de eficiencia

- Comparación visual entre algoritmos
- Métricas: uso de CPU, espera total, cambios de contexto

### ✅ Fase 6: Recomendación automática

- Basada en reglas heurísticas según los procesos
- Traducción multilenguaje

### ✅ Fase 7: Simulación paso a paso

- Reproducción visual del Gantt por pasos
- Botones de control: ▶️ ⏸️ ⏭️ 🔁
- Ideal para aprendizaje o debugging

### ✅ Fase 8: Animaciones y efectos visuales

- Animación de partículas con colores
- Gradientes personalizados y estilo mejorado
- Desactivables para accesibilidad

### ✅ Fase 9: Guardado/carga de ejecución completa

- Exporta todos los resultados como JSON
- Al cargar: se muestra tabla, Gantt, métricas, recomendación
- Vista especial para resultados desde JSON

---

## 🧠 Panel de decisiones del planificador

Explica paso a paso por qué se eligió un proceso:

- Muestra procesos disponibles
- Criterio utilizado (ráfaga, prioridad, llegada)
- Justificación de la elección

Ideal para aprendizaje y validación del algoritmo.

---

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/ElWaje/Planificador_CPU.git
cd Planificador_CPU
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la app:

```bash
streamlit run app_web.py
```

---

## 📝 Recursos

- [Presentación del Proyecto (ES)](./Presentacion_Proyecto_CPU_Solis_v3.pdf)
- [Project Presentation (EN)](./Project_Presentation_CPU_Solis_v3_en.pdf)

---

## 🧪 Tests

Para ejecutar las pruebas:

```bash
pytest
```

---

## 👨‍💻 Autor

Desarrollado por [ElWaje](https://github.com/ElWaje)

https://planificadorcpu-gv548bekautcujxbt6i8vt.streamlit.app/


---
