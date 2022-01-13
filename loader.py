import os
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import torch
import csv
import glob
import random
from PIL import Image
import json
#porject表示项目的名字
#usage表示该数据集的用法
#resize表示准备重新变化的大小
class myds(Dataset):
    def __init__(self,project:str,usage:str,resize:int,datafile:str):
        assert usage in ['train','val','test']
        super(myds, self).__init__()
        self.root = os.path.join('projects',project)
        type_list = os.listdir(self.root)
        self.resize = resize
        self.name2label={}
        with open(os.path.join('projects', project, 'config.json')) as f:
            self.name2label = json.load(f)
        self.images,self.labels = self.load_csv(datafile)
        if usage == 'train': #70%
            self.images = self.images[:int(0.85*len(self.images))]
            self.labels = self.labels[:int(0.85*len(self.labels))]
        elif usage == 'val': #20%
            self.images = self.images[int(0.85 * len(self.images)):]
            self.labels = self.labels[int(0.85 * len(self.labels)):]
        else: #10%
            self.images = self.images[int(0.85 * len(self.images)):]
            self.labels = self.labels[int(0.85 * len(self.labels)):]

    def load_csv(self,datafile:str):
        if not os.path.exists(os.path.join(self.root,datafile)):
            images = []
            for name in self.name2label.keys():
                images += glob.glob(os.path.join(self.root,name,'*.jpg'))
            random.shuffle(images)
            f = open(os.path.join(self.root, datafile), mode='w', newline='')
            writer = csv.writer(f)
            for image in images:
                name = image.split(os.sep)[-2]
                label = self.name2label[name]
                writer.writerow([image,label])
            f.close()
        #从文件中读取数据
        images = []
        labels = []
        with open(os.path.join(self.root,datafile))as f:
            reader = csv.reader(f)
            for row in reader:
                image,label = row
                images.append(image)
                labels.append(int(label))
        return images,labels



    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx] #image这还只是一个路径
        label = self.labels[idx]
        tf = transforms.Compose([
            lambda x: Image.open(x).convert('RGB'),
            transforms.Resize((self.resize, self.resize)),
            transforms.ToTensor()
        ])
        return tf(image),torch.tensor(label)

#返回值是dataloder
def get_loader(project:str,usage:str,batch_size:int,resize:int,datafile:str):
    if usage in ['train','val','test']:
        ds = myds(project,usage,resize,datafile)
        return DataLoader(ds,batch_size,True)
    else:
        return None

def predict_util(img,resize):
    tf = transforms.Compose([
        lambda x: Image.open(x).convert('RGB'),
        transforms.Resize((resize, resize)),
        transforms.ToTensor()
    ])
    x  =  tf(img)
    x = x.unsqueeze(dim=0)
    print(x.size())
    return x
def main():
    a = get_loader('first','train',1,16,'data.csv')
    print(len(a))
if __name__ =='__main__':
    main()