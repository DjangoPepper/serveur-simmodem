"""PyAudio Example: Record a few seconds of audio and save to a wave file."""
import datetime
import wave
import sys
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 15
FILENAME = ""
APPELANT_SRV = 5127
# class myaudio:

def FileNameWithDate() -> str:
	time_now  = datetime.datetime.now().strftime('%Y-%m-%d_%H%M:%S')
	return time_now

def recordheure(_APPELANT_SRV) -> str:
	FILENAME = str(_APPELANT_SRV) + "_" + str(FileNameWithDate()) + ".wav"
	# FILENAME = str(_APPELANT_SRV) + "_" + str(myaudio.FileNameWithDate()) + ".wav"
	return FILENAME

def main():
	# recordheure(APPELANT_SRV)
	with wave.open(recordheure(APPELANT_SRV), 'wb') as wf:
		p = pyaudio.PyAudio()
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)

		stream = p.open(format=FORMAT, 
						channels=CHANNELS, 
						rate=RATE, 
						input=True)

		print('Recording...')
		for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
			wf.writeframes(stream.read(CHUNK))
		print('Done')

		stream.close()
		p.terminate()
		FLAG_RECORDED = True

if __name__ == '__main__':
	main()