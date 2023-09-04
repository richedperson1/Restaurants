from flask import *
import mysql.connector as con
from datetime import datetime

todayDate = str(datetime.now().date())

app = Flask(__name__, template_folder='template', static_folder='static')

# Adding secrete key 
app.secret_key = "asjdkhfjaksnd1265484asdf"

mycon = con.connect(host='localhost', passwd='ru15070610',
                    user='root', database="resto")
query = "select * from dishes"
cur = mycon.cursor()
cur.execute(query)
final = cur.fetchall()

price_dish = []
for item in final:
    price_dish.append([item[1], int(item[-1])])


"""
This function renders the login page if the user is not already logged in.
:return: The function `loginPage()` returns the rendered HTML template "index.html".
"""

@app.route("/")
def loginPage():
    if "username" in session:
        return redirect(url_for("home_page"))
    return render_template("index.html")


"""
This function authenticates user login credentials by checking if the email and password match with
the ones stored in the database, and redirects the user to the home page if successful or the login
page if unsuccessful.

:return: If the verification is successful, the function will redirect to the home page. If the
verification fails, the function will redirect to the login page. If the request method is not POST,
the function will render the index.html template.

"""
@app.route("/autho", methods=["post"])
def autho():
    if request.method == "POST":

        email = request.form["EmailName"]
        password = request.form["PasswordName"]
        session["username"] = email
        cur = mycon.cursor()
        query = f"select * from customers where (userName='{email}' or email ='{email}') and user_password = '{password}'"
        cur.execute(query)
        finalUsers = cur.fetchall()

        if len(finalUsers)>=1:
            print("---"*5+">","Verification Sucess")
            return redirect(url_for("home_page"))
        
        print("---"*5+">","Verification failed")
        return redirect(url_for("loginPage"))
    return render_template("index.html")


"""
This function renders the home page of a restaurant website and displays a list of dishes from a
database if the user is logged in, otherwise it redirects to the login page.

:return: If the "username" key is present in the session, the function returns a rendered template
"api_templates.html" with the data fetched from the "dishes" table in the "resto" database. If the
"username" key is not present in the session, the function returns the response from the "loginPage"
function.

"""

@app.route("/HomePage", methods=["post", "get"])
def home_page():

    if "username" in session:
        mycon = con.connect(host='localhost', passwd='ru15070610',
                            user='root', database="resto")

        query = "select * from dishes"
        cur = mycon.cursor()
        cur.execute(query)
        final = cur.fetchall()
        return render_template("api_templates.html", dishes=final)
    loginPageResponse =  loginPage()
    return loginPageResponse


"""
This function logs out a user by removing their username from the session and redirects them to the
home page.

:return: a redirect to the home page using the `redirect` function from Flask and the `url_for`
function to generate the URL for the home page.

"""
@app.route("/logOut",methods = ["post","get"])
def logOutUser():
    session.pop("username")
    print(session)
    return redirect(url_for("home_page"))


@app.route("/totalValue", methods=["post"])
def totalValue():
    if request.method == "POST":
        print(request.form)
        item1 = request.form.get("items1")
        item2 = request.form.get("items2")
        item3 = request.form.get("items3")
        item4 = request.form.get("items4")
        item5 = request.form.get("items5")
        all_items = [item1, item2, item3, item4, item5]

        total_bills = 0
        for quantity, dish_details in zip(all_items, price_dish):
            item_name = dish_details[0]

            try:
                queryWant = f"insert into bills (item_name, quantity,price,total_price) values('{item_name}',{quantity},{dish_details[1]},{int(dish_details[1])*int(quantity)})"
                total_bills += int(dish_details[1])*int(quantity)
                cur = mycon.cursor()
                cur.execute(queryWant)
                mycon.commit()

            except:
                print("Not founds")

        billQuery = f"insert into Orders (order_date, total_amount) values  ('{todayDate}','{total_bills}')"
        cur = mycon.cursor()
        cur.execute(billQuery)
        mycon.commit()
        return render_template("orderFood.html")
    return "Hello"


@app.route("/fileCheck", methods=["post"])
def testingPost():
    if request.method == "POST":

        dataFileName = request.files.get("fileName")
        
        return "File name is "+ str(dataFileName)
    return "Not found"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
