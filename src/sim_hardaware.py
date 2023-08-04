	
import RPi.GPIO as IO, atexit, logging, sys
from time import sleep

GSM_ON=11			#11-17
GSM_RESET = 12		#12-18

IO.setwarnings(False)
IO.setmode(IO.BOARD)
IO.setup(GSM_ON, IO.OUT, initial=IO.HIGH)
IO.setup(GSM_RESET, IO.OUT, initial=IO.HIGH)

class SimHardaware:

	def L_OFFON():
		"""
		Reset (turn off and on) the SIM800 module by taking the power line for >1s
		and then wait 5s for the module to boot.
		"""
		print("LOOP OFF/ON")
		# print("LOOP OFF")
		SimHardaware.H_OFF()
		print("HARD OFF sleep")
		sleep(5.0)
		SimHardaware.R_OFF()
		print("RESET OFF sleep")
		sleep(5.0)
		
		SimHardaware.R_ON()
		print("RESET ON sleep")
		sleep(5.0)
		SimHardaware.H_ON()
		print("HARD ON sleep")
		sleep(5.0)

	def H_OFF():
		"""
		(turn off) the SIM800
		"""
		print("HARD Off")
		IO.output(GSM_ON, IO.LOW)
		sleep(1.0)

	def H_ON():
		"""
		(turn on) the SIM800 module
		"""
		print("HARD On")
		IO.output(GSM_ON, IO.HIGH)
		sleep(1.0)

	def R_ON():
		"""
		(reset pin on) the SIM800 module
		"""
		print("RESET On")
		IO.output(GSM_RESET, IO.HIGH)
		sleep(1.0)
	
	def R_OFF():
		"""
		(reset pin off) the SIM800 module
		"""
		print("RESET Off")
		IO.output(GSM_RESET, IO.LOW)
		sleep(1.0)