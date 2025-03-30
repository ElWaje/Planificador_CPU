
# 🧠 Planificador de CPU

![Banner](banner_metricas.gif)

Este proyecto permite simular múltiples algoritmos de planificación de CPU de forma interactiva y educativa. Incluye visualizaciones, métricas, exportación de resultados y soporte multilenguaje.

---

## 📦 Algoritmos Soportados

- FIFO (First-In First-Out)
- SJF (Shortest Job First)
- SRTF (Shortest Remaining Time First)
- Prioridad cooperativa
- Prioridad expropiativa
- Round Robin

---

## 🧪 Fase 4: Pruebas automáticas + CI/CD

- Archivo `test_algoritmos.py` con pruebas para los 6 algoritmos
- Uso de `pytest` para validación local
- GitHub Actions (`.github/workflows/ci.yml`) para CI/CD

---

## 📊 Fase 5: Métricas de eficiencia

- Cálculo de:
  - 🔁 Cambios de contexto
  - ⏳ Tiempo total en espera
  - ⚙️ Uso de CPU
- Visualización comparativa en gráficas
- Exportación como banner animado (`banner_metricas.gif`)

---

## 🌐 Fase 3: Internacionalización

- Traducción dinámica ES / EN
- Diccionario multilenguaje (`i18n.py`)
- Exportación en idioma seleccionado

---

## 🚀 Cómo ejecutar

```bash
streamlit run app_web.py
```

Requiere:  
- `streamlit`
- `matplotlib`
- `fpdf`
- `pandas`
- `pytest` (para pruebas)

---

## 📤 Exportaciones

- PDF con métricas y resultados
- Imagen del diagrama de Gantt
- Banner animado con métricas

---

## 🧠 Autor

Enrique Solís



## 📄 Presentación del proyecto

- [📘 Presentación en PDF (Español)](docs/Presentacion_Proyecto_CPU_Solis_v2.pdf)
- [📘 Project Presentation in PDF (English)](docs/CPU_Scheduler_Presentation_EN.pdf)


### 🧠 Fase 6: Recomendación inteligente del mejor algoritmo

Esta versión incluye una recomendación automática basada en reglas heurísticas.
Según las características de los procesos, el sistema sugiere el algoritmo de planificación más adecuado.

Ejemplo de salida:

> Se recomienda **SRTF** porque los procesos tienen ráfagas cortas y llegadas escalonadas.

Además, esta recomendación se incluye también en el PDF exportado.
