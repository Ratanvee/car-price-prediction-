from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('templates/model/carPricePredict.pkl', 'rb'))
car = pd.read_csv('templates/model/car.csv')

@app.route('/')
def index():
    car_name = sorted(car['car_name'].unique())
    year = sorted(car['manufacture'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()
    transmission = car['transmission'].unique()
    ownership = sorted(car['ownership'].unique())
    Seats = sorted(car['Seats'].unique())
    engine = sorted(car['engine'].unique())
    return render_template('index.html', car_names=car_name, year=year, engine=engine, Seats=Seats, fuel_type=fuel_type, transmission=transmission, ownership=ownership)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        car_name = request.form.get('company')
        fuel_type = request.form.get('fuel_type')
        transmission = request.form.get('transmission')
        owner = request.form.get('owner')
        year = int(request.form.get('year'))
        engine = request.form.get('engine')
        seats = request.form.get('seats')
        kms = request.form.get('kms')
        
        # Assuming the model requires numeric or encoded inputs
        # Encode categorical features if necessary
        # Example: If your model expects label encoding
        # car_name_encoded = label_encoder_car_name.transform([car_name])[0]
        # fuel_type_encoded = label_encoder_fuel_type.transform([fuel_type])[0]
        # transmission_encoded = label_encoder_transmission.transform([transmission])[0]
        # owner_encoded = label_encoder_owner.transform([owner])[0]
        
        # Since we don't have the encoders, let's assume the model was trained on the raw values
        # and will handle the encoding internally

        array = np.array([car_name, kms, fuel_type, transmission, owner, year, engine, seats], dtype=object).reshape(1, -1)
        
        # Predicting the price
        prediction = model.predict(array)
        
        # Return the prediction as a response
        return str(np.round(prediction[0], 2)) + " Lakhs rs"
    
    except ValueError as ve:
        print(f"A ValueError occurred: {ve}")
        return "Value Error occurred. Please check your inputs."
    except TypeError as te:
        print(f"A TypeError occurred: {te}")
        return "Type Error occurred. Please check your inputs."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again later."

if __name__ == "__main__":
    app.run(debug=True)
