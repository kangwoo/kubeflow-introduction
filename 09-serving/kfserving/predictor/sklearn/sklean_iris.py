import argparse
import os

from joblib import dump
from sklearn import datasets
from sklearn import svm


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', default='/mnt/pv/sklearn/iris/model', type=str)
    args = parser.parse_args()

    if not (os.path.exists(args.model_path)):
        os.makedirs(args.model_path)

    model_file = os.path.join(args.model_path, 'model.joblib')

    clf = svm.SVC(gamma='scale')
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    clf.fit(X, y)
    print('Finished Training')

    dump(clf, model_file)


if __name__ == '__main__':
    train()
