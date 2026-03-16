import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# Sample dataset (can be expanded)
data = {
    "password": [
        "123456", "password", "qwerty",
        "Admin@123", "Welcome@2024",
        "KaliLinux@Secure123", "StrongPass!99"
    ],
    "label": [0, 0, 0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df["password"]
y = df["label"]

vectorizer = CountVectorizer(analyzer="char", ngram_range=(2, 4))
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and vectorizer
with open("ml/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("ml/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("ML model trained and saved successfully")
