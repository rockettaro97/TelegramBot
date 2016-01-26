import urllib2, json, urllib, requests
from pprint import pprint
from random import randint

basicUrl = "https://api.telegram.org/bot"
token = "163052614:AAHAgAjpPkSGUOYv_fu1m9XcxDXyhDhsr2I/"

filesPath = "files/"

def sendChatAction(chat_id, action):
	r = requests.post(basicUrl+token+"sendChatAction", params={"chat_id":chat_id, "action":action})
	return r.text

def sendMessage(chat_id, text):
	parameters = {'chat_id':chat_id, 'text':text}
	r = requests.post(basicUrl+token+"sendMessage", params=parameters)
	return r.text

def sendAudio(chat_id, file_id, title):
	files = {"audio":open(filesPath+file_id, "rb")}
	parameters = {'chat_id':chat_id, 'title':title}
	r = requests.post(basicUrl+token+"sendAudio", files=files, params=parameters)
	return r.text


def sendPhoto(chat_id, file_id, caption):
	parameters = {'chat_id':chat_id,'caption':caption,'photo':file_id}
	files = {"photo":open(filesPath+file_id, "rb")}
	r = requests.post(basicUrl+token+"sendPhoto", files=files, params=parameters)
	return r.text

last_update_id = 0
while True:
	phrasesFile = open("phrases.json")
	phrases = json.load(phrasesFile)
	phrasesFile.close()
	
	logFile = open("chatLog.txt", "a+")
	
	#get the unconfired updates and confirm the past updates
	#jsonUpdate = urllib2.urlopen(basicUrl+token+"getUpdates?offset="+str(last_update_id+1)+"&timeout=100").read()
	values = {'offset':last_update_id+1, 'timeout':100}
	
	response = requests.post(basicUrl+token+"getUpdates", values).text
	
	updates = json.loads(response)
	result = updates['result']

	#write the messages in the log file
	if response!= "{\"ok\":true,\"result\":[]}":
		logFile.write(response+"\n")
	logFile.close()
	
	#iterate trought the message if any
	for i in result:
		
		#get info about the message
		senderName = i['message']['from']['first_name']
		update_id = i['update_id']
		chat_id = i['message']['chat']['id']

		if 'text' in i['message']:
			message = i['message']['text']
			messageList = message.lower().split(" ")

			#print phrases['output'][0]['musica']

			for w in messageList:
				if w in phrases['output']:
					info = phrases['output'][w]
					messageType = info['type']
					if messageType=="text":
						contentLen = len(info['content'])-1
						sendMessage(chat_id, info['content'][randint(0, contentLen)]['text'])
					elif messageType=="photo":
						contentLen = len(info['content'])-1
						randomInteger = randint(0, contentLen)
						sendChatAction(chat_id, "upload_photo")
						sendPhoto(chat_id, info['content'][randomInteger]['file_id'], info['content'][randomInteger]['caption'])
					if messageType=="audio":
						contentLen = len(info['content'])-1
						randomInteger = randint(0, contentLen)
						sendChatAction(chat_id, "upload_audio")
						sendAudio(chat_id, info['content'][randomInteger]['file_id'], info['content'][randomInteger]['title'])
					print "responded to {}".format(senderName)

		else:
			sendMessage(chat_id, "manda solo testo")
		#send a message to stefano
		#confirm = urllib2.urlopen(basicUrl+token+"sendMessage?chat_id={0}&text=responded to {1} who send {2}".format("166741861", senderName, message)).read()

		
		if update_id>last_update_id:
			last_update_id = update_id
	
