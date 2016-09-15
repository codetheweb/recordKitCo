import requests
import base64
import os.path

filename = "data.csv" # where the data will be saved

Symbols = ["DJIA", "USDX", "OIL", "SILVER", "GOLD"] # symbols that should be recorded

def getData(symbol): # gets specified symbol using Kitco's API
	r = requests.get('http://charts.kitco.com/KitcoCharts/RequestHandler?requestName=getSymbolSnapshot&Symbol=' + symbol)
	return base64.b64decode(r.content).split(',')

def getBid(symbol):
	return getData(symbol)[1]

def getBidTime(symbol):
	return getData(symbol)[0]

# for some reason opening with open(file, 'a') doesn't work even though it should
if (os.path.isfile(filename)):
	file = open(filename, 'r+')
else:
	file = open(filename, 'w+') # create the file too if it doesn't exist

if (file.read() == ""): # write out header if it doesn't exist
	file.write(','.join(Symbols) + "\n")

newDataRow = getBidTime(Symbols[0]) # start off new data row with the last updated time

for symbol in Symbols: # loops over the specified symbols and saves the bid price of each one
	newDataRow += getBid(symbol)

	if (Symbols.index(symbol) != len(Symbols) - 1): # unless we're on the last symbol
		newDataRow += ", " # add a seperator
	else:
		newDataRow += "\n" # otherwise add a newline

file.write(newDataRow) # write a new row to the CSV file

file.close()
