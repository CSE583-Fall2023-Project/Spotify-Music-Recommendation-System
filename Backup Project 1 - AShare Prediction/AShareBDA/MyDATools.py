#!/usr/bin/env python
# coding: utf-8

# In[1]:


# myDATools包


# # 依赖包的导入

# In[2]:


import numpy as np
import pandas as pd
import gc
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV


# # 读取数据

# In[3]:


#功能：读取三大报表类（资产负债表、利润表、现金流量表）数据
#思路：按照excel的sheet_name，读取三大报表类数据中银行、证券、保险、一般工商业数据

class ExcelReader:
    "读取三大报表类"
    def __init__(self, path=None):
        self.path = path
        self.dataAll = pd.read_excel(path,sheet_name=['General Business','Bank','Securities','Insurance'],
                                     converters={'TICKER_SYMBOL':str,'PARTY_ID':str})

    def getGB(self):
        data_part = pd.DataFrame(self.dataAll['General Business'])
        return(data_part)

    def getBank(self):
        data_part = pd.DataFrame(self.dataAll['Bank'])
        return(data_part)

    def getSecu(self):
        data_part = pd.DataFrame(self.dataAll['Securities'])
        return(data_part)

    def getInsu(self):
        data_part = pd.DataFrame(self.dataAll['Insurance'])
        return(data_part)


# # 增加时间特征（属性）

# In[4]:


#功能：提取并增设两个列——year和month，month
#思路：将年份和按计算周期（DATETIME_UNITS）转换的月份加到原数据表

def addDateTimeFeatures(df_s,date_column,DATETIME_UNITS):
    
    #提取年份year特征 
    df_s['year'] = df_s[date_column].map(lambda x:x.year)
    
    #提取月份month特征
    df_st = pd.DataFrame({'MONTH':df_s[date_column].astype(str).apply(lambda x:x[5:7])})
    
    #生成月份、季度、年份和半年的对应关系表
    df_dict = pd.DataFrame({'MONTH':['01','02','03','04','05','06','07','08','09','10','11','12'],
                            'QUARTER':['03','03','03','06','06','06','09','09','09','12','12','12'],
                           'HALF':['06','06','06','06','06','06','12','12','12','12','12','12'],
                           'YEAR':['12','12','12','12','12','12','12','12','12','12','12','12']})
    
    #合并df_month和 df_calendar
    df_output = pd.merge(df_st,df_dict,how='left')
    
    df_s = df_s.reset_index()
    
    #新增month 列    
    df_s['month'] = df_output[DATETIME_UNITS]
    
    return(df_s)


# # 数据规整化处理

# ## 宏观经济和产业数据表的规整化处理

# In[5]:


#功能：宏观经济和产业数据表的规整化处理
#思路：通过读取宏观数据与行业数据，按统计周期匹配出年月、按平均汇总、通过行转列等操作，产生宏观数据

def tidyMacroAndIndustryData(filename,DATETIME_UNITS):
        
    #读取MacroIndustry的sheet ——INDIC_DATA
    df_indus = pd.DataFrame(pd.read_excel(filename,sheet_name=['INDIC_DATA'])['INDIC_DATA'])
    
    #字段名称统一改为大写
    df_indus.columns = [x.upper() for x in df_indus.columns]
    
    #原表中新增 year 和 mongth两个列
    df_indus = addDateTimeFeatures(df_indus,'PERIOD_DATE',DATETIME_UNITS)
     
    #生成分组统计df_indus_g    
    df_indus_g =  df_indus.groupby(['INDIC_ID','year','month'])[['DATA_VALUE']].mean().reset_index()
    
    #数据类型的转换
    df_indus_g['INDIC_ID'] = df_indus_g['INDIC_ID'].astype(str)
     
    #生成透视表
    df_indus_g = df_indus_g.pivot_table(index=['year','month'],
                                        columns=["INDIC_ID"],
                                        values=["DATA_VALUE"]).reset_index()
    #将二级索引改为一级索引
    df_indus_g.columns = [ ''.join(col) for col in df_indus_g.columns.values]
    
    #缺失值的填充
    df_indus_g = df_indus_g.fillna(method='bfill')
    
    return(df_indus_g)


# ## 公司运营数据的规整化处理

# In[6]:


#功能：公司运营数据的规整化处理

