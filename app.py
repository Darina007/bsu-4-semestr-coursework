import joblib
import numpy as np
from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask, render_template, request
from graphics import is_diabetes_wedge, is_diabetes_bar, histogram

app = Flask(__name__)
model = joblib.load(open('model/classifier.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    return render_template('prediction.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    type_button = int_features.pop()
    final_features = [np.array(int_features)]
    predicting = model.predict(final_features)
    output = round(predicting[0], 2)
    result_text = 'Presumably the test for diabetes will be '
    if output == 1:
        result_text += 'positive'
    else:
        result_text += 'negative'
    if type_button == 'predict':
        return render_template('prediction.html', prediction_text=result_text)
    elif type_button == 'portray':
        return portray()


@app.route('/portray', methods=['POST'])
def portray(final_features=None, result=None):
    mass_plots_diabetes = []
    if final_features is None and result is None:
        mass_plots_diabetes.append(is_diabetes_wedge())
        mass_plots_diabetes.append(is_diabetes_bar())
        p = histogram()
        scripts = []
        div = []
        for i in range(len(p)):
            scripts.append(0)
            div.append(0)
            scripts[i], div[i] = components(p[i])
        scripts_diabetes = []
        div_diabetes = []
        for i in range(len(mass_plots_diabetes)):
            scripts_diabetes.append(0)
            div_diabetes.append(0)
            scripts_diabetes[i], div_diabetes[i] = components(mass_plots_diabetes[i])
        return render_template(
            'graphics.html',
            plot_script_diabetes=scripts_diabetes,
            plot_script=scripts,
            plot_div_diabetes=div_diabetes,
            plot_div=div,
            js_resources=INLINE.render_js(),
            css_resources=INLINE.render_css(),
        ).encode(encoding='UTF-8')


if __name__ == '__main__':
    app.run(debug=True)
