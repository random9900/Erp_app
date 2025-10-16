from flask import Flask, flash,render_template,request,redirect, session,url_for
from flask_mysqldb import MySQL


app = Flask(__name__)


app.secret_key = 'kuchbhi'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employee_db'

mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/contact')
def contact():
  return render_template('contact.html')

# admin end points

@app.route('/admin')
def admin():
  return render_template('admin_login.html')

@app.route('/admin_dashboard',methods=['post'])
def admin_dashboard():
  un = request.form.get('un')
  pw = request.form.get('pw')

  if(un == 'admin' and pw == 'root'):
   session["name"] = "Admin"  # session variable created
   return render_template('admin_dashboard.html')
  else:
    msg = "invalid username or password !"
    return render_template('admin_login.html',msg=msg)
  

@app.route('/admin_addemp')
def admin_add_emp():
  return render_template('admin_add_emp.html')

# -----> Select

@app.route('/admin_showemp')
def admin_show_emp():
  cur = mysql.connection.cursor()
  cur.execute('select emp_id,emp_name,emp_email,phone,designation,salary,gender from registration')
  record = cur.fetchall()
  cur.close()
  return render_template('admin_show_emp.html',record = record)




# ----> search

@app.route('/admin_searchemp')
def admin_search_emp():
  return render_template('admin_search_emp.html')



@app.route('/admin_search_process',methods=['post'])
def admin_search_process():

  name = request.form['txtname']
  cur = mysql.connection.cursor()
  q = "select * from registration where emp_name like '" +name+ "%'"
  print(q)
  cur.execute(q)
  data = cur.fetchall()
  cur.close()
  return render_template('admin_search_process.html',data = data)
# -----> Insert

@app.route('/save',methods=['post'])
def save():
  id = request.form['empid']
  name = request.form['empname']
  email = request.form['empemail']
  phone = request.form['empphone']
  designation = request.form['empdesignation']
  salary = request.form['empsalary']
  gender = request.form['empgender']

# Database Connection Open
  cur = mysql.connection.cursor()

#Query specification
  cur.execute('insert into registration(emp_id,emp_name,emp_email,phone,designation,salary,gender) values(%s,%s,%s,%s,%s,%s,%s)',(id,name,email,phone,designation,salary,gender))

# transaction save/commit
  mysql.connection.commit()

  # Database connection close
  cur.close()

  return render_template('admin_emp_reg_success.html')

# ------>  select

@app.route('/admin_emp_profile')
def admin_emp_list():
  id= request.args.get('EmpId')
 

  cur = mysql.connection.cursor()
  cur.execute('select * from registration where emp_id='+id)
  
  data = cur.fetchall()
  cur.close()
  return render_template('admin_emp_profile.html', data = data)

#------> Update

@app.route('/admin_emp_update',methods=['post'])
def admin_emp_update():
  id = request.form['empid']
  name = request.form['empname']
  email = request.form['empemail']
  phone = request.form['empphone']
  designation = request.form['empdesignation']
  salary = request.form['empsalary']
  gender = request.form['empgender']

  cur = mysql.connection.cursor()
  cur.execute('update registration set emp_id=%s,emp_name=%s,emp_email=%s,phone=%s,designation =%s,salary=%s,gender=%s where emp_id=%s',(id,name,email,phone,designation,salary,gender,id))
  # cur.execute('update registration set designation=%s where emp_id=%s',(designation,id,))
  mysql.connection.commit()
  cur.close()
  return render_template('admin_emp_update_success.html')

# -----> delete
@app.route('/admin_delete_emp')
def delete_employee():
  id = request.args['id']

  cur = mysql.connection.cursor()
  cur.execute('delete from registration where emp_id=%s',(id,))
  mysql.connection.commit()
  cur.close()
  return render_template('admin_delete_emp.html')
  # flash('Employee deleted successfully!', 'success')
  return redirect(url_for('admin_show_emp'))


@app.route('/logout')
def logout():
  session["name"]="none"
  return render_template('admin_login.html')

app.run(debug=True) 