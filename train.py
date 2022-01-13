import os.path

import torch

from model import Model #引入模型类

from loader import get_loader,predict_util #引入数据集获取函数

import json

from PIL import  Image

resize = 64
def evaluate(model,loader):#被调用的一个评估函数
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    correct = 0
    total = len(loader.dataset)
    for x,y in loader:
        x ,y = x.to(device),y.to(device)
        with torch.no_grad():
            y_pre = model(x)
            pred = y_pre.argmax(dim=1)
        correct += torch.eq(pred,y).sum().float().item()
    return correct/total

def predict(model,pic,dic:dict):
    ans = ''
    x = predict_util(pic,resize)
    pred = model(x).argmax(dim=1)
    for k,v in dic.items():
        if torch.eq(pred,int(v)):
            ans += k + '\nin['
    for k in dic.keys():
        ans += k+','
    ans += ']'
    return ans


def Train(pro_name:str):
    #这个是准备获取一次训练的模型
    max_acc = 0
    if not os.path.exists(os.path.join('projects',pro_name,'models')):
        os.mkdir(os.path.join('projects',pro_name,'models'))
    L = os.listdir(os.path.join('projects',pro_name,'models'))
    the_file = 'data' + str(len(L)) + '.csv'
    save_file = 'run_' + str(len(L))+' acc_'
    super_file = ''
    #4个超参数
    batch_sz = 4

    epochs = 50
    lr = 1e-4
    with open(os.path.join('projects',pro_name,'config.json'))as f:
        dim_num = len(json.load(f))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_loader = get_loader(pro_name, 'train', batch_size=batch_sz, resize=resize,datafile=the_file)
    test_loader = get_loader(pro_name, 'test', batch_size=batch_sz, resize=resize,datafile=the_file)
    val_loader = get_loader(pro_name, 'val', batch_size=batch_sz, resize=resize,datafile=the_file)
    model = Model(dim=dim_num, size=resize).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criteon = torch.nn.CrossEntropyLoss()
    for epoch in range(epochs):
        loss= None
        for step, (x, y) in enumerate(train_loader):
            x, y = x.to(device), y.to(device)
            y_pre = model(x)
            loss = criteon(y_pre, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        #处理和保存文件
        if epoch % 1 == 0:
            print('epoch:{}/{}:loss:{}'.format(epoch,epochs, loss))
            del x, y, y_pre, loss
            torch.cuda.empty_cache()
            acc = evaluate(model, val_loader)
            if epoch > 20 and acc > max_acc:
                if os.path.exists(super_file):
                    try:
                        os.remove(super_file)
                    except:
                        pass
                ff = save_file + str(int(round(acc,3)*1000)) + '.pth'
                super_file = os.path.join('projects',pro_name,'models',ff)
                torch.save(model.state_dict(),super_file)
                max_acc = acc
            print('val-acc:{}'.format(acc))

    test_acc = evaluate(model, test_loader)
    print('best_acc:{}'.format(max_acc))
    del model
    torch.cuda.empty_cache()
