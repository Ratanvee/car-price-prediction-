from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np
import os

app = Flask(__name__)

model = pickle.load(open('templates/model/carPricePredict.pkl', 'rb'))
car = pd.read_csv('templates/model/car.csv')

from flask import Flask, jsonify, url_for

app = Flask(__name__)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "My Flask PWA",
        "short_name": "FlaskPWA",
        "start_url": url_for('index'),  # Set dynamically
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4CAF50",
        "icons": [
            {
                "src": url_for('static', filename='icons/icon-192x192.png'),
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": url_for('static', filename='icons/icon-512x512.png'),
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

# @app.route('/')
# def home():
#     return "Welcome to the PWA Home Page"

# if __name__ == '__main__':
#     app.run(debug=True)


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

        array = np.array([car_name, kms, fuel_type, transmission, owner, year, engine, seats], dtype=object).reshape(1, -1)
        prediction = model.predict(array)

        return str(np.round(prediction[0], 2)) + " Lakhs Rs."
    
    except ValueError as ve:
        print(f"A ValueError occurred: {ve}")
        return "Value Error occurred. Please check your inputs."
    except TypeError as te:
        print(f"A TypeError occurred: {te}")
        return "Type Error occurred. Please check your inputs."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again later."

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port,debug=True, ssl_context='adhoc', ssl_context=('/path/to/fullchain.pem', '/path/to/privkey.pem'))

# if __name__ == '__main__':
#     app.run(debug=True, ssl_context='adhoc')

# if __name__ == '__main__':
#     app.run(debug=True, ssl_context=('/path/to/fullchain.pem', '/path/to/privkey.pem'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=True,ssl_context=None)


# ssl_cert_path = 'C:/Users/ratan/certificates/fullchain.pem'  # Update with the correct path
# ssl_key_path = 'C:/Users/ratan/certificates/privkey.pem'     # Update with the correct path

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))

#     app.run(host='0.0.0.0', port=port, debug=True, ssl_context=(ssl_cert_path, ssl_key_path))


# from flask import Flask
# from flask_talisman import Talisman

# # app = Flask(__name__)
# Talisman(app)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)





# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True, ssl_context=('/path/to/fullchain.pem', '/path/to/privkey.pem'))



