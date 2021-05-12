from math import pi
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import cumsum, factor_cmap

df = pd.read_csv('../coursework/model/diabetes.csv')
count_1 = len(df[df['Outcome'] == 1])
count_0 = len(df[df['Outcome'] == 0])

def is_diabetes_wedge():
    x = {'yes': count_1, 'no': count_0}
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'count'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    colors = ["#FF7400", "#009999"]
    data['color'] = colors[:len(x)]
    p = figure(plot_height=350, plot_width=350, toolbar_location=None,
               tools="hover", tooltips="@count: @value")
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='count', source=data)
    p.axis.axis_label = None
    p.axis.visible = False
    return p

def is_diabetes_bar():
    data = ['yes', 'no']
    count = [count_1, count_0]
    source = ColumnDataSource(data=dict(data=data, count=count))
    p = figure(x_range=data, plot_height=350, plot_width=350, toolbar_location=None)
    p.vbar(x='data', top='count', width=0.8, source=source,
           line_color='white', fill_color=factor_cmap('data', palette=Spectral6, factors=data))
    return p

# def heatmap():

def histogram():
    mass = [np.histogram(df.Pregnancies, density=True, bins=50), np.histogram(df.Glucose, density=True, bins=50),
            np.histogram(df.BloodPressure, density=True, bins=50),
            np.histogram(df.SkinThickness, density=True, bins=50), np.histogram(df.Insulin, density=True, bins=50),
            np.histogram(df.BMI, density=True, bins=50),
            np.histogram(df.DiabetesPedigreeFunction, density=True, bins=50),
            np.histogram(df.Age, density=True, bins=50)]
    p = []
    titles = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI',
              'Diabetes Pedigree Function', 'Age']
    for i in range(7):
        p.append(
            figure(title=titles[i], plot_height=300, plot_width=300, toolbar_location='below'))
        p[i].title.align = 'center'
        p[i].quad(top=mass[i][0], bottom=0, left=mass[i][1][:-1], right=mass[i][1][1:],
                  line_color="white")
    return p
