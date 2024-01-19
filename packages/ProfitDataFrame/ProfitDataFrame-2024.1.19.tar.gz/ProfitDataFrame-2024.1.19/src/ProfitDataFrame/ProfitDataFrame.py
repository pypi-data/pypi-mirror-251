#!/usr/bin/env python
# coding: utf-8
#author : Zhang Chuanpeng 张传鹏
#nickname :Zhang Xuanjin 张玄瑾 / yz7zzxj001
#updated in  2024年1月18日
#2020/5/26 profit q_info to suit whose index does not begins with 0
#2020/5/27 fixing the5th which it goes well on my pc ,but mistake on others
#2020/9/15 add 3 fuctions: gap_statistic finds best K in kmeans
#          dup_corr show the corr between duplications
#          sta_describe show the kde and joinplot of numberic and bar of object
#          增加了三个函数：区间间隔统计法寻找最优K值，重复值相关性探究每列重复值之间得相关性，以及数据分布描述
#          sankey_type_data(x,result_is_df = True) make a df pivot table into a df that suit sunkey plot 将一个df的透视表转换为桑基图/gephi所需要的格式
#2024/1/18 增加了一个返回日期列是否是节假日、调休日和预备日的函数


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import datetime



class Profitdataframe(pd.DataFrame):
    '''
    it's a package for myself to do somethings in ELT automatically。
    此包构建的目的是为了在EDA过程中自动化处理一些问题
    目前写了几个方法：
    q_info 方法是对原df.info()的重构。返回一个DataFrame,包含原表的列名、各列总计数目、非空、空、空率、字段类型、前五预览
    q_view 方法将原本pd.plotting.scatter_matrix(df) 缩写,即查看各列间的相关性
    q_tips 方法塞入了一些常用的命令，方便复制修改
    '''

    def q_info(self):
        '''
        it's a functhon which make a info with null_percent infos and traditional df.info()
        返回一个DataFrame,包含原表的列名、各列总计数目、非空、空、空率、字段类型、前五预览
        '''
        ind = self.index
        col = self.columns
        ind_len = len(ind)
        col_len = len(col)
        df = pd.DataFrame(columns = ['total_count',
                                     'non_null_count',
                                     'null_count',
                                     'null_percent',
                                     'ddtype',
                                     '5th_view',])
        for i in col:
            #the5th = ','.join([str(self[i][self.index[j]]) for j in range(5)])
            value = {'total_count':ind_len,
                     'non_null_count':self[i].count(),
                     'null_count':self[i].isnull().sum(),
                     'null_percent':self[i].isnull().sum()/ind_len,
                     'ddtype':self[i].dtype
                     #'5th_view':the5th
                    }
            temp = pd.Series(value,name = i)
            df.loc[i] =temp
        return df

    def q_view(self):
        """
        q_view 方法将原本pd.plotting.scatter_matrix(df) 缩写,即查看各列间的相关性
        """
        pd.plotting.scatter_matrix(self)

    def sta_describe(self,y_colname=None):
        for i in self.columns:
            if self[i].dtype != 'object':
                plt.figure(figsize = (10,6))
                sns.kdeplot(self[i],legend = True)
                if y_colname:
                    plt.figure(figsize = (10,6))
                    sns.joinplot(i,y_colname,data=self,kind='reg')
            else:
                plt.figure(figsize = (10,6))
                sns.barplot(self[i])

    def q_tips(self,code = 0):
        """
        q_tips 方法塞入了一些常用的命令，方便复制修改
        """
        if code == 0:
            print(r'本方法code参数已加载','code=0 默认。显示菜单',
                 r'code = 1 显示cell内所有结果而非最后结果的代码',
                 r'code = 2 显示plt中修复显示错误的代码',
                 r'code = 3 显示本module中包含的方法'
                 ,sep = '\n')
        if code == 1 :
            print(r"from IPython.core.interactiveshell import InteractiveShell",
                  r"InteractiveShell.ast_node_interactivity = 'all'"
                 ,sep = '\n')
        if code == 2 :
            print(r"# 解决坐标轴刻度负号乱码 plt.rcParams['axes.unicode_minus'] = False",
                  r"# 解决中文乱码问题(上) plt.rcParams['font.sans-serif'] = ['Simhei']",
                  r"解决中文乱码问题(下) plt.rcParams[‘font.family’] = 'Arial Unicode MS'"
                  r"sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})"
            ,sep = '/n')
        if code == 3:
            print(r".q_info() 增强显示df信息",
                r".q_view() 显示df内各列两两之间的散点图矩阵",
                r".q_tips(code = 0) 展示mod引导",
                r"gap_statistic(X,B = 10,K=range(1,11)) 在1到11之间使用区间间隔统计方法寻找最佳的kmeans聚类簇数",
                r"dup_corr(X,nodatetime) 显示重复值之间的相关性以确定重复原因，默认忽略dt类型，只针对object类。缺失值的相关性可以用missinggo",
                r".sta_describe(y_colname=None) 对数值型数据，绘制kde，当y_cilname传入内容时（即标签存在时、答案存在时即监督学习）绘制每列对标签的join图（散点kde复合图）；对object，绘制直方图bar。"
                r"sankey_type_data(x,result_is_df = True) 将一个特征1 特征2 值的表转换为sankey图或gephi用格式"
                ,sep = '\r\n')


def short_pair_wise_D(each_cluster):
    mu = each_cluster.mean(axis=0)
    Dk = sum(sum((each_cluster-mu)**2))*2.0*each_cluster.shape[0]
    return Dk

def compute_Wk(data,classfication_result):
    Wk=0
    label_set = set(classfication_result)
    for label in label_set:
        each_cluster = data[classfication_result==label,:]
        Wk += short_pair_wise_D(each_cluster)/(2.0*each_cluster.shape[0])
    return Wk

def gap_statistic(X,B=10,K= range(1,11),N_init=10):
    """使用区间间隔统计方法寻找最优K值得主函数"""
    X = np.array(X)
    shapes = X.shape
    tops = X.max(axis = 0)
    bots = X.min(axis = 0)
    dists = np.matrix(np.diag(tops - bots))
    rands = np.random.random_sample(size = (B,shapes[0],shapes[1]))
    for i in range(B):
        rands[i,:,:] = rands[i,:,:]*dists+bots

    gaps = np.zeros(len(K))
    Wks = np.zeros(len(K))
    Wkbs = np.zeros((len(K),B))

    for idxk,k in enumerate(K):
        k_means = KMeans(n_clusters = k)
        k_means.fit(X)
        classification_result = k_means.labels_
        Wks[idxk] = compute_Wk(X,classification_result)

        for i in range(B):
            Xb = rands[1,:,:]
            k_means.fit(Xb)
            classification_result_b = k_means.labels_
            Wkbs[idxk,i] = compute_Wk(Xb,classification_result_b)

    gaps =(np.log(Wkbs)).mean(axis=1)-np.log(Wks)
    sd_ks = np.std(np.log(Wkbs),axis=1)
    sk = sd_ks * np.sqrt(1+1.0/B)

    gapDiff = gaps[:-1] - gaps[1:] + sk[1:]
    plt.bar(np.arange(len(gapDiff))+1,gapDiff)
    plt.xlabel('k')
    plt.ylabel('gapdiff')
    plt.show()

