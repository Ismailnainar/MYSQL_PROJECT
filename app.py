from flask import Flask,render_template,url_for,redirect,request,session
from flask_mysqldb import MySQL

app=Flask(__name__)
app.secret_key = "Mohamed@124"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='Ismail@1529'
app.config['MYSQL_DB'] ='student_details'

mysql = MySQL(app)


@app.route('/',methods=["GET","POST"])
def signup():
    if request.method == "POST":
      Name=request.form.get("Name")
      Password=request.form.get("Password")
      cur=mysql.connection.cursor()
      cur.execute("INSERT INTO signup (Name,Password) VALUES (%s,%s)",(Name,Password))
      cur.connection.commit()
      cur.close()
      return redirect(url_for("login"))
    return render_template ("Signup.html") 
@app.route('/login',methods=["GET","POST"])
def login():
   if request.method == "POST":
      Name=request.form.get("Name")
      Password=request.form.get("Password")
      cur=mysql.connection.cursor()
      cur.execute("SELECT * FROM signup WHERE Name=%s AND Password=%s", (Name,Password))
      data=cur.fetchone()
      cur.close()
      if data:
         session["Name"]=Name
         return redirect(url_for("tabel"))
        #  return "login succesfully"
      else:
         return "invalid login password"

   return render_template ("login.html")

@app.route('/tabel',)
def tabel():
   cur = mysql.connection.cursor()
   cur.execute("SELECT * FROM student_values")
   data = cur.fetchall()
   cur.close()
   return render_template("table.html",values=data)

@app.route('/ADD',methods=["GET","POST"])
def ADD():
    if request.method == "POST":
      Name= request.form.get("Name")
      Phone_Number=request.form.get("Phone_Number")
      Depatment=request.form.get("Depatment")
      Email=request.form.get("Email")
      cur = mysql.connection.cursor()
      cur.execute("insert into student_values (Name,Phone_Number,Depatment,Email) values(%s,%s,%s,%s)",(Name,Phone_Number,Depatment,Email))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for("tabel"))
    return render_template("add.html")
@app.route('/Edit/<string:S1no>',methods=["GET","POST"])
def Edit(S1no):
    if request.method == "POST":
      Name= request.form.get("Name")
      Phone_Number=request.form.get("Phone_Number")
      Depatment=request.form.get("Depatment")
      Email=request.form.get("Email")
      cur = mysql.connection.cursor()
      cur.execute("UPDATE student_values SET Name=%s, Phone_number=%s, Depatment=%s, Email=%s WHERE S1no=%s", (Name,Phone_Number,Depatment,Email,S1no))
      cur.connection.commit()
      cur.close()
      return redirect(url_for("tabel"))
    cur=mysql.connection.cursor()
    cur.execute("select * from student_values where S1no=%s",(S1no,))
    data=cur.fetchone()
    cur.close()
    return render_template("edit.html",data=data)
@app.route('/Delete/<string:S1no>',methods=["GET","POST"])
def Delete(S1no):
   cur = mysql.connection.cursor()
   cur.execute("DELETE FROM student_values WHERE S1no=%s",(S1no,))
   cur.connection.commit()
   cur.close()
   return redirect(url_for("tabel"))

@app.route('/')
def logout():
   session.pop("Name",None)
   return redirect("signup")


if __name__ == "__main__":
  app.run(debug=True)

