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


@app.route("/")
def loginPage():
    # if "username" in session:
    #     return redirect(url)
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
