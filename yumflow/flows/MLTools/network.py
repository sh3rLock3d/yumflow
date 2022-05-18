import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from .enums import *

device = "cuda" if torch.cuda.is_available() else "cpu"


class NeuralNetwork(nn.Module):
    def __init__(self, layerlist):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(*layerlist)

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def create_layer(info):  # todo move this func to body of enum
    layerlist = []
    for i in info:
        if i[0] in set(item.value for item in Activation_function):
            if i[0] == Activation_function.RELU_FUNCTION.value:
                layerlist.append(nn.ReLU())
            elif i[0] == Activation_function.SIGMOID_FUNCTION.value:
                layerlist.append(nn.Sigmoid())
            elif i[0] == Activation_function.SOFT_MAX.value:
                layerlist.append(nn.Softmax(dim=0))
            elif i[0] == Activation_function.TANH.value:
                layerlist.append(nn.Tanh())
            else:
                print('some function is not mentioned here')

        elif i[0] in set(item.value for item in Weight):
            if i[0] == Weight.Linear.value:
                layerlist.append(nn.Linear(i[1], i[2]))
            elif i[0] == Weight.Conv.value:
                print('convoutional not implementes yet')
                pass
            else:
                print('some function is not mentioned here')
    return layerlist


def create_network(info):
    layer = create_layer(info)
    model = NeuralNetwork(layer).to(device)
    return model


def get_lossFn(info): # todo move this func to body of enum
    if info == Loss_fn.CROSS_ENTROPY.value:
        return nn.CrossEntropyLoss()
    elif info == Loss_fn.MEAN_SQUARE_ERROR.value:
        return nn.MSELoss()
    elif info == Loss_fn.MEAN_ABSOLUTE_ERROR.value:
        return nn.L1Loss()
    elif info == Loss_fn.NEGATIVE_LIKELIHOOD.value:
        return nn.NLLLoss()
    elif info == Loss_fn.BINARY_CROSS_ENTROPY.value:
        return nn.BCELoss()
    else:
        raise Exception(f'loss function ${info} is not available')


def get_optimizer(opt, l, param):
    if opt == Optimizer.SGD.value:
        return torch.optim.SGD(param, lr=l, momentum=0.9)
    elif opt == Optimizer.ADAM.value:
        a = torch.optim.Adam(param, lr=l)
        return a
    else:
        raise Exception(f'optimizer ${opt} is not available')


def train_the_network(info, model, x_train, y_train):
    loss_fn = get_lossFn(info['lossfn'])
    optimizer = get_optimizer(info['optimizer'], info['learning_rate'], model.parameters())
    batch_size = info['batch_size']
    result = []

    tensor_x = torch.Tensor(x_train.copy())  # transform to torch tensor

    tensor_y = torch.Tensor(y_train.copy())
    training_dataset = TensorDataset(tensor_x, tensor_y)  # create your datset
    train_dataloader = DataLoader(training_dataset, batch_size=batch_size)  # create your dataloader
    
    epochs = info['epochs']
    for t in range(epochs):
        size = len(train_dataloader.dataset)
        model.train()
        for batch, (X, y) in enumerate(train_dataloader):
            X, y = X.to(device), y.to(torch.float).to(device)
            # Compute prediction error
            pred = model(X)

            y = y.reshape(pred.shape[0])
            loss = loss_fn(pred, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        else:
            result.append(loss)
    return model, result


def test_network(info, model, x_test, y_test):
    
    batch_size = info['batch_size']
    tensor_x = torch.Tensor(x_test)  # transform to torch tensor
    tensor_y = torch.Tensor(y_test)
    test_dataset = TensorDataset(tensor_x, tensor_y)  # create your datset
    dataloader = DataLoader(test_dataset, batch_size=batch_size)  # create your dataloader

    loss_fn = get_lossFn(info['lossfn'])
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(torch.long).to(device)
            pred = model(X)
            y = y.reshape(pred.shape[0])
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    return f"Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"


def predict_by_network(model, x, y, classes):
    model.eval()
    with torch.no_grad():
        print(x.shape)
        print(x)
        pred = model(x)
        predicted, actual = classes[pred[0].argmax(0)], classes[y]
        print(f'Predicted: "{predicted}", Actual: "{actual}"')
