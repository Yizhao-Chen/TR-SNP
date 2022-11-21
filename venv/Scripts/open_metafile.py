#The selection logic should be improved
import csv
#import os
#from tkinter import messagebox

#def om(mf,year_in,year_out,reg_in,spec_in):
#def om(mf,year_in,year_out,lat_s,lat_e,lon_s,lon_e,reg_in,spec_in):
def om(mf, year_in, year_out, lat_in, lon_in, reg_in, spec_in):

    #mf = 'D:/chrome_download/Appendix S1/Cleaned datasets/itrdb-v713-cleaned-rwl/rwl_metadata.csv'
    file_list = []   #create an empty list
    #lat_s = 2500
    #lat_e = 4900
    #lon_s = -13000
    #lon_e = -7000
    with open(mf) as f:
        reader = csv.DictReader(f)
       # if len(lat_s) == 4:
       #     lat_st = '0' + lat_s
       # else:
       #     lat_st = lat_s

       # if len(lat_e) == 4:
       #     lat_et = '0' + lat_e
       # else:
       #     lat_et = lat_e

       # if len(lon_s) == 4:
       #     lon_st = '0' + lon_s
       # else:
       #     lon_st = lon_s

       # if len(lon_e) == 4:
       #     lon_et = '0' + lon_e
       # else:
       #     lon_et = lon_e

        for row in reader:
            start = row['start']
            end = row['end']
            id = row['id']
            region = row['region']
            species = row['species']
            lat = row['lat']
            lon = row['lon']
            #if len(lat) == 4:
            #    lat = '0' + lat
            #if len(lon) == 4:
            #    lon = '0' + lon
            if spec_in == 'all' and reg_in == 'all':
                #need revision in the future Yizhao 2019/12/22
            #    print(lat)
            #    print(lon)
                if start <= year_in and end >= year_out and lat == lat_in and lon == lon_in:

                        #and lat >= lat_st and lat <= lat_et and lon >= lon_st and lon <= lon_et:
                    file_list.append(id)

            elif spec_in != 'all' and reg_in == 'all':
                if start <= year_in and end >= year_out and species == spec_in: #\
                        #and lat >= lat_st and lat <= lat_et and lon >= lon_st and lon <= lon_et:
                    file_list.append(id)
            elif spec_in == 'all' and reg_in != 'all':
                if start <= year_in and end >= year_out and region == reg_in:#\
                        #and lat >= lat_st and lat <= lat_et and lon >= lon_st and lon <= lon_et:
                    file_list.append(id)
            else:
                if start <= year_in and end >= year_out and species == spec_in and region == reg_in:#\
                        #and lat >= lat_st and lat <= lat_et and lon >= lon_st and lon <= lon_et:
                    file_list.append(id)
            #if file_list:
    return file_list
            #else:
            #    messagebox.showerror("ERROR","No data fits")
            #    os._exit()

