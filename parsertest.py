# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 14:30:30 2021

@author: anna.damir
"""
#import xml.etree.ElementTree as et
import pandas as pd
import lxml 
from lxml import etree
from datetime import datetime
import time

filename = r'C:\Users\anna.damir\Downloads\EDW_Auction_Results_2021_03_04.xml'
schemaname = r'C:\Users\anna.damir\Downloads\EDW_Auction_Results.xsd'
timestamp = time.strftime('%Y%m%d%H%M')
xmlfile = lxml.etree.parse(filename)
xml_validator = lxml.etree.XMLSchema(file = schemaname)
is_valid = xml_validator.validate(xmlfile)

def validate_num(x):
    if float(x) > 0:
        return x
    else:
        return None
    
def validate_string(x):
    if not x:
        return None
    else:
        return x

def validate_make_model(m):
    if m==None or m.startswith('Unknown') or m.startswith('UNKNOWN') or m.startswith('unkonwn') or m.startswith('[OTHER') or m.startswith(':OTHER') or m.startswith('OTHER') or m.startswith('Other'):
        return None
    else:
        return m

def get_classification(auctioneer,desc,item,y,ma,mo):
    #if((string1 == null || string1.length == 0) && (string2 == null || string2.length == 0))
    if auctioneer == 'IronPlanet':
        phrase = desc
        if '(unverified)' in phrase or '(Unverified)' in phrase:
            phrase = phrase.replace('(unverified)','').strip()
            phrase = phrase.replace('(Unverified)','').strip()
        phrase = ' '.join(phrase.split())
# =============================================================================
#         if y != '0':
#             y=str(y)
#             phrase = phrase.replace(y,'').strip()
#         if mo:
#             phrase = phrase.replace(mo,'').strip()
#         if ma:
#             ma= ma.title()
#             phrase = phrase.replace(ma,'').strip()
# =============================================================================
        if mo:
            try:
                phrase = phrase[phrase.index(mo)+len(mo):].strip()
            except:
                phrase = phrase
            try:
                mo = mo.title()
                phrase = phrase[phrase.index(mo)+len(mo):].strip()
            except:
                phrase = phrase
            try: 
                mo = mo.upper()
                phrase = phrase[phrase.index(mo)+len(mo):].strip()
            except:
                phrase = phrase
            try: 
                mo = mo.lower()
                phrase = phrase[phrase.index(mo)+len(mo):].strip()
            except:
                phrase = phrase
        if ma:
            try:
                phrase = phrase[phrase.index(ma)+len(ma):].strip()
            except:
                phrase = phrase
            try:
                ma = ma.title()
                phrase = phrase[phrase.index(ma)+len(ma):].strip()
            except:
                phrase = phrase
            try:
                ma = ma.upper()
                phrase = phrase[phrase.index(ma)+len(ma):].strip()
            except:
                phrase = phrase
            try: 
                ma = ma.lower()
                phrase = phrase[phrase.index(ma)+len(ma):].strip()
            except:
                phrase = phrase
        if y != '0':
            y=str(y)
            phrase = phrase.replace(y,'').strip()
        
    else:
        if desc and item:
            phrase = desc + " " + item
        elif not item and desc:
            phrase = desc
        elif not desc and item: 
            phrase = item
        elif not (desc and item):
            phrase = None
    return phrase

def get_meter_code(meter):
    if meter == 'Hours':
        metercode = 'H'
    elif meter == "KM" or meter == 'KMs':
        metercode = 'K'
    elif meter == 'Miles':
        metercode = 'M'
    else:
        metercode = None
    return metercode

def get_lotnum(dataframe):
    if dataframe['Auctioneer']=='Ritchie Bros.':
        lotnum = dataframe['LotNum']
        if not lotnum:
            print('Missing Lot Num!!')
    elif dataframe['Auctioneer']=='IronPlanet':
        lotnum = dataframe['ItemId']
    return lotnum

def get_sale_type(auctioneer,sellingmethod,saletp):
    if auctioneer == 'Ritchie Bros.':
        saletype = 'Unreserved Auction'
    elif saletp == 'IP Weekly':
        saletype = 'Unreserved Auction'
    elif saletp == 'Marketplace E':
        if sellingmethod =='Daily Marketplace':
            saletype = 'Reserved Auction'
        elif sellingmethod == 'Fixed Price':
            saletype = 'Fixed Price'
        elif sellingmethod == 'Make Offer' or sellingmethod == 'Seller Bid Select':
            saletype = 'Accepted Offer'
    return saletype

def get_division(platform):
    if platform == 'Marketplace E':
        pltfrm = 'Marketplace-E'
    else:
        pltfrm = None
    return pltfrm

def check_postal_code(zipcode):
    if zipcode=='Unknown Postal Code':
        zipco = None
    else:
        zipco = zipcode
    return zipco

def check_year(year):
    if year == '0':
        modelyear = None
    else:
        modelyear = year
    return modelyear

def validate_serial(num):
    if num == None or num.startswith('Unknown S') or num.startswith('No serial'):
        num=None
    else:
        num=num
    return num
    

if is_valid ==True:
    root = xmlfile.getroot()
    #Make DataFrame
    item_id,year,make,model,usage,usagecode,comeswith,city,state,zipco,country,price,saledate,currcode,source,typename,desc,sn,sellingmethod,lot,platform = ([] for i in range(21))
    for item in xmlfile.iterfind('Auction_Result'):
        item_id.append(item.findtext('ITEM_ID'))
        year.append(item.findtext('ITEM_YEAR_OF_MANUFACTURE'))
        make.append(item.findtext('ITEM_MANUFACTURER'))
        model.append(item.findtext('ITEM_MODEL'))
        usage.append(item.findtext('ITEM_USAGE'))
        usagecode.append(item.findtext('ITEM_USAGE_UNITS'))
        comeswith.append(item.findtext('ITEM_COMES_WITH'))
        city.append(item.findtext('ITEM_LOCATION_CITY'))
        state.append(item.findtext('ITEM_LOCATION_PROV_STATE_CODE'))
        zipco.append(item.findtext('ITEM_LOCATION_POSTAL_ZIP_CODE'))
        country.append(item.findtext('ITEM_LOCATION_COUNTRY_CODE'))
        price.append(item.findtext('ITEM_SOLD_PRICE_LOCAL'))
        saledate.append(item.findtext('ITEM_SALE_DATE'))
        currcode.append(item.findtext('ITEM_CURRENCY_LOCAL'))
        source.append(item.findtext('ITEM_SOURCE'))
        typename.append(item.findtext('ITEM_TYPE_NAME'))
        desc.append(item.findtext('ITEM_SHORT_DESCRIPTION'))
        sn.append(item.findtext('ITEM_SERIAL_NUMBER'))
        sellingmethod.append(item.findtext('ITEM_SELLING_METHOD'))
        lot.append(item.findtext('ITEM_LOT_NUMBER'))
        platform.append(item.findtext('ITEM_SALE_GROUP_PLATFORM'))
    df = pd.DataFrame({'ItemId':item_id,'Year': year, 'AuctioneerMake': make,'AuctioneerModel': model,'Meter':usage,'MeterCode':usagecode,'AuctioneerDescription':comeswith,'City':city,'State':state,'Zip':zipco,'CountryCode':country,'Price':price,'SaleDate':saledate,'CurrencyCode':currcode,'Auctioneer':source,'TypeName':typename,'Description':desc,'SerialNumber':sn,'SellingMethod':sellingmethod,'LotNum':lot,'Platform':platform})
    #Data validation and Massaging on DataFrame
    df.loc[df['Auctioneer']=='RBA','Auctioneer']= 'Ritchie Bros.'
    df['SaleDate']=pd.to_datetime(df['SaleDate'])
    df['AuctionDate'] = [d.date() for d in df['SaleDate']]
    df['Price'] = df['Price'].apply(validate_num)
    df['Price']=df['Price'].apply(pd.to_numeric)
    df['Price']=df['Price'].astype(int)
    df['Meter'] = df['Meter'].apply(validate_num)
    df['Year']=df['Year'].apply(check_year)
    df['AuctioneerMake']=df['AuctioneerMake'].apply(validate_string)
    df['AuctioneerMake']=df['AuctioneerMake'].apply(validate_make_model)
    df['AuctioneerModel']=df['AuctioneerModel'].apply(validate_string)
    df['AuctioneerModel']=df['AuctioneerModel'].apply(validate_make_model)
    df['AuctioneerClassification'] = df.apply(lambda x: get_classification(x['Auctioneer'],x['Description'],x['TypeName'],x['Year'],x['AuctioneerMake'],x['AuctioneerModel']), axis=1)
    df['MeterCode'] = df['MeterCode'].apply(get_meter_code)
    df['LotNumber']= df.apply(get_lotnum,axis=1)
    df['SaleType'] = df.apply(lambda x: get_sale_type(x['Auctioneer'],x['SellingMethod'],x['Platform']), axis=1)
    df['AuctioneerDivision']=df['Platform'].apply(get_division)
    df['State']=df['State'].apply(validate_make_model)
    df['SerialNumber']=df['SerialNumber'].apply(validate_serial)
    df['Zip']=df['Zip'].apply(check_postal_code)
    df['DataSource']= df['Auctioneer']
    df['DataSourceType']='Primary'
    #Remove rows where city or Lot number may be null
    df = df[df.City.notnull()]
    df = df[df.LotNum.notnull()]
    #Slice out what we need to create our upload dataframe
    upload_df = df[['Auctioneer','AuctioneerDivision','AuctionDate','LotNumber','Price','CurrencyCode','Year','AuctioneerMake','AuctioneerModel','AuctioneerClassification','AuctioneerDescription','Meter','MeterCode','SerialNumber','City','State','Zip','CountryCode','DataSource','DataSourceType','SaleType']]

else:
    print('File does not match schema')
    raise
    input("Close to exit")


upload_df.to_csv('Ritchie'+timestamp+'.csv',index=False,na_rep='')
print('Scrape Done')
#input("Scrape Complete! Please Exit Now. Press any key to quit...")