def dup_corr(x,nodatetime = True):
    """检验重复值相关性以确定重复值原因"""
    """注意，这里只判断dtype为object的重复值情况，因为如int/period/float重复值是没啥意义的"""
    tempdf = pd.DataFrame()
    for i in x.columns:
        if nodatetime:
            if x.loc[:,i].dtype == 'object':
                tempdf[i] = x.loc[:,i].duplicated()
        else:
            if (x.loc[:,i].dtype == 'object') or (x.loc[:,i].dtype == 'DatetimeIndex'):
                tempdf[i] = x.loc[:,i].duplicated()
    plt.figure(figsize =(10,10))
    sns.heatmap(tempdf.corr(),annot = True)


def sankey_type_data(x,result_is_df = True):
    """将df转换为符合桑基图绘制形式的关系网络图数据集。
    imput 特征1 特征2 特征3 ... 值的表
    output source target value 的表 其中，value之和等于input值合的二倍
    """
    nodes =[]
    columns = x.columns.tolist()
    for column in columns[:-1]:
        nodes =nodes + (x[column].tolist())
    py_nodes =[] # 提取了node数值数据
    for i in list(set(nodes)):
        dic = {}
        dic['name'] = i
        py_nodes.append(dic)
    links = pd.DataFrame(columns=['source', 'target', 'value'])
    for i in range(len(columns)-2):
        ass = x[columns[-1]].groupby([x[columns[i]],x[columns[i+1]]]).sum()
        sublinks = pd.DataFrame(ass.reset_index())
        sublinks.columns = ['source', 'target', 'value']
        links=links.append(sublinks)
    py_links = links.to_dict('records')
    if result_is_df :
        df_sankey = pd.DataFrame(py_links)
        return df_sankey
    else:
        return py_links

#定义三个字典以标记与周节律不同的日子
#_holidays 即每年法定节假日
#_workdays 即每年调休日
#_preholidays 即春节的预备日，预备日内消费者行为已经改变

