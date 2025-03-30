
# 🧠 CPU Scheduler

![Banner](banner_metricas.gif)

This project simulates multiple CPU scheduling algorithms interactively and educationally. It includes visualizations, metrics, exportable results, and multilingual support.

---

## 📦 Supported Algorithms

- FIFO (First-In First-Out)
- SJF (Shortest Job First)
- SRTF (Shortest Remaining Time First)
- Cooperative Priority
- Preemptive Priority
- Round Robin

---

## 🧪 Phase 4: Automated Testing + CI/CD

- `test_algorithms.py` with unit tests for all 6 algorithms
- `pytest` for local validation
- GitHub Actions (`.github/workflows/ci.yml`) for CI/CD

---

## 📊 Phase 5: Efficiency Metrics

- Metrics:
  - 🔁 Context switches
  - ⏳ Total waiting time
  - ⚙️ CPU usage
- Comparative visualization charts
- Exportable animated banner (`banner_metricas.gif`)

---

## 🌐 Phase 3: Internationalization

- Dynamic ES / EN translation
- Multilanguage dictionary (`i18n.py`)
- Export results and PDF in selected language

---

## 🚀 How to Run

```bash
streamlit run app_web.py
```

Dependencies:
- `streamlit`
- `matplotlib`
- `fpdf`
- `pandas`
- `pytest` (for testing)

---

## 📤 Exports

- PDF with metrics and results
- Gantt chart as image
- Animated metrics banner

---

## 🧠 Author

Enrique Solís


## 📄 Project Presentation

- [📘 Presentation in PDF (Spanish)](docs/Presentacion_Proyecto_CPU_Solis_v2.pdf)
- [📘 Presentation in PDF (English)](docs/CPU_Scheduler_Presentation_EN.pdf)


### 🧠 Phase 6: Smart scheduling algorithm recommendation

This version includes an automatic recommendation based on heuristic rules.
According to the characteristics of the processes, the system suggests the most suitable scheduling algorithm.

Example output:

> **SRTF** is recommended because processes have short bursts and staggered arrivals.

This recommendation is also included in the exported PDF.
