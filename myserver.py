import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://jr3990:293875@34.73.36.248/project1"

engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None


@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():
   return render_template("index.html")

@app.route('/hotelinfo', methods = ['POST'])
def hotelinfo():    
  if request.method == 'POST':
    city = request.form["city"]
    result = g.conn.execute("SELECT * FROM hotel WHERE city_name = %s",city)
    tour = g.conn.execute("SELECT name, price FROM touristattraction WHERE city_name = %s",city)
    trans = g.conn.execute("SELECT K.destination, K.destprice, K.start,K.startprice, T.type,T.price FROM (SELECT A.id as destid, A.name as destination, A.price as destprice,B.id as startid,B.name as start,B.price as startprice FROM touristattraction A CROSS JOIN touristattraction B) K JOIN transportation T ON (T.to_ID=K.destid AND T.from_ID=K.startid)")  
    data= []
    data2 = []
    data3 = []

    for row in result:
      data.append(row)
    for row in tour:
      data2.append(row)
    for row in trans:
      data3.append(row)

    context = dict(data = data)
    context2 = dict(data2= data2)
    context3 = dict(data3= data3)    
    return render_template("hotelinfo.html", **context, **context2,**context3)

@app.route('/book', methods = ['POST']) 
def book():
  if request.method == 'POST':
     hotel = request.form["hotel"]
     result = g.conn.execute("SELECT room_number, size, price_per_night FROM room WHERE hotel_id = %s",hotel)
     booked = g.conn.execute("SELECT room_number, check_in_date,check_out_date FROM room NATURAL JOIN booking WHERE hotel_id = %s",hotel)
     data = []
     data2 = []
     for row in result:
       data.append(row)
     for row in booked:
       data2.append(row)
     context = dict(data = data)
     context2 = dict(data2=data2)
     return render_template("book.html", **context,**context2)

@app.route('/login')
def login():
  return render_template("login.html")
 
@app.route('/pastbooking', methods = ['POST'])
def pastbooking():
  if request.method == 'POST':
    id = request.form["id"]
 
    result = g.conn.execute("""SELECT city_name, hotel.name, room_number, check_in_date, check_out_date
    FROM (booking NATURAL JOIN room) K JOIN hotel USING (hotel_id) 
    WHERE cust_id = %s""", id)

    rec = g.conn.execute("""SELECT name, city_name, number_of_stars
    FROM hotel
    WHERE number_of_stars IN
    (SELECT DISTINCT(number_of_stars)
    FROM (booking NATURAL JOIN room) JOIN hotel USING (hotel_id)
    WHERE cust_id = %s)""",id)

    data = []
    data2 = []
    for row in result:
      data.append(row)
    for row in rec:
      data2.append(row)
    context = dict(data = data)
    context1 = dict(data2= data2)

    return render_template("pastbooking.html",**context,**context1) 

    
@app.route('/register')
def register():
  return render_template("register.html")


@app.route('/add', methods=['POST'])
def add():
  id = request.form['id']
  yob = request.form['year_of_birth']
  name = request.form['name']
  email = request.form['email']
  gender = request.form['gender']
  g.conn.execute('INSERT INTO customer VALUES (%s,%s,%s,%s,%s)',id,yob,name,email,gender)
  return render_template("login.html")

@app.route('/addbooking', methods=['POST'])
def addbooking():
  room = request.form['room']
  checkin = request.form['check-in']
  checkout = request.form['check-out']
  id = request.form['id']
  g.conn.execute('INSERT INTO booking VALUES (%d,%d-%m-%Y,%d-%m-%Y,%s)',room,checkin,checkout,id)
  g.conn.execute('INSERT INTO timeslot VALUEUS (%d-%m-%Y,%d-%m-%Y)',checkin,checkout)
  return "Booking Complete"

@app.route('/addcompanion', methods=['POST'])
def addcompanion():
  id = request.form['id']
  relation = request.form['relation']
  yob = request.form['yob']
  name = request.form['name']
  gender = request.form['gender']
  cust_id = request.form['cust_id']
  g.conn.execute('INSERT INTO travelcompanion VALUES (%d,%s,%d,%s,%s,%s)',id,relation,yob,name,gender,cust_id)
  return "Added to Guest List"

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
