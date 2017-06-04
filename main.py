import quandl
import datetime
import csv
import sys
from pprint import pprint
quandl.ApiConfig.api_key="DfbkPnn4g-T4sjzWXKtf" #This is a free key, it is not confidential

src="list_of_stocks.csv"
dest="historic_info.csv"
start_date = datetime.date(2013,6,4)
# start_date = datetime.date(2017,1,1)
end_date = datetime.date.today();

stockList = []
notFoundSymbols = []

def writeColumnHeaders(ticker, data, writer):
  writer.writerow([ticker] + data.meta['column_names'])
  
hasRun = False
def writeToFile(ticker, data, writer):
  global hasRun;
  if not hasRun:
    writeColumnHeaders(ticker, data, writer);
    hasRun = True
  for row in data.values:
    writer.writerow([ticker] + row._raw_data);

def readFromStockList():
  with open(src, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    return next(reader)

def getStockData(stockList, start_date):
  with open(dest, 'wb') as destFile:
    writer = csv.writer(destFile, delimiter=',')
    for i, ticker in enumerate(stockList):
      print "Parsing stock # " + str(i) + ", " + str(ticker);
      quandlSrc = "WIKI/" + ticker.upper().strip();
      try:
        data = quandl.Dataset(quandlSrc).data(params={'start_date': str(start_date),'end_date': end_date})
        writeToFile(ticker, data, writer);
      except quandl.errors.quandl_error.NotFoundError:
        notFoundSymbols.append(ticker);

def run(startDate):
  stockList = readFromStockList()
  print "Parsing " + str(len(stockList)) + " stocks"
  getStockData(stockList, startDate)
  print ("symbols not on quandl: " + str(notFoundSymbols))
        
def parseCommandLineArgs():
  if (len(sys.argv) != 2):
    print "Please enter a start date as such: \"YYYY-MM-DD\""
  else:
    date = sys.argv[1].split("-")
    startDate = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    run(startDate);
        
parseCommandLineArgs();        