_holidays = {
    datetime.date(year=2004, month=1, day=1): "元旦",
    datetime.date(year=2004, month=1, day=22): "春节",
    datetime.date(year=2004, month=1, day=23): "春节",
    datetime.date(year=2004, month=1, day=24): "春节",
    datetime.date(year=2004, month=1, day=25): "春节",
    datetime.date(year=2004, month=1, day=26): "春节",
    datetime.date(year=2004, month=1, day=27): "春节",
    datetime.date(year=2004, month=1, day=28): "春节",
    datetime.date(year=2004, month=5, day=1): "五一",
    datetime.date(year=2004, month=5, day=2): "五一",
    datetime.date(year=2004, month=5, day=3): "五一",
    datetime.date(year=2004, month=5, day=4): "五一",
    datetime.date(year=2004, month=5, day=5): "五一",
    datetime.date(year=2004, month=5, day=6): "五一",
    datetime.date(year=2004, month=5, day=7): "五一",
    datetime.date(year=2004, month=10, day=1): "国庆",
    datetime.date(year=2004, month=10, day=2): "国庆",
    datetime.date(year=2004, month=10, day=3): "国庆",
    datetime.date(year=2004, month=10, day=4): "国庆",
    datetime.date(year=2004, month=10, day=5): "国庆",
    datetime.date(year=2004, month=10, day=6): "国庆",
    datetime.date(year=2004, month=10, day=7): "国庆",
    datetime.date(year=2005, month=1, day=1): "元旦",
    datetime.date(year=2005, month=1, day=2): "元旦",
    datetime.date(year=2005, month=1, day=3): "元旦",
    datetime.date(year=2005, month=2, day=9): "春节",
    datetime.date(year=2005, month=2, day=10): "春节",
    datetime.date(year=2005, month=2, day=11): "春节",
    datetime.date(year=2005, month=2, day=12): "春节",
    datetime.date(year=2005, month=2, day=13): "春节",
    datetime.date(year=2005, month=2, day=14): "春节",
    datetime.date(year=2005, month=2, day=15): "春节",
    datetime.date(year=2005, month=5, day=1): "五一",
    datetime.date(year=2005, month=5, day=2): "五一",
    datetime.date(year=2005, month=5, day=3): "五一",
    datetime.date(year=2005, month=5, day=4): "五一",
    datetime.date(year=2005, month=5, day=5): "五一",
    datetime.date(year=2005, month=5, day=6): "五一",
    datetime.date(year=2005, month=5, day=7): "五一",
    datetime.date(year=2005, month=10, day=1): "国庆",
    datetime.date(year=2005, month=10, day=2): "国庆",
    datetime.date(year=2005, month=10, day=3): "国庆",
    datetime.date(year=2005, month=10, day=4): "国庆",
    datetime.date(year=2005, month=10, day=5): "国庆",
    datetime.date(year=2005, month=10, day=6): "国庆",
    datetime.date(year=2005, month=10, day=7): "国庆",
    datetime.date(year=2006, month=1, day=1): "元旦",
    datetime.date(year=2006, month=1, day=2): "元旦",
    datetime.date(year=2006, month=1, day=3): "元旦",
    datetime.date(year=2006, month=1, day=29): "春节",
    datetime.date(year=2006, month=1, day=30): "春节",
    datetime.date(year=2006, month=1, day=31): "春节",
    datetime.date(year=2006, month=2, day=1): "春节",
    datetime.date(year=2006, month=2, day=2): "春节",
    datetime.date(year=2006, month=2, day=3): "春节",
    datetime.date(year=2006, month=2, day=4): "春节",
    datetime.date(year=2006, month=5, day=1): "五一",
    datetime.date(year=2006, month=5, day=2): "五一",
    datetime.date(year=2006, month=5, day=3): "五一",
    datetime.date(year=2006, month=5, day=4): "五一",
    datetime.date(year=2006, month=5, day=5): "五一",
    datetime.date(year=2006, month=5, day=6): "五一",
    datetime.date(year=2006, month=5, day=7): "五一",
    datetime.date(year=2006, month=10, day=1): "国庆",
    datetime.date(year=2006, month=10, day=2): "国庆",
    datetime.date(year=2006, month=10, day=3): "国庆",
    datetime.date(year=2006, month=10, day=4): "国庆",
    datetime.date(year=2006, month=10, day=5): "国庆",
    datetime.date(year=2006, month=10, day=6): "国庆",
    datetime.date(year=2006, month=10, day=7): "国庆",
    datetime.date(year=2007, month=1, day=1): "元旦",
    datetime.date(year=2007, month=1, day=2): "元旦",
    datetime.date(year=2007, month=1, day=3): "元旦",
    datetime.date(year=2007, month=2, day=18): "春节",
    datetime.date(year=2007, month=2, day=19): "春节",
    datetime.date(year=2007, month=2, day=20): "春节",
    datetime.date(year=2007, month=2, day=21): "春节",
    datetime.date(year=2007, month=2, day=22): "春节",
    datetime.date(year=2007, month=2, day=23): "春节",
    datetime.date(year=2007, month=2, day=24): "春节",
    datetime.date(year=2007, month=5, day=1): "五一",
    datetime.date(year=2007, month=5, day=2): "五一",
    datetime.date(year=2007, month=5, day=3): "五一",
    datetime.date(year=2007, month=5, day=4): "五一",
    datetime.date(year=2007, month=5, day=5): "五一",
    datetime.date(year=2007, month=5, day=6): "五一",
    datetime.date(year=2007, month=5, day=7): "五一",
    datetime.date(year=2007, month=10, day=1): "国庆",
    datetime.date(year=2007, month=10, day=2): "国庆",
    datetime.date(year=2007, month=10, day=3): "国庆",
    datetime.date(year=2007, month=10, day=4): "国庆",
    datetime.date(year=2007, month=10, day=5): "国庆",
    datetime.date(year=2007, month=10, day=6): "国庆",
    datetime.date(year=2007, month=10, day=7): "国庆",
    datetime.date(year=2007, month=12, day=30): "元旦",
    datetime.date(year=2007, month=12, day=31): "元旦",
    datetime.date(year=2008, month=1, day=1): "元旦",
    datetime.date(year=2008, month=2, day=6): "春节",
    datetime.date(year=2008, month=2, day=7): "春节",
    datetime.date(year=2008, month=2, day=8): "春节",
    datetime.date(year=2008, month=2, day=9): "春节",
    datetime.date(year=2008, month=2, day=10): "春节",
    datetime.date(year=2008, month=2, day=11): "春节",
    datetime.date(year=2008, month=2, day=12): "春节",
    datetime.date(year=2008, month=4, day=4): "清明",
    datetime.date(year=2008, month=4, day=5): "清明",
    datetime.date(year=2008, month=4, day=6): "清明",
    datetime.date(year=2008, month=5, day=1): "五一",
    datetime.date(year=2008, month=5, day=2): "五一",
    datetime.date(year=2008, month=5, day=3): "五一",
    datetime.date(year=2008, month=6, day=7): "端午",
    datetime.date(year=2008, month=6, day=8): "端午",
    datetime.date(year=2008, month=6, day=9): "端午",
    datetime.date(year=2008, month=9, day=13): "中秋",
    datetime.date(year=2008, month=9, day=14): "中秋",
    datetime.date(year=2008, month=9, day=15): "中秋",
    datetime.date(year=2008, month=9, day=29): "国庆",
    datetime.date(year=2008, month=9, day=30): "国庆",
    datetime.date(year=2008, month=10, day=1): "国庆",
    datetime.date(year=2008, month=10, day=2): "国庆",
    datetime.date(year=2008, month=10, day=3): "国庆",
    datetime.date(year=2008, month=10, day=4): "国庆",
    datetime.date(year=2008, month=10, day=5): "国庆",
    datetime.date(year=2009, month=1, day=1): "元旦",
    datetime.date(year=2009, month=1, day=2): "元旦",
    datetime.date(year=2009, month=1, day=3): "元旦",
    datetime.date(year=2009, month=1, day=25): "春节",
    datetime.date(year=2009, month=1, day=26): "春节",
    datetime.date(year=2009, month=1, day=27): "春节",
    datetime.date(year=2009, month=1, day=28): "春节",
    datetime.date(year=2009, month=1, day=29): "春节",
    datetime.date(year=2009, month=1, day=30): "春节",
    datetime.date(year=2009, month=1, day=31): "春节",
    datetime.date(year=2009, month=4, day=4): "清明",
    datetime.date(year=2009, month=4, day=5): "清明",
    datetime.date(year=2009, month=4, day=6): "清明",
    datetime.date(year=2009, month=5, day=1): "五一",
    datetime.date(year=2009, month=5, day=2): "五一",
    datetime.date(year=2009, month=5, day=3): "五一",
    datetime.date(year=2009, month=5, day=28): "端午",
    datetime.date(year=2009, month=5, day=29): "端午",
    datetime.date(year=2009, month=5, day=30): "端午",
    datetime.date(year=2009, month=10, day=1): "国庆",
    datetime.date(year=2009, month=10, day=2): "国庆",
    datetime.date(year=2009, month=10, day=3): "中秋",
    datetime.date(year=2009, month=10, day=4): "国庆",
    datetime.date(year=2009, month=10, day=5): "国庆",
    datetime.date(year=2009, month=10, day=6): "国庆",
    datetime.date(year=2009, month=10, day=7): "国庆",
    datetime.date(year=2009, month=10, day=8): "国庆",
    datetime.date(year=2010, month=1, day=1): "元旦",
    datetime.date(year=2010, month=1, day=2): "元旦",
    datetime.date(year=2010, month=1, day=3): "元旦",
    datetime.date(year=2010, month=2, day=13): "春节",
    datetime.date(year=2010, month=2, day=14): "春节",
    datetime.date(year=2010, month=2, day=15): "春节",
    datetime.date(year=2010, month=2, day=16): "春节",
    datetime.date(year=2010, month=2, day=17): "春节",
    datetime.date(year=2010, month=2, day=18): "春节",
    datetime.date(year=2010, month=2, day=19): "春节",
    datetime.date(year=2010, month=4, day=3): "清明",
    datetime.date(year=2010, month=4, day=4): "清明",
    datetime.date(year=2010, month=4, day=5): "清明",
    datetime.date(year=2010, month=5, day=1): "五一",
    datetime.date(year=2010, month=5, day=2): "五一",
    datetime.date(year=2010, month=5, day=3): "五一",
    datetime.date(year=2010, month=6, day=14): "端午",
    datetime.date(year=2010, month=6, day=15): "端午",
    datetime.date(year=2010, month=6, day=16): "端午",
    datetime.date(year=2010, month=9, day=22): "中秋",
    datetime.date(year=2010, month=9, day=23): "中秋",
    datetime.date(year=2010, month=9, day=24): "中秋",
    datetime.date(year=2010, month=10, day=1): "国庆",
    datetime.date(year=2010, month=10, day=2): "国庆",
    datetime.date(year=2010, month=10, day=3): "国庆",
    datetime.date(year=2010, month=10, day=4): "国庆",
    datetime.date(year=2010, month=10, day=5): "国庆",
    datetime.date(year=2010, month=10, day=6): "国庆",
    datetime.date(year=2010, month=10, day=7): "国庆",
    datetime.date(year=2011, month=1, day=1): "元旦",
    datetime.date(year=2011, month=1, day=2): "元旦",
    datetime.date(year=2011, month=1, day=3): "元旦",
    datetime.date(year=2011, month=2, day=2): "春节",
    datetime.date(year=2011, month=2, day=3): "春节",
    datetime.date(year=2011, month=2, day=4): "春节",
    datetime.date(year=2011, month=2, day=5): "春节",
    datetime.date(year=2011, month=2, day=6): "春节",
    datetime.date(year=2011, month=2, day=7): "春节",
    datetime.date(year=2011, month=2, day=8): "春节",
    datetime.date(year=2011, month=4, day=3): "清明",
    datetime.date(year=2011, month=4, day=4): "清明",
    datetime.date(year=2011, month=4, day=5): "清明",
    datetime.date(year=2011, month=4, day=30): "五一",
    datetime.date(year=2011, month=5, day=1): "五一",
    datetime.date(year=2011, month=5, day=2): "五一",
    datetime.date(year=2011, month=6, day=4): "端午",
    datetime.date(year=2011, month=6, day=6): "端午",
    datetime.date(year=2011, month=9, day=10): "中秋",
    datetime.date(year=2011, month=9, day=11): "中秋",
    datetime.date(year=2011, month=9, day=12): "中秋",
    datetime.date(year=2011, month=10, day=1): "国庆",
    datetime.date(year=2011, month=10, day=2): "国庆",
    datetime.date(year=2011, month=10, day=3): "国庆",
    datetime.date(year=2011, month=10, day=4): "国庆",
    datetime.date(year=2011, month=10, day=5): "国庆",
    datetime.date(year=2011, month=10, day=6): "国庆",
    datetime.date(year=2011, month=10, day=7): "国庆",
    datetime.date(year=2012, month=1, day=1): "元旦",
    datetime.date(year=2012, month=1, day=2): "元旦",
    datetime.date(year=2012, month=1, day=3): "元旦",
    datetime.date(year=2012, month=1, day=22): "春节",
    datetime.date(year=2012, month=1, day=23): "春节",
    datetime.date(year=2012, month=1, day=24): "春节",
    datetime.date(year=2012, month=1, day=25): "春节",
    datetime.date(year=2012, month=1, day=26): "春节",
    datetime.date(year=2012, month=1, day=27): "春节",
    datetime.date(year=2012, month=1, day=28): "春节",
    datetime.date(year=2012, month=4, day=2): "清明",
    datetime.date(year=2012, month=4, day=3): "清明",
    datetime.date(year=2012, month=4, day=4): "清明",
    datetime.date(year=2012, month=4, day=29): "五一",
    datetime.date(year=2012, month=4, day=30): "五一",
    datetime.date(year=2012, month=5, day=1): "五一",
    datetime.date(year=2012, month=6, day=22): "端午",
    datetime.date(year=2012, month=6, day=24): "端午",
    datetime.date(year=2012, month=9, day=30): "中秋",
    datetime.date(year=2012, month=10, day=1): "国庆",
    datetime.date(year=2012, month=10, day=2): "国庆",
    datetime.date(year=2012, month=10, day=3): "国庆",
    datetime.date(year=2012, month=10, day=4): "国庆",
    datetime.date(year=2012, month=10, day=5): "国庆",
    datetime.date(year=2012, month=10, day=6): "国庆",
    datetime.date(year=2012, month=10, day=7): "国庆",
    datetime.date(year=2013, month=1, day=1): "元旦",
    datetime.date(year=2013, month=1, day=2): "元旦",
    datetime.date(year=2013, month=1, day=3): "元旦",
    datetime.date(year=2013, month=2, day=9): "春节",
    datetime.date(year=2013, month=2, day=10): "春节",
    datetime.date(year=2013, month=2, day=11): "春节",
    datetime.date(year=2013, month=2, day=12): "春节",
    datetime.date(year=2013, month=2, day=13): "春节",
    datetime.date(year=2013, month=2, day=14): "春节",
    datetime.date(year=2013, month=2, day=15): "春节",
    datetime.date(year=2013, month=4, day=4): "清明",
    datetime.date(year=2013, month=4, day=5): "清明",
    datetime.date(year=2013, month=4, day=6): "清明",
    datetime.date(year=2013, month=4, day=29): "五一",
    datetime.date(year=2013, month=4, day=30): "五一",
    datetime.date(year=2013, month=5, day=1): "五一",
    datetime.date(year=2013, month=6, day=10): "端午",
    datetime.date(year=2013, month=6, day=11): "端午",
    datetime.date(year=2013, month=6, day=12): "端午",
    datetime.date(year=2013, month=9, day=19): "中秋",
    datetime.date(year=2013, month=9, day=20): "中秋",
    datetime.date(year=2013, month=9, day=21): "中秋",
    datetime.date(year=2013, month=10, day=1): "国庆",
    datetime.date(year=2013, month=10, day=2): "国庆",
    datetime.date(year=2013, month=10, day=3): "国庆",
    datetime.date(year=2013, month=10, day=4): "国庆",
    datetime.date(year=2013, month=10, day=5): "国庆",
    datetime.date(year=2013, month=10, day=6): "国庆",
    datetime.date(year=2013, month=10, day=7): "国庆",
    datetime.date(year=2014, month=1, day=1): "元旦",
    datetime.date(year=2014, month=1, day=31): "春节",
    datetime.date(year=2014, month=2, day=1): "春节",
    datetime.date(year=2014, month=2, day=2): "春节",
    datetime.date(year=2014, month=2, day=3): "春节",
    datetime.date(year=2014, month=2, day=4): "春节",
    datetime.date(year=2014, month=2, day=5): "春节",
    datetime.date(year=2014, month=2, day=6): "春节",
    datetime.date(year=2014, month=4, day=5): "清明",
    datetime.date(year=2014, month=4, day=6): "清明",
    datetime.date(year=2014, month=4, day=7): "清明",
    datetime.date(year=2014, month=5, day=1): "五一",
    datetime.date(year=2014, month=5, day=2): "五一",
    datetime.date(year=2014, month=5, day=3): "五一",
    datetime.date(year=2014, month=6, day=2): "端午",
    datetime.date(year=2014, month=9, day=8): "中秋",
    datetime.date(year=2014, month=10, day=1): "国庆",
    datetime.date(year=2014, month=10, day=2): "国庆",
    datetime.date(year=2014, month=10, day=3): "国庆",
    datetime.date(year=2014, month=10, day=4): "国庆",
    datetime.date(year=2014, month=10, day=5): "国庆",
    datetime.date(year=2014, month=10, day=6): "国庆",
    datetime.date(year=2014, month=10, day=7): "国庆",
    datetime.date(year=2015, month=1, day=1): "元旦",
    datetime.date(year=2015, month=1, day=2): "元旦",
    datetime.date(year=2015, month=1, day=3): "元旦",
    datetime.date(year=2015, month=2, day=18): "春节",
    datetime.date(year=2015, month=2, day=19): "春节",
    datetime.date(year=2015, month=2, day=20): "春节",
    datetime.date(year=2015, month=2, day=21): "春节",
    datetime.date(year=2015, month=2, day=22): "春节",
    datetime.date(year=2015, month=2, day=23): "春节",
    datetime.date(year=2015, month=2, day=24): "春节",
    datetime.date(year=2015, month=4, day=5): "清明",
    datetime.date(year=2015, month=4, day=6): "清明",
    datetime.date(year=2015, month=5, day=1): "五一",
    datetime.date(year=2015, month=6, day=20): "端午",
    datetime.date(year=2015, month=6, day=22): "端午",
    datetime.date(year=2015, month=9, day=3): "抗战",
    datetime.date(year=2015, month=9, day=4): "抗战",
    datetime.date(year=2015, month=9, day=27): "中秋",
    datetime.date(year=2015, month=10, day=1): "国庆",
    datetime.date(year=2015, month=10, day=2): "国庆",
    datetime.date(year=2015, month=10, day=3): "国庆",
    datetime.date(year=2015, month=10, day=4): "国庆",
    datetime.date(year=2015, month=10, day=5): "国庆",
    datetime.date(year=2015, month=10, day=6): "国庆",
    datetime.date(year=2015, month=10, day=7): "国庆",
    datetime.date(year=2016, month=1, day=1): "元旦",
    datetime.date(year=2016, month=2, day=7): "春节",
    datetime.date(year=2016, month=2, day=8): "春节",
    datetime.date(year=2016, month=2, day=9): "春节",
    datetime.date(year=2016, month=2, day=10): "春节",
    datetime.date(year=2016, month=2, day=11): "春节",
    datetime.date(year=2016, month=2, day=12): "春节",
    datetime.date(year=2016, month=2, day=13): "春节",
    datetime.date(year=2016, month=4, day=4): "清明",
    datetime.date(year=2016, month=5, day=1): "五一",
    datetime.date(year=2016, month=5, day=2): "五一",
    datetime.date(year=2016, month=6, day=9): "端午",
    datetime.date(year=2016, month=6, day=10): "端午",
    datetime.date(year=2016, month=6, day=11): "端午",
    datetime.date(year=2016, month=9, day=15): "中秋",
    datetime.date(year=2016, month=9, day=16): "中秋",
    datetime.date(year=2016, month=9, day=17): "中秋",
    datetime.date(year=2016, month=10, day=1): "国庆",
    datetime.date(year=2016, month=10, day=2): "国庆",
    datetime.date(year=2016, month=10, day=3): "国庆",
    datetime.date(year=2016, month=10, day=4): "国庆",
    datetime.date(year=2016, month=10, day=5): "国庆",
    datetime.date(year=2016, month=10, day=6): "国庆",
    datetime.date(year=2016, month=10, day=7): "国庆",
    datetime.date(year=2017, month=1, day=1): "元旦",
    datetime.date(year=2017, month=1, day=2): "元旦",
    datetime.date(year=2017, month=1, day=27): "春节",
    datetime.date(year=2017, month=1, day=28): "春节",
    datetime.date(year=2017, month=1, day=29): "春节",
    datetime.date(year=2017, month=1, day=30): "春节",
    datetime.date(year=2017, month=1, day=31): "春节",
    datetime.date(year=2017, month=2, day=1): "春节",
    datetime.date(year=2017, month=2, day=2): "春节",
    datetime.date(year=2017, month=4, day=2): "清明",
    datetime.date(year=2017, month=4, day=3): "清明",
    datetime.date(year=2017, month=4, day=4): "清明",
    datetime.date(year=2017, month=5, day=1): "五一",
    datetime.date(year=2017, month=5, day=28): "端午",
    datetime.date(year=2017, month=5, day=29): "端午",
    datetime.date(year=2017, month=5, day=30): "端午",
    datetime.date(year=2017, month=10, day=1): "国庆",
    datetime.date(year=2017, month=10, day=2): "国庆",
    datetime.date(year=2017, month=10, day=3): "国庆",
    datetime.date(year=2017, month=10, day=4): "中秋",
    datetime.date(year=2017, month=10, day=5): "国庆",
    datetime.date(year=2017, month=10, day=6): "国庆",
    datetime.date(year=2017, month=10, day=7): "国庆",
    datetime.date(year=2017, month=10, day=8): "国庆",
    datetime.date(year=2018, month=1, day=1): "元旦",
    datetime.date(year=2018, month=2, day=15): "春节",
    datetime.date(year=2018, month=2, day=16): "春节",
    datetime.date(year=2018, month=2, day=17): "春节",
    datetime.date(year=2018, month=2, day=18): "春节",
    datetime.date(year=2018, month=2, day=19): "春节",
    datetime.date(year=2018, month=2, day=20): "春节",
    datetime.date(year=2018, month=2, day=21): "春节",
    datetime.date(year=2018, month=4, day=5): "清明",
    datetime.date(year=2018, month=4, day=6): "清明",
    datetime.date(year=2018, month=4, day=7): "清明",
    datetime.date(year=2018, month=4, day=29): "五一",
    datetime.date(year=2018, month=4, day=30): "五一",
    datetime.date(year=2018, month=5, day=1): "五一",
    datetime.date(year=2018, month=6, day=18): "端午",
    datetime.date(year=2018, month=9, day=24): "中秋",
    datetime.date(year=2018, month=10, day=1): "国庆",
    datetime.date(year=2018, month=10, day=2): "国庆",
    datetime.date(year=2018, month=10, day=3): "国庆",
    datetime.date(year=2018, month=10, day=4): "国庆",
    datetime.date(year=2018, month=10, day=5): "国庆",
    datetime.date(year=2018, month=10, day=6): "国庆",
    datetime.date(year=2018, month=10, day=7): "国庆",
    datetime.date(year=2018, month=12, day=30): "元旦",
    datetime.date(year=2018, month=12, day=31): "元旦",
    datetime.date(year=2019, month=1, day=1): "元旦",
    datetime.date(year=2019, month=2, day=4): "春节",
    datetime.date(year=2019, month=2, day=5): "春节",
    datetime.date(year=2019, month=2, day=6): "春节",
    datetime.date(year=2019, month=2, day=7): "春节",
    datetime.date(year=2019, month=2, day=8): "春节",
    datetime.date(year=2019, month=2, day=9): "春节",
    datetime.date(year=2019, month=2, day=10): "春节",
    datetime.date(year=2019, month=4, day=5): "清明",
    datetime.date(year=2019, month=4, day=6): "清明",
    datetime.date(year=2019, month=4, day=7): "清明",
    datetime.date(year=2019, month=5, day=1): "五一",
    datetime.date(year=2019, month=5, day=2): "五一",
    datetime.date(year=2019, month=5, day=3): "五一",
    datetime.date(year=2019, month=5, day=4): "五一",
    datetime.date(year=2019, month=6, day=7): "端午",
    datetime.date(year=2019, month=6, day=8): "端午",
    datetime.date(year=2019, month=6, day=9): "端午",
    datetime.date(year=2019, month=9, day=13): "中秋",
    datetime.date(year=2019, month=9, day=14): "中秋",
    datetime.date(year=2019, month=9, day=15): "中秋",
    datetime.date(year=2019, month=10, day=1): "国庆",
    datetime.date(year=2019, month=10, day=2): "国庆",
    datetime.date(year=2019, month=10, day=3): "国庆",
    datetime.date(year=2019, month=10, day=4): "国庆",
    datetime.date(year=2019, month=10, day=5): "国庆",
    datetime.date(year=2019, month=10, day=6): "国庆",
    datetime.date(year=2019, month=10, day=7): "国庆",
    datetime.date(year=2020, month=1, day=1): "元旦",
    datetime.date(year=2020, month=1, day=24): "春节",
    datetime.date(year=2020, month=1, day=25): "春节",
    datetime.date(year=2020, month=1, day=26): "春节",
    datetime.date(year=2020, month=1, day=27): "春节",
    datetime.date(year=2020, month=1, day=28): "春节",
    datetime.date(year=2020, month=1, day=29): "春节",
    datetime.date(year=2020, month=1, day=30): "春节",
    datetime.date(year=2020, month=1, day=31): "春节",
    datetime.date(year=2020, month=2, day=1): "春节",
    datetime.date(year=2020, month=2, day=2): "春节",
    datetime.date(year=2020, month=4, day=4): "清明",
    datetime.date(year=2020, month=4, day=5): "清明",
    datetime.date(year=2020, month=4, day=6): "清明",
    datetime.date(year=2020, month=5, day=1): "五一",
    datetime.date(year=2020, month=5, day=2): "五一",
    datetime.date(year=2020, month=5, day=3): "五一",
    datetime.date(year=2020, month=5, day=4): "五一",
    datetime.date(year=2020, month=5, day=5): "五一",
    datetime.date(year=2020, month=6, day=25): "端午",
    datetime.date(year=2020, month=6, day=26): "端午",
    datetime.date(year=2020, month=6, day=27): "端午",
    datetime.date(year=2020, month=10, day=1): "国庆",
    datetime.date(year=2020, month=10, day=2): "国庆",
    datetime.date(year=2020, month=10, day=3): "国庆",
    datetime.date(year=2020, month=10, day=4): "国庆",
    datetime.date(year=2020, month=10, day=5): "国庆",
    datetime.date(year=2020, month=10, day=6): "国庆",
    datetime.date(year=2020, month=10, day=7): "国庆",
    datetime.date(year=2020, month=10, day=8): "国庆",
    datetime.date(year=2021, month=1, day=1): "元旦",
    datetime.date(year=2021, month=1, day=2): "元旦",
    datetime.date(year=2021, month=1, day=3): "元旦",
    datetime.date(year=2021, month=2, day=11): "春节",
    datetime.date(year=2021, month=2, day=12): "春节",
    datetime.date(year=2021, month=2, day=13): "春节",
    datetime.date(year=2021, month=2, day=14): "春节",
    datetime.date(year=2021, month=2, day=15): "春节",
    datetime.date(year=2021, month=2, day=16): "春节",
    datetime.date(year=2021, month=2, day=17): "春节",
    datetime.date(year=2021, month=4, day=3): "清明",
    datetime.date(year=2021, month=4, day=4): "清明",
    datetime.date(year=2021, month=4, day=5): "清明",
    datetime.date(year=2021, month=5, day=1): "五一",
    datetime.date(year=2021, month=5, day=2): "五一",
    datetime.date(year=2021, month=5, day=3): "五一",
    datetime.date(year=2021, month=5, day=4): "五一",
    datetime.date(year=2021, month=5, day=5): "五一",
    datetime.date(year=2021, month=6, day=12): "端午",
    datetime.date(year=2021, month=6, day=13): "端午",
    datetime.date(year=2021, month=6, day=14): "端午",
    datetime.date(year=2021, month=9, day=19): "中秋",
    datetime.date(year=2021, month=9, day=20): "中秋",
    datetime.date(year=2021, month=9, day=21): "中秋",
    datetime.date(year=2021, month=10, day=1): "国庆",
    datetime.date(year=2021, month=10, day=2): "国庆",
    datetime.date(year=2021, month=10, day=3): "国庆",
    datetime.date(year=2021, month=10, day=4): "国庆",
    datetime.date(year=2021, month=10, day=5): "国庆",
    datetime.date(year=2021, month=10, day=6): "国庆",
    datetime.date(year=2021, month=10, day=7): "国庆",
    datetime.date(year=2022, month=1, day=1): "元旦",
    datetime.date(year=2022, month=1, day=2): "元旦",
    datetime.date(year=2022, month=1, day=3): "元旦",
    datetime.date(year=2022, month=1, day=31): "春节",
    datetime.date(year=2022, month=2, day=1): "春节",
    datetime.date(year=2022, month=2, day=2): "春节",
    datetime.date(year=2022, month=2, day=3): "春节",
    datetime.date(year=2022, month=2, day=4): "春节",
    datetime.date(year=2022, month=2, day=5): "春节",
    datetime.date(year=2022, month=2, day=6): "春节",
    datetime.date(year=2022, month=4, day=3): "清明",
    datetime.date(year=2022, month=4, day=4): "清明",
    datetime.date(year=2022, month=4, day=5): "清明",
    datetime.date(year=2022, month=4, day=30): "五一",
    datetime.date(year=2022, month=5, day=1): "五一",
    datetime.date(year=2022, month=5, day=2): "五一",
    datetime.date(year=2022, month=5, day=3): "五一",
    datetime.date(year=2022, month=5, day=4): "五一",
    datetime.date(year=2022, month=6, day=3): "端午",
    datetime.date(year=2022, month=6, day=4): "端午",
    datetime.date(year=2022, month=6, day=5): "端午",
    datetime.date(year=2022, month=9, day=10): "中秋",
    datetime.date(year=2022, month=9, day=11): "中秋",
    datetime.date(year=2022, month=9, day=12): "中秋",
    datetime.date(year=2022, month=10, day=1): "国庆",
    datetime.date(year=2022, month=10, day=2): "国庆",
    datetime.date(year=2022, month=10, day=3): "国庆",
    datetime.date(year=2022, month=10, day=4): "国庆",
    datetime.date(year=2022, month=10, day=5): "国庆",
    datetime.date(year=2022, month=10, day=6): "国庆",
    datetime.date(year=2022, month=10, day=7): "国庆",
    datetime.date(year=2022, month=12, day=31): "元旦",
    datetime.date(year=2023, month=1, day=1): "元旦",
    datetime.date(year=2023, month=1, day=2): "元旦",
    datetime.date(year=2023, month=1, day=21): "春节",
    datetime.date(year=2023, month=1, day=22): "春节",
    datetime.date(year=2023, month=1, day=23): "春节",
    datetime.date(year=2023, month=1, day=24): "春节",
    datetime.date(year=2023, month=1, day=25): "春节",
    datetime.date(year=2023, month=1, day=26): "春节",
    datetime.date(year=2023, month=1, day=27): "春节",
    datetime.date(year=2023, month=4, day=5): "清明",
    datetime.date(year=2023, month=4, day=29): "五一",
    datetime.date(year=2023, month=4, day=30): "五一",
    datetime.date(year=2023, month=5, day=1): "五一",
    datetime.date(year=2023, month=5, day=2): "五一",
    datetime.date(year=2023, month=5, day=3): "五一",
    datetime.date(year=2023, month=6, day=22): "端午",
    datetime.date(year=2023, month=6, day=23): "端午",
    datetime.date(year=2023, month=6, day=24): "端午",
    datetime.date(year=2023, month=9, day=29): "中秋",
    datetime.date(year=2023, month=9, day=30): "国庆",
    datetime.date(year=2023, month=10, day=1): "国庆",
    datetime.date(year=2023, month=10, day=2): "国庆",
    datetime.date(year=2023, month=10, day=3): "国庆",
    datetime.date(year=2023, month=10, day=4): "国庆",
    datetime.date(year=2023, month=10, day=5): "国庆",
    datetime.date(year=2023, month=10, day=6): "国庆",
    datetime.date(year=2024, month=1, day=1): "元旦",
    datetime.date(year=2024, month=2, day=10): "春节",
    datetime.date(year=2024, month=2, day=11): "春节",
    datetime.date(year=2024, month=2, day=12): "春节",
    datetime.date(year=2024, month=2, day=13): "春节",
    datetime.date(year=2024, month=2, day=14): "春节",
    datetime.date(year=2024, month=2, day=15): "春节",
    datetime.date(year=2024, month=2, day=16): "春节",
    datetime.date(year=2024, month=2, day=17): "春节",
    datetime.date(year=2024, month=4, day=4): "清明",
    datetime.date(year=2024, month=4, day=5): "清明",
    datetime.date(year=2024, month=4, day=6): "清明",
    datetime.date(year=2024, month=5, day=1): "五一",
    datetime.date(year=2024, month=5, day=2): "五一",
    datetime.date(year=2024, month=5, day=3): "五一",
    datetime.date(year=2024, month=5, day=4): "五一",
    datetime.date(year=2024, month=5, day=5): "五一",
    datetime.date(year=2024, month=6, day=10): "端午",
    datetime.date(year=2024, month=9, day=15): "中秋",
    datetime.date(year=2024, month=9, day=16): "中秋",
    datetime.date(year=2024, month=9, day=17): "中秋",
    datetime.date(year=2024, month=10, day=1): "国庆",
    datetime.date(year=2024, month=10, day=2): "国庆",
    datetime.date(year=2024, month=10, day=3): "国庆",
    datetime.date(year=2024, month=10, day=4): "国庆",
    datetime.date(year=2024, month=10, day=5): "国庆",
    datetime.date(year=2024, month=10, day=6): "国庆",
    datetime.date(year=2024, month=10, day=7): "国庆",
}

