from sklearn.linear_model import LogisticRegression
import joblib

print('fuck')

import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('diabetes.csv')

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Model
LR = LogisticRegression(solver='liblinear')

LR.fit(X_train, y_train)

y_pred = LR.predict(X_test)

print("Accuracy ", LR.score(X_test, y_test) * 100)

joblib.dump(LR, 'classifier.pkl')
