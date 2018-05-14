

import pandas as pd
import numpy as np
import urllib.request
import csv
from dateutil import parser

urlInputs = ['http://www.bcb.gov.br/pec/Indeco/Ingl/ie5-24i.xlsx', 'http://www.bcb.gov.br/pec/Indeco/Ingl/ie5-26i.xlsx']
inputFiles = []


class timeSeriesTest:
    def __init__(self, url='', excelInput=''):
        self.url = url
        self.excelInput = excelInput
        self.currentDate = ''
        self.df = ''
        self.outputList = []
        print("Downloading inputs from", url)
        inputFiles.append(url.split('/')[-1])
        urllib.request.urlretrieve(url, filename=url.split('/')[-1])
        
        
    def loadTimeSeriesData(self):
        print("Loading time series data from", self.url)
        
        if self.excelInput == 'ie5-24i.xlsx':
            self.outputList = []
            self.df = pd.read_excel(self.excelInput, headers=None)
            parsedDate = parser.parse('{}/{}/{}'.format(self.df.iloc[-7][0], self.df.iloc[-7][1][0:3], self.df.iloc[-11][1]))
            self.currentDate = '{}/{}/{}'.format(parsedDate.month, parsedDate.day, parsedDate.year)
            #print(self.currentDate)
            self.outputList.append(self.currentDate)
            self.outputList.extend(self.df.iloc[-11][2:].values.tolist())
            
        else:
            self.outputList = []
            self.df = pd.read_excel(self.excelInput, headers=None)
            parsedDate = parser.parse(self.df.columns[2])
            self.currentDate = '{}/{}/{}'.format(parsedDate.month, 1, parsedDate.year)
            self.outputList.append(self.currentDate)
            self.outputList.append(self.df.iloc[-6].values[-1])

    
    def writeOutputData(self):
        if self.excelInput == 'ie5-24i.xlsx':
            with open('bcb_output_1.csv', 'a') as outputFile1:
                wr = csv.writer(outputFile1, quoting=csv.QUOTE_ALL)
                #print(inputSeries[0].iloc[-11])
                wr.writerow(self.outputList)
        
        else:
            with open('bcb_output_2.csv', 'a') as outputFile2:
                wr2 = csv.writer(outputFile2, quoting=csv.QUOTE_ALL)
                wr2.writerow(self.outputList)
            




    
def main():
    seriesObj1 = timeSeriesTest(url=urlInputs[0], excelInput='ie5-24i.xlsx')
    seriesObj2 = timeSeriesTest(url=urlInputs[1], excelInput='ie5-26i.xlsx')
    inputFiles.clear()
    seriesObj1.loadTimeSeriesData()
    seriesObj2.loadTimeSeriesData()
    seriesObj1.writeOutputData()
    seriesObj2.writeOutputData()

if __name__ == '__main__':
    main()