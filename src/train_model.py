from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)

def train(X, y):
    model.fit(X, y)
    return model
