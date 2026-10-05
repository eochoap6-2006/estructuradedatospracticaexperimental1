import json
from pathlib import Path
from tempfile import TemporaryDirectory

import views
from shared.json_manager import GestorJSON


def comprobar():
    original = views.gestor
    try:
        with TemporaryDirectory() as temporal:
            views.gestor = GestorJSON(str(Path(temporal) / "estudiantes.json"))
            ana = {
                "nombre": "Ana", "apellido": "Pérez",
                "email": "ana@escuela.edu", "carnet": "EST2026001"
            }
            luis = {
                "nombre": "Luis", "apellido": "Mora",
                "email": "luis@escuela.edu", "carnet": "EST2026002"
            }

            assert views.crear_estudiante(ana)[0]
            assert not views.crear_estudiante(dict(luis, carnet="est2026001"))[0]
            assert views.crear_estudiante(luis)[0]
            assert len(views.obtener_todos()) == 2
            assert len(views.buscar_estudiantes("mora")) == 1
            assert views.obtener_por_id(99) is None
            assert not views.actualizar_estudiante(2, {"carnet": "EST2026001"})[0]
            assert views.actualizar_estudiante(2, {"apellido": "Ruiz"})[0]
            assert views.obtener_por_id(2).apellido == "Ruiz"

            for nota in (-1, 21, "texto", "nan", "inf", True):
                assert not views.agregar_nota(1, "Matemática", nota)[0]
            assert not views.agregar_nota(99, "Matemática", 18)[0]
            assert views.agregar_nota(1, "Matemática", 18)[0]
            assert views.agregar_nota(1, "Inglés", 16)[0]
            assert views.agregar_nota(2, "Matemática", 20)[0]
            assert views.obtener_promedio(1) == (True, 17)
            assert views.materias_ofertadas() == {"Matemática", "Inglés"}
            assert views.estudiantes_en_comun(1, 2) == (True, {"Matemática"})
            assert not views.estudiantes_en_comun(1, 99)[0]

            archivo = Path(temporal) / "estudiantes.json"
            guardados = json.loads(archivo.read_text(encoding="utf-8"))
            assert guardados[0]["materias"] == ["Inglés", "Matemática"]
            assert guardados[0]["notas"]["Matemática"] == [18]
            assert views.obtener_por_id(1).materias == {"Inglés", "Matemática"}
            assert views.eliminar_estudiante(2)[0]
            assert not views.eliminar_estudiante(2)[0]
            assert len(views.obtener_todos()) == 1
    finally:
        views.gestor = original

    print("Comprobaciones correctas: CRUD, validaciones, notas, promedio y JSON.")


if __name__ == "__main__":
    comprobar()

