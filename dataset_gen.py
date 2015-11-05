#!/usr/bin/env python

import csv
import json


# List of features to load
features = ['maxhumidity','minhumidity','humidity',
            'maxdewptm','mindewptm','meandewptm',
            'maxpressurem','minpressurem','meanpressurem',
            'maxwspdm','minwspdm','meanwindspdm',
            'maxvism','minvism','meanvism',
            'precipm',
            'thunder',
            'tornado',
            'meantempm']

filepath = "data"

places = ['USA/Chicago,IL','USA/Houston,TX','USA/Austin,TX','USA/Seattle,WA',
          'USA/Columbus,OH','USA/San Diego,CA','USA/Ithaca,NY', 'USA/New York,NY',
          'USA/Washington,DC','USA/Philadelphia,PA']

dates = ['20150902','20150903','20150904','20150905','20150906','20150907',
         '20150908','20150909','20150910','20150911','20150912','20150913',
         '20150914','20150915','20150916','20150917','20150918','20150919',
         '20150920','20150921','20150922','20150923','20150924','20150925',
         '20150926','20150927','20150928','20150929','20150930','20151001',
         '20151002','20151003','20151004','20151005','20151006','20151007',
         '20151008','20151009','20151010','20151011','20151012','20151013',
         '20151014','20151015','20151016','20151017','20151018','20151019',
         '20151020','20151021','20151022','20151023','20151024','20151025',
         '20151026','20151027','20151028','20151029','20151030','20151031',
         '20151101'] 

date_header = ['month','day','year']

empty_features = []
# read all the json files in the current directory 
for p in places: 
        total_data = []
        for d in dates:
                full_filename = filepath + '/' + p + '/' + d + '.json'
                data_file = open(full_filename)
                data = json.load(data_file)
                x = []

                # including numerical date in mm,dd,yyyy format
                q = data['history']['dailysummary'][0]
                x.append(q['date']['mon'])
                x.append(q['date']['mday'])
                x.append(q['date']['year'])
                
                # calculating mean-humidity if empty
                if not q['humidity']:
                        q['humidity'] = str(0.5*(eval(q['maxhumidity']) + eval(q['minhumidity'])))
                # replacing 'T' in precipm
                if q['precipm'] == 'T':
                        q['precipm'] = '0'

                # checking if any other elements are empty
                for feat in features:
                        if not q[feat]:
                                empty_features.append([p,d,feat])
                        x.append(q[feat])
                total_data.append(x)
                data_file.close()
        # replacing the last entry to the next day's temperature
        k = 0
        for i in range(1,len(total_data)):
                total_data[k][21] = total_data[i][21]
                k = k + 1
        popped_el = total_data.pop()
        # write data in csv file
        startpos = len(p)-p[::-1].find('/')
        city_name = p[startpos:]
        output_file = open(filepath+'/' + p + '/' + city_name + '.csv','wb')#,newline='')
        writer = csv.writer(output_file)#delimiter=',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(date_header + features)
        for row in total_data:
                writer.writerow(row)

        output_file.close()