workdays = {
    datetime.date(year=2004, month=1, day=17): "春节调休",
    datetime.date(year=2004, month=1, day=18): "春节调休",
    datetime.date(year=2004, month=5, day=8): "五一调休",
    datetime.date(year=2004, month=5, day=9): "五一调休",
    datetime.date(year=2004, month=10, day=9): "国庆调休",
    datetime.date(year=2004, month=10, day=10): "国庆调休",
    datetime.date(year=2005, month=2, day=5): "春节调休",
    datetime.date(year=2005, month=2, day=6): "春节调休",
    datetime.date(year=2005, month=4, day=30): "五一调休",
    datetime.date(year=2005, month=5, day=8): "五一调休",
    datetime.date(year=2005, month=10, day=8): "国庆调休",
    datetime.date(year=2005, month=10, day=9): "国庆调休",
    datetime.date(year=2006, month=1, day=28): "春节调休",
    datetime.date(year=2006, month=2, day=5): "春节调休",
    datetime.date(year=2006, month=4, day=29): "五一调休",
    datetime.date(year=2006, month=4, day=30): "五一调休",
    datetime.date(year=2006, month=9, day=30): "国庆调休",
    datetime.date(year=2006, month=10, day=8): "国庆调休",
    datetime.date(year=2006, month=12, day=30): "元旦调休",
    datetime.date(year=2006, month=12, day=31): "元旦调休",
    datetime.date(year=2007, month=2, day=17): "春节调休",
    datetime.date(year=2007, month=2, day=25): "春节调休",
    datetime.date(year=2007, month=4, day=28): "五一调休",
    datetime.date(year=2007, month=4, day=29): "五一调休",
    datetime.date(year=2007, month=9, day=29): "国庆调休",
    datetime.date(year=2007, month=9, day=30): "国庆调休",
    datetime.date(year=2007, month=12, day=29): "元旦调休",
    datetime.date(year=2008, month=2, day=2): "春节调休",
    datetime.date(year=2008, month=2, day=3): "春节调休",
    datetime.date(year=2008, month=5, day=4): "五一调休",
    datetime.date(year=2008, month=9, day=27): "国庆调休",
    datetime.date(year=2008, month=9, day=28): "国庆调休",
    datetime.date(year=2009, month=1, day=4): "元旦调休",
    datetime.date(year=2009, month=1, day=24): "春节调休",
    datetime.date(year=2009, month=2, day=1): "春节调休",
    datetime.date(year=2009, month=5, day=31): "端午调休",
    datetime.date(year=2009, month=9, day=27): "国庆调休",
    datetime.date(year=2009, month=10, day=10): "国庆调休",
    datetime.date(year=2010, month=2, day=20): "春节调休",
    datetime.date(year=2010, month=2, day=21): "春节调休",
    datetime.date(year=2010, month=6, day=12): "端午调休",
    datetime.date(year=2010, month=6, day=13): "端午调休",
    datetime.date(year=2010, month=9, day=19): "中秋调休",
    datetime.date(year=2010, month=9, day=25): "中秋调休",
    datetime.date(year=2010, month=9, day=26): "国庆调休",
    datetime.date(year=2010, month=10, day=9): "国庆调休",
    datetime.date(year=2011, month=1, day=30): "春节调休",
    datetime.date(year=2011, month=2, day=12): "春节调休",
    datetime.date(year=2011, month=4, day=2): "清明调休",
    datetime.date(year=2011, month=10, day=8): "国庆调休",
    datetime.date(year=2011, month=10, day=9): "国庆调休",
    datetime.date(year=2011, month=12, day=31): "元旦调休",
    datetime.date(year=2012, month=1, day=21): "春节调休",
    datetime.date(year=2012, month=1, day=29): "春节调休",
    datetime.date(year=2012, month=3, day=31): "清明调休",
    datetime.date(year=2012, month=4, day=1): "清明调休",
    datetime.date(year=2012, month=4, day=28): "五一调休",
    datetime.date(year=2012, month=9, day=29): "国庆调休",
    datetime.date(year=2013, month=1, day=5): "元旦调休",
    datetime.date(year=2013, month=1, day=6): "元旦调休",
    datetime.date(year=2013, month=2, day=16): "春节调休",
    datetime.date(year=2013, month=2, day=17): "春节调休",
    datetime.date(year=2013, month=4, day=7): "清明调休",
    datetime.date(year=2013, month=4, day=27): "五一调休",
    datetime.date(year=2013, month=4, day=28): "五一调休",
    datetime.date(year=2013, month=6, day=8): "端午调休",
    datetime.date(year=2013, month=6, day=9): "端午调休",
    datetime.date(year=2013, month=9, day=22): "中秋调休",
    datetime.date(year=2013, month=9, day=29): "国庆调休",
    datetime.date(year=2013, month=10, day=12): "国庆调休",
    datetime.date(year=2014, month=1, day=26): "春节调休",
    datetime.date(year=2014, month=2, day=8): "春节调休",
    datetime.date(year=2014, month=5, day=4): "五一调休",
    datetime.date(year=2014, month=9, day=28): "国庆调休",
    datetime.date(year=2014, month=10, day=11): "国庆调休",
    datetime.date(year=2015, month=1, day=4): "元旦调休",
    datetime.date(year=2015, month=2, day=15): "春节调休",
    datetime.date(year=2015, month=2, day=28): "春节调休",
    datetime.date(year=2015, month=9, day=6): "抗战调休",
    datetime.date(year=2015, month=10, day=10): "国庆调休",
    datetime.date(year=2016, month=2, day=6): "春节调休",
    datetime.date(year=2016, month=2, day=14): "春节调休",
    datetime.date(year=2016, month=6, day=12): "端午调休",
    datetime.date(year=2016, month=9, day=18): "中秋调休",
    datetime.date(year=2016, month=10, day=8): "国庆调休",
    datetime.date(year=2016, month=10, day=9): "国庆调休",
    datetime.date(year=2017, month=1, day=22): "春节调休",
    datetime.date(year=2017, month=2, day=4): "春节调休",
    datetime.date(year=2017, month=4, day=1): "清明调休",
    datetime.date(year=2017, month=5, day=27): "端午调休",
    datetime.date(year=2017, month=9, day=30): "国庆调休",
    datetime.date(year=2018, month=2, day=11): "春节调休",
    datetime.date(year=2018, month=2, day=24): "春节调休",
    datetime.date(year=2018, month=4, day=8): "清明调休",
    datetime.date(year=2018, month=4, day=28): "五一调休",
    datetime.date(year=2018, month=9, day=29): "国庆调休",
    datetime.date(year=2018, month=9, day=30): "国庆调休",
    datetime.date(year=2018, month=12, day=29): "元旦调休",
    datetime.date(year=2019, month=2, day=2): "春节调休",
    datetime.date(year=2019, month=2, day=3): "春节调休",
    datetime.date(year=2019, month=4, day=28): "五一调休",
    datetime.date(year=2019, month=5, day=5): "五一调休",
    datetime.date(year=2019, month=9, day=29): "国庆调休",
    datetime.date(year=2019, month=10, day=12): "国庆调休",
    datetime.date(year=2020, month=1, day=19): "春节调休",
    datetime.date(year=2020, month=4, day=26): "五一调休",
    datetime.date(year=2020, month=5, day=9): "五一调休",
    datetime.date(year=2020, month=6, day=28): "端午调休",
    datetime.date(year=2020, month=9, day=27): "国庆调休",
    datetime.date(year=2020, month=10, day=10): "国庆调休",
    datetime.date(year=2021, month=2, day=7): "春节调休",
    datetime.date(year=2021, month=2, day=20): "春节调休",
    datetime.date(year=2021, month=4, day=25): "五一调休",
    datetime.date(year=2021, month=5, day=8): "五一调休",
    datetime.date(year=2021, month=9, day=18): "中秋调休",
    datetime.date(year=2021, month=9, day=26): "国庆调休",
    datetime.date(year=2021, month=10, day=9): "国庆调休",
    datetime.date(year=2022, month=1, day=29): "春节调休",
    datetime.date(year=2022, month=1, day=30): "春节调休",
    datetime.date(year=2022, month=4, day=2): "清明调休",
    datetime.date(year=2022, month=4, day=24): "五一调休",
    datetime.date(year=2022, month=5, day=7): "五一调休",
    datetime.date(year=2022, month=10, day=8): "国庆调休",
    datetime.date(year=2022, month=10, day=9): "国庆调休",
    datetime.date(year=2023, month=1, day=28): "春节调休",
    datetime.date(year=2023, month=1, day=29): "春节调休",
    datetime.date(year=2023, month=4, day=23): "五一调休",
    datetime.date(year=2023, month=5, day=6): "五一调休",
    datetime.date(year=2023, month=6, day=25): "端午调休",
    datetime.date(year=2023, month=10, day=7): "国庆调休",
    datetime.date(year=2023, month=10, day=8): "国庆调休",
    datetime.date(year=2024, month=2, day=4): "春节调休",
    datetime.date(year=2024, month=2, day=18): "春节调休",
    datetime.date(year=2024, month=4, day=7): "清明调休",
    datetime.date(year=2024, month=4, day=28): "五一调休",
    datetime.date(year=2024, month=5, day=11): "五一调休",
    datetime.date(year=2024, month=9, day=14): "中秋调休",
    datetime.date(year=2024, month=9, day=29): "国庆调休",
    datetime.date(year=2024, month=10, day=12): "国庆调休",
}

