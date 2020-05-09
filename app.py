from flask import Flask, jsonify, request
from flask_cors import CORS
from naive_bayes import mapping
from naive_bayes import Naive_Bayes
# from secrets import api_key

app = Flask(__name__)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/', methods=['GET'])
@app.route('/params', methods=['GET'])
def home():
    return jsonify(mapping)

@app.route('/ages/all', methods=['GET'])
def age_fields():
    return jsonify(
        {
            '0–9 years': (0.01, 0.99),
            '10–19 years': (0.0408, 0.959),
            '20–29 years': (0.0104, 0.99),
            '30–39 years': (0.0343, 0.966),
            '40–49 years': (0.0425, 0.958),
            '50–59 years': (0.0816, 0.918),
            '60–69 years': (0.118, 0.882),
            '70–79 years': (0.166, 0.834),
            '≥80 years': (0.184, 0.816)
        }
    )

@app.route('/conditions', methods=['GET'])
def query():
    query_parameters = request.args
    assert(len(query_parameters)) == 1
    condition = query_parameters.get('condition').strip("\"")
    return jsonify({condition : mapping[condition]} if condition in mapping else dict())

@app.route('/age', methods=['GET'])
def query_age():
    query_parameters = request.args
    assert(len(query_parameters)) == 1
    age = int(query_parameters.get('age'))

    if age >= 110:
        raise ValueError("Invalid age.")
    elif age >= 80:
        condition = '≥80 years'
    elif age >= 70:
        condition = '70–79 years'
    elif age >= 60:
        condition = '60–69 years'
    elif age >= 50:
        condition = '50–59 years'
    elif age >= 40:
        condition = '40–49 years'
    elif age >= 30:
        condition = '30–39 years'
    elif age >= 20:
        condition = '20–29 years'
    elif age >= 10:
        condition = '10–19 years'
    else:
       condition = '0–9 years'

    return jsonify({condition : mapping[condition]})


@app.route('/conditions/all', methods=['GET'])
def conditions():
    return jsonify(
        {
            'Cardiovascular disease': (0.202, 0.046),
            'Chronic liver disease': (0.008, 0.005),
            'Chronic lung disease': (0.145, 0.071),
            'Chronic renal disease': (0.08, 0.01),
            'Control': (0.836, 0.164),
            'Current smoker': (0.017, 0.012),
            'Former smoker': (0.042, 0.016),
            'Diabetes mellitus': (0.224, 0.064),
            'Immunocompromised condition': (0.061, 0.027),
            'Neurologic disorder/Intellectual disability': (0.017, 0.003),
            'Other chronic disease': (0.297, 0.113),
            'Pregnant': (0.035, 0.014),
        }
    )

# TODO : HANDLE PUT, DELETE REQUESTS
@app.route('/', methods=['POST'])
def post():
    # if request.is_json:
    data = request.get_json() if request.is_json else request.get_data()
    # else:
    #     raise ValueError("Cannot parse data.")
    assert(len(data)) == 2
    try:
        age = data['age']
        condition_list = data['conditions']
    except KeyError:
        return jsonify(dict())
    nb = Naive_Bayes(age, condition_list)
    return jsonify({'probability': nb.get_probability()})

@app.errorhandler(404)
def error(e):
    return "<h1 style='text-align: center; padding-top: 10%;'>404</h1><p style='text-align: center;'>The resource could not be found.</p>", 404

@app.errorhandler(405)
def error_405(e):
    return f"<title>405 Method Not Allowed</title><h1>The method {request.method} is not allowed for the requested url.</h1>", 405

if __name__ == '__main__':
    app.run(debug=True)
