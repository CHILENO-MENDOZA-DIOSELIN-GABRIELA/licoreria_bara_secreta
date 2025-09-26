from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "licoreria_bara_secreta"


# ------------------ DECORADOR LOGIN REQUIRED ------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ------------------ REGISTRO ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                           (nombre, email, hashed_pw))
            conn.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("El correo ya está registrado o hubo un error.", "danger")
        finally:
            conn.close()

    return render_template("register.html")


# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["nombre"]
            flash(f"Bienvenido {user['nombre']} 🍷", "success")
            return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template("login.html")


# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


# ------------------ RUTAS PRINCIPALES ------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ------------------ CRUD PRODUCTOS ------------------
@app.route("/productos")
@login_required
def productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)


@app.route("/agregar_producto", methods=["POST"])
@login_required
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

    flash("Producto agregado con éxito", "success")
    return redirect(url_for("productos"))


@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
@login_required
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
        flash("Producto actualizado correctamente", "success")
        return redirect(url_for("productos"))

    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("editar_producto.html", producto=producto)


@app.route("/eliminar_producto/<int:id>")
@login_required
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash("Producto eliminado", "info")
    return redirect(url_for("productos"))


# ------------------ CRUD CLIENTES ------------------
@app.route("/clientes")
@login_required
def clientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes)


@app.route("/agregar_cliente", methods=["POST"])
@login_required
def agregar_cliente():
    nombre = request.form["nombre"]
    correo = request.form["correo"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, correo) VALUES (%s, %s)", (nombre, correo))
    conn.commit()
    conn.close()

    flash("Cliente agregado con éxito", "success")
    return redirect(url_for("clientes"))


@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
@login_required
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
        flash("Cliente actualizado correctamente", "success")
        return redirect(url_for("clientes"))

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/eliminar_cliente/<int:id>")
@login_required
def eliminar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash("Cliente eliminado", "info")
    return redirect(url_for("clientes"))


# ------------------ INVENTARIO ------------------
@app.route("/inventario")
@login_required
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
