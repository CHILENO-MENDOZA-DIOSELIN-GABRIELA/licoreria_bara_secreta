from flask import Flask, render_template, request, redirect, url_for, flash
from config import get_connection

app = Flask(__name__)
app.secret_key = "licoreria_bara_secreta"

# ------------------ RUTAS PRINCIPALES ------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ------------------ CRUD PRODUCTOS ------------------

@app.route("/productos")
def productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)

@app.route("/agregar_producto", methods=["POST"])
def agregar_producto():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                   (nombre, precio, stock))
    conn.commit()
    conn.close()

    flash("Producto agregado con éxito")
    return redirect(url_for("productos"))

@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id=%s",
                       (nombre, precio, stock, id))
        conn.commit()
        conn.close()
        flash("Producto actualizado correctamente")
        return redirect(url_for("productos"))

    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar_producto/<int:id>")
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash("Producto eliminado")
    return redirect(url_for("productos"))

# ------------------ CRUD CLIENTES ------------------

@app.route("/clientes")
def clientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes)

@app.route("/agregar_cliente", methods=["POST"])
def agregar_cliente():
    nombre = request.form["nombre"]
    correo = request.form["correo"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, correo) VALUES (%s, %s)", (nombre, correo))
    conn.commit()
    conn.close()

    flash("Cliente agregado con éxito")
    return redirect(url_for("clientes"))

@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]

        cursor.execute("UPDATE clientes SET nombre=%s, correo=%s WHERE id=%s",
                       (nombre, correo, id))
        conn.commit()
        conn.close()
        flash("Cliente actualizado correctamente")
        return redirect(url_for("clientes"))

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/eliminar_cliente/<int:id>")
def eliminar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash("Cliente eliminado")
    return redirect(url_for("clientes"))

# ------------------ INVENTARIO ------------------

@app.route("/inventario")
def inventario():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    inventario = cursor.fetchall()
    conn.close()
    return render_template("inventario.html", inventario=inventario)

# ------------------ MAIN ------------------

if __name__ == "__main__":
    app.run(debug=True)
