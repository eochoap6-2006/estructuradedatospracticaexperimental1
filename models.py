# Importa el módulo estándar 'json', que sirve para convertir datos de Python
# (diccionarios, listas, textos, números) a texto JSON y viceversa.
import json

# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
# Una tupla es INMUTABLE: nadie puede agregar, quitar ni cambiar campos por error.
# Nota: no incluye "id" porque el id lo genera el sistema, no lo escribe el usuario.
CAMPOS_CLIENTE = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")


# Define la clase Cliente: el "molde" a partir del cual se crean objetos cliente.
# Pertenece al MODELO en el patrón MVC (Modelo-Vista-Controlador): solo guarda
# datos y sabe transformarlos; no imprime menús ni pide datos al usuario.
class Cliente:
    """Representa los datos y operaciones básicas de un cliente.

    La clase permite crear un cliente, obtener su nombre completo y convertir
    sus datos a diccionario o texto JSON para guardarlos en un archivo.
    """

    # __init__ es el CONSTRUCTOR: se ejecuta automáticamente al hacer
    # Cliente(...). 'self' es el objeto que se está creando; los demás
    # parámetros son los valores que recibe para llenar sus atributos.
    def __init__(self, id_cliente, nombre, apellido, email, telefono, ciudad, direccion):
        """Crea un objeto cliente con sus datos personales y de contacto.

        Args:
            id_cliente: Identificador único del cliente.
            nombre: Nombres del cliente.
            apellido: Apellidos del cliente.
            email: Dirección de correo electrónico del cliente.
            telefono: Número telefónico del cliente.
            ciudad: Ciudad donde vive el cliente.
            direccion: Dirección física del cliente.
        """
        # Guarda el identificador en el atributo 'id' del objeto.
        self.id = id_cliente          # no usamos 'id' como parámetro: es una función de Python
        # Guarda el nombre recibido como atributo del objeto (self.nombre).
        self.nombre = nombre
        # Guarda el apellido del cliente.
        self.apellido = apellido
        # Guarda el correo electrónico del cliente.
        self.email = email
        # Guarda el teléfono (como texto, para conservar ceros iniciales, ej: "0991234567").
        self.telefono = telefono
        # Guarda la ciudad donde vive el cliente.
        self.ciudad = ciudad
        # Guarda la dirección física del cliente.
        self.direccion = direccion

    # Método de INSTANCIA: se llama sobre un objeto ya creado, ej: cliente.obtener_nombre_completo()
    def obtener_nombre_completo(self):
        """Une el nombre y el apellido del cliente en un solo texto.

        Returns:
            El nombre completo formado por el nombre y el apellido.
        """
        # f-string: inserta los valores de self.nombre y self.apellido
        # dentro del texto, separados por un espacio. Ej: "Ana Pérez".
        return f"{self.nombre} {self.apellido}"

    # Convierte el objeto en un diccionario. Se necesita porque json.dump()
    # no sabe guardar objetos de nuestras clases, pero sí diccionarios.
    def a_diccionario(self):
        """Convierte el cliente a un diccionario compatible con JSON.

        Returns:
            Diccionario con todos los atributos del cliente.
        """
        # Objeto -> diccionario (listo para JSON)
        # Cada par "clave": valor toma un atributo del objeto.
        return {
            "id": self.id,                  # clave "id"        -> atributo id
            "nombre": self.nombre,          # clave "nombre"    -> atributo nombre
            "apellido": self.apellido,      # clave "apellido"  -> atributo apellido
            "email": self.email,            # clave "email"     -> atributo email
            "telefono": self.telefono,      # clave "telefono"  -> atributo telefono
            "ciudad": self.ciudad,          # clave "ciudad"    -> atributo ciudad
            "direccion": self.direccion,    # clave "direccion" -> atributo direccion
        }

    # @classmethod convierte el método en un método de CLASE: en lugar de
    # recibir 'self' (un objeto), recibe 'cls' (la clase Cliente misma).
    # Se usa como "constructor alternativo": crear un Cliente desde un diccionario.
    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un cliente a partir de un diccionario previamente guardado.

        Args:
            datos: Diccionario con los campos del cliente. `ciudad` y
                `direccion` son opcionales para admitir archivos antiguos.

        Returns:
            Una instancia de `Cliente` construida con los datos recibidos.
        """
        # Diccionario -> objeto. Es un método de la CLASE, no de un objeto:
        # se usa así -> Cliente.desde_diccionario({...})
        # cls(...) equivale a Cliente(...): llama al constructor __init__.
        return cls(
            datos["id"],                  # datos["clave"]: si la clave NO existe lanza KeyError
            datos["nombre"],              # campo obligatorio
            datos["apellido"],            # campo obligatorio
            datos["email"],               # campo obligatorio
            datos["telefono"],            # campo obligatorio
            datos.get("ciudad", ""),      # .get por si el archivo es de una versión vieja
            datos.get("direccion", ""),   # .get devuelve "" si la clave no existe (no da error)
        )

    # Devuelve el cliente como un texto JSON (un string), no como diccionario.
    def a_json(self):
        """Convierte los datos del cliente a una cadena de texto JSON.

        Returns:
            Texto JSON con la información del cliente.
        """
        # json.dumps ("dump string") convierte el diccionario a texto JSON.
        # ensure_ascii=False permite que tildes y ñ se vean tal cual
        # ("Pérez") en lugar de códigos como "Pérez".
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    # __str__ es un método "mágico": Python lo llama automáticamente
    # cuando hacemos print(cliente) o str(cliente).
    def __str__(self):
        """Devuelve una representación breve y legible del cliente.

        Returns:
            Texto con el identificador, nombre completo y correo del cliente.
        """
        # Reutiliza obtener_nombre_completo() para no repetir código.
        # Ej: "[1] Ana Pérez - ana@correo.com"
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"


# Define la clase Estudiante. Además de datos personales, usa dos estructuras
# de datos: un DICCIONARIO DE LISTAS (notas) y un CONJUNTO (materias).
class Estudiante:
    """Representa a un estudiante, sus materias y sus calificaciones.

    La clase usa un diccionario de listas para almacenar notas por materia y
    un conjunto para evitar materias duplicadas.
    """

    # Constructor. 'notas' y 'materias' tienen valor por defecto None, así que
    # son OPCIONALES: se puede crear Estudiante(1, "Ana", "Pérez", "a@x.com", "EST1").
    # Se usa None (y no {} o set()) porque un valor por defecto mutable se
    # COMPARTIRÍA entre todos los estudiantes creados: un error clásico de Python.
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        """Crea un estudiante con sus datos académicos iniciales.

        Args:
            id_estudiante: Identificador único del estudiante.
            nombre: Nombres del estudiante.
            apellido: Apellidos del estudiante.
            email: Dirección de correo electrónico del estudiante.
            carnet: Código o carnet académico del estudiante.
            notas: Diccionario opcional con materias y listas de notas.
            materias: Colección opcional de materias inscritas.
        """
        # Guarda el identificador único del estudiante.
        self.id = id_estudiante
        # Guarda los nombres.
        self.nombre = nombre
        # Guarda los apellidos.
        self.apellido = apellido
        # Guarda el correo electrónico.
        self.email = email
        # Guarda el carnet (código académico).
        self.carnet = carnet                      # ej: EST2026001
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        # Expresión condicional: si llegaron notas se usan; si no (None o
        # vacío) se crea un diccionario vacío NUEVO para este estudiante.
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito, sin repetidos
        # set(materias) convierte cualquier colección (lista, tupla, set) en
        # conjunto, eliminando duplicados. Si no llegó nada, set() vacío.
        self.materias = set(materias) if materias else set()

    # Igual que en Cliente: une nombre y apellido en un solo texto.
    def obtener_nombre_completo(self):
        """Une el nombre y el apellido del estudiante.

        Returns:
            El nombre completo formado por el nombre y el apellido.
        """
        # Ej: "Ana Pérez"
        return f"{self.nombre} {self.apellido}"

    # Agrega una materia al conjunto de materias del estudiante.
    def inscribir_materia(self, materia):
        """Inscribe al estudiante en una materia.

        Args:
            materia: Nombre de la materia que se desea agregar.

        La materia se guarda en un conjunto, por lo que agregarla varias veces
        no crea registros repetidos.
        """
        # add() no duplica: si ya estaba inscrito, no pasa nada
        self.materias.add(materia)

    # Registra una calificación en una materia.
    def agregar_nota(self, materia, nota):
        """Registra una nota y asegura la inscripción en la materia.

        Args:
            materia: Nombre de la materia asociada a la nota.
            nota: Calificación que se agregará a la lista de notas.
        """
        # Primero se asegura de que el estudiante esté inscrito en la materia
        # (reutiliza el método anterior; si ya estaba, no pasa nada).
        self.inscribir_materia(materia)
        # setdefault crea la lista vacía la primera vez que aparece la materia
        # Paso a paso:
        #   1) self.notas.setdefault(materia, []) -> devuelve la lista de esa
        #      materia; si no existía, crea la clave con [] y devuelve esa lista.
        #   2) .append(nota) -> agrega la nota al final de esa lista.
        # Ej: {} -> {"Matemática": [18]} -> {"Matemática": [18, 19]}
        self.notas.setdefault(materia, []).append(nota)

    # Calcula el promedio general juntando las notas de TODAS las materias.
    def obtener_promedio(self):
        """Calcula el promedio de todas las notas del estudiante.

        Returns:
            Promedio de todas las calificaciones redondeado a dos decimales.
            Devuelve `0` si todavía no existen notas registradas.
        """
        # Lista donde se juntarán todas las notas, sin importar la materia.
        # Al final queda una lista plana de números, ej: [18, 19, 17]
        todas = []
        # self.notas.values() recorre solo las LISTAS de notas del diccionario.
        # Si self.notas = {"Matemática": [18, 19], "Inglés": [17]}
        # entonces lista_notas vale [18, 19] y luego [17].
        for lista_notas in self.notas.values():
            # extend() agrega CADA elemento de la lista (no la lista entera,
            # eso haría append). [] -> [18, 19] -> [18, 19, 17]
            todas.extend(lista_notas)
        # Una lista vacía se evalúa como False: si no hay notas, se devuelve 0
        # y así se evita dividir entre cero (len(todas) sería 0).
        if not todas:
            return 0
        # sum() suma todas las notas, len() cuenta cuántas hay; su división es
        # el promedio. round(..., 2) lo redondea a 2 decimales.
        # Devuelve solo el promedio, como indica el docstring.
        return round(sum(todas) / len(todas), 2)

    # Compara este estudiante con otro y devuelve las materias que comparten.
    def materias_en_comun(self, otro_estudiante):
        """Obtiene las materias que comparten dos estudiantes.

        Args:
            otro_estudiante: Segundo estudiante con quien se compararán las
                materias inscritas.

        Returns:
            Conjunto con las materias presentes en ambos estudiantes.
        """
        # INTERSECCIÓN de conjuntos: qué materias comparten dos estudiantes
        # El operador & equivale a self.materias.intersection(otro_estudiante.materias).
        # Ej: {"Física", "Matemática"} & {"Matemática", "Programación"} -> {"Matemática"}
        return self.materias & otro_estudiante.materias

    # Convierte el estudiante en un diccionario listo para guardarse en JSON.
    def a_diccionario(self):
        """Convierte el estudiante a un diccionario compatible con JSON.

        Returns:
            Diccionario con los datos personales, notas y materias. Las
            materias se convierten en una lista ordenada porque JSON no admite
            conjuntos.
        """
        return {
            "id": self.id,              # identificador
            "nombre": self.nombre,      # nombres
            "apellido": self.apellido,  # apellidos
            "email": self.email,        # correo
            "carnet": self.carnet,      # código académico
            "notas": self.notas,        # el diccionario de listas SÍ es compatible con JSON
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            # sorted() recibe el conjunto y devuelve una LISTA en orden alfabético,
            # así el archivo siempre queda igual y es fácil de leer.
            "materias": sorted(self.materias),
        }

    # Constructor alternativo: reconstruye un Estudiante desde un diccionario
    # (por ejemplo, uno leído desde un archivo JSON).
    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un estudiante a partir de un diccionario guardado.

        Args:
            datos: Diccionario con los datos del estudiante. Las notas y
                materias pueden faltar y, en ese caso, se usan valores vacíos.

        Returns:
            Una instancia de `Estudiante` reconstruida desde el diccionario.
        """
        # cls(...) equivale a Estudiante(...).
        return cls(
            # Campos obligatorios: se leen con [] (si faltan, lanza KeyError).
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"],
            # Argumento por NOMBRE (keyword). Si no hay "notas", usa {}.
            notas=datos.get("notas", {}),
            # y al leer lo volvemos a convertir en set
            # En el JSON las materias están como lista; set() las regresa a conjunto.
            materias=set(datos.get("materias", [])),
        )

    # Se ejecuta automáticamente con print(estudiante) o str(estudiante).
    def __str__(self):
        """Devuelve una representación breve y legible del estudiante.

        Returns:
            Texto con el carnet, nombre completo y promedio del estudiante.
        """
        # Ej: "[EST2026001] Ana Pérez - Promedio: 18.0"
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"


