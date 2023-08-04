
	# def get_crec_list(self) -> str:
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

	# def get_crec_idone(self) -> str:
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

# def StartRecordAndSendAudio(self) -> str:
# 	# <mode>     1 Start record, to stop send anything on uart
# 	# <interval> range 1-50, unit is 20ms 50*20 = 1000ms soit 1s 
# 	# <crcmode>  Data form 0 UART data is the audio data
	
# 	self.comm.send("AT+CRECORD=1,50,0") #1 record,50*20ms = 1 seconde,0 audio data
# 	read = self.comm.read_lines()
# 	return read

# 	# readraw = self.comm.read_raw(100)
# 	# return readraw
	
# def StopRecordAndSendAudio(self) -> str:
# 	# <mode>     0 Stop record, 
	
# 	if self.debug:
# 		self.comm.send("AT+CRECORD=0")
# 		read = self.comm.read_lines()
# 		if read[-1] != "OK":
# 			raise Exception("Unsupported AT+CRECORD command")
# 		print("Sending: AT+CRECORD=0")

# 	self.comm.send("AT+CRECORD=0")
# 	read = self.comm.read_lines()

	
# 	if self.debug:
# 		print("AT+CRECORD=0 responded: ", read)

# 	if read[-1] != "OK":
# 		raise Exception("AT+CRECORD=0 failed")
# 	# return read[1].split(",")[2].strip('"')
# 	return read

# AT+CREC=1,1,0 
# 1,record
# 1,id
# 0, amr
# 1, wav

def start_record(self,id,form) -> str:
	if self.debug:
		# .format(volume)
		self.comm.send("AT+CREC=1,{},{}".format(id,form))
		read = self.comm.read_lines()
		if read[-1] != "OK":
			raise Exception("Unsupported AT+CREC=7 command")
		print("Sending: AT+CREC=1,{},{}".format(id,form))

	self.comm.send("AT+CREC=1,{},{}".format(id,form))
	read = self.comm.read_lines()

	# ['AT+CREC=1', 'OK']
	if self.debug:
		print("AT+CREC=1,{},{}".format(id,form),"responded: ", read)

	if read[-1] != "OK":
		raise Exception("AT+CREC=1,{},{}".format(id,form),"failed")
	# return read[1].split(",")[2].strip('"')
	# return read[1].split(",")[2]
	return read[-1]

def stop_record(self) -> str:
	if self.debug:
		self.comm.send("AT+CREC=2")
		read = self.comm.read_lines()
		if read[-1] != "OK":
			raise Exception("Unsupported AT+CREC=2 command")
		print("Sending: AT+CREC=2")

	self.comm.send("AT+CREC=2")
	read = self.comm.read_lines()

	# ['AT+CREC=1', 'OK']
	if self.debug:
		print("AT+CREC=2 responded: ", read)

	if read[-1] != "OK":
		raise Exception("AT+CREC=2 failed")
	# return read[1].split(",")[2].strip('"')
	# return read[1].split(",")[2]
	return read[-1]

def delete_record(self) -> str:
	if self.debug:
		self.comm.send("AT+CREC=3")
		read = self.comm.read_lines()
		if read[-1] != "OK":
			raise Exception("Unsupported AT+CREC=3 command")
		print("Sending: AT+CREC=3")

	self.comm.send("AT+CREC=3")
	read = self.comm.read_lines()

	# ['AT+CREC=1', 'OK']
	if self.debug:
		print("AT+CREC=3 responded: ", read)

	if read[-1] != "OK":
		raise Exception("AT+CREC=3 failed")
	# return read[1].split(",")[2].strip('"')
	# return read[1].split(",")[2]
	return read[-1]

def play_record(self,id,channel,level) -> str:
	if self.debug:
		self.comm.send("AT+CREC=4,{},{},{}".format(id.channel.level))
		read = self.comm.read_lines()
		if read[-1] != "OK":
			raise Exception("Unsupported AT+CREC=4 command")
		print("Sending: AT+CREC=4,{},{},{}".format(id.channel.level))

	self.comm.send("AT+CREC=4,{},{},{}".format(id.channel.level))
	read = self.comm.read_lines()

	# ['AT+CREC=1', 'OK']
	if self.debug:
		print("AT+CREC=4,{},{},{}".format(id.channel.level),"responded: ", read)

	if read[-1] != "OK":
		raise Exception("AT+CREC=4,{},{},{}".format(id.channel.level),"failed")
	# return read[1].split(",")[2].strip('"')
	# return read[1].split(",")[2]
	return read[-1]

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

#Get record data in hex format, the max length is 32K in bytes
def get_data_record(self,id,len,offset) -> str:
	if self.debug:
		self.comm.send("AT+CREC=6,{},{},{}".format(id,len,offset))
		read = self.comm.read_lines()
		if read[-1] != "OK":
			raise Exception("Unsupported AT+CREC=6 command")
		print("Sending: AT+CREC=6,{},{},{}".format(id,len,offset))

	self.comm.send("AT+CREC=6,{},{},{}".format(id,len,offset))
	read = self.comm.read_lines()

	# ['AT+CREC=1', 'OK']
	if self.debug:
		print("AT+CREC=6,{},{},{}".format(id,len,offset),"responded: ", read)

	if read[-1] != "OK":
		raise Exception("AT+CREC=6,{},{},{}".format(id,len,offset),"failed")
	# return read[1].split(",")[2].strip('"')
	# return read[1].split(",")[2]
	return read[-1]
	
def list_record(self,id) -> str:
	if self.debug:
		# .format(volume)
		self.comm.send("AT+CREC=7,{}".format(id))
		read = self.comm.read_lines()
		if read[-1] != "OK":
			raise Exception("Unsupported AT+CREC=7 command")
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
	if self.debug:
		print("AT+CREC=8 responded: ", read)

	if read[-1] != "OK":
		raise Exception("AT+CREC=8 failed")
	# return read[1].split(",")[2].strip('"')
	# return read[1].split(",")[2]
	return read[-1]