def tidyCompOperatingData(filename,DATETIME_UNITS):
    
    #读取数据
    df_comp = pd.DataFrame(pd.read_excel(filename,
                                         sheet_name=['EN'],
                                         converters={'TICKER_SYMBOL':str,'PARTY_ID':str})['EN'])
    
    #读取列名
    df_comp.columns = [x.lstrip().rstrip() for x in df_comp.columns] 
    
    #按周期新增year列和Month列
    df_comp = addDateTimeFeatures(df_comp,'END_DATE',DATETIME_UNITS)
    
    #分组统计
    df_comp_g =  df_comp.groupby(['TICKER_SYMBOL','INDIC_NAME_EN','year','month'])        [['VALUE']].        sum().        reset_index()
    
    #改为分类变量
    f_indic = pd.factorize(df_comp_g['INDIC_NAME_EN'])
    
    #新增列——指标名称'INDIC_NAME_ID'
    df_comp_g['INDIC_NAME_ID'] ="COMP"+ pd.Series(f_indic[0]).astype(str)
    
    #定义透视表
    df_comp_g = df_comp_g.pivot_table(index=['TICKER_SYMBOL','year','month'],
                                      columns=["INDIC_NAME_ID"],
                                      values=["VALUE"]).reset_index()
   
    #处理列名
    df_comp_g.columns = [ ''.join(col) for col in df_comp_g.columns.values]
    
    #填充缺失值
    df_comp_g = df_comp_g.fillna(0)
    
    return(df_comp_g)


# In[7]:


#功能：股票数据的规整化处理
#思路：生成由以下列组成的数据表:TICKER_SYMBOL，year,month，CLOSE_PRICE，TURNOVER_VOL，TURNOVER_VALUE，MARKET_VALUE

def tidyShareData(filename,DATETIME_UNITS):

    #读取数据
    df_shares = pd.DataFrame(pd.read_excel(filename,
                                           sheet_name=['DATA'],
                                           converters={'TICKER_SYMBOL':str,'PARTY_ID':str})['DATA'])
    
    #选择特征列
    df_shares = df_shares[['TICKER_SYMBOL','END_DATE_','CLOSE_PRICE','TURNOVER_VOL','TURNOVER_VALUE','MARKET_VALUE']]
    
    df_shares.columns = ['TICKER_SYMBOL','END_DATE','CLOSE_PRICE','TURNOVER_VOL','TURNOVER_VALUE','MARKET_VALUE']
    
    #将'END_DATE'一列的类型改为日期类型
    df_shares['END_DATE'] = pd.to_datetime(df_shares['END_DATE'])
    
    #增加时间特征列
    df_shares = addDateTimeFeatures(df_shares,'END_DATE',DATETIME_UNITS)
    
    #分组统计
    df_shares_g =  df_shares.groupby(['TICKER_SYMBOL','year','month'])        [['CLOSE_PRICE','TURNOVER_VOL','TURNOVER_VALUE','MARKET_VALUE']].        mean().        reset_index()
    
    return(df_shares_g)


# In[8]:


#功能：资产负债表和利润表的合并与规整化处理

