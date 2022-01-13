import torch
from torch import nn


class Model(nn.Module):
    def __init__(self,dim,size):
        super(Model, self).__init__()
        assert size % 2 == 0
        size = int(size / 2)
        self.size = size
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, 1, 1),
            nn.MaxPool2d(2, 1, 1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, 1, 1),
            nn.MaxPool2d(2, 1, 1),
            nn.ReLU(),
            nn.Conv2d(32,32,3,1,1),
            nn.MaxPool2d(kernel_size=(2,1),stride=(2,1),padding=(1,0)),
            nn.ReLU(),
            nn.Conv2d(32,32,3,1,1),
            nn.MaxPool2d(kernel_size=(1,2),stride=(1,2),padding=(0,1)),
            nn.Conv2d(32,32,3,stride= 1),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(32*size*size,256),
            nn.ReLU(),
            nn.Linear(256,dim),
            nn.Sigmoid()
        )
    def forward(self,x):
        x = self.encoder(x)
        x = x.view(-1,32*self.size*self.size)
        return self.decoder(x)

def main():
    x = torch.randn((32, 3, 32, 32))
    model = Model(dim=10, size=32)
    x = model(x)
    print(x.size())

if __name__ =='__main__':
    main()