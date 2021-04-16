import joblib
import numpy as np
from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask, render_template, request

from graphics import is_diabetes_wedge, is_diabetes_bar

app = Flask(__name__)
model = joblib.load(open('model/classifier.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index1.html')


@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    return render_template('prediction1.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    predicting = model.predict(final_features)
    output = round(predicting[0], 2)
    result_text = 'Presumably the test for diabetes will be '
    if output == 1:
        result_text += 'positive'
    else:
        result_text += 'negative'
    return render_template('prediction1.html', prediction_text=result_text)


@app.route('/portray', methods=['POST'])
def portray():
    p = is_diabetes_wedge()
    t = is_diabetes_bar()
    script, div = components(p)
    script1, div1 = components(t)
    return render_template(
        'graphics.html',
        plot_script=script,
        plot_script1=script1,
        plot_div=div,
        plot_div1=div1,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')


if __name__ == '__main__':
    app.run(debug=True)
