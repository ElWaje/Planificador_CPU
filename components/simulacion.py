import streamlit as st
import time

# ================= ESTILOS PARTICULAS =================
def render_particle_styles():
    return """
    <style>
        .particle {
            position: absolute;
            width: 10px;
            height: 10px;
            background: #00bcd4;
            border-radius: 50%;
            pointer-events: none;
            animation: boom 600ms ease-out forwards;
            opacity: 0.9;
            box-shadow: 0 0 8px rgba(255, 255, 255, 0.7);
            z-index: 9999;
        }

        @keyframes boom {
            100% {
                transform: translate(var(--x), var(--y)) scale(0.2);
                opacity: 0;
            }
        }
    </style>
    """

# ================= SCRIPT PARTICULAS =================
def render_particle_script():
    return """
    <script>
        const colores = ["#00bcd4", "#ff4081", "#ffc107", "#8bc34a", "#3f51b5", "#e91e63", "#ff5722"];

        function explodeParticles(e) {
            const button = e.currentTarget;
            const rect = button.getBoundingClientRect();

            for (let i = 0; i < 20; i++) {
                const particle = document.createElement("div");
                particle.className = "particle";

                const color = colores[Math.floor(Math.random() * colores.length)];
                particle.style.background = `radial-gradient(circle at 30% 30%, ${color}, white)`;

                const size = Math.floor(Math.random() * 8) + 6;
                particle.style.width = size + "px";
                particle.style.height = size + "px";
                particle.style.borderRadius = Math.random() > 0.5 ? "50%" : "12%";

                particle.style.left = (e.clientX - rect.left) + "px";
                particle.style.top = (e.clientY - rect.top) + "px";
                particle.style.setProperty('--x', (Math.random() - 0.5) * 160 + "px");
                particle.style.setProperty('--y', (Math.random() - 0.5) * 160 + "px");

                button.appendChild(particle);

                setTimeout(() => particle.remove(), 600);
            }

            document.dispatchEvent(new CustomEvent('customNextStep'));
        }
    </script>
    """

# ================= SIMULACION PASO A PASO =================
def simulacion_paso_a_paso(gantt, T):
    
    # Asegurar claves
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "auto" not in st.session_state:
        st.session_state.auto = False

    step = st.session_state.get("step", 0)
    auto = st.session_state.get("auto", False)

    col1, col2, col3, col4 = st.columns(4)

    if col1.button(T["play"]):
        st.session_state.auto = True
    if col2.button(T["pause"]):
        st.session_state.auto = False
    if col3.button(T["paso"]):
        st.session_state.step = min(step + 1, len(gantt))
    if col4.button(T["reiniciar"]):
        st.session_state.step = 0
        st.session_state.auto = False

    if st.session_state.auto and step < len(gantt):
        time.sleep(0.8)
        st.session_state.step += 1
        st.rerun()

    st.write("---")
    for i in range(st.session_state.step):
        p, ini, fin = gantt[i]
        st.success(f"{p} → [{ini} - {fin}]")

    if step >= len(gantt):
        st.info(T["finalizado"])
        st.session_state.auto = False
