from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


#Mysql conexion
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'P4empleados'
mysql = MySQL(app)

# configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados')
    data = cur.fetchall()
    return render_template('index.html', empleados = data)

@app.route('/add_empleado', methods=['POST'])
def add_empleado():
  if request.method == 'POST':
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cedula = request.form['cedula']
    cargo = request.form['cargo']
    telefono = request.form['telefono']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO empleados (Nombre, Apellido, Cedula, Cargo, Telefono) VALUES (%s, %s, %s, %s, %s)',
    (nombre, apellido, cedula, cargo, telefono))
    mysql.connection.commit()
    flash('Empleado agrado')
    return redirect(url_for('Index'))
    

@app.route('/edit/<dni>')
def get_empleado(dni):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empleados WHERE dni = %s', (dni))
    data = cur.fetchall()
    return render_template('editar.html', emple = data[0])

@app.route('/update/<dni>', methods = ['POST'])
def update_empleado(dni):
    if request.method == 'POST':
      nombre = request.form['nombre']
      apellido = request.form['apellido']  
      cedula = request.form['cedula']  
      cargo= request.form['cargo']  
      telefono = request.form['telefono']  
      cur = mysql.connection.cursor()
      cur.execute("""
        UPDATE empleados
            SET nombre = %s,
                apellido = %s,
                cedula = %s,
                cargo = %s,
                telefono = %s
        WHERE dni = %s
      """, (nombre, apellido, cedula, cargo, telefono, dni))
      mysql.connection.commit()
      flash('empleado actualizado')
      return redirect(url_for('Index'))


@app.route('/delete/<string:dni>')
def delete_empleado(dni):
 cur = mysql.connection.cursor()
 cur.execute('DELETE FROM empleados WHERE DNI = {0}'.format(dni))
 mysql.connection.commit()
 flash('empleado eliminado')
 return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)