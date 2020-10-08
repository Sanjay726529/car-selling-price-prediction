from flask import Flask, render_template, request
import pickle
import numpy as np
import datetime as dt
import os


# load the model
model_path = os.path.join(os.path.curdir, 'car_prediction.pkl')
model = pickle.load(open(model_path, 'rb'))


# create the flask app
app = Flask(__name__)


# home route
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predict():

    prediction_text = ""
    
    if request.method == 'POST':
        make_year = request.form['year']
        year_old = 0
        
        if int(make_year) > dt.datetime.now().year:
            prediction_text = f"Hello Time Traveller, The {make_year} isn't arrived yet in present"
        elif len(make_year) != 4:
            prediction_text = f"{make_year} is invalid"
        else:
            year_old = dt.datetime.now().year - int(make_year)
    
        present_price = np.round(float(request.form['present_price']), 2)

        kms_driven = int(request.form['kms_driven'])

        # owner
        owner = int(request.form['owner'])
        if owner == 2:
            owner = 3
        elif owner > 3:
            owner = 3
        else:
            owner = int(request.form['owner'])


        if request.form['fuel_type'] == 'petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        

        if request.form['seller_type'] == 'individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        


        if request.form['Transmission'] == 'manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        data = np.array([[present_price, kms_driven, owner, year_old, Fuel_Type_Diesel, 
                Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        
        selling_price = np.round(model.predict(data), 2)

        print(selling_price)

        if selling_price < 0:
            prediction_text = "Sorry, You cannot sell the car"
        else:
            prediction_text = f"The selling price for your car can be around {selling_price[0]} lakhs"
    
        return render_template('index.html', prediction_text=prediction_text)        
    else:
        return render_template("index.html")



if __name__ == "__main__":
    app.run(port=8888, debug=True)





