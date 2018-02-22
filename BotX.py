import os
import time
import requests
import sys
import json
import requests.packages.urllib3
from firebase import firebase
from twitter import *
import twitter

#Setup a loop to send Temperature values at fixed intervals
fixed_interval = 1
start_interval = 2
deviceCondition = 0

#Init Firebase
firebase = firebase.FirebaseApplication('https://ramean.firebaseio.com/', None)
firebase_url = 'https://ramean.firebaseio.com/asap/device1'
auth_token = 'OoJx3VopPK3wqezjYKvCyGcsWHhcHg8qBBVUJSPv'

#Init TwitBot
CONSUMER_KEY = '7uBhEGYqgwE11PFj9UXz8fSpe'
CONSUMER_SECRET = 'oSgB3ZVlvFOiug69yPDuzXW7ZCEwDuSL07t36lbKoA6WD8k0vr'
ACCESS_KEY = '4114832412-N1dXpuYIZsyosGtrzEu55sB631SHcsXlSV6cV9L'
ACCESS_SECRET = 'MzkqHeH0NgQWoZT1NbGvM8CJSLZGPGoYZnUceMjO3XZFT'
me = 'iPamungkasss'
myDevice = 'TheEx_Project'
		
def slice_rsponc(main_string):          # If the response from the user contains two tasks, 
    main_string=main_string.lower()     # this function divides and returns them as individual
    sl_indx = 0
    if ' and ' in main_string:
        sl_indx = main_string.find('and')
    elif ' & ' in main_string:
        sl_indx = main_string.find('&')
    return(main_string[0:sl_indx],main_string[sl_indx:len(main_string)])
		
def take_action(i,Pi_buddy):
	global deviceCondition
	if (len(i)==0):
		return
	elif 'show device status, please' in i:
		print 'kondisi : '+str(deviceCondition)
		if deviceCondition==1 :
			status = {0:'OFF', 1:'ON'}
			print 'reply : device status here\n'
			resultTemp = firebase.get('/asap/device1/deviceTemp', 'value')
			resultSmokeIn = firebase.get('/asap/device1/deviceSmokeIn', 'value')
			resultSmokeOut = firebase.get('/asap/device1/deviceSmokeOut', 'value')
			resultCOIn = firebase.get('/asap/device1/deviceCOIn', 'value')
			resultCOOut = firebase.get('/asap/device1/deviceCOOut', 'value')
			resultFan = firebase.get('/asap/device1/deviceFan', 'value')
			Pi_buddy.direct_messages.new(user=me, text= ("Temperature = "+resultTemp+" *C"
														+"\nSmoke In = "+resultSmokeIn
														+"\nSmoke Out = "+resultSmokeOut
														+"\nCO In = "+resultCOIn
														+"\nCO Out = "+resultCOOut
														+"\nFan = "+status[int(resultFan)]
														+"\n\nAnything else?"
														))
		else:
			print 'no action on device stat'
			Pi_buddy.direct_messages.new(user=me, text="You should say \"Hi asap!\" first. Thankyou :)")
		return
	elif 'show local status, please' in i:
		print 'kondisi : '+str(deviceCondition)
		if deviceCondition==1 :
			#print 'reply : local status here\n'
			resultTemp = firebase.get('/asap/device1/localTemp', 'value')
			resultSmoke = firebase.get('/asap/device1/localSmoke', 'value')
			resultCO = firebase.get('/asap/device1/localCO', 'value')
			Pi_buddy.direct_messages.new(user=me, text= ("Temperature = "+resultTemp+" *C"		
														+"\nSmoke = "+resultSmoke
														+"\nCO = "+resultCO
														+"\n\nAnything else?"
														))
		else:
			print 'no action on local stat'
			Pi_buddy.direct_messages.new(user=me, text="You should say \"Hi asap!\" first. Thankyou :)")
		return
	elif 'show desc device, please' in i:
		print 'kondisi : '+str(deviceCondition)
		if deviceCondition==1 :
			#print 'reply : desc status here\n'
			resultID = firebase.get('/asap/device1/id', 'value')
			resultSN = firebase.get('/asap/device1/serialnumber', 'value')
			Pi_buddy.direct_messages.new(user=me, text= ("Device ID = "+resultID
														+"\nSerial Number = "+resultSN
														+"\n\nAnything else?"
														))
		else:
			print 'no action on desc device'
			Pi_buddy.direct_messages.new(user=me, text="You should say \"Hi asap!\" first. Thankyou :)")
		return
	elif 'nope' in i:
		print 'kondisi sebelumnya : '+str(deviceCondition)
		if deviceCondition==1:
			Pi_buddy.direct_messages.new(user=me, text="Okayy! See you next time\nHave a nice day")
			print 'kondisi sekarang : '+str(deviceCondition)
			deviceCondition=0
		else:
			print 'no action dude'
			Pi_buddy.direct_messages.new(user=me, text="Hmm, what do you mean dude?")
		return
	elif 'hi' in i:
		print 'kondisi sebelumnya : '+str(deviceCondition)
		if deviceCondition==0:
			Pi_buddy.direct_messages.new(user=me, text="Holaa, Welcome Back! May I help you?")
			print 'kondisi sekarang : '+str(deviceCondition)
			deviceCondition=1
		else:
			print 'no action bro'
			Pi_buddy.direct_messages.new(user=me, text="Hmm okayyy. What can I do for bro?")
		return
	elif 'sorry' in i:
		print 'kondisi : '+str(deviceCondition)
		if deviceCondition==1:
			Pi_buddy.direct_messages.new(user=me, text="Hmm ok, No Problem.")
		else:
			print 'no action guys'
			Pi_buddy.direct_messages.new(user=me, text="Hmm, what do you mean guys?")
		return
	else :
		#print 'reply : UNKNOWN\n'
		Pi_buddy.direct_messages.new(user=me, text="Can't understand!!!\nActually I am machine, dude :(")
		return
	requests.packages.urllib3.disable_warnings()

