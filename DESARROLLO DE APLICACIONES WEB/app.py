from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Crear la base de datos y las tablas (solo se ejecuta una vez)
with app.app_context():
    db.create_all()

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para guardar datos en la base de datos
@app.route('/guardar_db', methods=['POST'])
def guardar_db():
    nombre = request.form['nombre']
    email = request.form['email']
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para leer datos desde la base de datos
@app.route('/leer_db')
def leer_db():
    usuarios = Usuario.query.all()
    return render_template('resultado.html', datos=usuarios)

# Ruta para eliminar un usuario por ID
@app.route('/eliminar_db/<int:id>')
def eliminar_db(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('leer_db'))

if __name__ == '__main__':
    app.run(debug=True)