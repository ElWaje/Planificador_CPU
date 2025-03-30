# CPU Scheduler

This project is an interactive educational tool that simulates different CPU scheduling algorithms. It's designed to help understand how these algorithms work and compare their performance using visualizations and metrics.

## 🔧 Features

- Support for various scheduling algorithms:
  - FIFO
  - SJF
  - SRTF
  - Round Robin
  - Cooperative and Preemptive Priority
- Step-by-step visualization of the simulation
- Animated particles and Gantt diagrams
- Export of results to PDF and JSON
- Configuration and multilingual support (ES/EN)
- Efficiency metrics and algorithm recommendation
- Load/save full sessions with configuration and results

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/ElWaje/Planificador_CPU.git
cd Planificador_CPU
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the application:

```bash
streamlit run app_web.py
```

## 🧠 Project Phases

1. Basic functionality and individual algorithms
2. Result table and averages
3. Gantt visualization
4. Automatic tests and CI/CD
5. Efficiency metrics (context switches, CPU usage, etc.)
6. Heuristic-based recommendation of the best algorithm
7. Step-by-step simulation
8. Explanation of scheduling decisions
9. Save/load complete execution sessions as JSON

## 📂 Files and Modules

- `app_web.py`: Main file with the Streamlit app
- `algoritmos_cpu.py`: Scheduling algorithms
- `metricas_cpu.py`: Efficiency metric calculations
- `recomendador.py`: Algorithm recommendation logic
- `components/`: UI components (step-by-step simulation, particles, decisions, etc.)
- `i18n.py`: Translations and multilingual support

## 📝 Resources

- [Project Presentation (ES)](./docs/Presentacion_Proyecto_CPU_Solis_v3.pdf)
- [Project Presentation (EN)](./docs/Project_Presentation_CPU_Solis_v3_en.pdf)

---

## 🎓 Educational Objective

The application is designed as an educational tool to help students and professionals understand and compare CPU scheduling algorithms interactively.

## 📄 License

This project is licensed under the MIT License.

## ✨ Author

Created by [@ElWaje](https://github.com/ElWaje)
