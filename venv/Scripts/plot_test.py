#a script to test new features in Tree ring plotting before incorporation

import rpy2
import tzlocal
#import matplotlib
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
#from rpy2.robjects import *

#to use transform R vectors to numpy
from rpy2.robjects.packages import importr,data
from rpy2.robjects.vectors import DataFrame, StrVector
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import r, pandas2ri
#import numpy as np
import pandas as pd
from pandas import *

#plot
#import ggplot
#import ggpy
from matplotlib import *
from matplotlib import pyplot
#import plotnine

#import R package
dplR = importr('dplR')
r_base = importr('base')
pandas2ri.activate()
pd.options.mode.chained_assignment = None

TR_input_dir = 'D:/MEGA/Live_cases/Hybrid/Tree_ring_data_collection_NOAA_ITRDB/Appendix S1/Cleaned datasets' \
               '/plot_test_data/cana249.rwl'
TR_input_dir1 = 'D:/MEGA/Live_cases/Hybrid/Tree_ring_data_collection_NOAA_ITRDB/Appendix S1/Cleaned datasets' \
                '/plot_test_data/mexi029.rwl'

TR_input = r['read.tucson'](TR_input_dir)
# get start and end dates of observations to set the years for the data frame
start = r['as.numeric'](r['min'](r['rownames'](TR_input)))
end = r['as.numeric'](r['max'](r['rownames'](TR_input)))
# get observation period
TRW = r['data.frame'](year=r['seq'](start,end,1))
# select only important rows ( the tree (?) or series names, e.g. "LF317s")
all = r['names'](TR_input)

#convert the R data.frame to pandas data.frame
with localconverter(rpy2.robjects.default_converter + pandas2ri.converter):
    pdf_input = rpy2.robjects.conversion.ri2py(TR_input)
    t_start = rpy2.robjects.conversion.ri2py(start)
    t_end = rpy2.robjects.conversion.ri2py(end)

    years = range(int(t_start), int(t_end) + 1)
    pdf_input.index = years
    pdf_input.insert(0,'years',years)

TR_input1 = r['read.tucson'](TR_input_dir1)
# get start and end dates of observations to set the years for the data frame
start1 = r['as.numeric'](r['min'](r['rownames'](TR_input1)))
end1 = r['as.numeric'](r['max'](r['rownames'](TR_input1)))
# get observation period
TRW1 = r['data.frame'](year=r['seq'](start1,end1,1))
# select only important rows ( the tree (?) or series names, e.g. "LF317s")
all1 = r['names'](TR_input1)

#convert the R data.frame to pandas data.frame
with localconverter(rpy2.robjects.default_converter + pandas2ri.converter):
    pdf_input1 = rpy2.robjects.conversion.ri2py(TR_input1)
    t_start1 = rpy2.robjects.conversion.ri2py(start1)
    t_end1 = rpy2.robjects.conversion.ri2py(end1)

    years1 = range(int(t_start1), int(t_end1) + 1)
    pdf_input1.index = years1
    pdf_input1.insert(0,'years',years1)

pdf_input = pd.merge(pdf_input, pdf_input1, how='outer')  # merge the input dataframes
pdf_input.sort_values("years", inplace=True)  # sort values according to years
pdf_input.drop(pdf_input.columns[0], axis=1)  # delect the first column of years
index = list(range(0,len(pdf_input["years"])))
pdf_input.index = index
index_length = len(pdf_input["years"])
#remove the years column temporally
pdf_input2 = pdf_input.drop(columns=["years"])

#BAI calculation
bai_sum = pdf_input2.copy()
bai_sum[bai_sum.columns[0:len(bai_sum.columns)]] = np.nan
#remove the years column temporally
#bai_sub = bai_sum.drop(columns=["years"])

#set up a dataframe might be useful in the future
#bai_sum = pd.DataFrame({'years':pdf_input["years"]})

#do calculation in each column

for key,value in pdf_input2.iteritems():
    col_current = value
    #set initial values
    bai = np.zeros(index_length + 1)  # basal area increment
    tr_accum = np.zeros(index_length + 1)  # tree ring accumulation
    for i in range(len(col_current)):
        #print(col_current[i])
        if pd.isna(col_current[i]):
            col_current[i] = 0
            bai[i+1] = 0
            tr_accum[i+1] = tr_accum[i]
        else:
            tr_accum[i+1] = tr_accum[i] + col_current[i]
            bai[i+1] = 3.1415926 * (tr_accum[i+1] * tr_accum[i+1] - tr_accum[i] * tr_accum[i])
            bai[i+1] = bai[i+1] / 100
    bai_sum[key] = bai[1:(index_length+1)]




pdf_mean = pdf_input2.mean(axis=1)
pdf_max = pdf_input2.max(axis=1)
pdf_min = pdf_input2.min(axis=1)
pdf_std = pdf_input2.std(axis=1)

bai_mean = bai_sum.mean(axis=1)
bai_max = bai_sum.max(axis=1)
bai_min = bai_sum.min(axis=1)
bai_std = bai_sum.std(axis=1)
bai_summary = bai_sum.describe()

#output the plot source file
pdf_input_csv = pdf_input.to_csv("D:/MEGA/Live_cases/Hybrid/Tree_ring_data_collection_NOAA_ITRDB/Appendix S1/Cleaned datasets"
          "/plot_test_data/output_test.csv",index=False,sep=',')
#with open("D:/MEGA/Live_cases/Hybrid/Tree_ring_data_collection_NOAA_ITRDB/Appendix S1/Cleaned datasets"
#          "/plot_test_data/output_test.csv", 'w') as ff:
#        ff.write(pdf_input_csv)



pdf_mean.plot(label='TR mean')
pyplot.show()
bai_mean.plot(label='BAI mean')
pyplot.show()