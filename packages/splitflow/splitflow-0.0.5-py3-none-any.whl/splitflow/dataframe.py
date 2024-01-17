import polars as pl
import pandas as pd
import numpy as np
import random
import string
import os
from concurrent.futures import ThreadPoolExecutor
import functools

class SplitFlow:
    def __init__(self):
        self.column=[]
        self.index=None   
        self.path_data=None
        self.index_name=None

    
    def connect(self,data='data',index='index'):
        try:
            self.index=pd.read_csv(data+'/'+index+'.csv')
            a=list(self.index['column'])
            unique_list = list(set(a))
            self.column=self.column+unique_list
            self.path_data=data
            self.index_name=index

        except:
            print('error')
            
    def load(self,data,thresh=100,index='index',dest='data'):
        self.index_name=index
        self.path_data=dest
        df=pd.read_csv(data)
        df[index] = df.index
        csv_file_name=dest+'/'+index+'.csv'
        csv_loc=dest+'/'
        if not os.path.exists(dest):
            os.makedirs(dest)
            
        if not os.path.exists(csv_file_name):
            data_frame=pd.DataFrame({'column':[],'csv':[],'low':[],'high':[],'type':[],'indexes':[],'count':[]})
            data_frame.to_csv(csv_file_name,index=False)
            self.index=data_frame
            print(data_frame)
        else:
            data_frame=pd.read_csv(csv_file_name)
            self.index=data_frame
            print(data_frame)
        
        self.column=self.column+list(df.columns)
        for i in df.columns:
            if i == index:
                continue
            sorted_df = df[[i,index]].sort_values(by=i)

            num_rows = len(sorted_df)
            num_full_blocks = num_rows // thresh
            last_block_size = num_rows % thresh

            smaller_dfs = []
            start_index = 0

            for i in range(num_full_blocks):
                end_index = start_index + thresh
                smaller_dfs.append(sorted_df.iloc[start_index:end_index])
                start_index = end_index
            if last_block_size > 0:
                smaller_dfs.append(sorted_df.iloc[start_index:])
            
            for i in smaller_dfs:
                ran=''.join(random.choices(string.ascii_letters, k=30))
                final=i.columns[0]+'_'+ran+'.csv'
                while True:
                    if (data_frame['csv'] != final).all():
                        i.to_csv(csv_loc+final,index=False)
                        data_frame=pd.concat([data_frame,pd.DataFrame({'column':i.columns[0],'csv':final,'low':i.iloc[0,0],'high':i.iloc[i.shape[0]-1,0],'type':i[i.columns[0]].dtype,'indexes':list(i[index]),'count':int(i[index].shape[0])})])
                        break
            data_frame.to_csv(csv_file_name,index=False)
            self.index=data_frame
    
    def csv_list(self,col):
        return list(self.index.loc[self.index['column']==col,'csv'])
    
    
    
    def mean_function(self,path,col):
        file=self.path_data+'/'+path
        df = pl.read_csv(file)
        return df[col].sum()
            
        
        
    def mean(self,col):
        if col not in self.column:
            print(col,' it not there in the dataset')
            return
        partial_function = functools.partial(self.mean_function, col=col)
        paths=self.csv_list(col)
        with ThreadPoolExecutor() as executor:
            result_list_concurrent = list(executor.map(partial_function, paths))

        return sum(result_list_concurrent)/(self.index.loc[self.index['column']==col,'count'].sum())
    
    
    def med_num(self,col,types):
        if col not in self.column:
            log(col,' it not there in the dataset')
            return
        n=sum(self.index.loc[self.index['column']==col,'count'])
        if n % 2 == 0:
            mid1 = n // 2
            mid1=int(mid1-1)
            mid2 = int(mid1 - 1)
            cols=list(self.index.loc[self.index['column']==col,'count'])
            temp=0
            a=0
            ind=0
            for i in cols:
                a=a+int(i)
                if mid2<a:
                    if mid1<a:
                        mid1=mid1-temp
                        data=pd.read_csv(self.path_data+'/'+str(list(self.index.loc[self.index['column']==col,'csv'])[ind]))
                        mid2=mid2-temp
                        print(mid1,mid2)
                        if types==0:
                            return (data.iloc[mid1,0]+data.iloc[mid2,0])/2
                        else:
                            return (data.iloc[mid1,0],data.iloc[mid2,0])
                    else:
                        data=pd.read_csv(self.path_data+'/'+str(list(self.index.loc[self.index['column']==col,'csv'])[ind]))
                        data1=pd.read_csv(self.path_data+'/'+str(list(self.index.loc[self.index['column']==col,'csv'])[ind+1]))
                        if types==0:
                            print(data.shape[0])
                            return (data1.iloc[0,0]+data.iloc[data.shape[0]-1,0])/2
                        else:
                            return (data1.iloc[0,0],data.iloc[data.shape[0]-1,0])
                    break
                temp=a
                ind=ind+1

        else:
            mid = n // 2
            mid=int(mid-1)
            print(mid)
            cols=list(self.index.loc[self.index['column']==col,'count'])
            a=0
            ind=0
            for i in cols:
                a=a+i
                if mid<a:
                    mid=mid-temp
                    data=pd.read_csv(self.path_data+'/'+str(list(self.index.loc[self.index['column']==col,'csv'])[ind]))
                    if types==0:
                        return data.iloc[mid,0]
                    else:
                        return (data.iloc[mid,0])
                    break
                temp=a
                ind=ind+1    
    
    def median(self,col):
        if col not in self.column:
            print('not there')
            return
        toc=list(self.index.loc[self.index['column']==col,'type'])[0]
        if str(toc) in ['int64','float64']:
            return self.med_num(col,0)
        else:
            return self.med_num(col,1)
    
    def count(self,col):
        if col not in self.column:
            print(col,' it not there in the dataset')
            return
        return np.sum(self.index.loc[self.index['column']=='Column5','count'])
    
    def val_funct(self,path,col):
        file=self.path_data+'/'+path
        df = pd.read_csv(file)
        return df[col].value_counts().to_dict()
    
    def value_count(self,col):
        if col not in self.column:
            print(col,' it not there in the dataset')
            return
        partial_function = functools.partial(self.val_funct, col=col)
        path=self.csv_list(col)
        with ThreadPoolExecutor() as executor:
            result_list_concurrent = list(executor.map(partial_function, path))
        combined_dict = {}

        for dictionary in result_list_concurrent:
            for key, value in dictionary.items():
                combined_dict[key] = combined_dict.get(key, 0) + value
                
        return dict(sorted(combined_dict.items(), key=lambda item: item[1], reverse=True))
    
    
    def mode(self,col):
        if col not in self.column:
            print(col,' it not there in the dataset')
            return
        try:
            return list(self.value_count(col).items())[0][0]
        except:
            log('Error')
        
    def col_funct(self,path,col):
        file=self.path_data+'/'+path
        df = pd.read_csv(file)
        return list(df[col].values)
    
    def column_values(self,col):
        if col not in self.column:
            log(col,' it not there in the dataset')
            return
        partial_function = functools.partial(self.col_funct, col=col)
        path=self.csv_list(col)
        with ThreadPoolExecutor() as executor:
            list_of_col = list(executor.map(partial_function, path))
        combined_list = []
        for sublist in list_of_col:
            combined_list += sublist
        return combined_list

    
    def find_funct(self,path,col,value,relation):
        file=self.path_data+'/'+path
        df = pd.read_csv(file)
        if relation == 'eq':
            return list(df.loc[df[col]==value[0],self.index_name])
        elif relation == 'lt':
            return list(df.loc[df[col]<=value[0],self.index_name])
        elif relation == '-lt':
            return list(df.loc[df[col]<value[0],self.index_name])
        elif relation == 'gt':
            return list(df.loc[df[col]>=value[0],self.index_name])
        elif relation == '-gt':
            return list(df.loc[df[col]>value[0],self.index_name])            
    
    
    def find(self,col,relation=None,value=None):
        if col not in self.column:
            log(col,' it not there in the dataset')
            return
        
        if not value:
            combined_list=[]
            for sublist in list(self.index.loc[self.index['column']==col ,'indexes'].values):
                combined_list +=[int(x) for x in sublist[1:-1].split(',')]
            return combined_list
            
        if not relation:
            combined_list=[]
            for sublist in list(self.index.loc[self.index['column']==col ,'indexes'].values):
                combined_list +=[int(x) for x in sublist[1:-1].split(',')]
            return combined_list
                
        if relation not in ['eq','lt','gt','-gt','-lt']:
            print('relation needs to be eq, lt, gt ,-gt or -lt')
            return
        
        value=np.array([value]).astype(self.index.loc[self.index['column']==col,'type'].values[0])
        a=self.index.loc[self.index['column']==col]
        a[['low','high']]=a[['low','high']].astype(a['type'].values[0])
            
        path=list(a['csv'])
            
        partial_function = functools.partial(self.find_funct, col=col,value=value,relation=relation)
            
            
        with ThreadPoolExecutor() as executor:
            list_of_index = list(executor.map(partial_function,path ))
        combined_list = []
        for sublist in list_of_index:
            combined_list += sublist
                
        return combined_list
    
    def val_funct1(self,path,col,ind):
        file=self.path_data+'/'+path
        df = pd.read_csv(file)
        return list(df.loc[df[self.index_name].isin(ind),col])
    
    
    def values(self,col,indexes):
        pass
        if col is None:
            raise Exception("No Column given")
            
        if indexes is None:
            raise Exception("No index given")
            
        elif not isinstance(indexes, list):
            raise TypeError("Input must be a list")
        
        path=self.index.loc[self.index['column']==col,'csv']     
        
        partial_function = functools.partial(self.val_funct1, col=col,ind=indexes)
        with ThreadPoolExecutor() as executor:
            list_of_index = list(executor.map(partial_function,path ))
        
        combined_list = []
        for sublist in list_of_index:
            combined_list += sublist
                
        return combined_list
                
    def count_duplicates(self,path,col):
        file=self.path_data+'/'+path
        df = pd.read_csv(file)
        counts = {}
        for element in list(df[col]):
            counts[element] = counts.get(element, 0) + 1
        counts = {key: value for key, value in counts.items() if value > 1}
        return counts
    
    
    def duplicates(self,col):
        if col not in self.column:
            print(col,' it not there in the dataset')
            return
        partial_function = functools.partial(self.count_duplicates, col=col)
        path=self.csv_list(col)
        with ThreadPoolExecutor() as executor:
            result_list_concurrent = list(executor.map(partial_function, path))
        combined_dict = {}

        for dictionary in result_list_concurrent:
            for key, value in dictionary.items():
                combined_dict[key] = combined_dict.get(key, 0) + value
                
        return dict(sorted(combined_dict.items(), key=lambda item: item[1], reverse=True))
    
    def funct_map(self,path,col,mapper):
        file=self.path_data+'/'+path
        df = pd.read_csv(file)
        return mapper(df)
    
    
    def MapRed(self,col,mapper,reducer):
        if not callable(mapper) and hasattr(mapper, '__call__'):
            raise Exception("Mapper needs to be a function")
            
        if not callable(reducer) and hasattr(reducer, '__call__'):
            raise Exception("Reducer needs to be a function")
        
        path=self.csv_list(col)
        partial_function = functools.partial(self.funct_map, col=col,mapper=mapper)
        with ThreadPoolExecutor() as executor:
            result_list_concurrent = list(executor.map(partial_function, path))
        
        return reducer(result_list_concurrent)