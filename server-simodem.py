#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

#sudo apt-get install python3-pyaudio
#pip install mysql
#pip install mysql-connector
#trop long :
#Sending: AT+CPIN?
#Device responded:  ['AT+CPIN?', '+CPIN: SIM PIN', '', 'OK']
#AT+CPIN=0000
#Device responded:  ['AT+CPIN=0000', 'OK', '', '+CPIN: READY']

from src.serial_comm import SerialComm
from src.sim_other import *
from src.sim_audio import *
from src.sim_sql import *
from src.simmodem import *
from src.sim_hardaware import *
import time
import datetime
from pydub import AudioSegment
modem = Modem('/dev/ttyS0', baudrate=115200, timeout=0.5, at_cmd_delay=0.1, debug=True)

FLAG_ONLINE = False

global FLAG_CAN_RECORD
FLAG_CAN_RECORD = False

FLAG_OFFLINE = True
FLAG_CONNECTED = False
global FLAG_RECORDED
FLAG_RECORDED = False
FLAG_CALLCOUNTDOWN = False

global APPELANT_SRV
APPELANT_SRV = 5366

global USER_ID
USER_ID = 1

global DTMF_SONG
DTMF_SONG = ""


PIN_NUMBER = "0000"

TELM = "0664018952"
TELB = "0800943376"
TEL = TELB

global RECORDED_MESSAGE
# RECORDED_MlESSAGE = bin(0)

def CreateSoundFileName(_APPELANT_SRV) -> str:
    
    FILENAME = str(_APPELANT_SRV) + "_" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')) + ".amr"
    # FILENAME = str(_APPELANT_SRV) + "_" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')) + ".wav"
    return FILENAME

def CallCountDown(t):
	# define the countdown func.

	while t:
		mins, secs = divmod(t, 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		print(timer, end="\r")
		time.sleep(1)
		t -= 1

def main_initmodem():
	modem.set_cmee(0)
	modem.set_mode_record(2)
	modem.get_signal_quality_range()
       	#modem.check_sim_pin(10, PIN_NUMBER)
	modem.check_sim_pin(10, PIN_NUMBER)
	modem.get_network_registration_status()
	modem.set_recognition(0)
	modem.set_vtd(10)
	modem.hangup()

def main_loop():
		global USER_ID
		global FLAG_OFFLINE
		global FLAG_CONNECTED
		global FLAG_RECORDED
		global APPELANT_SRV
		DTMF_SONG = MySqlDATABASE.get_appelant(USER_ID)
		APPELANT_SRV = DTMF_SONG[1]
		DTMF_SONG = DTMF_SONG[0]

		print("DTMF SONG: ", DTMF_SONG)

		if FLAG_OFFLINE == True:
			modem.call(TEL)
			CallCountDown(5)
			FLAG_CONNECTED = modem.check_callinprogress()
			for x in range (10):
				if FLAG_CONNECTED == False :
					FLAG_CONNECTED = modem.check_callinprogress()
					print ("Recall : ", x)
					CallCountDown(1)
					if x > 10 :
						print("server didn't answer")
						modem.hangup()
						main_exit()

			if FLAG_CONNECTED == True :
				# print("user id : ", USER_ID)
				# print("Must waiting....")
				# CallCountDown(3)
				FLAG_CAN_RECORD = modem.send_dtmf_code(DTMF_SONG)
				print("DTMF SEND")


			if FLAG_CAN_RECORD == True and FLAG_RECORDED == False :
				# print ("RECORD WAV2 AUDIO id 1 in progress")
				print ("RECORD AMR AUDIO id 1 in progress")
				modem.start_record(1,0) #record call in id 1(slot) mode 0 AMR,1 wav,2 wav adpcm. Auto channel 0
				t = 1
				while FLAG_CONNECTED == True :
					FLAG_CONNECTED = modem.check_callinprogress()
					mins, secs = divmod(t, 60)
					timer = '{:02d}:{:02d}'.format(mins, secs)
					t += 1
					print(timer, end="\r")
					# print(t," ", timer, end="\r")
					time.sleep(1)
					
					if t > 4 :
						print("4s elapsed")
						FLAG_CONNECTED = False
				modem.hangup()
				modem.stop_record()
				modem.list_record(1)
				modem.hangup()
				
				FLAG_CAN_RECORD = False
				FLAG_CONNECTED  = False
				FLAG_OFFLINE = True
				FLAG_CONNECTED = False
				print ("RECORD AUDIO ended")
				
				RECORDED_SIZE = modem.size_record(1)
				RECORDED_MESSAGE = modem.get_data_record(1,RECORDED_SIZE,0)
				# RECORDED_MESSAGE_AS_BYTE = RECORDED_MESSAGE.encode('utf-8')		
				RECORDED_MESSAGE_AS_BYTE = RECORDED_MESSAGE.encode('ISO-8859-1')						
				print ("RECORD Downloaded")
				
				FILENAME = CreateSoundFileName(USER_ID)
				datafile=open(FILENAME, 'wb')#juillet
				datafile.write(RECORDED_MESSAGE_AS_BYTE)
				print ("RECORD File create")
				# 	main_exit()

				# Chemin vers le fichier AMR que tu souhaites lire
				# chemin_fichier_amr = FILENAME

				# Charger le fichier AMR à l'aide de pydub
				audio = AudioSegment.from_file(FILENAME, format="amr")

				# Lecture du fichier audio (peut varier selon ton système d'exploitation)
				audio.export("sortie.wav", format="wav")


def main_exit():
	# nice and clean exit
	modem.send_sms('+33664018952', 'Your job will be mine : .... !')
	# SimHardaware.L_OFFON()

def main():
	main_initmodem()
	main_loop()
	
if __name__ == "__main__":
	main()
