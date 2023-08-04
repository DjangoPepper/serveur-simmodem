import time
import datetime


class simother :
	def CreateFileNameWithDate() -> str:
		time_now  = datetime.datetime.now().strftime('%Y-%m-%d_%H%M:%S')
		return time_now

	def CreateFileNameForSoundFile(_APPELANT_SRV) -> str:
		# FILENAME = str(_APPELANT_SRV) + "_" + str(CreateFileNameWithDate()) + ".wav"
		# FILENAME = str(_APPELANT_SRV) + "_" + str(CreateFileNameWithDate()) + ".amr"
		FILENAME = str(_APPELANT_SRV) + "_" + str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M:%S')) + ".amr"
		return FILENAME

	def CallCountDown(t):
		# define the countdown func.	
		while t:
			mins, secs = divmod(t, 60)
			timer = '{:02d}:{:02d}'.format(mins, secs)
			print(timer, end="\r")
			time.sleep(1)
			t -= 1
