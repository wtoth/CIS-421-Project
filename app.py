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

#Works
@app.route('/emergency-contact', methods=['GET', 'POST'])
def getEmergencyContact():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("SELECT contact_name, Phone_number, Relationship From emergency_contact where  patient_id = %s", (ID))
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('emergencyContact.html')

#Works
@app.route('/admittance-date', methods=['GET', 'POST'])
def admitDate():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("select Date_admitted from patient where  patient_id = %s", (ID))
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('admitDate.html')

#Works
@app.route('/patient-info', methods=['GET', 'POST'])
def patientInfo():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("SELECT s.Name, t.Diagnosis, t.prescribed_treatment From treats t, patient p, staff s where  p.Patient_id = %s AND p.Patient_id = t.Patient_id AND t.Doctor_id = s.Employee_id;", (ID))
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('getInfo.html')


@app.route('/delete-patient', methods=['GET', 'POST'])
def deletePatient():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("DELETE FROM `cis421`.`emergency_contact` WHERE Patient_id = %s;", (ID))
        cur.execute("DELETE FROM `cis421`.`treats` WHERE Patient_id = %s;", (ID))
        cur.execute("DELETE FROM `cis421`.`patient` WHERE Patient_id = %s;", (ID))
    
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return 'Patient Deleted'
    return render_template('deletePatient.html')

if __name__ == '__main__':
    app.run()