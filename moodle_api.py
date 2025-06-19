import os
import requests

<<<<<<< HEAD
# Cargar las variables de entorno
MOODLE_URL = os.getenv("MOODLE_URL")  # Asegúrate de usar la variable en mayúsculas y correctamente configurada
MOODLE_TOKEN = os.getenv("MOODLE_TOKEN")

# Validación de las variables de entorno
if not MOODLE_URL or not MOODLE_TOKEN:
    raise ValueError("❌ Las variables de entorno 'MOODLE_URL' o 'MOODLE_TOKEN' no están definidas.")

=======
# Cargar variables de entorno
MOODLE_URL = os.getenv("moodle_url")
MOODLE_TOKEN = os.getenv("moodle_token")

if not MOODLE_URL or not MOODLE_TOKEN:
    raise ValueError("❌ Las variables de entorno 'moodle_url' o 'moodle_token' no están definidas.")

# Función genérica para llamar funciones de la API de Moodle
>>>>>>> 039b5b3b23918234b018d73f6e827399afb18d9d
def call_moodle_function(function_name, params=None):
    if params is None:
        params = {}
    base_params = {
        "wstoken": MOODLE_TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": function_name,
    }
    all_params = {**base_params, **params}
    response = requests.get(MOODLE_URL, params=all_params)
<<<<<<< HEAD
    
    # Verificación de respuesta
=======
>>>>>>> 039b5b3b23918234b018d73f6e827399afb18d9d
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"🔴 Error {response.status_code} al llamar a Moodle: {response.text}")

<<<<<<< HEAD
=======
# 🔹 Títulos de todos los cursos
>>>>>>> 039b5b3b23918234b018d73f6e827399afb18d9d
def get_all_course_titles():
    try:
        cursos = call_moodle_function("core_course_get_courses")
        if not cursos:
            return "No se encontraron cursos disponibles."
        return "\n".join(f"- {curso['fullname']}" for curso in cursos)
    except Exception as e:
        return f"⚠️ Error al obtener los títulos de los cursos: {e}"

<<<<<<< HEAD
=======
# 🔹 Contenidos de todos los cursos
>>>>>>> 039b5b3b23918234b018d73f6e827399afb18d9d
def get_all_course_contents():
    try:
        cursos = call_moodle_function("core_course_get_courses")
    except Exception as e:
        return f"⚠️ Error al obtener la lista de cursos: {e}"

    all_contents = []

    for curso in cursos:
        course_id = curso.get("id")
        course_name = curso.get("fullname", "Sin nombre")
        try:
            secciones = call_moodle_function("core_course_get_contents", {"courseid": course_id})
            for seccion in secciones:
                nombre_sec = seccion.get("name", "")
                for modulo in seccion.get("modules", []):
                    nombre_modulo = modulo.get("name", "")
                    tipo_modulo = modulo.get("modname", "")
                    descripcion = modulo.get("description", "")
                    contenido = f"[{course_name}] {nombre_sec} - {nombre_modulo} ({tipo_modulo})"
                    if descripcion:
                        contenido += f": {descripcion}"
                    all_contents.append(contenido)
        except Exception as e:
            all_contents.append(f"[{course_name}] ❌ Error al cargar contenidos: {e}")

    return "\n".join(all_contents) if all_contents else "No se pudo recuperar contenido detallado desde Moodle."

<<<<<<< HEAD
=======
# 🔹 Contenidos completos de los cursos del usuario por email
def get_user_course_contents_by_email(email):
    try:
        users = call_moodle_function("core_user_get_users", {
            "criteria[0][key]": "email",
            "criteria[0][value]": email
        })

        if not users:
            return "⚠️ No se encontró ningún usuario con ese correo."

        user_id = users[0]["id"]
        cursos = call_moodle_function("core_enrol_get_users_courses", {"userid": user_id})

        if not cursos:
            return "⚠️ No estás matriculado en ningún curso."

        all_contents = []

        for curso in cursos:
            course_id = curso.get("id")
            course_name = curso.get("fullname", "Sin nombre")
            try:
                secciones = call_moodle_function("core_course_get_contents", {"courseid": course_id})
                for seccion in secciones:
                    nombre_sec = seccion.get("name", "")
                    for modulo in seccion.get("modules", []):
                        nombre_modulo = modulo.get("name", "")
                        tipo_modulo = modulo.get("modname", "")
                        descripcion = modulo.get("description", "")
                        contenido = f"[{course_name}] {nombre_sec} - {nombre_modulo} ({tipo_modulo})"
                        if descripcion:
                            contenido += f": {descripcion}"
                        all_contents.append(contenido)
            except Exception as e:
                all_contents.append(f"[{course_name}] ❌ Error al cargar contenidos: {e}")

        return "\n".join(all_contents) if all_contents else "No se pudo recuperar contenido detallado desde Moodle."

    except Exception as e:
        return f"❌ Error al obtener contenidos del usuario: {e}"
>>>>>>> 039b5b3b23918234b018d73f6e827399afb18d9d
