# Comandi per installare le librerie
## pip install flask
## pip install flask_sqlalchemy
## pip install mysql-connector

# Come avviare il programma
## python .\flask_app.py

# Ricorda
## Hai bisogno di un db pronto più un user gia completato

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["DEBUG"] = True

# stringa di connessione con il database
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="admin",
    password="admin1",
    hostname="%localhost",
    databasename="ambientali",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# inizializzazione database
db = SQLAlchemy(app)

# data model
class Sensor(db.Model):

    __tablename__ = "sensors"

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)

# route per la webapp
@app.route("/")
def index():
    return "Eccoti! Sono ruscito a collegarmi a MySQL. Ora puoi usare i comandi 'creadb', 'importa' e 'visualizza'"

@app.route("/visualizza", methods=["GET", "POST"])
def visualizza():
    if request.method == "GET":
        return render_template("main_page.html", sensors=Sensor.query.all())

    sensor = Sensor(temperature=request.form["temperature"], humidity=request.form["humidity"], pressure=request.form["pressure"] )
    db.session.add(sensor)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/importa")
def importazione():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(THIS_FOLDER, 'sensors-data.csv')
    myfile = open(filename,'r')
    for linea in myfile.read().splitlines():
        campi=linea.split(';')
        sensor = Sensor(temperature=campi[0],humidity=campi[1],pressure=campi[2])
        db.session.add(sensor)
        db.session.commit()
    myfile.close()
    return "Dati importati"

@app.route("/creadb")
def creadb():
    db.create_all()
    return "Database creato"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
