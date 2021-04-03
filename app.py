import joblib
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)
model = joblib.load(open('model/classifier.pkl', 'rb'))


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    result_text = 'Presumably the test for diabetes will be '
    if output == 1:
        result_text += 'positive'
    else:
        result_text += 'negative'
    return render_template('index.html', prediction_text=result_text)


if __name__ == '__main__':
    app.run(debug=True)
