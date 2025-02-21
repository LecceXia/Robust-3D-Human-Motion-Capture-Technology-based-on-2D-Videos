 
import torch as th
import torch.nn as nn
import torch.nn.functional as F

from torchsample.modules import ModuleTrainer
from torchsample import regularizers as reg
from torchsample import constraints as con

import os
from torchvision import datasets
ROOT = '/users/ncullen/desktop/data/mnist'
dataset = datasets.MNIST(ROOT, train=True, download=True)
x_train, y_train = th.load(os.path.join(dataset.root, 'processed/training.pt'))
x_test, y_test = th.load(os.path.join(dataset.root, 'processed/test.pt'))

x_train = x_train.float()
y_train = y_train.long()
x_test = x_test.float()
y_test = y_test.long()

x_train = x_train / 255.
x_test = x_test / 255.
x_train = x_train.unsqueeze(1)
x_test = x_test.unsqueeze(1)

# only train on a subset
x_train = x_train[:1000]
y_train = y_train[:1000]
x_test = x_test[:1000]
y_test = y_test[:1000]


# Define your model EXACTLY as if you were using nn.Module
class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.fc1 = nn.Linear(1600, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 1600)
        x = F.relu(self.fc1(x))
        #x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


model = Network()
trainer = ModuleTrainer(model)

trainer.compile(loss='nll_loss',
                optimizer='adadelta',
                regularizers=[reg.L1Regularizer(1e-4)])

trainer.fit(x_train, y_train, 
            val_data=(x_test, y_test),
            num_epoch=3, 
            batch_size=128,
            verbose=1)

ypred = trainer.predict(x_train)
print(ypred.size())

eval_loss = trainer.evaluate(x_train, y_train)
print(eval_loss)

print(trainer.history)
#print(trainer.history['loss'])

