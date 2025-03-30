# components/resultados.py
import json
import streamlit as st

def guardar_resultados(data, resultados, gantt, metricas, recomendacion, config, T):
    export = {
        "configuracion": config,
        "procesos": data,
        "resultados": resultados,
        "gantt": gantt,
        "metricas": metricas,
        "recomendacion": recomendacion
    }

    try:
        json_str = json.dumps(export, indent=4)
        st.download_button(
            label="📤 " + T["descargar_resultados"],
            data=json_str,
            file_name="resultados_planificador.json",
            mime="application/json"
        )
        st.toast(T["resultados_guardados"], icon="✅")
    except Exception as e:
        st.toast(T["error_guardado"] + str(e), icon="❌")


def cargar_resultados(T):
    st.markdown("---")
    st.subheader("📥 " + T["cargar_resultados"])
    archivo = st.file_uploader("📂 " + T["subir_json"], type="json")

    if archivo:
        try:
            contenido = json.load(archivo)
            st.session_state["resultado_json"] = contenido
            st.success(T["resultados_cargados"])
            st.rerun()
        except Exception as e:
            st.error(T["error_config"] + str(e))
