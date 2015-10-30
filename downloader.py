import time
import schedule
import csv
import subprocess
import logging
from datetime import datetime

def loadConfig():
	with open('channels.csv', 'rb') as csvFile:
		reader = csv.reader(csvFile)
		headerLine = True
		rowsList = []
		for row in reader:
			if headerLine:
				headerLine = False
				continue
			rowTup = (row[0], row[1])
			rowsList.append(rowTup)
		return rowsList

def buildArtistName(artistName):
	artistName = artistName.replace(' ', '\ ')
	return artistName

def buildOutputPath(artistName):
	outputpath = 'music/' + artistName + '\ -\ ' + 'Uploads' + '/%(title)s.%(ext)s'
	outputpath = outputpath.replace('(', '\(')
	outputpath = outputpath.replace(')', '\)')
	return outputpath

def download():
	logging.info('Begin Processing: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	config = loadConfig()
	for row in config:
		artistname = buildArtistName(row[1])
		outputpath = buildOutputPath(artistname)
		script = 'youtube-dl --add-metadata --embed-thumbnail --playlist-end 10 --dateafter now-2month -f 140 -i -o ' + outputpath + ' ' + row[0]
		with open('youtube-dl-log.log', "w") as outfile:
			try:
				subprocess.check_call(script, shell=True, stdout=outfile)
			except:
				logging.info('Something went wrong while executing command.')
	#upload_google()
	logging.info('End Processing: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def upload_google():
	logging.info('Begin Google Upload: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	with open('google-upload.log', "w") as outfile:
		try:
			script = 'python /home/michael/git/gmusicapi-scripts/gmsync.py -c /home/michael/youtube-downloader/oauth /home/michael/youtube-downloader/music'
			subprocess.check_call(script, shell=True, stdout=outfile)
		except:
			logging.info('Something went wrong while executing command.')
	logging.info('End Google Upload: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

logging.basicConfig(filename='app.log', level=logging.INFO)
#upload_google()
download()
schedule.every(30).minutes.do(download)

while 1:
	schedule.run_pending()
	time.sleep(1)
