import argparse
import os

import xgboost as xgb
from sklearn.datasets import load_iris


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', default='/mnt/pv/models/xgboost/iris', type=str)
    args = parser.parse_args()

    if not (os.path.exists(args.model_path)):
        os.makedirs(args.model_path)

    model_file = os.path.join(args.model_path, 'model.bst')

    iris = load_iris()
    X = iris['data']
    y = iris['target']
    dtrain = xgb.DMatrix(X, label=y)
    param = {'max_depth': 6,
             'eta': 0.1,
             'silent': 1,
             'nthread': 4,
             'num_class': 10,
             'objective': 'multi:softmax'
             }
    xgb_model = xgb.train(params=param, dtrain=dtrain)
    print('Finished Training')

    xgb_model.save_model(model_file)


if __name__ == '__main__':
    train()
