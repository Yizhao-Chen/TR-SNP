import rpy2
import tzlocal
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector

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

def simple_plot(fd,mm,list):
    #set up the framework of the output figure
    pyplot.rcParams['savefig.dpi'] = 300
    pyplot.rcParams['figure.dpi'] = 300
    #plot all
    if mm == "all":
        TR_input_dir = fd + "/" + list[1] + ".rwl"
        TR_input = r['read.tucson'](TR_input_dir)
        start = r['as.numeric'](r['min'](r['rownames'](TR_input)))
        end = r['as.numeric'](r['max'](r['rownames'](TR_input)))
        # get observation period
        TRW = r['data.frame'](year=r['seq'](start, end, 1))
        # select only important rows ( the tree (?) or series names, e.g. "LF317s")
        all = r['names'](TR_input)
        with localconverter(rpy2.robjects.default_converter + pandas2ri.converter):
            pdf_input = rpy2.robjects.conversion.ri2py(TR_input)
            t_start = rpy2.robjects.conversion.ri2py(start)
            t_end = rpy2.robjects.conversion.ri2py(end)
            # dataframe processing for plot
            years = range(int(t_start), int(t_end) + 1)  # get the year index in the data
            pdf_input.index = years  # put the year as the index in the data
            pdf_input.insert(0, "year", years)  # put years as the first column

        for i in range(2,len(list)):
            TR_input_dir = fd + "/" + list[i] + ".rwl"
            TR_input = r['read.tucson'](TR_input_dir)
            start = r['as.numeric'](r['min'](r['rownames'](TR_input)))
            end = r['as.numeric'](r['max'](r['rownames'](TR_input)))
            # get observation period
            TRW = r['data.frame'](year=r['seq'](start, end, 1))
            # select only important rows ( the tree (?) or series names, e.g. "LF317s")
            all = r['names'](TR_input)

            with localconverter(rpy2.robjects.default_converter + pandas2ri.converter):
                pdf_input1 = rpy2.robjects.conversion.ri2py(TR_input)
                t_start = rpy2.robjects.conversion.ri2py(start)
                t_end = rpy2.robjects.conversion.ri2py(end)
                #dataframe processing for plot
                years = range(int(t_start), int(t_end) + 1) #get the year index in the data
                pdf_input1.index = years                    #put the year as the index in the data
                pdf_input1.insert(0,"year",years)           #put years as the first column

            pdf_input = pd.merge(pdf_input,pdf_input1,how='outer')   #merge the input dataframes
            pdf_input.sort_values("year",inplace=True)               #sort values according to years

        years_index = pdf_input["year"]                          #get the "year" column for the final dataframe
        pdf_input.index = years_index                            #put it as the final index
        pdf_input = pdf_input.drop(pdf_input.columns[0],axis=1)              #delect the first column of years

    else:
        TR_input_dir = fd + "/"+ mm + ".rwl"
#    TR_input_dir = 'D:/MEGA/Live_cases/Hybrid/Tree_ring_data_collection_NOAA_ITRDB/Appendix S1/Cleaned datasets' \
#                   '/script_test/me037.rwl'
        print(TR_input_dir)
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

#put the row names(years) back
            years = range(int(t_start),int(t_end)+1)
            pdf_input.index = years

#statistical summary
    pdf_mean = pdf_input.mean(axis=1)
    pdf_max = pdf_input.max(axis=1)
    pdf_min = pdf_input.min(axis=1)
    pdf_std = pdf_input.std(axis=1)
    pdf_c_summary = pdf_input.describe()
    pdf_upper = pdf_mean + pdf_std
    pdf_lower = pdf_mean - pdf_std

#need to put a transposition here to get the index summary
    #pdf_r_summary
        #print(pdf_mean)
#===================================================================================
#plotting
#very simple right now,need major revision to make it more useful
#===================================================================================

    pdf_mean.plot(label = 'TR mean')
    #pdf_upper.plot(label = 'upper error')
    #pdf_lower.plot(label = 'lower error')
    pyplot.legend(loc = 'upper left')
    pyplot.ylabel('TRW (mm)')
    pyplot.xlabel('year')
    pyplot.show()

    pdf_std.plot(label = 'TR std')
    pyplot.legend(loc = 'upper left')
    pyplot.ylabel('TRW_std (mm)')
    pyplot.xlabel('year')
    pyplot.show()
#output the plot file
    pdf_input.to_csv(path_or_buf=fd + "/" + mm + ".csv",sep=',',na_rep="-999")

