from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<Insert Password Here>
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
@app.route('/add-patient', methods=['GET', 'POST'])#Added
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
@app.route('/emergency-contact', methods=['GET', 'POST'])#Added
def getEmergencyContact():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("SELECT contact_name, Phone_number, Relationship From emergency_contact where  patient_id = %s", [ID])
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('emergencyContact.html')

#Works
@app.route('/admittance-date', methods=['GET', 'POST'])#Added
def admitDate():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("select Date_admitted from patient where  patient_id = %s", [ID])
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('admitDate.html')

#Works
@app.route('/patient-info', methods=['GET', 'POST'])#Added
def patientInfo():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("SELECT s.Name, t.Diagnosis, t.prescribed_treatment From treats t, patient p, staff s where  p.Patient_id = %s AND p.Patient_id = t.Patient_id AND t.Doctor_id = s.Employee_id;", [ID])
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('getInfo.html')

#Works
@app.route('/delete-patient', methods=['GET', 'POST'])#Added
def deletePatient():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("DELETE FROM `cis421`.`emergency_contact` WHERE Patient_id = %s;", [ID])
        cur.execute("DELETE FROM `cis421`.`treats` WHERE Patient_id = %s;", [ID])
        cur.execute("DELETE FROM `cis421`.`patient` WHERE Patient_id = %s;", [ID])
    
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return 'Patient Deleted'
    return render_template('deletePatient.html')


#Works
@app.route('/ventilator-use', methods=['GET', 'POST'])#Added
def getVents():
    if request.method == "POST":

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("Select patient_id, Name, Room_number from patient where On_ventilator=\"y\"")
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('getVents.html')

#works
@app.route('/update-ventilator', methods=['GET', 'POST'])#Added
def updateVent():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']
        vent = details['vent']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("UPDATE patient SET On_ventilator = %s WHERE Patient_id = %s;", (vent, ID))
        
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return 'Status Updated'
    return render_template('updateVent.html')

#Works
@app.route('/update-room-number', methods=['GET', 'POST'])#Added
def updateRoomNum():
    if request.method == "POST":
        details = request.form

        #Save Values to Variables
        ID = details['ID']
        roomNum = details['roomNum']

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("UPDATE patient SET Room_number = %s WHERE Patient_id = %s;", (roomNum, ID))
        
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return 'Room Number Updated'
    return render_template('updateRoom.html')

#Works
@app.route('/covid-patients', methods=['GET', 'POST'])#added
def getCovid():
    if request.method == "POST":

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("select p.Name, p.Patient_id from patient p, treats t where t.Diagnosis = \"Covid-19\" and p.Patient_id = t.Patient_id")
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('getCovid.html')

#Works
@app.route('/assigned-nurses', methods=['GET', 'POST'])
def currNurses():
    if request.method == "POST":

        #Connect to DB
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("select distinct s.Name from staff s, nurse n, assigned_to a where n.Nurse_id = a.Nurse_id And s.Employee_id = n.Nurse_id")
        
        data = cur.fetchall()
        #Commit Query through connection
        mysql.connection.commit()
        
        #Close DB Connection
        cur.close()
        return str(data)
    return render_template('currNurses.html')


#Startup
if __name__ == '__main__':
    app.run()