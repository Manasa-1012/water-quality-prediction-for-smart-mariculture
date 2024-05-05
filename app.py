from flask import Flask, render_template, request, flash, redirect
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
import pickle
rfc=pickle.load(open("rf.pkl","rb"))
    
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            import requests
            data=requests.get("https://api.thingspeak.com/channels/2509022/feeds.json?api_key=OLI8QCB5L2W37LKB&results=2")
            temp=data.json()['feeds'][-1]['field1']
            con=data.json()['feeds'][-1]['field3']
            ph=data.json()['feeds'][-1]['field4']
            tur=data.json()['feeds'][-1]['field5']
            return render_template('fetal.html',temp=temp,con=con,ph=ph,tur=tur)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route("/fetalPage", methods=['GET', 'POST'])
def fetalPage():
    import requests
    data=requests.get("https://api.thingspeak.com/channels/2509022/feeds.json?api_key=OLI8QCB5L2W37LKB&results=2")
    temp=data.json()['feeds'][-1]['field1']
    con=data.json()['feeds'][-1]['field3']
    ph=data.json()['feeds'][-1]['field4']
    tur=data.json()['feeds'][-1]['field5']
    return render_template('fetal.html',temp=temp,con=con,ph=ph,tur=tur)




@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        name = request.form['a_id']
        Conductivity = request.form['Conductivity']
        Turbidity = request.form['Turbidity']
        Temperature = request.form['Temperature']
        Ph = request.form['Ph']
        
        data = np.array([[Conductivity, Turbidity, Temperature, Ph]])
        my_prediction = rfc.predict(data)
        result = my_prediction[0]
        
        print(result)

        
        if result == 0 :
            res='Good Condition for Mariculture'
        elif result == 1: 
            res='Not Good Condition for Mariculture , <br> Do the water treatment'
        
        print(res)

           
        return render_template('predict.html',name=name, pred = result,status=res)

    return render_template('predict.html')

if __name__ == '__main__':
	app.run(debug = True)