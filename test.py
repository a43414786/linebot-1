import pickle as pkl
import os
data = pkl.load(open(os.path.join('stock_infos','20211210.pkl'),'rb'))
for i in data:
    print(i)