def main():
	try:
		os.system('cls')
		print '============================================================'
		print '\t\tWelcome to ASAP-Botv1.0'
		print '\tIntegrated w/ '+me+ "'s Twitter Account"
		print '\t\tGetting Started ...'
		print '============================================================\n'
		time.sleep(start_interval)
			
		read_out = False
		count = 0
		
		while 1:
			global deviceCondition
			tweetEx = Twitter(auth=OAuth(ACCESS_KEY,ACCESS_SECRET,CONSUMER_KEY,CONSUMER_SECRET))
			auth = OAuth(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,token=ACCESS_KEY,token_secret=ACCESS_SECRET)
			
			twitter_userstream = TwitterStream(auth=auth, domain='userstream.twitter.com')
			if count == 0:
				first_greeting = "Holaa! May I help you?"
				tweetEx.direct_messages.new(user=me, text=first_greeting)
				deviceCondition = 1
				print 'First Greeting!'
				print 'kondisi : '+str(deviceCondition)
			for msg in twitter_userstream.user():
				if 'direct_message' in msg:
					new_msg = msg ['direct_message']['text']
					user_msg = msg ['direct_message']['sender']['name']
					print user_msg + " said : " + new_msg
					if (msg['direct_message']['sender_screen_name']==me):
						for i in slice_rsponc(new_msg):
							take_action(i, tweetEx)
					elif (msg['direct_message']['sender_screen_name']!=me) and (msg['direct_message']['sender_screen_name']!=myDevice):
						tweetEx.direct_messages.new(user=msg['direct_message']['sender_screen_name'], text="Who are you? You're not part of my life, dude!")
						deviceCondition = 0
				time.sleep(fixed_interval)
						
			requests.packages.urllib3.disable_warnings()
			count = count + 1

	except IOError:
		print('Error! Something went wrong.')
	except KeyboardInterrupt:
		print('\n\nOPERATION HAS BEEN CANCELED!\n')
		sys.exit()
		
	print 'System has been exit'
	sys.exit()

if __name__ == '__main__':main()