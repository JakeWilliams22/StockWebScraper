import quandl
import datetime
import csv
from pprint import pprint
quandl.ApiConfig.api_key="DfbkPnn4g-T4sjzWXKtf" #This is a free key, it is not confidential

src="stockList.csv"
dest="historic_info.csv"
start_date = datetime.date(2017,01,01)
end_date = datetime.date.today();

stockList = []
notFoundSymbols = []

def writeColumnHeaders(data, writer):
  writer.writerow(data.meta['column_names'])
  
hasRun = False
def writeToFile(data, writer):
  global hasRun;
  if not hasRun:
    writeColumnHeaders(data, writer);
    hasRun = True
  for row in data.values:
    writer.writerow(row._raw_data);

def readFromStockList():
  with open(src, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    return next(reader)

def getStockData(stockList):
  with open(dest, 'wb') as destFile:
    writer = csv.writer(destFile, delimiter=',')
    for ticker in stockList:
      quandlSrc = "WIKI/" + ticker.upper().strip();
      try:
        data = quandl.Dataset(quandlSrc).data(params={'start_date': start_date,'end_date': end_date})
        writeToFile(data, writer);
      except quandl.errors.quandl_error.NotFoundError:
        notFoundSymbols.append(ticker);


stockList = readFromStockList()
getStockData(stockList)
print "symbols not on quandl: " + str(notFoundSymbols)

