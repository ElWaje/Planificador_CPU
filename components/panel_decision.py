import streamlit as st

def mostrar_decision(procesos, criterio, elegido, T):
    with st.expander("📋 " + T["panel_decision"]):
        st.markdown(f"### 🧠 {T['decision_planificador']}")

        disponibles = ', '.join(p['Proceso'] for p in procesos)
        st.markdown(f"**{T['procesos_disponibles']}:** {disponibles}")

        if criterio == "Rafaga":
            comparaciones = ' | '.join(f"{p['Proceso']} → {p['Rafaga']}" for p in procesos)
            st.markdown(f"**{T['criterio_rafaga']}:** {comparaciones}")
        elif criterio == "Prioridad":
            comparaciones = ' | '.join(f"{p['Proceso']} → {p['Prioridad']}" for p in procesos)
            st.markdown(f"**{T['criterio_prioridad']}:** {comparaciones}")
        elif criterio == "Llegada":
            llegada = procesos[0]['Llegada'] if procesos else '?'
            st.markdown(f"**{T['criterio_llegada']}:** {elegido} → {llegada}")
            st.markdown(f"**{T['criterio_llegada']}:** {elegido} → {llegada}")
        elif criterio == "Cola":
            st.markdown(f"**{T['criterio_cola']}:** {elegido}")

        st.markdown(f"➡️ **{T['elegido']}:** {elegido}")

