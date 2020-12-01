import pandas as pd
from collections import defaultdict
import json


path = "C:/Users/Sirui/QuesTek/WastePD Data/"
file = "AC reduced dimension.xlsx"
df1 = pd.read_excel(path+file, sheet_name = 'comprehensive')

df1 = df1.iloc[0:119,:]
df1 = df1.where(pd.notnull(df1), None)


df2 = pd.read_excel(path+file, sheet_name = 'Phases')
df2 = df2.where(pd.notnull(df2), None)


def tree():
    return defaultdict(tree)


def inflate(tree, path, value):
    path = path.split('.')
    level = len(path)
        
    if level == 1:
        tree['%s' %(path[0])] = value
        
    elif level == 2:
        tree['%s' %(path[0])]['%s' %(path[1])] = value
 
    elif level == 3:
        tree['%s' %(path[0])]['%s' %(path[1])]['%s' %(path[2])] = value
           
    elif level == 4:
        tree['%s' %(path[0])]['%s' %(path[1])]['%s' %(path[2])]['%s' %(path[3])] = value
    
    elif level == 5:
        print('Need to manually increase levels!')     
    
    return tree


def merge(dict_1,dict_2, merge_path):
    tree1 = tree() 
    tree2 = tree()
    
    for k,v in dict_1.items():
        inflate(tree = tree1, path = k, value = v)
    
    dict_2.update({merge_path : [tree1]})
    
    for k,v in dict_2.items():
        inflate(tree = tree2, path = k, value = v)
    
    return tree2
    

temp_list1 = df1.to_dict('records')
temp_list2 = df2.to_dict('records') 

position_index = list(range(len(temp_list2)))

store = []

for i in position_index:
    j = (merge(temp_list2[i], temp_list1[i], merge_path = 'material.phases')) 
    store.append(j)
    
with open('119.json','a') as file:
        json.dump(store, file, indent = 2)