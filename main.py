from flask import Flask, render_template, jsonify, request, flash
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
#import os
#import pandas as pd


app = Flask(__name__)

cors = CORS(app)

app.config['SECRET_KEY'] = 'my super key xd'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lia_alessia'

mysql = MySQL(app)

#create a Form Class
class ContactForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    phone = StringField("Teléfono", validators=[DataRequired()])
    msg = TextAreaField("Dejanos tu mensaje", validators=[DataRequired()])
    submit = SubmitField("ENVIAR")

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/cuero') #GET
def showLeatherProducts():

    sql = "SELECT codigo,precio FROM modelo WHERE material in ('cuero','gamuza');"
    cur = mysql.connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()

    prodsCuero = []
    for row in result:
        codigo = row[0]
        precio = row[1]
        #urlImagen = "../static/imagenes/Zapatillas-41.png"
        productoCuero = {'codigo': codigo,
                   'precio': precio
                   #'urlImagen': urlImagen
                   }
        prodsCuero.append(productoCuero)

    return render_template('productos-cuero.html',productosCuero=prodsCuero)

@app.route('/sintetico')
def showSyntheticProducts():

    sql = "SELECT codigo,precio FROM modelo WHERE material not in ('cuero','gamuza');"
    cur = mysql.connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()

    prodsSintetico = []
    for row in result:
        codigo = row[0]
        precio = row[1]
        #urlImagen = "../static/imagenes/Zapatillas-41.png"
        productoSintetico = {'codigo': codigo,
                   'precio': precio
                   #'urlImagen': urlImagen
                   }
        prodsSintetico.append(productoSintetico)

    return render_template('productos-sintetico.html',productosSintetico=prodsSintetico)

@app.route('/contacto', methods=['GET','POST'])
def contact():
    name = None
    email = None
    phone = None
    msg = None
    form = ContactForm()

    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        msg = form.msg.data
        form.name.data = ''
        form.email.data = ''
        form.phone.data = ''
        form.msg.data = ''

        flash("Formulario enviado correctamente.")

    return render_template('contacto.html', name=name, email=email, phone=phone, msg=msg, form=form)

@app.route('/sobre-nosotros')
def aboutUs():
    return render_template('sobreNosotros.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)