from flask import Flask, render_template, request, redirect
import sqlite3

# Crear la aplicación Flask
app = Flask(__name__)


# ---------------------------------------------------------
# CONEXIÓN CON LA BASE DE DATOS
# ---------------------------------------------------------

def conectar_bd():
    """
    Establece la conexión con la base de datos SQLite.
    También permite acceder a los registros utilizando
    los nombres de las columnas.
    """
    conexion = sqlite3.connect("sgsst.db")
    conexion.row_factory = sqlite3.Row

    return conexion


# ---------------------------------------------------------
# CREACIÓN DE LA TABLA
# ---------------------------------------------------------

def crear_tabla():
    """
    Crea la tabla documentos si todavía no existe.
    """
    conexion = conectar_bd()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            responsable TEXT NOT NULL,
            fecha TEXT NOT NULL,
            version INTEGER NOT NULL,
            descripcion TEXT
        )
    """)

    conexion.commit()
    conexion.close()


# ---------------------------------------------------------
# PÁGINA PRINCIPAL
# ---------------------------------------------------------

@app.route("/")
def inicio():
    """
    Consulta los documentos registrados y los muestra
    en la página principal.
    """

    conexion = conectar_bd()

    # Obtener todos los documentos ordenados
    # desde el más reciente hasta el más antiguo.
    documentos = conexion.execute(
        "SELECT * FROM documentos ORDER BY id DESC"
    ).fetchall()

    conexion.close()

    return render_template(
        "index.html",
        documentos=documentos
    )


# ---------------------------------------------------------
# REGISTRO DE DOCUMENTOS
# ---------------------------------------------------------

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    """
    Permite mostrar el formulario y registrar
    nuevos documentos.
    """

    error = None

    # Comprobar si el formulario fue enviado.
    if request.method == "POST":

        # Obtener los datos enviados por el usuario.
        nombre = request.form["nombre"].strip()
        tipo = request.form["tipo"].strip()
        responsable = request.form["responsable"].strip()
        fecha = request.form["fecha"].strip()
        version = request.form["version"].strip()
        descripcion = request.form["descripcion"].strip()

        # Validar que el nombre haya sido diligenciado.
        if not nombre:
            error = "El nombre del documento es obligatorio."

        # Validar que se haya seleccionado un tipo.
        elif not tipo:
            error = "Debe seleccionar un tipo de documento."

        # Validar el responsable.
        elif not responsable:
            error = "El responsable es obligatorio."

        # Validar la fecha.
        elif not fecha:
            error = "La fecha es obligatoria."

        # Validar que la versión sea un número válido.
        elif not version.isdigit() or int(version) < 1:
            error = "La versión debe ser un número entero mayor o igual a 1."

        # Si no existen errores, guardar el documento.
        if error is None:

            conexion = conectar_bd()

            conexion.execute("""
                INSERT INTO documentos
                (nombre, tipo, responsable, fecha, version, descripcion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nombre,
                tipo,
                responsable,
                fecha,
                int(version),
                descripcion
            ))

            conexion.commit()
            conexion.close()

            # Regresar al listado principal.
            return redirect("/")

    return render_template(
        "registrar.html",
        error=error
    )


# ---------------------------------------------------------
# EDICIÓN DE DOCUMENTOS
# ---------------------------------------------------------

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    """
    Permite consultar y modificar un documento existente.
    """

    conexion = conectar_bd()

    # Buscar el documento mediante su identificador.
    documento = conexion.execute(
        "SELECT * FROM documentos WHERE id = ?",
        (id,)
    ).fetchone()

    # Si el documento no existe, regresar al inicio.
    if documento is None:
        conexion.close()
        return redirect("/")

    error = None

    # Comprobar si se enviaron cambios.
    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        tipo = request.form["tipo"].strip()
        responsable = request.form["responsable"].strip()
        fecha = request.form["fecha"].strip()
        version = request.form["version"].strip()
        descripcion = request.form["descripcion"].strip()

        # Validaciones de los datos.
        if not nombre:
            error = "El nombre del documento es obligatorio."

        elif not tipo:
            error = "Debe seleccionar un tipo de documento."

        elif not responsable:
            error = "El responsable es obligatorio."

        elif not fecha:
            error = "La fecha es obligatoria."

        elif not version.isdigit() or int(version) < 1:
            error = "La versión debe ser un número entero mayor o igual a 1."

        # Actualizar el documento si los datos son válidos.
        if error is None:

            conexion.execute("""
                UPDATE documentos
                SET nombre = ?,
                    tipo = ?,
                    responsable = ?,
                    fecha = ?,
                    version = ?,
                    descripcion = ?
                WHERE id = ?
            """, (
                nombre,
                tipo,
                responsable,
                fecha,
                int(version),
                descripcion,
                id
            ))

            conexion.commit()
            conexion.close()

            return redirect("/")

    conexion.close()

    return render_template(
        "editar.html",
        documento=documento,
        error=error
    )


# ---------------------------------------------------------
# ELIMINACIÓN DE DOCUMENTOS
# ---------------------------------------------------------

@app.route("/eliminar/<int:id>")
def eliminar(id):
    """
    Elimina un documento de la base de datos
    utilizando su identificador.
    """

    conexion = conectar_bd()

    conexion.execute(
        "DELETE FROM documentos WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    # Regresar al listado después de eliminar.
    return redirect("/")


# ---------------------------------------------------------
# EJECUCIÓN DE LA APLICACIÓN
# ---------------------------------------------------------

if __name__ == "__main__":

    # Crear la tabla al iniciar la aplicación.
    crear_tabla()

    # Ejecutar el servidor Flask.
    app.run(debug=True)