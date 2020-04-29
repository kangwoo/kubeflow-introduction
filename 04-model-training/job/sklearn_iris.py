from sklearn import datasets
from sklearn import svm


def train():
    iris = datasets.load_iris()
    x_train = iris.data[:-30]
    y_train = iris.target[:-30]
    x_test = iris.data[-30:]
    y_test = iris.target[-30:]

    clf = svm.SVC(gamma='scale')
    clf.fit(x_train, y_train)

    prediction = clf.predict(x_test)
    print(prediction == y_test)
    acc = clf.score(x_test, y_test)
    print("Accuracy : ", acc)


if __name__ == '__main__':
    train()