import math

from models import Estudiante
from shared.herramientas import es_email_valido
from shared.json_manager import GestorJSON


gestor = GestorJSON("data/estudiantes.json")

CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = CAMPOS_ESTUDIANTE


def carnets_registrados(excepto_id=None):
    return {r["carnet"].strip().upper() for r in gestor.leer()
            if r["id"] != excepto_id}


def emails_registrados(excepto_id=None):
    return {r["email"].strip().lower() for r in gestor.leer()
            if r["id"] != excepto_id}


def siguiente_id():
    ids = [r["id"] for r in gestor.leer()]
    return max(ids) + 1 if ids else 1


def crear_estudiante(datos):
    if not isinstance(datos, dict):
        return False, "Los datos deben ser un diccionario"
    valores = {campo: str(datos.get(campo, "")).strip()
               for campo in CAMPOS_ESTUDIANTE}
    faltantes = [campo for campo in CAMPOS_ESTUDIANTE if not valores[campo]]
    if faltantes:
        return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"
    if not es_email_valido(valores["email"]):
        return False, "El email no tiene un formato válido"
    if valores["email"].lower() in emails_registrados():
        return False, "Ese email ya está registrado"
    if valores["carnet"].upper() in carnets_registrados():
        return False, "Ese carnet ya está registrado"

    estudiante = Estudiante(siguiente_id(), **valores)
    registros = gestor.leer()
    registros.append(estudiante.a_diccionario())
    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"
    return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"


def obtener_todos():
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def buscar_estudiantes(termino):
    termino = str(termino).strip().lower()
    if not termino:
        return []
    encontrados = []
    for registro in gestor.leer():
        if any(termino in str(registro.get(campo, "")).lower()
               for campo in CAMPOS_BUSCABLES):
            encontrados.append(Estudiante.desde_diccionario(registro))
    return encontrados


def actualizar_estudiante(id_estudiante, cambios):
    if not isinstance(cambios, dict):
        return False, "Los cambios deben ser un diccionario"
    desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
    if not cambios:
        return False, "No se indicó ningún cambio"
    if obtener_por_id(id_estudiante) is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    cambios = {campo: str(valor).strip() for campo, valor in cambios.items()}
    vacios = [campo for campo, valor in cambios.items() if not valor]
    if vacios:
        return False, f"No pueden quedar vacíos: {', '.join(vacios)}"
    if "email" in cambios:
        if not es_email_valido(cambios["email"]):
            return False, "El email no tiene un formato válido"
        if cambios["email"].lower() in emails_registrados(id_estudiante):
            return False, "Ese email ya lo usa otro estudiante"
    if ("carnet" in cambios
            and cambios["carnet"].upper() in carnets_registrados(id_estudiante)):
        return False, "Ese carnet ya lo usa otro estudiante"

    registros = gestor.leer()
    for registro in registros:
        if registro["id"] == id_estudiante:
            registro.update(cambios)
            if not gestor.guardar(registros):
                return False, "No se pudo escribir el archivo"
            return True, f"Estudiante {id_estudiante} actualizado"
    return False, f"No existe un estudiante con id {id_estudiante}"


def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    restantes = [r for r in registros if r["id"] != id_estudiante]
    if len(restantes) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"
    if not gestor.guardar(restantes):
        return False, "No se pudo escribir el archivo"
    return True, f"Estudiante {id_estudiante} eliminado"


def agregar_nota(id_estudiante, materia, nota):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    materia = str(materia).strip()
    if not materia:
        return False, "La materia no puede estar vacía"
    try:
        if isinstance(nota, bool):
            raise ValueError
        numero = float(nota)
    except (TypeError, ValueError):
        return False, "La nota debe ser un número entre 0 y 20"
    if not math.isfinite(numero) or not 0 <= numero <= 20:
        return False, "La nota debe ser un número entre 0 y 20"
    numero = int(numero) if numero.is_integer() else numero

    estudiante.agregar_nota(materia, numero)
    registros = gestor.leer()
    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[indice] = estudiante.a_diccionario()
            if not gestor.guardar(registros):
                return False, "No se pudo escribir el archivo"
            return True, f"Nota {numero} agregada en {materia}"
    return False, f"No existe un estudiante con id {id_estudiante}"


def obtener_promedio(id_estudiante):
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        return False, f"No existe un estudiante con id {id_estudiante}"
    return True, estudiante.obtener_promedio()


def materias_ofertadas():
    materias = set()
    for estudiante in obtener_todos():
        materias.update(estudiante.materias)
    return materias


def estudiantes_en_comun(id_a, id_b):
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)
    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"
    return True, estudiante_a.materias & estudiante_b.materias

