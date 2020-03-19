import pandas as pd
import numpy as np

def B_clean(bestbuy):
    bestbuy.drop_duplicates(subset = ['model'],inplace=True)

    bestbuy['price'] = bestbuy['price'].str.replace(',','').astype('float')
    bestbuy['review number'] = bestbuy['review number'].str.replace(',','').astype('float')
    bestbuy['Screen Size'] = bestbuy['Screen Size'].str.split().str[0].astype('float')
    bestbuy['color'] = np.where(bestbuy['color'].str.contains('Black',case=False),'Black',
                       np.where(bestbuy['color'].str.contains('Gray',case=False),'Gray',
                       np.where(bestbuy['color'].str.contains('Silver',case=False),'Silver',
                       np.where(bestbuy['color'].str.contains('White',case=False),'White',
                       np.where(bestbuy['color'].str.contains('Brown',case=False),'Brown',
                       np.where(bestbuy['color'].str.contains('Gold',case=False),'Gold',
                       np.where(bestbuy['color'].isna(),np.nan,'Other')))))))

    bestbuy.loc[bestbuy['Storage Type']=='SSD, HDD','Storage Type']='HDD, SSD'
    splitstring = bestbuy['Total Storage Capacity'].str.split().str
    bestbuy['Total Storage Capacity']=np.where(splitstring[1]=='terabytes',splitstring[0].astype('float')*1000,splitstring[0].astype('float'))
    splitstring = bestbuy['Hard Drive Capacity'].str.split().str
    bestbuy['Hard Drive Capacity']=np.where(splitstring[1]=='terabytes',splitstring[0].astype('float')*1000,splitstring[0].astype('float'))
    splitstring = bestbuy['System Memory (RAM)'].str.split().str
    bestbuy['System Memory (RAM)']=np.where(splitstring[1]=='terabytes',splitstring[0].astype('float')*1000,splitstring[0].astype('float'))
    bestbuy['Processor Speed (Base)'] = bestbuy['Processor Speed (Base)'].str.split().str[0].astype('float')

    bestbuy['Operating System'] = np.where(bestbuy['Operating System'].str.contains('Mac',case=False),'MacOS',
                       np.where(bestbuy['Operating System'].str.contains('chrome',case=False),'Chrome OS',
                       np.where(bestbuy['Operating System'].str.contains('windows',case=False),'Windows',
                       np.where(bestbuy['Operating System'].isna(),np.nan,'Other'))))

    bestbuy['Processor Model'] = np.where(bestbuy['Processor Model'].isna(),np.nan,
                       np.where(bestbuy['Processor Model'].str.contains('Core i7',case=False),'Intel Core i7',
                       np.where(bestbuy['Processor Model'].str.contains('Core i5',case=False),'Intel Core i5',
                       np.where(bestbuy['Processor Model'].str.contains('Core i3',case=False),'Intel Core i3',
                       np.where(bestbuy['Processor Model'].str.contains('Ryzen 3',case=False),'AMD Ryzen 3',
                       np.where(bestbuy['Processor Model'].str.contains('Ryzen 5',case=False),'AMD Ryzen 5',        
                       np.where(bestbuy['Processor Model'].str.contains('Ryzen 7',case=False),'AMD Ryzen 7',
                       np.where(bestbuy['Processor Model'].str.contains('Core i9',case=False),'Intel Core i9',
                       np.where(bestbuy['Processor Model'].str.contains('Pentium',case=False),'Intel Pentium',                            
                       np.where(bestbuy['Processor Model'].str.contains('Non-AMD/Intel processor',case=False),'Non-AMD/Intel processor',
                       np.where(bestbuy['Processor Model'].str.contains('AMD',case=False),'AMD other',
                       np.where(bestbuy['Processor Model'].str.contains('Celeron',case=False),'Intel Celeron',
                       np.where(bestbuy['Processor Model'].str.contains('Intel',case=False),'Intel other','other')))))))))))))                                             

    bestbuy['Battery Life'] = bestbuy['Battery Life'].str.split().str[0].astype('float')
    bestbuy['Product Height'] = bestbuy['Product Height'].str.split().str[0].astype('float')
    bestbuy['Product Width'] = bestbuy['Product Width'].str.split().str[0].astype('float')
    bestbuy['Product Depth'] = bestbuy['Product Depth'].str.split().str[0].astype('float')
    splitstring = bestbuy['Product Weight'].str.split().str
    bestbuy['Product Weight']=np.where(splitstring[1]=='ounces',splitstring[0].astype('float')*0.0625,splitstring[0].astype('float'))

    bestbuy.drop(['index'],axis=1,inplace = True)
    
    return(bestbuy)


