import urllib2, json, urllib
from pprint import pprint

basicUrl = "https://api.telegram.org/bot"
token = "90700313:AAGff_A4qQ90nKduJiymVZtv3jYdOivVvzc/"

def sendMessage(chat_id, text):
	parameters = {'chat_id':chat_id, 'text':text}
	TextData = urllib.urlencode(parameters)
	requestText = urllib2.Request(basicUrl+token+"sendMessage", TextData)
	responseText = urllib2.urlopen(requestText).read()

def sendAudio(chat_id, file_id, title):
	parameters = {'chat_id':chat_id, 'audio':file_id, 'title':title}
	AudioData = urllib.urlencode(parameters)
	requestAudio = urllib2.Request(basicUrl+token+"sendAudio", AudioData)
	responseAudio = urllib2.urlopen(requestAudio).read()
	return requestAudio

last_update_id = 0
while True:
	
	logFile = open("chatLog.txt", "a+")
	
	#get the unconfired updates and confirm the past updates
	#jsonUpdate = urllib2.urlopen(basicUrl+token+"getUpdates?offset="+str(last_update_id+1)+"&timeout=100").read()
	values = {'offset':last_update_id+1, 'timeout':100}
	data = urllib.urlencode(values)
	request = urllib2.Request(basicUrl+token+"getUpdates", data)
	response = urllib2.urlopen(request)
	jsonUpdate = response.read()
	
	updates = json.loads(jsonUpdate)
	result = updates['result']

	#write the messages in the log file
	if jsonUpdate!= "{\"ok\":true,\"result\":[]}":
		logFile.write(jsonUpdate+"\n")
	logFile.close()
	
	#iterate trought the message if any
	for i in result:
		
		#get info about the message
		senderName = i['message']['from']['first_name']
		update_id = i['update_id']
		chat_id = i['message']['chat']['id']
		message = i['message']['text']
		messageList = message.lower().split(" ")
		if "musica" in messageList:
			sendAudio(chat_id, "BQADBAADAQADZUfwCbWV_Q3CLxrLAg", "Il canto del Capro")
		else:
			sendMessage(chat_id, "Ciao {0}".format(senderName))
		
		#send a message to stefano
		#confirm = urllib2.urlopen(basicUrl+token+"sendMessage?chat_id={0}&text=responded to {1} who send {2}".format("166741861", senderName, message)).read()

		print "responded to {}".format(senderName)
		
		if update_id>last_update_id:
			last_update_id = update_id
	