if __name__ == "__main__":
    # Pruebas rápidas de la clase Estudiante: solo al correr este archivo directamente
    est1 = Estudiante(1, "Ana", "Pérez", "ana@unemi.edu.ec", "EST2026001")
    est2 = Estudiante(2, "Luis", "Mora", "luis@unemi.edu.ec", "EST2026002")

    print("--- obtener_nombre_completo ---")
    print(est1.obtener_nombre_completo())
    print(est2.obtener_nombre_completo())

    print("\n--- obtener_promedio sin notas (debe ser 0) ---")
    print(est1.obtener_promedio())

    print("\n--- inscribir_materia (Física repetida no debe duplicarse) ---")
    est1.inscribir_materia("Física")
    est1.inscribir_materia("Física")
    print(est1.materias)

    print("\n--- agregar_nota (también inscribe la materia) ---")
    est1.agregar_nota("Matemática", 18)
    est1.agregar_nota("Matemática", 19)
    est1.agregar_nota("Inglés", 17)
    est2.agregar_nota("Matemática", 15)
    est2.agregar_nota("Programación", 20)
    print("est1 notas:", est1.notas, "| materias:", est1.materias)
    print("est2 notas:", est2.notas, "| materias:", est2.materias)

    print("\n--- obtener_promedio ---")
    print("est1:", est1.obtener_promedio())
    print("est2:", est2.obtener_promedio())

    print("\n--- materias_en_comun ---")
    print(est1.materias_en_comun(est2))

    print("\n--- a_diccionario ---")
    datos = est1.a_diccionario()
    print(datos)

    print("\n--- desde_diccionario ---")
    copia = Estudiante.desde_diccionario(datos)
    print(copia)
    print("¿Mismas notas?", copia.notas == est1.notas)
    print("¿Mismas materias?", copia.materias == est1.materias)

    print("\n--- __str__ ---")
    print(est1)
    print(est2)