_preholidays = {
    datetime.date(year=2018, month=2, day=8): "春节准备",
    datetime.date(year=2018, month=2, day=9): "春节准备",
    datetime.date(year=2018, month=2, day=10): "春节准备",
    datetime.date(year=2018, month=2, day=11): "春节准备",
    datetime.date(year=2018, month=2, day=12): "春节准备",
    datetime.date(year=2018, month=2, day=13): "春节准备",
    datetime.date(year=2018, month=2, day=14): "春节准备",
    datetime.date(year=2019, month=1, day=28): "春节准备",
    datetime.date(year=2019, month=1, day=29): "春节准备",
    datetime.date(year=2019, month=1, day=30): "春节准备",
    datetime.date(year=2019, month=1, day=31): "春节准备",
    datetime.date(year=2019, month=2, day=1): "春节准备",
    datetime.date(year=2019, month=2, day=2): "春节准备",
    datetime.date(year=2019, month=2, day=3): "春节准备",
    datetime.date(year=2020, month=1, day=17): "春节准备",
    datetime.date(year=2020, month=1, day=18): "春节准备",
    datetime.date(year=2020, month=1, day=19): "春节准备",
    datetime.date(year=2020, month=1, day=20): "春节准备",
    datetime.date(year=2020, month=1, day=21): "春节准备",
    datetime.date(year=2020, month=1, day=22): "春节准备",
    datetime.date(year=2020, month=1, day=23): "春节准备",
    datetime.date(year=2021, month=2, day=4): "春节准备",
    datetime.date(year=2021, month=2, day=5): "春节准备",
    datetime.date(year=2021, month=2, day=6): "春节准备",
    datetime.date(year=2021, month=2, day=7): "春节准备",
    datetime.date(year=2021, month=2, day=8): "春节准备",
    datetime.date(year=2021, month=2, day=9): "春节准备",
    datetime.date(year=2021, month=2, day=10): "春节准备",
    datetime.date(year=2022, month=1, day=24): "春节准备",
    datetime.date(year=2022, month=1, day=25): "春节准备",
    datetime.date(year=2022, month=1, day=26): "春节准备",
    datetime.date(year=2022, month=1, day=27): "春节准备",
    datetime.date(year=2022, month=1, day=28): "春节准备",
    datetime.date(year=2022, month=1, day=29): "春节准备",
    datetime.date(year=2022, month=1, day=30): "春节准备",
    datetime.date(year=2023, month=1, day=14): "春节准备",
    datetime.date(year=2023, month=1, day=15): "春节准备",
    datetime.date(year=2023, month=1, day=16): "春节准备",
    datetime.date(year=2023, month=1, day=17): "春节准备",
    datetime.date(year=2023, month=1, day=18): "春节准备",
    datetime.date(year=2023, month=1, day=19): "春节准备",
    datetime.date(year=2023, month=1, day=20): "春节准备",
    datetime.date(year=2024, month=2, day=2): "春节准备",
    datetime.date(year=2024, month=2, day=3): "春节准备",
    datetime.date(year=2024, month=2, day=4): "春节准备",
    datetime.date(year=2024, month=2, day=5): "春节准备",
    datetime.date(year=2024, month=2, day=6): "春节准备",
    datetime.date(year=2024, month=2, day=7): "春节准备",
    datetime.date(year=2024, month=2, day=8): "春节准备",
    datetime.date(year=2024, month=2, day=9): "春节准备",
}

def mark_holidays(x):
    """对df日期列(series)返回其对应的节日、调休日、预备日的三个列"""
    a = x.apply(lambda x : _holidays.get(x))
    b = x.apply(lambda x : _workdays.get(x))
    c = x.apply(lambda x : _preholidays.get(x))
    return a,b,c