def tidyBalanceAndIncomeData(df_BalanceSheet,df_IncomeStatement):
     
    #缺失值的处理
    df_BalanceSheet.loc[:, df_BalanceSheet.dtypes == 'float64'] =         df_BalanceSheet.loc[:, df_BalanceSheet.dtypes == "float64"].fillna(0.00001)
    
    #样本选择
    df_BalanceSheet = df_BalanceSheet[(df_BalanceSheet.MERGED_FLAG == 1)]
    
    #特征选择
        #PARTY_ID_机构内部ID，END_DATE_REP_报告截止日期，REPORT_TYPE_报告类型
    df_BalanceSheet = df_BalanceSheet[df_BalanceSheet.columns.drop(["PARTY_ID", "END_DATE_REP", "REPORT_TYPE"])]
   
    #样本排序
        #TICKER_SYMBOL_股票代码，PUBLISH_DATE_发布时间，END_DATE_截止日期
    df_BalanceSheet = df_BalanceSheet.sort_values(by = ['TICKER_SYMBOL', 'PUBLISH_DATE', 'END_DATE'], ascending = False)
    
    #重复过滤
    df_BalanceSheet = df_BalanceSheet.drop_duplicates(['TICKER_SYMBOL', 'END_DATE'], keep='first')
    
    #转换数据类型
    df_BalanceSheet["END_DATE"] =pd.to_datetime(df_BalanceSheet["END_DATE"])
    
    #重复过滤
    df_BalanceSheet = df_BalanceSheet.drop_duplicates()


    ##定义资产分类表_ASSET_CATEGORIES
    ASSET_CATEGORIES=pd.DataFrame({'ORIGINAL_COLUMN_NAMES':["C_RESER_CB","DEPOS_IN_OTH_BFI","PRECI_METALS","LOAN_TO_OTH_BANK_FI","TRADING_FA","DERIV_ASSETS","PUR_RESALE_FA","INT_RECEIV","DISBUR_LA","FINAN_LEASE_RECEIV","AVAIL_FOR_SALE_FA","HTM_INVEST","INVEST_AS_RECEIV","LT_EQUITY_INVEST","INVEST_REAL_ESTATE","FIXED_ASSETS","CIP","INTAN_ASSETS","GOODWILL","DEFER_TAX_ASSETS","OTH_ASSETS","AE","AA"],
                                  'ASSET_CLASS':["CRASH_ASSETS","CRASH_ASSETS","INVEST_ASSETS","CRASH_ASSETS","INVEST_ASSETS","INVEST_ASSETS","INVEST_ASSETS","INVEST_ASSETS","LOANS_ASSETS","LOANS_ASSETS","INVEST_ASSETS","INVEST_ASSETS","LOANS_ASSETS","INVEST_ASSETS","INVEST_ASSETS","OPERATION_ASSET","OPERATION_ASSET","OPERATION_ASSET","OPERATION_ASSET","OPERATION_ASSET","OPERATION_ASSET","OPERATION_ASSET","OPERATION_ASSET"]})


    #显式列名清单
    temp = ASSET_CATEGORIES['ORIGINAL_COLUMN_NAMES'].values

    #在列名清单中增加两个列'TICKER_SYMBOL', 'END_DATE'
    temp = np.append(temp, ['TICKER_SYMBOL', 'END_DATE'])
    
    #按照新的列名清单对数据框df_BalanceSheet_Bank进行切片处理
    temp = df_BalanceSheet[temp]

    ##改变df_BalanceSheet_Bank1的形状，id为'TICKER_SYMBOL', 'END_DATE'
    temp = pd.melt(temp, 
                   id_vars=['TICKER_SYMBOL', 'END_DATE'],
                   var_name='ORIGINAL_COLUMN_NAMES',
                   value_name='valuenum')

    #合并df_BalanceSheet_Bank2和 ASSET_CATEGORIES
    temp = pd.merge(temp, ASSET_CATEGORIES, how='left', on='ORIGINAL_COLUMN_NAMES')

    #按资产类型分组统计
    temp = temp.groupby(['TICKER_SYMBOL','END_DATE', 'ASSET_CLASS'], as_index=False)['valuenum'].sum()
    
    #产生分组统计的透视表
    temp = (temp.pivot_table(index=['TICKER_SYMBOL','END_DATE'], 
                             columns='ASSET_CLASS', 
                             values='valuenum').reset_index())


    #读取数值型列
    temp1_name=df_BalanceSheet.columns[df_BalanceSheet.dtypes=='float64']
    temp1=df_BalanceSheet[temp1_name]

    #读取两列——'TICKER_SYMBOL','END_DATE'的值
    temp1_label=df_BalanceSheet[['TICKER_SYMBOL','END_DATE']]

    #每一类资产在总资产的占比
    temp1_T_ASSETS=np.array([[w]*temp1.shape[1] for w in temp1.T_ASSETS])
    temp1_T_ASSETS=temp1/temp1_T_ASSETS
    
    #删除两列——T_ASSETS和T_LIAB_EQUITY
    temp1_T_ASSETS=temp1_T_ASSETS[temp1_T_ASSETS.columns.drop(['T_ASSETS','T_LIAB_EQUITY'])]
    
    #每个列名前加前缀T_ASSETS
    temp1_T_ASSETS.columns=np.char.add('T_ASSETS_',list(temp1_T_ASSETS.columns))
    
    ## 合并id和values列，即 Percentage_OF_TotalAseets 和 df_BalanceSheet_Bank_idcolumns
    temp1_T_ASSETS=pd.concat([temp1_label,temp1_T_ASSETS],axis=1)

    temp1_T_ASSETS.columns.value_counts()

    #所有列/字段在总负债的占比
    temp1_T_LIAB=np.array([[w]*temp1.shape[1] for w in temp1.T_LIAB])
    temp1_T_LIAB=temp1/temp1_T_LIAB
    temp1_T_LIAB=temp1_T_LIAB[temp1_T_LIAB.columns.drop(['T_LIAB','T_LIAB_EQUITY'])]
    temp1_T_LIAB.columns=np.char.add('T_LIAB_',list(temp1_T_LIAB.columns))
    temp1_T_LIAB=pd.concat([temp1_label,temp1_T_LIAB],axis=1)

    #所有字段在所有者权益的占比
    temp1_T_SH_EQUITY=np.array([[w]*temp1.shape[1] for w in temp1.T_SH_EQUITY])
    temp1_T_SH_EQUITY=temp1/temp1_T_SH_EQUITY
    temp1_T_SH_EQUITY=temp1_T_SH_EQUITY[temp1_T_SH_EQUITY.columns.drop(['T_SH_EQUITY','T_LIAB_EQUITY'])]
    temp1_T_SH_EQUITY.columns=np.char.add('T_SH_EQUITY_',list(temp1_T_SH_EQUITY.columns))

    temp1_T_SH_EQUITY=pd.concat([temp1_label,temp1_T_SH_EQUITY],axis=1)



    #合并基础资产表以及资产分类表
    df_BalanceSheet = pd.merge(df_BalanceSheet, temp, how='left', on=["TICKER_SYMBOL","END_DATE"])

    
    #功能：计算增速
    #思路：构建计算增速特征的函数，根据shiftnum的取值，计算各季度增速
    def growthcal(data, shiftnum, groupcol, igcol):
        datacolname = list(data.columns)
        igcol = np.append(groupcol, igcol)
        colname_need_cal = [x for x in datacolname if x not in igcol]
        results = data.loc[:, groupcol]
        for i in colname_need_cal:
            calcol = np.append(groupcol, i)
            columndel = np.append(i, 'B_shifted')
            temp = data.loc[:, calcol]
            temp2 = temp.copy()
            temp.END_DATE = temp.END_DATE + pd.DateOffset(months = shiftnum)
            temp.columns = np.append(groupcol, ['B_shifted'])
            uu = temp.loc[(temp['END_DATE'].dt.month == 12) & (temp['END_DATE'].dt.day == 30), ]
            if len(uu) > 0 :
                temp.loc[(temp['END_DATE'].dt.month == 12) & (temp['END_DATE'].dt.day == 30), 'END_DATE'] = temp.loc[(temp['END_DATE'].dt.month == 12) & (temp['END_DATE'].dt.day==30), 'END_DATE'] + pd.DateOffset(days = 1)
            uu = temp.loc[(temp['END_DATE'].dt.month == 3) & (temp['END_DATE'].dt.day == 30), 'END_DATE']
            if len(uu) > 0 :
                temp.loc[(temp['END_DATE'].dt.month == 3) & (temp['END_DATE'].dt.day == 30), 'END_DATE'] = temp.loc[(temp['END_DATE'].dt.month == 3) & (temp['END_DATE'].dt.day==30), 'END_DATE'] + pd.DateOffset(days = 1)
            temp2 = pd.merge(temp2, temp, how='left', on=["TICKER_SYMBOL","END_DATE"])
            growthname = [i + '_GROWTH' + str(shiftnum)]
            growthname = growthname[0]
            temp2[growthname] = temp2[i].squeeze() / temp2.B_shifted -1
            temp2.drop(columndel, axis=1, inplace=True)
            results = pd.merge(results, temp2, how='left', on=["TICKER_SYMBOL","END_DATE"])
        return results

    ##FISCAL_PERIOD_会计区间，MERGED_FLAG_合并标志，PUBLISH_DATE_发布时间，EXCHANGE_CD_交易市场代码
    #计算同比增速
    bsgrowth12 = growthcal(data = df_BalanceSheet, shiftnum = 12,
                       groupcol = ['TICKER_SYMBOL', 'END_DATE'],
                       igcol = ['EXCHANGE_CD', 'PUBLISH_DATE', 'FISCAL_PERIOD', 'MERGED_FLAG'])
    #计算同三个季度的增速
    bsgrowth9 = growthcal(data = df_BalanceSheet, shiftnum = 9,
                       groupcol = ['TICKER_SYMBOL', 'END_DATE'],
                       igcol = ['EXCHANGE_CD', 'PUBLISH_DATE', 'FISCAL_PERIOD', 'MERGED_FLAG'])
    #计算半年同比增速
    bsgrowth6 = growthcal(data = df_BalanceSheet, shiftnum = 6,
                       groupcol = ['TICKER_SYMBOL', 'END_DATE'],
                       igcol = ['EXCHANGE_CD', 'PUBLISH_DATE', 'FISCAL_PERIOD', 'MERGED_FLAG'])
    #计算环比增速
    bsgrowth3 = growthcal(data = df_BalanceSheet, shiftnum = 3,
                       groupcol = ['TICKER_SYMBOL', 'END_DATE'],
                       igcol = ['EXCHANGE_CD', 'PUBLISH_DATE', 'FISCAL_PERIOD', 'MERGED_FLAG'])




    #利润表的处理
    
    df_IncomeStatement.loc[:, df_IncomeStatement.dtypes == 'float64'] =         df_IncomeStatement.loc[:, df_IncomeStatement.dtypes == "float64"].fillna(0.00001)

    df_IncomeStatement = df_IncomeStatement[(df_IncomeStatement.MERGED_FLAG == 1)]

    df_IncomeStatement = df_IncomeStatement[df_IncomeStatement.columns.drop(["PARTY_ID", "END_DATE_REP", "REPORT_TYPE"])]

    df_IncomeStatement = df_IncomeStatement.sort_values(by = ['TICKER_SYMBOL', 'PUBLISH_DATE', 'END_DATE'],
                                                        ascending = False)

    df_IncomeStatement = df_IncomeStatement.drop_duplicates(['TICKER_SYMBOL', 'END_DATE'],
                                                            keep='first')

    df_IncomeStatement = df_IncomeStatement[df_IncomeStatement.columns.drop(["EXCHANGE_CD", "PUBLISH_DATE", "FISCAL_PERIOD", "MERGED_FLAG"])]



    df_IncomeStatement['year'] = df_IncomeStatement.END_DATE.str.slice(start = 0, stop = 4)

    df_IncomeStatement['month'] = df_IncomeStatement.END_DATE.str.slice(start = 5, stop = 7)

    df_IncomeStatement = df_IncomeStatement.drop_duplicates()





    df_IncomeStatement_Q = pd.melt(df_IncomeStatement, 
                                   id_vars=['TICKER_SYMBOL', 'END_DATE', "year", "month"],
                                   var_name='ORIGINAL_COLUMN_NAMES',
                                   value_name='valuenum')
    
    df_IncomeStatement_Q["END_DATE"] = df_IncomeStatement_Q["END_DATE"].astype("datetime64[ns]")


    df_IncomeStatement_Q = df_IncomeStatement_Q.sort_values(by = ['TICKER_SYMBOL', 'ORIGINAL_COLUMN_NAMES', 'END_DATE'],
                                                            ascending = True)

    
    new_column = df_IncomeStatement_Q.groupby(['TICKER_SYMBOL','ORIGINAL_COLUMN_NAMES', 'year'],
                                              as_index=False)['valuenum'].diff()

    df_IncomeStatement_Q["diffs"] = new_column.reset_index(level=0, drop=True)

    df_IncomeStatement_Q["Qvaluenum"] = df_IncomeStatement_Q.diffs.fillna(df_IncomeStatement_Q.valuenum)

    df_IncomeStatement_Q = df_IncomeStatement_Q[df_IncomeStatement_Q.columns.drop(['valuenum', 'diffs'])]

    df_IncomeStatement_Q = (df_IncomeStatement_Q.pivot_table(index=['TICKER_SYMBOL','END_DATE', "year", "month"], columns='ORIGINAL_COLUMN_NAMES', values='Qvaluenum').reset_index())

    df_IncomeStatement_Q  = df_IncomeStatement_Q.sort_values(by = ['TICKER_SYMBOL', 'END_DATE'],ascending = True)


    ab_names=list(df_IncomeStatement_Q.columns)
    ab_names=[i+'_Q1' for i in ab_names if i not in ['TICKER_SYMBOL','END_DATE', "year", "month"]]
    ab_names = np.append(['TICKER_SYMBOL','END_DATE', "year", "month"],ab_names)
    df_IncomeStatement_Q.columns = ab_names


    df_IncomeStatement["END_DATE"] = df_IncomeStatement["END_DATE"].astype("datetime64[ns]")

    df_IncomeStatement_Q=pd.merge(df_IncomeStatement_Q,df_IncomeStatement, 
                                  how='left',
                                  on=['TICKER_SYMBOL','END_DATE', "year", "month"])


    #银行数据合并--资产负债以及利润表
    temp_data=pd.merge(df_BalanceSheet,temp1_T_ASSETS, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,temp1_T_LIAB, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,temp1_T_SH_EQUITY, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,bsgrowth3, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,bsgrowth6, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,bsgrowth9, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,bsgrowth12, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=pd.merge(temp_data,df_IncomeStatement_Q, how='left', on=["TICKER_SYMBOL","END_DATE"])

    temp_data=temp_data.fillna(0)


    del temp1_T_ASSETS
    del temp1_T_LIAB
    del temp1_T_SH_EQUITY
    del bsgrowth3
    del bsgrowth6
    del bsgrowth9
    del bsgrowth12
    del df_IncomeStatement_Q


    df_IncomeStatement=temp_data
    
    df_IncomeStatement=df_IncomeStatement.fillna(0)


    df_IncomeStatement = df_IncomeStatement.sort_values(['TICKER_SYMBOL','END_DATE'])
    
    df_IncomeStatement = df_IncomeStatement.drop(['PUBLISH_DATE','EXCHANGE_CD','MERGED_FLAG','FISCAL_PERIOD'],1)
    
    return(df_IncomeStatement)


# # 数据分箱处理

# In[9]:


#功能：处理极值，进行百分位离散化
#思路：通过箱图处理极值，利用pd.qcut函数按照数据出现频率百分比划分，将极值离散化，来减弱极值对最终结果的影响

def biningData(sr,n_Quantile,is_onehot):
    
    #分箱处理
    df_bins = pd.qcut(sr,n_Quantile,duplicates = 'drop').to_frame()
     #pandas.qcut:基于分位数的离散化函数。Quantile-based discretization function.
        #第一个参数：x为被分箱处理的数据，必须为1d ndarray or Series
        #第二个参数：n_Quantile为分位数
        #第三个参数：duplicates如有重复值如何处理
        
    df_bins['DIS_'+sr.name] = pd.Categorical(df_bins.iloc[:,0]).codes
    if(is_onehot==True):
        df_bins['DIS_'+sr.name]=df_bins['DIS_'+sr.name].astype('category')
    return(df_bins['DIS_'+sr.name])


# In[10]:


#功能：对每个列进行分箱处理，并为分箱给出排名号码

def biningAndRankingData(df,n_Quantile,is_onehot):
    print('————调用函数biningAndRankingData，开始为每个分箱分配排名值——————')
    bin_columns = ['DIS_'+ i for i in df.columns]
    rank_columns = ['RANK_'+ i for i in df.columns]
    
    if(is_onehot==True):
        df_bins = df.apply(lambda x:biningData(x,n_Quantile=n_Quantile,is_onehot=is_onehot))
        df_bins.columns = bin_columns
        df_bins = pd.get_dummies(df_bins, prefix=bin_columns)
    else:
        df_bins = df.apply(lambda x:biningData(x,n_Quantile=n_Quantile,is_onehot=is_onehot))
        df_bins.columns = bin_columns
        
    #为每个分箱分配排名值
    df_bins[rank_columns] = df.rank(method = 'min')
    return(df_bins)


# In[11]:


#功能：产生偏移数据
#思路：根据n_lag的设置进行几节数据偏移

def featureEngineeringTimeSeriesData(df_s,n_lag):
    print('————调用函数featureEngineeringTimeSeriesData，生成窗口特征——————')
    list_col = df_s.columns[2:]
    df_append =  []
    for i in range(n_lag):
        df_tmp = df_s.groupby(['TICKER_SYMBOL'])[list_col].shift(i+1)
        list_col_target = [col+'_'+'LAG'+str(i+1) for col in df_tmp.columns]
        df_tmp.columns = list_col_target
        df_append.append(df_tmp)
    df_s = pd.concat(df_append, axis=1)
    del df_append
    del df_tmp
    gc.collect()
    return(df_s)


# # 特征矩阵的生成

# In[12]:


#功能：特征矩阵构建

def createFeatureMatrix(df_IncomeStatement,df_indus_g,df_comp_g,df_share_g,START_DATE=pd.Timestamp('2008-01-01'),
                  IS_ONEHOT=False,N_QUANTILES=100,N_LAG=5):
    
    df_IncomeStatement['TICKER_SYMBOL'] = df_IncomeStatement['TICKER_SYMBOL'].astype(str)
    df_comp_g['TICKER_SYMBOL'] = df_comp_g['TICKER_SYMBOL'].astype(str)
    df_share_g['TICKER_SYMBOL'] = df_share_g['TICKER_SYMBOL'].astype(str)
    df_IncomeStatement['year'] = df_IncomeStatement['year'].astype(str)
    df_indus_g['year'] = df_indus_g['year'].astype(str)
    df_comp_g['year'] = df_comp_g['year'].astype(str)
    df_share_g['year'] = df_share_g['year'].astype(str)
    df_IncomeStatement['month'] = df_IncomeStatement['month'].astype(str)
    df_indus_g['month'] = df_indus_g['month'].astype(str)
    df_comp_g['month'] = df_comp_g['month'].astype(str)
    df_share_g['month'] = df_share_g['month'].astype(str)
    print('*合并..............')
    #df_train = pd.merge(list_company,df_IncomeStatement,how='left',on=['TICKER_SYMBOL'])
    df_train = pd.merge(df_IncomeStatement,df_comp_g,how='left',on=['TICKER_SYMBOL','year', 'month']).fillna(0)
    df_train = pd.merge(df_train,df_indus_g,how='left',on=['year', 'month']).fillna(0)
    df_train = pd.merge(df_train,df_share_g,how='left',on=['TICKER_SYMBOL','year', 'month']).fillna(0)
    del df_indus_g
    del df_comp_g
    del df_share_g
    del df_IncomeStatement
    gc.collect()
    #筛选时间
    df_train = df_train[df_train['END_DATE']>=START_DATE]
    print('*删除方差为0的变量......')
    #删除方差为0的变量***
    #df_train['OTH_EFFECT_OP'] = 1
    df_train = df_train.drop(['year','month'],1).sort_values(['TICKER_SYMBOL','END_DATE'])
    df_train = df_train.replace([np.inf, -np.inf], np.nan)

    df_train = df_train.groupby("TICKER_SYMBOL").apply(lambda x:x.ffill())
    sr_var = df_train.var(axis =0)
    kill_col = sr_var[sr_var<=0.0000001]
    df_train = df_train.drop(kill_col.index,1)
    df_train.to_csv('Data/df_train.csv')

    #时间窗口特征
    df_train_lag = featureEngineeringTimeSeriesData(df_train,N_LAG)
    df_train_f =  pd.concat([df_train,df_train_lag],axis=1)
    del df_train_lag
    gc.collect()

    #对每个列进行分箱处理，并按分箱为单位排名
    #df_train_f = pd.read_csv('df_train_f.csv')
    df_dis_rank = biningAndRankingData(df_train.iloc[:,2:],n_Quantile=N_QUANTILES,is_onehot=IS_ONEHOT)#排序
    del df_train
    gc.collect()
    df_train_f =  pd.concat([df_train_f,df_dis_rank],axis=1)
    del df_dis_rank
    gc.collect()
    df_train_f = df_train_f.fillna(0)
    
    return(df_train_f)


# # 特征选择

# In[13]:


#功能：特征筛选
#思路：按照特征选择比例为0.8，因子筛选：树数量为100，选择因子前99.99%的重要性进行变量筛选

def selectFeatures(df,pro,n_estimators=500,max_features=0.8):
    #pro：累计重要性的选择比例= 0.99 
    #n_estimators：树数量
    #max_features： 特征选择比例
    df = df.sort_values(by = ['TICKER_SYMBOL', 'END_DATE'], ascending = True)
    df['target_REVENUE_Q1'] = df.groupby(['TICKER_SYMBOL'])['REVENUE_Q1'].shift(-1)
    X = df[pd.notnull(df['target_REVENUE_Q1'])].iloc[:,2:-1].values
    Y = df[pd.notnull(df['target_REVENUE_Q1'])].iloc[:,-1].values
    names = df.iloc[:,2:-1].columns.values
    rf = RandomForestRegressor(n_estimators = n_estimators,max_features=max_features,oob_score=True,n_jobs=-1)
    print(rf)
    rf.fit(X, Y)
    col_select = pd.DataFrame({'COL':names,'IMP':rf.feature_importances_}).sort_values('IMP',ascending=False)
    col_select['CUM_IMP'] = col_select['IMP'].cumsum()
    pro = pro if col_select['IMP'][0:1].values[0]<pro else col_select['IMP'][0:1].values[0]
    col_select = col_select[col_select['CUM_IMP']<=pro]

    print('特征选择结果：%d个特征，累计%.7f%%的重要性。'%(col_select.shape[0],pro*100))
    col_s = col_select['COL']
    if(col_select[col_select['COL']=='MARKET_VALUE'].shape[0]==0):
        col_s = pd.Series('MARKET_VALUE').append(col_s)
    if(col_select[col_select['COL']=='REVENUE_Q1'].shape[0]==0):
        col_s = pd.Series('REVENUE_Q1').append(col_s)
    names_col = pd.Series(['TICKER_SYMBOL','END_DATE']).append(col_s).append(pd.Series('target_REVENUE_Q1'))
    df = df[names_col]
    
    #保存临时结果
    df.to_csv("Data/df_bank.csv")
    
    return(df,col_select)


# # 模型集成

# In[14]:


#功能：模型融合
#思路：确定使用的模型与权重，进行模型的生成与预测

class EnsembleLearners(BaseEstimator, RegressorMixin):
    def __init__(self, mod, weight):
        self.mod = mod
        self.weight = weight

    def fit(self, X, y): 
        self.models_ = [clone(x) for x in self.mod]
        for model in self.models_:
            model.fit(X, y)
        return self

    def predict(self, X): 
        w = list()
        pred = np.array([model.predict(X) for model in self.models_])
        # for every data point, single model prediction times weight, then add them together
        for data in range(pred.shape[1]):
            single = [pred[model, data] * weight for model, weight in zip(range(pred.shape[0]), self.weight)]
            w.append(np.sum(single))
        return w


# # 模型训练与预测

# In[15]:


#功能：模型训练预测
#思路：对所有的银行数据的目标变量进行对数log10变换，对特征集进行归一化，
    #根据AlgorithmsInEL的值确定模型与权重，
    #集成 ExtraTreesRegressor、GradientBoostingRegressor、RandomForestRegressor、XGBRegressor等算法
    #根据各自的n_estimators、max_features进行模型训练，得出预测数据。

def trainModel(df,LOG_N,gbr_EST,gbr_FEAT,gbr_LRAT,etr_EST,etr_FEAT,rf_EST,rf_FEAT,xgb_EST,xgb_SAM,xgb_LRAT,AlgorithmsInEL):
    
    df.END_DATE = df['END_DATE'].astype("datetime64[ns]")
    if(AlgorithmsInEL==0):
        df = df.loc[df['END_DATE'].dt.month == 3,]
    df = df.replace([np.inf, -np.inf], np.nan)

    X_test = df.loc[(df['target_REVENUE_Q1'].isnull()) & (df['END_DATE'] == '2018-03-31'), ]
    X_test.drop('target_REVENUE_Q1', axis=1, inplace=True)

    X = df.loc[(df['target_REVENUE_Q1'] > 0.), ]
    y = X['target_REVENUE_Q1']
    X.drop('target_REVENUE_Q1', axis=1, inplace=True)

    X.loc[:, X.dtypes == 'float64'] = X.loc[:, X.dtypes == "float64"].fillna(0.00001)
    cols = [i for i in df.columns if i not in ['TICKER_SYMBOL', 'END_DATE', 'target_REVENUE_Q1']]
    X = X[cols]

    y = y / 10000.0
    log_y = np.log(y)/np.log(LOG_N)

    scaler = MinMaxScaler() 
    scaler.fit(df[cols])
    
    
    xgb = XGBRegressor(n_estimators = xgb_EST, subsample=xgb_SAM, learning_rate = xgb_LRAT)
    extra = ExtraTreesRegressor(n_estimators = etr_EST, max_features= etr_FEAT)
    gbr = GradientBoostingRegressor(n_estimators = gbr_EST, max_features= gbr_FEAT, learning_rate = gbr_LRAT)
    rf = RandomForestRegressor(n_estimators = rf_EST, max_features= rf_FEAT)

    # 根据需求选择不同的集成学习方案
    if(AlgorithmsInEL == 0):
        print([extra,rf])
        ensembleModel = EnsembleLearners(mod=[extra,rf], weight= [0.5,0.5])
    elif(AlgorithmsInEL == 1):
        print([gbr,xgb])
        ensembleModel = EnsembleLearners(mod=[gbr,xgb], weight= [0.5,0.5])
    elif(AlgorithmsInEL == 2):
        print([extra,gbr,rf,xgb])
        ensembleModel = EnsembleLearners(mod=[extra,gbr,rf,xgb], weight= [0.25,0.25,0.25,0.25])


    X_scaled = scaler.transform(X)
    
    #模型预测
    ensembleModel.fit(X_scaled,log_y)
    to_pred_x = X_test[cols]
    to_pred_scaled_x = scaler.transform(to_pred_x)
    
    pred = np.power(LOG_N, ensembleModel.predict(to_pred_scaled_x)) * 10000.

    submit_symbols = list(X_test.TICKER_SYMBOL)
    submit_results = list((np.array(X_test.REVENUE_Q1) + np.array(pred)) / 1000000.)
    submit_results = [float('%.2f' % w) for w in submit_results]

    res = pd.DataFrame({'TICKER_SYMBOL': submit_symbols, 'PRED': submit_results})
    
    return(res)


# # 预测结果的提交

# In[16]:


#功能：得出预测结果
#思路：将预测数据合并，输出预测结果

def appendPredictToSubmit(df_FDDC_financial_submit,df_bank_predicted):
    
    df_submit_with_predict = pd.merge(df_FDDC_financial_submit,
                                      df_bank_predicted,
                                      how='left',
                                      on=['TICKER_SYMBOL'])
     
    df_submit_with_predict['TICKER_SYMBOL'] = df_submit_with_predict['TICKER_SYMBOL']+                                         '.'+df_submit_with_predict['StockExchange']
    
    df_submit_with_predict = df_submit_with_predict.drop(['StockExchange'],1)

    return(df_submit_with_predict)


# In[ ]:





# In[ ]:




