import sqlite3

conn = sqlite3.connect("almacen.db")
cursor = conn.cursor()

# Crear tabla de productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)
""")

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para la página principal (leer productos)
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM producto").fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para crear un nuevo producto
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conn = get_db_connection()
        conn.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)",
                     (descripcion, cantidad, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# Ruta para editar un producto
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    producto = conn.execute("SELECT * FROM producto WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conn.execute("UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?",
                     (descripcion, cantidad, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM producto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
