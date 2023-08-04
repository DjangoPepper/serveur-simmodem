from src.serial_comm import SerialComm
import time
from enum import Enum
from logging import getLogger
SIM_NUMBER = 0000
# _FLAG_RECORD = False

class StateOfCall(Enum):
	"""fourth element CLCC """
	Active = 0
	Held = 1
	Dialing = 2
	Alerting = 3
	Incoming = 4
	Waiting = 5
	Disconnect = 6
	Errors = 7

class NetworkMode(Enum):
	"""Network mode of the modem (get/set)"""

	AUTOMATIC = 2
	GSM_ONLY = 13
	LTE_ONLY = 38
	ANY_BUT_LTE = 48

class SignalQuality(Enum):
	"""Signal quality expressed as ranges"""

	LOW = "LOW"
	FAIR = "FAIR"
	GOOD = "GOOD"
	EXCELLENT = "EXCELLENT"


class Modem:
	"""Class for interfacing with mobile modem"""

	def __init__(
		self,
		address,
		baudrate=115200,
		timeout=1,
		at_cmd_delay=0.1,
		debug=True,
	):
		self.comm = SerialComm(
			address=address,
			baudrate=baudrate,
			timeout=timeout,
			at_cmd_delay=at_cmd_delay,
		)
		self.debug = debug
		self.comm.send("ATZ")
		self.comm.send("ATE1")
		read = self.comm.read_lines()
		# ['ATZ', 'OK', 'ATE1', 'OK']
		if read[-1] != "OK":
			raise Exception("Modem do not respond", read)

		if self.debug:
			print("Modem connected, debug mode enabled")

	def reconnect(self) -> None:
		try:
			self.comm.close()
		except:
			pass

		self.comm = SerialComm(
			address=self.comm.address,
			baudrate=self.comm.baudrate,
			timeout=self.comm.timeout,
			at_cmd_delay=self.comm.at_cmd_delay,
		)

		self.comm.send("ATZ")
		self.comm.send("ATE1")
		read = self.comm.read_lines()
		# ['ATZ', 'OK', 'ATE1', 'OK']
		if read[-1] != "OK":
			raise Exception("Connection lost", read)

		if self.debug:
			print("Modem connected, debug mode enabled")

	def close(self) -> None:
		self.comm.close()

	# --------------------------------- HARDWARE --------------------------------- #

	def get_manufacturer_identification(self) -> str:
		if self.debug:
			self.comm.send("AT+CGMI=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGMI")

		self.comm.send("AT+CGMI")
		read = self.comm.read_lines()

		if self.debug:
			print("Device responded: ", read)
		# ['AT+CGMI', 'SIMCOM INCORPORATED', '', 'OK']

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def get_model_identification(self) -> str:
		if self.debug:
			self.comm.send("AT+CGMM=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGMM")

		self.comm.send("AT+CGMM")
		read = self.comm.read_lines()

		# ['AT+CGMM', 'SIM7000E', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def get_serial_number(self) -> str:
		if self.debug:
			self.comm.send("AT+CGSN=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGSN")

		self.comm.send("AT+CGSN")
		read = self.comm.read_lines()

		# ['AT+CGSN', '89014103211118510700', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def get_firmware_version(self) -> str:
		if self.debug:
			self.comm.send("AT+CGMR=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGMR")

		self.comm.send("AT+CGMR")
		read = self.comm.read_lines()

		# ['AT+CGMR', '+CGMR: LE20B03SIM7600M22', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(": ")[1]

	def get_volume(self) -> str:
		if self.debug:
			self.comm.send("AT+CLVL=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CLVL")

		self.comm.send("AT+CLVL?")
		read = self.comm.read_lines()

		# ['AT+CLVL?', '+CLVL: 5', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(": ")[1]

	def set_volume(self, volume: int) -> str:
		if self.debug:
			self.comm.send("AT+CLVL=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CLVL={}".format(volume))

		if int(volume) < 0 or int(volume) > 5:
			raise Exception("Volume must be between 0 and 5")
		self.comm.send("AT+CLVL={}".format(volume))
		read = self.comm.read_lines()

		# ['AT+CLVL=5', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def improve_tdd(self) -> str:
		if self.debug:
			self.comm.send("AT+AT+PWRCTL=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+AT+PWRCTL=0,1,3")

		# ['AT+PWRCTL=?', '+PWRCTL: (0-1),(0-1),(0-3)', '', 'OK']
		self.comm.send("AT+PWRCTL=0,1,3")
		read = self.comm.read_lines()

		# ['AT+PWRCTL=0,1,3', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def enable_echo_suppression(self) -> str:
		if self.debug:
			self.comm.send("AT+CECM=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CECM=1")

		self.comm.send("AT+CECM=1")
		read = self.comm.read_lines()

		# ['AT+CECM=1', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def disable_echo_suppression(self) -> str:
		if self.debug:
			self.comm.send("AT+CECM=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CECM=0")

		self.comm.send("AT+CECM=0")
		read = self.comm.read_lines()

		# ['AT+CECM=0', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	# ---------------------------------- NETWORK --------------------------------- #

	def get_network_registration_status(self) -> str:
		if self.debug:
			self.comm.send("AT+CREG=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CREG?")

		self.comm.send("AT+CREG?")
		read = self.comm.read_lines()

		# ['AT+CREG?', '+CREG: 0,1', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(": ")[1]

	def get_network_mode(self) -> NetworkMode:
		if self.debug:
			self.comm.send("AT+CNMP=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CNMP?")

		self.comm.send("AT+CNMP?")
		read = self.comm.read_lines()

		# ['AT+CNMP?', '+CNMP: 2', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		nm = read[1].split(": ")[1]

		return NetworkMode(int(nm))

	def get_network_name(self) -> str:
		if self.debug:
			self.comm.send("AT+COPS=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+COPS?")

		self.comm.send("AT+COPS?")
		read = self.comm.read_lines()

		# ['AT+COPS?', '+COPS: 0,0,"Vodafone D2",7', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(",")[2].strip('"')

	def get_network_operator(self) -> str:
		if self.debug:
			self.comm.send("AT+COPS=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+COPS?")

		self.comm.send("AT+COPS?")
		read = self.comm.read_lines()

		# ['AT+COPS?', '+COPS: 0,0,"Vodafone D2",7', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(",")[2].strip('"').split(" ")[0]

	def get_signal_quality(self) -> str:
		if self.debug:
			self.comm.send("AT+CSQ=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CSQ")

		self.comm.send("AT+CSQ")
		read = self.comm.read_lines()

		# ['AT+CSQ', '+CSQ: 19,99', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(": ")[1]

	def get_signal_quality_db(self) -> int:
		if self.debug:
			self.comm.send("AT+CSQ=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CSQ")

		self.comm.send("AT+CSQ")
		read = self.comm.read_lines()

		# ['AT+CSQ', '+CSQ: 19,99', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		raw = read[1].split(": ")[1].split(",")[0]
		return -(111 - (2 * int(raw)))

	def get_signal_quality_range(self) -> SignalQuality:
		if self.debug:
			self.comm.send("AT+CSQ=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CSQ")

		self.comm.send("AT+CSQ")
		read = self.comm.read_lines()

		# ['AT+CSQ', '+CSQ: 19,99', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		raw = read[1].split(": ")[1].split(",")[0]
		if int(raw) < 7:
			return SignalQuality.LOW
		elif int(raw) < 15:
			return SignalQuality.FAIR
		elif int(raw) < 20:
			return SignalQuality.GOOD
		else:
			return SignalQuality.EXCELLENT

	def get_phone_number(self) -> str:
		if self.debug:
			self.comm.send("AT+CNUM=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CNUM")

		self.comm.send("AT+CNUM")
		read = self.comm.read_lines()

		# ['AT+CNUM', '+CNUM: ,"+491234567890",145', '', 'OK']
		# ['AT+CNUM', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK" or read[1] == "OK":
			raise Exception("Command failed")
		return read[1].split(",")[1].strip('"')

	def set_network_mode(self, mode: NetworkMode) -> str:
		self.comm.send("AT+CNMP={}".format(mode.value))
		read = self.comm.read_lines()
		# ['AT+CNMP=2', 'OK']
		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	# ------------------------------------ GPS ----------------------------------- #

	def get_gps_status(self) -> str:
		if self.debug:
			self.comm.send("AT+CGPS=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGPS?")

		self.comm.send("AT+CGPS?")
		read = self.comm.read_lines()

		# ['AT+CGPS?', '+CGPS: 0,1', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1].split(": ")[1]

	def start_gps(self) -> str:
		if self.debug:
			self.comm.send("AT+CGPS=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGPS=1,1")

		self.comm.send("AT+CGPS=1,1")
		read = self.comm.read_lines()

		# ['AT+CGPS=1', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def stop_gps(self) -> str:
		if self.debug:
			self.comm.send("AT+CGPS=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGPS=0")

		self.comm.send("AT+CGPS=0")
		read = self.comm.read_lines()

		# ['AT+CGPS=0', 'OK', '', '+CGPS: 0']
		# ['AT+CGPS=0', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] == "+CGPS: 0" or read[-1] == "OK":
			raise Exception("Command failed")
		return read[1]

	def get_gps_coordinates(self) -> dict:
		if self.debug:
			self.comm.send("AT+CGPS=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CGPS=1,1")
			print("Sending: AT+CGPSINFO")

		self.comm.send("AT+CGPS=1,1")
		self.comm.send("AT+CGPSINFO")
		# self.comm.send("AT+CGPS=0")
		read = self.comm.read_lines()

		# +CGPSINFO: [lat],[N/S],[log],[E/W],[date],[UTC time],[alt],[speed],[course]
		# ['AT+CGPS=1', 'OK', 'AT+CGPSINFO', '+CGPSINFO: 1831.991044,N,07352.807453,E,141008,112307.0,553.9,0.0,113', 'OK']
		# ['AT+CGPS=1', 'OK', 'AT+CGPSINFO', '+CGPSINFO: ,,,,,,,,', '', 'OK'] # if no gps signal
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return {
			"latitude": read[3].split(": ")[1].split(",")[0]
			+ read[3].split(": ")[1].split(",")[1],
			"longitude": read[3].split(": ")[1].split(",")[2]
			+ read[3].split(": ")[1].split(",")[3],
			"altitude": read[3].split(": ")[1].split(",")[6],
			"speed": read[3].split(": ")[1].split(",")[7],
			"course": read[3].split(": ")[1].split(",")[8],
		}

	# ------------------------------------ SMS ----------------------------------- #

	def get_sms_list(self) -> list:
		if self.debug:
			self.comm.send("AT+CMGF=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CMGF=1")
			print('Sending: AT+CMGL="ALL"')

		self.comm.send("AT+CMGF=1")
		self.comm.send('AT+CMGL="ALL"')

		read = self.comm.read_lines()
		sms_lines = [x for x in read if x != ""]  # remove empty lines
		sms_lines = sms_lines[5 : len(sms_lines) - 1]  # remove command and OK
		tuple_list = [
			tuple(sms_lines[i : i + 2]) for i in range(0, len(sms_lines), 2)
		]  # group sms info with message

		sms_list = []
		for i in tuple_list:
			sms_list.append(
				{
					"index": i[0].split(":")[1].split(",")[0].strip(),
					"number": i[0].split('READ","')[1].split('","","')[0],
					"date": i[0].split('","","')[1].split(",")[0],
					"time": i[0].split(",")[5].split("+")[0],
					"message": i[1].replace("\r\n", "").strip(),
				}
			)

		# ['AT+CMGL="ALL"', '+CMGL: 1,"REC READ","+491234567890",,"12/08/14,14:01:06+32"', 'Test', '', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return sms_list

	def empty_sms(self) -> str:
		if self.debug:
			self.comm.send("AT+CMGF=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CMGF=1")
			print("Sending: AT+CMGD=1,4")

		self.comm.send("AT+CMGF=1")
		self.comm.send("AT+CMGD=1,4")
		read = self.comm.read_lines()

		# ['AT+CMGF=1', 'OK', 'AT+CMGD=1,4', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")

	def send_sms(self, recipient, message) -> str:
		if self.debug:
			self.comm.send("AT+CMGF=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CMGF=1")
			print('Sending: AT+CMGS="{}"'.format(recipient))
			print("Sending: {}".format(message))
			print("Sending: {}".format(chr(26)))

		self.comm.send("AT+CMGF=1")
		self.comm.send('AT+CMGS="{}"'.format(recipient))
		self.comm.send(message)
		self.comm.send(chr(26))
		read = self.comm.read_lines()

		# ['AT+CMGF=1', 'OK', 'AT+CMGS="491234567890"', '', '> Test', chr(26), 'OK']
		if self.debug:
			print("Sms sender responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[4]

	def get_sms(self, slot) -> dict:
		if self.debug:
			self.comm.send("AT+CMGF=?")
			self.comm.send("AT+CMGR=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CMGF=1")
			print("Sending: AT+CMGR={}".format(slot))

		self.comm.send("AT+CMGF=1")
		self.comm.send("AT+CMGR={}".format(slot))
		read = self.comm.read_lines()

		# ['AT+CMGF=1', 'OK', 'AT+CMGR=1', '+CMGR: "REC READ","+491234567890",,"12/08/14,14:01:06+32"', 'Test', '', 'OK']
		# ['AT+CMGF=1', 'OK'] # if empty
		if self.debug:
			print("Device responded: ", read)

		if len(read) < 3 or read[-1] != "OK":
			raise Exception("Command failed")
		return {
			"slot": read[1].split(":")[1].split(",")[0].strip(),
			"number": read[1].split('READ","')[1].split('","","')[0],
			"date": read[1].split('","","')[1].split(",")[0],
			"time": read[1].split(",")[5].split("+")[0],
			"message": read[4].replace("\r\n", "").strip(),
		}

	def delete_sms(self, slot: int) -> str:
		if self.debug:
			self.comm.send("AT+CMGF=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+CMGF=1")
			print("Sending: AT+CMGD={}".format(slot))

		self.comm.send("AT+CMGF=1")
		self.comm.send("AT+CMGD={}".format(slot))
		read = self.comm.read_lines()

		# ['AT+CMGF=1', 'OK', 'AT+CMGD=1', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	# ----------------------------------- CALLS ---------------------------------- #

	def call(self, number: str) -> str:
		if self.debug:
			print("Sending: ATD{};".format(number))

		self.comm.send("ATD{};".format(number))
		read = self.comm.read_lines()

		# ['ATD491234567890;', 'OK']
		if self.debug:
			print("ATD Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("ATD Command failed")
		return read[1]

	def answer(self) -> str:
		if self.debug:
			print("Sending: ATA")

		self.comm.send("ATA")
		read = self.comm.read_lines()

		# ['ATA', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def hangup(self) -> str:
		if self.debug:
			print("Sending: AT+CHUP")

		self.comm.send("AT+CHUP")
		read = self.comm.read_lines()

		# ['AT+CHUP', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]
	# ----------------------------------- SIM-SERVER ---------------------------------- #

	# ----------------------------------- FRED ---------------------------------- #	

	def get_sim_status(self, NEW_TIMEOUT) -> str:
		backup_timeout = self.comm.modem_serial.timeout
		self.comm.modem_serial.timeout = NEW_TIMEOUT
		if self.debug:
			self.comm.send("AT+CPIN=?")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				print(read)
				raise Exception("Unsupported command")
			print("Sending: AT+CPIN?")
		self.comm.send("AT+CPIN?")
		read = self.comm.read_lines()
		# print(read)
		# ['AT+CPIN?', '+CPIN: READY', '', 'OK']
		if self.debug:
			print("Device responded: ", read)
		self.comm.modem_serial.timeout = backup_timeout
		# print(self.comm.modem_serial.timeout)
		return read[1].split(": ")[1]

	def set_sim_pin(self, newpin) -> str:
		if self.debug:
			print("AT+CPIN={}".format(newpin))
		self.comm.send("AT+CPIN={}".format(newpin))
		read = self.comm.read_lines()
		if self.debug:
			print("Device responded: ", read)
		return read[3].split(": ")[1]	
		if read[3].split(": ")[1] != "READY":
			raise Exception("Command failed")
		time.sleep(5)
		return read-[1]

	def check_sim_pin(self,newtimeout, newpinnumber) -> str:
		sim_status = self.get_sim_status(1) #1sec timeout
		# sim_status = self.get_sim_status(newtimeout)
		if sim_status == "SIM PIN":
			self.set_sim_pin(newpinnumber)
			time.sleep(newtimeout)
		elif sim_status == "READY":
			# sim_status = self.get_sim_status(newtimeout)
			return "REaDY"
			pass
		else :
			raise Exception("Sim failed")

	def set_cmee(self, value) -> str:
		if self.debug:
			print("AT+CMEE={}".format(value))
		self.comm.send("AT+CMEE={}".format(value))
		read = self.comm.read_lines()
		if self.debug:
			print("Device responded: ", read)
		# ['AT+CMEE=0', 'OK'] ['AT+CMEE=1', 'OK'] ['AT+CMEE=2', 'OK']
		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def set_recognition(self, value) -> str:
		if self.debug:
			self.comm.send("AT+COLP={}".format(value))
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+COLP={}".format(value))

		self.comm.send("AT+COLP={}".format(value))
		read = self.comm.read_lines()

		# ['AT+COLP=x', 'OK']
		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command failed")
		return read[1]

	def set_vtd(self, value) -> str:
		if self.debug:
			self.comm.send("AT+VTD={}".format(value))
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported command")
			print("Sending: AT+VTD={}".format(value))

		self.comm.send("AT+VTD={}".format(value))
		read = self.comm.read_lines()

		if self.debug:
			print("Device responded: ", read)

		if read[-1] != "OK":
			raise Exception("Command VTD failed")
		return read[1]

	def send_dtmf_code(self, recipient_dtmf) -> str:
			# AT+VTD=10 1sec
			#AT+CLDTMF=? +CLDTMF:(1-100),(0-9,A,B,C,D,*,#),(10-100)
			#AT+CLDTMF=1,”5,1,0,2”,100
			#AT+CLDTMF reset/stop

			if self.debug:
				self.comm.send("AT+CLDTMF=?")
				read = self.comm.read_lines()
				if read[-1] != "OK":
					raise Exception("Unsupported dtmf command")
				# print("Sending: AT+CLDTMF=?")
				recipient_dtmf = recipient_dtmf.replace("'", "")
				print('Sending: AT+CLDTMF="{}"'.format(recipient_dtmf))

			self.comm.send('AT+CLDTMF={}'.format(recipient_dtmf))
			read = self.comm.read_lines()
			# read = read.replace("'", "")
			if self.debug:
				print("Device responded: ", read)

			if read[-1] != "OK":
				raise Exception("Noisy and failed")
			return True

	def depreacated_check_Callstatus(self,_ONLINE_FLAG, _CAN_RECORD_FLAG) -> str:
		print ("    _ONLINE_FLAG {}".format(_ONLINE_FLAG))	# = False
		print ("_CAN_RECORD_FLAG {}".format(_CAN_RECORD_FLAG))	# = False 
		while True :
				# if _ONLINE_FLAG ==  True : break

				StateOfCall_value=Modem.get_CLCC(self,_ONLINE_FLAG, _CAN_RECORD_FLAG)

		""""		
				if StateOfCall_value ==  "0" :
					print("Active You can record")
					return True
					_ONLINE_FLAG = True
					_CANRECORD_FLAG = True
					print()
				
				
				elif StateOfCall_value ==  "1" :
					print("Held can't record")
					print()
					_ONLINE_FLAG = True
					_CANRECORD_FLAG = False

				
				
				elif StateOfCall_value ==  "2" :
					print("Dialing you must retry")
					print()
					_ONLINE_FLAG = False
					_CANRECORD_FLAG = False
				
				
				elif StateOfCall_value ==  "3" :
					print("Alerting/Ringing no luck")
					print()
					_ONLINE_FLAG = False
					_CANRECORD_FLAG = False

				
				elif StateOfCall_value ==  "7" :
					print("CALL ENDED FORCE 7")
					print()
					_ONLINE_FLAG = False
					_CANRECORD_FLAG = False
					# return False
								
				else :
					if _ONLINE_FLAG == False :
						print("4,5,6,7 errors")
						print()
						# break
						# return False
						_CANRECORD_FLAG = False	
					else :
						print ("NOTHING ELSE Proceed with STT")
						print()
						## _ONLINE_FLAG = True
						# return True
						_CANRECORD_FLAG = False
				
				
		 		
			Check CLCC.
			AT+CLCC
			+CLCC: 1,0,0,0,0,"0664018952",129,""

			OK
			AT+CLCC?
			+CLCC: 0

			<idx>
			1..7  Call identification number
			This number can be used in +CHLD command operations

			<dir>
			0  Mobile originated (MO) call
			1  Mobile terminated (MT) call

			<stat> State of the call:
			0  Active
			1  Held
			2  Dialing (MO call)
			3  Alerting (MO call)
			4  Incoming (MT call)
			5  Waiting (MT call)
			6  Disconnect

			<mode> Bearer/tele service:
			0  Voice
			1  Data
			2  Fax

			<mpty>
			0  Call is not one of multiparty (conference) call parties
			1  Call is one of multiparty (conference) call parties

			<number>
			String type (string should be included in quotation marks)
			phone number in format specified by <type>.

			<type>
			Type of address

			<alphaId>
			String type (string should be included in quotation marks)
			alphanumeric representation of
			<number>
			corresponding to the entry found in phone book.
		"""		
		"""
			self._logger.debug("Get CLCC status")
			dataclcc=self.Sreturn("AT+CLCC","OK")
			dataclcc=self.parseReply(dataclcc[0], beginning="+CLCC:", divider=",", index=3)
			return None
		"""
	
	def depreacated_get_CLCC(self, __ONLINE_FLAG, __CAN_RECORD_FLAG) -> str: #default FLAGS ARE FALSE
		# _FLAG_RECORD = FLAG_RECORD
		if self.debug:
			print("Sending: AT+CLCC")
		
		self.comm.send("AT+CLCC")
		read = self.comm.read_lines()
		

		if self.debug:
			print("Device CLCC? respondead: ", read)
			print(".")
		
		# Device CLCC? responded:  ['AT+CLCC', 'OK']
		if len(read) <= 2 :
			print("MODEM SEND SHORT SENTENCE")
			if __CAN_RECORD_FLAG == True :
				print("The call has ended, proceed  with Audio")
				__CAN_RECORD_FLAG = True
				__ONLINE_FLAG = False
				return 7
			if __CAN_RECORD_FLAG == False :
				print("No call begin, restart CLCC loop")
				__CAN_RECORD_FLAG = False
				__ONLINE_FLAG = False
		else :
			if len(read) >= 4 and read[-1] == "OK":
				print("Long sentence detected from CLCC response")
				if read[1] != "NO CARRIER" :
					print("\'NO CARRIER\' FLAG FOUND, WE ARE ONLINE extract state dataS")
					bidir = read[1].split(": ")[1].split(",")[0] 	#bidir
					state = read[1].split(": ")[1].split(",")[2]	#state
					__ONLINE_FLAG = True

					if bidir == "1" :
						if state == "0" :
							print("we are connected proceed with audio \'CAN_RECORD\' is True")
							__CAN_RECORD_FLAG = True
							return True
						else : 
							print("MODEM NOT connected, DIALING,ALERTING, ETC...")
							__CAN_RECORD_FLAG = False
							return False
					else :
						print("MODEM not in emitting mode, can't send")
						return False
				else :
					__FLAG_RECORD = False
					__ONLINE_FLAG = False
					print("MODEM receive \'NO CARRIER\' FLAG or strange things")
					return False

		
		
		
		# Device CLCC? responded:  ['AT+CLCC', '+CLCC: 1,0,2,0,0,"0800943376",129,""', '', 'OK']
		# if read[0] == "AT+CLCC":
			# pos3 = read[1].split(": ")[1].split(",")[2]


		# # Device CLCC? responded:  ['AT+CLCC', 'OK']
		# if len(read) == 2 and read[1] == "OK" and __FLAG_RECORD == True :
		# 		__FLAG_RECORD = False
		# 		print("A call has ended")
		# 		# return "Ended.Call"
		# 		return 7
		# Device CLCC? responded:  ['AT+CLCC', '+CLCC: 1,0,2,0,0,"0800943376",129,""', '', 'OK']
		# Device CLCC? responded:  ['AT+CLCC', '+CLCC: 1,0,0,0,0,"0800943376",129,""', '', 'OK']
		# if len(read) == 4 and read[-1] == "OK" :
		# 	raw = read[1].split(": ")[1].split(",")[2]
		# 	if raw == 0 :
		# 		print ("YOU CAN RECORd NOW")
		# 		__FLAG_RECORD = True
		# 	return raw	
		
		# if len(read) == 5 and read[-1] != "OK":
		# 		raise Exception("CLCC Command failed")
		
		# # Device CLCC? responded:  ['AT+CLCC', '+CLCC: 1,0,0,0,0,"0800943376",129,""', '', 'OK', '', 'NO CARRIER']
		# if len(read) > 4 and read[-1] != "NO CARRIER":
		# 		print("A Solong call was ended")
		# 		# return "Solong_Ended.Call"
		# 		return 7
		
		# # Device CLCC? responded:  ['', 'NO CARRIER', 'AT+CLCC', 'OK']
		# if len(read) == 4 and read[-1] == "NO CARRIER" and __FLAG_RECORD == True :
		# 	__FLAG_RECORD = False
		# 	print("A short call was ended")
		# 	# return "short_Ended.Call"
		# 	return 7
		
		# # Device CLCC? responded:  ['AT+CLCC', '+CLCC: 1,0,0,0,0,"0800943376",129,""', '', 'OK', '', 'NO CARRIER']
		# if len(read) == 4 and read[-1] == "NO CARRIER" and __FLAG_RECORD == True : 
		# 		__FLAG_RECORD = False
		# 		print("A long call was ended")
		# 		# return "Long_Ended.Call"
		# 		return 7
		
		
		# raw = read[1].split(": ")[1].split(",")[2]
		# if raw == 0 :
		# 	print ("YOU CAN RECORd NOW")
		# 	__FLAG_RECORD = True
		# 	return "RecordCall"

	def check_callinprogress(self) -> str: #default FLAGS ARE FALSE
		self.comm.send("AT+CLCC")
		read = self.comm.read_lines()

		if self.debug:
			print("Sending: AT+CLCC")
			print("Device CLCC? responded: ", read)
		
		if len(read) >= 4 and read[-1] == "OK":
			# if self.debug:
			# 	print ("CLCC correct length and callback ok")
			try: 
				bidir = read[1].split(": ")[1].split(",")[0]
				# if self.debug:
				# 	print ("CLCC extracting bidir ",bidir)
			except :
				bidir = 9 
				# if self.debug:
				# 	print ("CLCC bidir incorrect", bidir)
			
			try:
				state = read[1].split(": ")[1].split(",")[2]	#state
				# if self.debug:
				# 	print ("CLCC extracting state", state)
			except : 
				state = 9
				# if self.debug:
				# 	print ("CLCC state incorrect", state)
			
			if bidir == "1" and state == "0" :
				FLAG_CONNECTED = True
				return True
			else :
				FLAG_CONNECTED = False
				return False
		else : 
			# if self.debug:
			# 	print ("CLCC INcorrect length and callback")
			FLAG_CONNECTED = False
			return False

	# def depreacated_get_crec_list(self) -> str:
	# 	if self.debug:
	# 		self.comm.send("AT+CREC=7")
	# 		read = self.comm.read_lines()
	# 		if read[-1] != "OK":
	# 			raise Exception("Unsupported AT+CREC=7 command")
	# 		print("Sending: AT+CREC=7")

	# 	self.comm.send("AT+CREC=7")
	# 	read = self.comm.read_lines()

	# 	# ['AT+CREC=7', '+CREC: 7,1,6118,0', '+CREC: 7,2,6502,0', '', 'OK']
	# 	if self.debug:
	# 		print("AT+CREC=7 responded: ", read)

	# 	if read[-1] != "OK":
	# 		raise Exception("AT+CREC=7 failed")
	# 	# return read[1].split(",")[2].strip('"')
	# 	return read[1].split(",")[2]

	# def depreacated_get_crec_idone(self) -> str:
	# 	zobilamaouche = self.get_crec_list()
	# 	print("zobilamaouche", zobilamaouche)
	# 	if int(zobilamaouche) > 32768 :
	# 		raise Exception("Too Big file length")
	# 	if self.debug:
	# 		# print("Sending: AT+CLVL={}".format(volume))
	# 		self.comm.send("AT+CREC=6,1,{},0".format(self.get_crec_list()))
	# 		read = self.comm.read_lines()
	# 		if read[-1] != "OK":
	# 			raise Exception("Unsupported AT+CREC=6 command")
	# 		print("Sending: AT+CREC=6,1,{},0".format(self.get_crec_list()))

	# 	self.comm.send("AT+CREC=6,1,{},0".format(self.get_crec_list()))
	# 	read = self.comm.read_lines()

	# 	# [b'AT+CREC=6,1,6118,0\r\r\n', b'+CREC: 6,1,6118\r\n', b'F8C...etc...090\r\n', b'\r\n', b'OK\r\n']
	# 	if self.debug:
	# 		print("AT+CREC=6 responded: ", read)
	# 	if read[-1] != "OK":
	# 		raise Exception("AT+CREC=6 failed")
	# 	return read[2] #b'F8C...etc...090\r\n'

	def StartRecordAndSendAudio(self) -> str:
		# <mode>     1 Start record, to stop send anything on uart
		# <interval> range 1-50, unit is 20ms 50*20 = 1000ms soit 1s 
		# <crcmode>  Data form 0 UART data is the audio data

		self.comm.send("AT+CRECORD=1,50,0") #1 record,50*20ms = 1 seconde,0 audio data
		# read = self.comm.read_lines() 	#original
		read = self.comm.read_raw(32768)			#fred
		return read

		# readraw = self.comm.read_raw(100)
		# retursend("AT+CRECORD=1,50,0")n readraw

	def StopRecordAndSendAudio(self) -> str:
		# <mode>     0 Stop record, 

		if self.debug:
			self.comm.send("AT+CRECORD=0")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported AT+CRECORD command")
			print("Sending: AT+CRECORD=0")

		self.comm.send("AT+CRECORD=0")
		read = self.comm.read_lines()


		if self.debug:
			print("AT+CRECORD=0 responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+CRECORD=0 failed")
		# return read[1].split(",")[2].strip('"')
		return read

	# AT+CREC=1,1,0
	# 1,record
	# 1,id
	# 0, amr
	# 1, wav
	#1
	def start_record(self,id,form) -> str:
		# if self.debug:
		# 	self.comm.send("AT+CREC=1,{},{}".format(id,form))
		# 	read = self.comm.read_lines()
		# 	if read[-1] != "OK":
		# 		raise Exception("Unsupported AT+CREC=1 command")
		# 	print("Sending: AT+CREC=1,{},{}".format(id,form))

		self.comm.send("AT+CREC=1,{},{}".format(id,form))
		# read = self.comm.read_lines()		#original
		read = self.comm.read_raw(32768)	#fred
		# ['AT+CREC=1,3,0', 'OK']
		# if self.debug:
		# print("AT+CREC=1,{},{} ressponded: {}".format(id,form,read))
		print("AT+CREC=1,{},{}".format(id,form))

		# if read[-1] != "OK":
		# 	raise Exception("AT+CREC=1,{},{} failed".format(id,form))
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[-1]
	
	# #2
	# def stop_record(self) -> str:
		
	# 	if self.debug:
	# 		self.comm.send("AT+CREC=2")
	# 		read = self.comm.read_lines()
	# 		if read[1] != "OK":
	# 			raise Exception("Unsupported AT+CREC=2 command")
	# 		print("Sending: AT+CREC=2")

	# 	self.comm.send("AT+CREC=2")
	# 	read = self.comm.read_lines()

	# 	# ['AT+CREC=1', 'OK']
	# 	if self.debug:
	# 		print("AT+CREC=2 responded: ", read)

	# 	if read[-1] != "OK":
	# 		raise Exception("AT+CREC=2 failed")
	# 	# return read[1].split(",")[2].strip('"')
	# 	# return read[1].split(",")[2]
	# 	return read[-1]
	# #2b
	def stop_record(self) -> str:
		print("Sending: AT+CREC=2")
		self.comm.send("AT+CREC=2")
		read = self.comm.read_lines()

		# +CREC: 2,<id>,<form>,<time>,<len>
		# ['AT+CREC=2', 'OK', ,'', '+CREC: 2,1,0,1,32768']
		print("AT+CREC=2 responded: ", read)
		
		if len(read) == 4 :
			recordlen = int(read[3].split(": ")[1].split(",")[4])
			# if self.debug:
			# 	print("a new record ",recordlen)
			# if (int(recordlen) > 0) and (int(recordlen) < 32769) :
			if recordlen > 0 and recordlen < 32769 :
				return True
		else :				
			if read[-1] == "OK" :
				# if self.debug:
				# 	print("no new record")
				return True
			else :
				# if self.debug:
				# 	print("error")
				return False
				
	
	#3
	def delete_record(self) -> str:
		if self.debug:
			self.comm.send("AT+CREC=3")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported AT+CREC=3 command")
			print("Sending: AT+CREC=3")

		self.comm.send("AT+CREC=3")
		read = self.comm.read_lines()

		# ['AT+CREC=3', 'OK']
		if self.debug:
			print("AT+CREC=3 responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+CREC=3 failed")
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[-1]
	
	#4
	def play_record(self,id,channel,level) -> str:
		## change timeout
		# NEW_TIMEOUT = 5
		# backup_timeout = self.comm.modem_serial.timeout
		# print("previous tout : ", backup_timeout)
		# self.comm.modem_serial.timeout = NEW_TIMEOUT
		# print("new tout : ", timeout)
		##
		# if self.debug:
		# 	self.comm.send("AT+CREC=4,{},{},{}".format(id,channel,level))
		# 	read = self.comm.read_lines()
		# 	if read[-1] != "OK":
		# 		raise Exception("Unsupported AT+CREC=4 command")
		# 	print("Sending: AT+CREC=4,{},{},{}".format(id,channel,level))

		self.comm.send("AT+CREC=4,{},{},{}".format(id,channel,level))
		read = self.comm.read_lines()

		# ['AT+CREC=1', 'OK']
		# if self.debug:
		# 	print("AT+CREC=4,{},{},{}".format(id,channel,level),"responded: ", read)

		# if read[-1] != "OK":
		# 	raise Exception("AT+CREC=4,{},{},{}".format(id,channel,level),"failed")
		
		# self.comm.modem_serial.timeout = backup_timeout
		# print("original tout restored : ", backup_timeout)
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[-1]
	
	#5
	def stop_play_record(self) -> str:
		if self.debug:
			self.comm.send("AT+CREC=5")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported AT+CREC=5 command")
			print("Sending: AT+CREC=5")

		self.comm.send("AT+CREC=5")
		read = self.comm.read_lines()

		# ['AT+CREC=1', 'OK']
		if self.debug:
			print("AT+CREC=5 responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+CREC=5 failed")
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[-1]
	
	#6
	#Get record data in hex format, the max length is 32K in bytes
	def get_data_record(self,id,len,offset) -> str:

		self.comm.send("AT+CREC=6,{},{},{}".format(id,len,offset))
		read = self.comm.read_lines()
		time.sleep(5)
		##doit attendre fin transfert !!
		if self.debug:
			if read[-1] != "OK":
				raise Exception("Unsupported AT+CREC=6 command")
			print("Sending: AT+CREC=6,{},{},{}".format(id,len,offset))
		
		# AT+CREC=6,1,32768,0 responded:  ['AT+CREC=6,1,32768,0', '+CREC: 6,1,24678', '232...342', '','OK']
		if self.debug:
			print("AT+CREC=6,{},{},{}".format(id,len,offset),"responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+CREC=6,{},{},{}".format(id,len,offset),"failed")
		# RECORDED_MESSAGE = read[2]
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[2]
	
	#7	
	def list_record(self,id) -> str:
		if self.debug:
			self.comm.send("AT+CREC=7,{}".format(id))
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported AT+CREC=7 command {}", read)
			print("Sending: AT+CREC=7,{}".format(id))

		self.comm.send("AT+CREC=7,{}".format(id))
		read = self.comm.read_lines()

		# ['AT+CREC=1', 'OK']
		if self.debug:
			print("AT+CREC=7,{}".format(id),"responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+CREC=7,{}".format(id),"failed")
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[-1]
	
	#8	
	def space_record(self) -> str:
		if self.debug:
			self.comm.send("AT+CREC=8")
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported AT+CREC=8 command")
			print("Sending: AT+CREC=8")

		self.comm.send("AT+CREC=8")
		read = self.comm.read_lines()

		# ['AT+CREC=1', 'OK']
		if self.debug :
			print("AT+CREC=8 responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+CREC=8 failed")
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
	# k	return read[-1]
	
	#a
	def status_record(self) -> str:
		print("Sending: AT+CREC?")
		self.comm.send("AT+CREC?")
		read = self.comm.read_lines()
		
		# ['AT+CREC?', 'OK']
		if self.debug:
			print("AT+CREC? responded: ", read)
			if read[-1] != "OK" :
				raise Exception("UnKnow AT+CREC? status")
		#return read[-1]
		return read[1].split(": ")[1]

	#b
	def set_mode_record(self,mode) -> str:
		if self.debug:
			self.comm.send("AT+DTAM={}".format(mode))
			read = self.comm.read_lines()
			if read[-1] != "OK":
				raise Exception("Unsupported AT+DTAM command {}", read)
			print("Sending: AT+DTAM={}".format(mode))

		self.comm.send("AT+DTAM={}".format(mode))
		read = self.comm.read_lines()

		# ['AT+CREC=1', 'OK']
		if self.debug:
			print("AT+DTAM={}".format(mode),"responded: ", read)

		if read[-1] != "OK":
			raise Exception("AT+DTAM={}".format(mode),"failed")
		# return read[1].split(",")[2].strip('"')
		# return read[1].split(",")[2]
		return read[-1]

	def size_record(self,id) -> str:
		self.comm.send("AT+CREC=7,{}".format(id))
		read = self.comm.read_lines()
		if read[-1] != "OK":
				return 0
				raise Exception("Unsupported AT+CREC=7 command {}", read)

		if self.debug:
			print("AT+CREC=7,{}".format(id),"responded: ", read)

		# ['AT+CREC=7,1', '+CREC: 7,1,24966,0', '', 'OK']
		return read[1].split(": ")[1].split(",")[2]



