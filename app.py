from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import Usuario
from models.modelsp import Producto
from flask import Flask, render_template, request, redirect, url_for, flash, session,  jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from Conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_seguro'  # Necesario para formularios con CSRF

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Definir la clase de formulario
class NombreForm(FlaskForm):
    nombre = StringField('Ingresa tu nombre', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Enviar')

# Ruta principal (Página de inicio)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        session['nombre'] = form.nombre.data  # Guardar en sesión
        flash('Formulario enviado con éxito!', 'success')
        return redirect(url_for('resultado'))
    return render_template('formulario.html', form=form)

# Ruta para mostrar el resultado
@app.route('/resultado')
def resultado():
    nombre = session.get('nombre', None)  # Obtener de sesión

    if nombre is None:  # Evita errores si no se ha llenado el formulario
        flash('No hay datos en la sesión. Ingresa tu nombre en el formulario.', 'warning')
        return redirect(url_for('formulario'))

    return render_template('resultado.html', nombre=nombre)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test_db')
def test_db():
    conexion = obtener_conexion()
    if conexion:
        return "Conexión exitosa a MySQL"
    else:
        return "Error en la conexión a MySQL"

# Ruta para mostrar los usuarios en una tabla HTML
@app.route('/agregar_producto', methods=['GET'])
def usuarios_tabla():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Para obtener los resultados en formato de diccionario
        cursor.execute("SELECT * FROM cafelocal.producto")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('agregar_producto.html', usuarios=usuarios)
    else:
        return "Error en la conexión a la base de datos", 500


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Lógica para registrar usuario
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        if nombre and precio and stock:
            Producto.insertar(nombre, float(precio), int(stock))
            flash('Producto creado exitosamente.')
            return redirect(url_for('listar_productos'))
        else:
            flash('Todos los campos son obligatorios.')
    return render_template('crear_productos.html')
@app.route('/productos')
def listar_productos():
    productos = Producto.obtener_todos()
    return render_template('productos.html', productos=productos)

@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    producto = Producto.obtener_por_id(id_producto)
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        Producto.actualizar(id_producto, nombre, float(precio), int(stock))
        flash('Producto actualizado correctamente.')
        return redirect(url_for('listar_productos'))
    return render_template('editar_productos.html', producto=producto)

@app.route('/eliminar/<int:id_producto>', methods=['GET', 'POST'])
def eliminar_producto(id_producto):
    if request.method == 'POST':
        Producto.eliminar(id_producto)
        flash('Producto eliminado correctamente.')
        return redirect(url_for('listar_productos'))
    producto = Producto.obtener_por_id(id_producto)
    return render_template('eliminar_productos.html', producto=producto)


# Ruta para procesar el formulario y agregar producto
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    # Aquí puedes agregar la lógica para almacenar el producto en la base de datos
    # Por ahora, solo redirige a la página de éxito
    return redirect(url_for('producto_exito'))

# Ruta para mostrar la página de éxito
@app.route('/producto_exito')
def producto_exito():
    return render_template('producto_exito.html')

# Ruta de inicio
@app.route('/')
def inicio():
    return "Bienvenido a la página principal"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Simulación de autenticación
        if email == "admin@example.com" and password == "admin":
            return redirect("http://eddie2707.great-site.net/")  # Redirige a tu web
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template('login.html')



@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)