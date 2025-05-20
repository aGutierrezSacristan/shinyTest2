from shiny import App, ui, render, reactive, req
import pandas as pd
import os

# ---------- Setup ----------
BASE_DIR = os.path.dirname(__file__)
CSV_FILE = os.path.join(BASE_DIR, "cursos.csv")
print("✅ Using CSV at:", CSV_FILE)

# Create CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    pd.DataFrame([
        {
            "code": "FARM_7101",
            "title_es": "Desarrollo de Intervenciones Avanzadas en Comunicación en Salud",
            "title_en": "Development of Advanced Interventions in Health Communications",
            "credits": 3,
            "contact_hours": 54,
            "year": 1,
            "semester": 1,
            "status": "Activo",
            "description": "Curso centrado en estrategias de comunicación en salud",
            "comments": "Actualizado 2022"
        },
        {
            "code": "FARM_7102",
            "title_es": "Terapéutica Avanzada",
            "title_en": "Advanced Therapeutics",
            "credits": 4,
            "contact_hours": 60,
            "year": 1,
            "semester": 2,
            "status": "Activo",
            "description": "Curso sobre uso clínico avanzado de medicamentos",
            "comments": "Modificado por comité académico 2021"
        }
    ]).to_csv(CSV_FILE, index=False)

# Load courses
course_df = pd.read_csv(CSV_FILE)

# ---------- App UI ----------
logged_in = reactive.Value(False)

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style("""
            .panel-content {
                height: 200px;
                overflow-y: auto;
                white-space: pre-wrap;
                background: #fefefe;
                border: 1px solid #ccc;
                padding: 10px;
            }
            textarea.form-control {
                font-family: monospace;
                font-size: 14px;
                min-height: 150px;
            }
        """)
    ),
    ui.output_ui("main_ui")
)

# ---------- Server ----------
def server(input, output, session):
    selected_course = reactive.Value(None)

    @output
    @render.ui
    def main_ui():
        if not logged_in():
            return ui.div(
                ui.h2("📘 Bienvenido a Pi v2", style="text-align: center;"),
                ui.div(
                    ui.input_text("user", "Usuario:"),
                    ui.input_password("password", "Contraseña:"),
                    ui.input_action_button("login_btn", "Login", class_="btn-primary"),
                    style="text-align: center; max-width: 400px; margin: 50px auto;"
                )
            )

        return ui.div(
            ui.h3("📚 Base de Datos de Cursos"),
            ui.input_select("course_select", "Seleccione un curso:", choices=course_df["code"].tolist()),
            ui.output_ui("course_details")
        )

    @output
    @render.ui
    def course_details():
        req(input.course_select())
        selected_course.set(input.course_select())

        row = course_df[course_df["code"] == input.course_select()].iloc[0]

        return ui.div(
            ui.row(
                ui.column(6, ui.tags.p(ui.tags.b("Codificación:"), f" {row['code']}")),
                ui.column(6, ui.tags.p(ui.tags.b("Estado:"), f" {row['status']}"))
            ),
            ui.row(
                ui.column(6, ui.tags.p(ui.tags.b("Título (ES):"), f" {row['title_es']}")),
                ui.column(6, ui.tags.p(ui.tags.b("Título (EN):"), f" {row['title_en']}"))
            ),
            ui.row(
                ui.column(4, ui.tags.p(ui.tags.b("Créditos:"), f" {row['credits']}")),
                ui.column(4, ui.tags.p(ui.tags.b("Horas Contacto:"), f" {row['contact_hours']}")),
                ui.column(4, ui.tags.p(ui.tags.b("Año:"), f" {row['year']} | Semestre: {row['semester']}"))
            ),
            ui.hr(),
            ui.row(
                ui.column(6,
                    ui.tags.h5("📄 Descripción del Curso"),
                    ui.input_text_area("edit_description", "", value=row["description"])
                ),
                ui.column(6,
                    ui.tags.h5("📑 Comentarios"),
                    ui.input_text_area("edit_comments", "", value=row["comments"])
                )
            ),
            ui.br(),
            ui.input_action_button("save_changes", "💾 Guardar cambios", class_="btn-success"),
            ui.hr(),
            ui.tags.h5("📎 Archivos disponibles"),
            render_file_list(row["code"])
        )

    def render_file_list(course_code):
        folder_path = os.path.join(BASE_DIR, "www", course_code)
        if not os.path.exists(folder_path):
            return ui.tags.p("No se encontraron archivos.")

        files = sorted(os.listdir(folder_path))
        if not files:
            return ui.tags.p("No hay archivos disponibles.")

        return ui.tags.ul(
            *[
                ui.tags.li(
                    ui.tags.a(
                        f"📎 Descargar {file}",
                        href=f"/{course_code}/{file}",
                        target="_blank",
                        download=file
                    )
                )
                for file in files
            ]
        )

    @reactive.effect
    @reactive.event(input.save_changes)
    def save_to_csv():
        code = selected_course.get()
        idx = course_df[course_df["code"] == code].index
        if not idx.empty:
            i = idx[0]
            course_df.at[i, "description"] = input.edit_description()
            course_df.at[i, "comments"] = input.edit_comments()
            course_df.to_csv(CSV_FILE, index=False)
            ui.notification_show("Cambios guardados en el archivo.", type="message")

    @reactive.effect
    @reactive.event(input.login_btn)
    def _():
        if input.user().strip() == "admin" and input.password().strip() == "1234":
            logged_in.set(True)
        else:
            ui.notification_show("Credenciales incorrectas", type="error")

# ---------- Run ----------
app = App(app_ui, server)