def W_clean(walmart):
    walmart.drop_duplicates(subset = ['model'],inplace=True)

    walmart['operating_system'] = np.where(walmart['operating_system'].str.contains('Mac',case=False),'MacOS',
                       np.where(walmart['operating_system'].str.contains('chrome',case=False),'Chrome OS',
                       np.where(walmart['operating_system'].str.contains('windows',case=False),'Windows',
                       np.where(walmart['operating_system'].isna(),np.nan,'Other'))))

    splitstring = walmart['battery_life'].str.split().str
    walmart['battery_life']=np.where(splitstring.len()==4, splitstring[0].astype('float')+splitstring[2].astype('float')/60,
                            np.where(walmart['battery_life'].str.contains('wh',case=False),np.nan,
                            np.where(walmart['battery_life'].str.contains('minutes',case=False),
                                     splitstring[0].astype('float')/60,splitstring[0].astype('float'))))
    walmart['Product Depth']=walmart['dimensions'].str.split().str[0].astype('float')
    walmart['Product Width']=walmart['dimensions'].str.split().str[2].astype('float')
    walmart['Product height']=walmart['dimensions'].str.split().str[4].astype('float')

    walmart.drop(['dimensions'],axis=1,inplace=True)

    walmart['screen_size'] = walmart['screen_size'].str.replace(r"[a-zA-Z\"\\,]",'').str.strip().str.split().str[0].astype('float')

    splitstring = walmart['Hard_Drive_Capacity'].str.split(' |,').str
    walmart['Hard_Drive_Capacity']=np.where(walmart['Hard_Drive_Capacity'].str.contains('tb',case=False),splitstring[0].astype('float')*1000,splitstring[0].astype('float'))

    walmart['Processor Type'] = np.where(walmart['Processor Type'].isna(),np.nan,
                       np.where(walmart['Processor Type'].str.contains('i7',case=False),'Intel Core i7',
                       np.where(walmart['Processor Type'].str.contains('i5',case=False),'Intel Core i5',
                       np.where(walmart['Processor Type'].str.contains('i3',case=False),'Intel Core i3',
                       np.where(walmart['Processor Type'].str.contains('Ryzen 3',case=False),'AMD Ryzen 3',
                       np.where(walmart['Processor Type'].str.contains('Ryzen 5',case=False),'AMD Ryzen 5',        
                       np.where(walmart['Processor Type'].str.contains('Ryzen 7',case=False),'AMD Ryzen 7',
                       np.where(walmart['Processor Type'].str.contains('i9',case=False),'Intel Core i9',
                       np.where(walmart['Processor Type'].str.contains('Pentium',case=False),'Intel Pentium',                            
                       np.where(walmart['Processor Type'].str.contains('Non-AMD/Intel processor',case=False),'Non-AMD/Intel processor',
                       np.where(walmart['Processor Type'].str.contains('AMD',case=False),'AMD other',
                       np.where(walmart['Processor Type'].str.contains('Celeron',case=False),'Intel Celeron',
                       np.where(walmart['Processor Type'].str.contains('Intel',case=False),'Intel other','other')))))))))))))                                             

    splitstring = walmart['Processor Speed'].str.split(' |G|,').str
    walmart['Processor Speed']=np.where(walmart['Processor Type'].str.contains('mhz',case=False),splitstring[0].astype('float')/1000,splitstring[0].astype('float'))

    walmart['RAM Memory'] = walmart['RAM Memory'].str.split(' |,').str[0].astype('float')

    walmart.drop(['Unnamed: 0'],axis=1,inplace = True)
    
    return(walmart)

