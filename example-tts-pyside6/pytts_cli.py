import pyttsx3
import sys
def main():
	#pyttsx3 tts engine
	engine = pyttsx3.init()
	#get engine properties
	rate = int(sys.argv[1]) #rate:  0 - 200
	volume = float(sys.argv[2]) / 10.0 #volume 0.0 - 10.0
	voice  = int(sys.argv[3]) #depends on installed voices usally 0 or 1
	engine.setProperty("rate",rate)
	engine.setProperty("volume", volume)
	engine.setProperty("voice",engine.getProperty("voices")[voice].id)
	text = " " .join(sys.argv[4:])
	#speak
	engine.say(text)
	engine.runAndWait()
if __name__ == "__main__":
	main()
