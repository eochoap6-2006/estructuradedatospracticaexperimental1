import sys

from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    CAMPOS_ESTUDIANTE, crear_estudiante, obtener_todos, obtener_por_id,
    buscar_estudiantes, actualizar_estudiante, eliminar_estudiante,
    agregar_nota, obtener_promedio, materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_id(texto="Id del estudiante: "):
    try:
        return int(input(texto))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None


def mostrar_resultado(resultado):
    exito, mensaje = resultado
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<16}{'NOMBRE':<27}{'EMAIL':<30}{'PROMEDIO':>9}")
    print("-" * 87)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.carnet:<16}"
              f"{estudiante.obtener_nombre_completo():<27}"
              f"{estudiante.email:<30}{estudiante.obtener_promedio():>9.2f}")
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")
    mostrar_resultado(crear_estudiante(datos))


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("Todavía no hay estudiantes")


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    estudiantes = buscar_estudiantes(termino)
    if estudiantes:
        mostrar_tabla(estudiantes)
    else:
        imprimir_info("No se encontraron estudiantes")


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return
    for clave, valor in estudiante.a_diccionario().items():
        print(f"  {clave.capitalize():<12}: {valor}")


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return
    imprimir_info("Deje en blanco el campo que no quiera cambiar.")
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        nuevo = input(f"{campo.capitalize()} [{getattr(estudiante, campo)}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    mostrar_resultado(actualizar_estudiante(id_estudiante, cambios))


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return
    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(eliminar_estudiante(id_estudiante))
    else:
        imprimir_info("Operación cancelada")


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return
    materia = input("Materia: ")
    nota = input("Nota (0 a 20): ")
    mostrar_resultado(agregar_nota(id_estudiante, materia, nota))


def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    id_estudiante = pedir_id()
    if id_estudiante is None:
        return
    exito, valor = obtener_promedio(id_estudiante)
    if exito:
        imprimir_info(f"Promedio general: {valor:.2f}")
    else:
        imprimir_error(valor)


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    id_a = pedir_id("Id del primer estudiante: ")
    if id_a is None:
        return
    id_b = pedir_id("Id del segundo estudiante: ")
    if id_b is None:
        return
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if exito:
        imprimir_info(", ".join(sorted(resultado)) if resultado else "No comparten materias")
    else:
        imprimir_error(resultado)


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()
    imprimir_info(", ".join(sorted(materias)) if materias else "Todavía no hay materias")


def salir():
    imprimir_info("¡Hasta luego!")
    return "salir"


OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue
        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break
        pausa()


if __name__ == "__main__":
    if "--comprobar" in sys.argv[1:]:
        from comprobaciones import comprobar
        comprobar()
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\nPrograma interrumpido por el usuario.")
