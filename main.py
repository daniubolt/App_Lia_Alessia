from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
#import os
#import pandas as pd


app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lia_alessia'

mysql = MySQL(app)

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

    #prodsCuero = []
    #for row in result:
        #prodsCuero.append(row[0])

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

    #prodsSintetico = []
    #for row in result:
        #prodsSintetico.append(row[0])
    return render_template('productos-sintetico.html',productosSintetico=prodsSintetico)

@app.route('/contacto')
def contact():
    return render_template('contacto.html')

@app.route('/sobre-nosotros')
def aboutUs():
    return render_template('sobreNosotros.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)