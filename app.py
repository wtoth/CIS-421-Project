from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '**'
app.config['MYSQL_DB'] = 'cis421'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


#Works
@app.route('/add-patient', methods=['GET', 'POST'])
def addPatient():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        Name = details['name']
        patID = details['id']
        dateAdmitted = details['date']
        onVent = details['onVent']
        roomNum = details['RoomNumber']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("INSERT INTO Patient(Patient_id, Name, Date_admitted, On_ventilator, Room_number) VALUES (%s, %s, %s, %s, %s)", (patID, Name, dateAdmitted, onVent, roomNum))
        
        #Commit Query through connection
        mysql.connection.commit()

        #Close DB Connection
        cur.close()
        return 'success'
    return render_template('addPatient.html')

if __name__ == '__main__':
    app.run()