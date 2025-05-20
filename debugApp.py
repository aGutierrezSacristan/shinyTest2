import streamlit as st
import pandas as pd
import os

st.write("👋 App started")  # Confirm Streamlit rendered

# ---------- Setup ----------
BASE_DIR = os.path.dirname(__file__)
CSV_FILE = os.path.join(BASE_DIR, "cursos.csv")
st.write(f"📁 CSV path: `{CSV_FILE}`")

# Create CSV if not found
if not os.path.exists(CSV_FILE):
    st.warning("⚠️ cursos.csv not found — creating sample file.")
    df = pd.DataFrame([
        {
            "code": "FARM_7101",
            "title_es": "Título prueba",
            "title_en": "Test title",
            "credits": 3,
            "contact_hours": 45,
            "year": 1,
            "semester": 1,
            "status": "Activo",
            "description": "Texto de prueba",
            "comments": "Comentario de prueba"
        }
    ])
    df.to_csv(CSV_FILE, index=False)
else:
    st.success("✅ cursos.csv found")

# Load course data
try:
    course_df = pd.read_csv(CSV_FILE)
    st.write("🧾 CSV loaded with", len(course_df), "rows")
except Exception as e:
    st.error("❌ Error loading CSV")
    st.exception(e)
    st.stop()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login form
if not st.session_state.logged_in:
    st.subheader("🔐 Login required")
    with st.form("login"):
        user = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")
        if st.form_submit_button("Login"):
            if user == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")
else:
    st.success("✅ Usuario logeado")
    st.subheader("📚 Cursos disponibles")

    # Dropdown selector
    course_code = st.selectbox("Seleccione un curso:", course_df["code"].tolist())
    st.write("📌 Curso seleccionado:", course_code)

    row = course_df[course_df["code"] == course_code].iloc[0]
    st.write("📄 Descripción:", row["description"])
    st.write("📝 Comentarios:", row["comments"])
