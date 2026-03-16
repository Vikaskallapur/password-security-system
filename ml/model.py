import pickle

with open("ml/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("ml/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def predict_strength(password: str):
    X = vectorizer.transform([password])
    prediction = model.predict(X)[0]
    return "Strong" if prediction == 1 else "Weak"
