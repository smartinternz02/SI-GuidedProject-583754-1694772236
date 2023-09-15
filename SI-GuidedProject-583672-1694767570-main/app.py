from flask import Flask, render_template, request, session
import ibm_db

app=Flask(__name__)
app.secret_key= "mnbcaba"

conn=ibm_db.connect("DATABASE= bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud; PORT=30756;UID=tyk83438;PWD=U7aytFLnscp1gI8H; SECURITY=SSL; SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(ibm_db.active(conn))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print("hi")
        print(uname, pword)
        sql = "SELECT * FROM REGISTER_GITAM WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username'] = uname
            session['emailid'] = out['EMAIL']
            
            if out['ROLE'] == 0:
                return render_template("adminprofile.html",adname = uname, ademail = out['EMAIL'] )
            elif out['ROLE'] == 1:
                return render_template("studentprofile.html",sdname = uname, sdemail = out['EMAIL'])
            else: 
                return render_template("facultyprofile.html",fname = uname, femail = out['EMAIL'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def regsiter():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        uname = request.form['username']
        pword = request.form['password']
        role = request.form['role']
        print(uname,email,pword,role)
        sql = "SELECT * FROM REGISTER_GITAM WHERE USERNAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg = "Already Registered"
            return render_template("register.html",msg = msg)
        else:
            sql = "INSERT INTO REGISTER_GITAM VALUES(?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, uname)     
            ibm_db.bind_param(stmt, 3, pword)
            ibm_db.bind_param(stmt, 4,email)
            ibm_db.bind_param(stmt, 5, role)
            ibm_db.execute(stmt)
            msg = "Registered"
            return render_template("register.html", msg =msg)

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)
