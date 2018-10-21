from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import requests
from fuzzywuzzy import fuzz

# key = full company name -> tuple of info ( ticker, sector, industry)
companiesMap = {}


def index(request):
    return HttpResponse("This is a test page")

def blackrockTest(request):
    ticker = companyToTicker('apple')
    with open('app/page/pageBegin.html', 'r') as f:
        data1 = f.read()
    data2 = blackrockPerformance(ticker)
    with open('app/page/pageMiddle1.html', 'r') as f:
        data3 = f.read()
    data4 = blackrockSearchSecurities(ticker)
    with open('app/page/pageMiddle2.html', 'r') as f:
        data5 = f.read()
    data6 = blackrockSecurityData(ticker)
    with open('app/page/pageEnd.html', 'r') as f:
        data7 = f.read()
    return HttpResponse(data1+data2+data3+data4+data5+data6+data7)


def buildCompaniesMap():
    """
    builds a map of company names using the
    pandas data frame
    """
    df = pd.read_csv('../../secwiki_tickers.csv')
    # print (df)
    for index, row in df.iterrows():
        companyName = row["name"]
        # print (companyName)
        ticker = row["ticker"]
        sector = row["sector"]
        industry = row["industry"]
        companiesMap[companyName] = (ticker, sector, industry)

def companyToTicker(company):
    for key, value in companiesMap.items():
        if fuzz.token_set_ratio(key, company.lower()) > 80 :
            print(value[0])
            return value[0]
    return None

def blackrockPerformance(ticker):
    output = requests.get(
            url="https://www.blackrock.com/tools/hackathon/performance",
            params={ 'identifiers' : ticker })
    return output.text

def blackrockSearchSecurities(ticker):
    output = requests.get(
            url="https://www.blackrock.com/tools/hackathon/search-securities",
            params={ 'identifiers' : ticker })
    return output.text

def blackrockSecurityData(ticker):
    output = requests.get(
            url="https://www.blackrock.com/tools/hackathon/security-data",
            params={ 'identifiers' : ticker })
    return output.text

buildCompaniesMap()
