import os

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', default='/mnt/pv/models/onnx/cifar10', type=str)
    args = parser.parse_args()

    model_path = args.model_path
    if not (os.path.isdir(model_path)):
        os.makedirs(model_path)

    model_file = os.path.join(model_path, 'model.onnx')

    net = Net()
    state_dict = torch.load("/mnt/pv/models/pytorch/cifar10/model.pt")
    net.load_state_dict(state_dict)
    net.eval()

    x = torch.empty(1, 3, 32, 32)
    torch.onnx.export(net, x, model_file, input_names=['input1'], output_names=['output1'])
