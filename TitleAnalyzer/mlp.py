import numpy as np
import pandas as pd
import nltk
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split 
from nltk.corpus import stopwords

data = pd.read_csv('/Users/macintosh/Desktop/TitleAnalyzer/data/book30-listing-train.csv',encoding = "ISO-8859-1")
columns = ['Id', 'Image', 'Image_link', 'Title', 'Author', 'Class', 'Genre']
data.columns = columns
books = pd.DataFrame(data['Title'])
genre = pd.DataFrame(data['Genre'])
data['Title'] = data['Title'].fillna('No Book')

feat = ['Genre']
for x in feat:
    le = LabelEncoder()
    le.fit(list(genre[x].values))
    genre[x] = le.transform(list(genre[x]))

def change(t):
    t = t.split()
    return ' '.join([(i) for (i) in t if i not in stop])
stop = list(stopwords.words('english'))
data['Title'].apply(change)

vectorizer = TfidfVectorizer(min_df=2, max_features=70000, strip_accents='unicode',lowercase =True,
                            analyzer='word', token_pattern=r'\w+', use_idf=True, 
                            smooth_idf=True, sublinear_tf=True, stop_words = 'english')
vectors = vectorizer.fit_transform(data['Title'])

X_train, X_valid, y_train, y_valid = train_test_split(vectors, genre['Genre'], test_size=5700)

from sklearn import linear_model
clf = linear_model.LogisticRegression(solver= 'sag',max_iter=200,random_state=450)
clf.fit(X_train, y_train)
pred = clf.predict(X_valid)
print(metrics.f1_score(y_valid, pred, average='macro'))
print('Accuracy of the model', metrics.accuracy_score(y_valid, pred))

joblib.dump(clf, '/Users/macintosh/Desktop/TitleAnalyzer/models/logreg.pkl')