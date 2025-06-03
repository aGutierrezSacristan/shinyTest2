import streamlit as st

st.set_page_config(page_title="Demo Filtros Dinámicos", layout="centered")

st.title("🎯 Filtros de Búsqueda Dinámicos")

# Paso 1: Elegir tipo de filtro
tipo_filtro = st.radio(
    "Selecciona el tipo de filtro:",
    ["Por código", "Por título del curso", "Por palabra clave"],
    index=None
)

# Datos de ejemplo
codigos = ["BIO101", "CHE102", "PHY103"]
titulos = ["Biología General", "Química Orgánica", "Física I"]

# Paso 2: Mostrar el campo correspondiente según la selección
if tipo_filtro == "Por código":
    codigo_sel = st.selectbox("Selecciona el código del curso:", codigos)
    st.write(f"Has seleccionado el código: `{codigo_sel}`")

elif tipo_filtro == "Por título del curso":
    titulo_sel = st.selectbox("Selecciona el título del curso:", titulos)
    st.write(f"Has seleccionado el curso: **{titulo_sel}**")

elif tipo_filtro == "Por palabra clave":
    palabra_clave = st.text_input("Ingresa una palabra clave:")
    if palabra_clave:
        st.write(f"Buscando resultados relacionados con: _{palabra_clave}_")

# Botón opcional para limpiar filtros
if tipo_filtro:
    if st.button("🔄 Limpiar Filtro"):
        st.experimental_rerun()
