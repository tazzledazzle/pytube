import time
import schedule
import csv
import subprocess

def download():
	with open('channels.csv','rb') as csvFile:
		reader = csv.reader(csvFile)
		firstline = True
		for row in reader:
			if firstline:
				firstline = False
				continue
			artistname = row[1]
			artistname = artistname.replace(' ', '\ ')
			outputpath = 'music' + artistname + '/%(title)s.%(ext)s'
			outputpath = outputpath.replace('(', '\(')
			outputpath = outputpath.replace(')', '\)')
			subprocess.check_call('youtube-dl --dateafter now-1month -f 140 -o ' + outputpath + ' ' + row[0], shell=True)

schedule.every(30).minutes.do(download)

while 1:
	schedule.run_pending()
	time.sleep(1)

