
<img src="output.jpg" >





# Example: text to speech widget with different engines
Lets test different text to speech engines and build a pyside6 widgets around them.

You can try to listen to a conversation of a group trying to figure out how to create tts widgets.

[PLAYME.webm](https://github.com/ip-repo/guides/assets/123945379/ee6bfedc-ce0e-4b41-aef6-74e49bb5aedd)


<details><summary>Before we start</summary>
If you want to use this example files follow the instructions:
	
```
#python 3.12
git clone https://github.com/ip-repo/guides.git
cd example-tts-pyside6
python -m venv ttsv
ttsv\Scripts\activate
pip install PySide6 #6.6.2
pip install gtts #2.5.1
pip install pyttsx3 #2.90
# now you can run the scripts of the example:
python gtts_widget_run.py
```

</details>

<details><summary>Quick engines basic usage</summary>

 <details>                <summary>gtts</summary>
	
gtts can be used as a cli.
```
#convert txt file to audio
gtts-cli "Hello world" --output hello-world.mp3
#convert txt file to slower audio
gtts-cli "Slow speech" --slow --output hello-world.mp3
gtts-cli -f text.txt --output text-as-speech.mp3
#convert txt file to audio with other supported language
gtts-cli -f text.txt -l fr --output french-speech.mp3 
#convert to other supported language
gtts-cli "Bonjour mounde" -l fr --output french.mp3
#list supported languages
gtts-cli --all
#help
gtts-cli --help
```
String to speech.
```python
from gtts import gTTS
mytext = "Bonjour monde"
language = "fr"
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("french.mp3")

```
Text file to speech mp3
```python
from gtts import gTTS
with open("textfile.txt", "r") as f:
    mytext = f.read()
language = "vi"
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("vietnamese.mp3")

```

</details>
<details>
	<summary>Pyttsx3</summary>

Using pyttsx3 from command line.

```python
import pyttsx3
import sys
def main():
	#pyttsx3 tts engine
	engine = pyttsx3.init()
	#get engine properties
	rate = int(sys.argv[1]) #rate:  0 - 200
	volume = float(sys.argv[2]) / 10.0 #volume 0.0 - 10.0
	voice  = int(sys.argv[3]) #depend on installed voices usally 0 or 1
	engine.setProperty("rate",rate)
	engine.setProperty("volume", volume)
	engine.setProperty("voice",engine.getProperty("voices")[voice].id)
	text = " ".join(sys.argv[4:])
	#speak
	engine.say(text)
	engine.runAndWait()
if __name__ == "__main__":
	main()
```
Now we can use it from command line.
```console
python pytts_cli.py 150 10.0 1 hello world

```
</details>
<details>
	<summary>QTextToSpeech</summary>
	
A quick Qt tts widget.

```python
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget,QStyleFactory

def speak_text():
	""" called when speak button clicked """
	speech.say(text_edit.toPlainText())

def handle_speech_state(state: QTextToSpeech.State):
	""" called when engine state changes """
	if state == QTextToSpeech.State.Ready:
		speak_btn.setEnabled(True)
	else:
		speak_btn.setEnabled(False)

if __name__ == '__main__':
	#application instance
	app = QApplication([])
	app.setStyle(QStyleFactory.keys()[2])
	#tts engine
	speech = QTextToSpeech()
	#widget
	widget = QWidget()
	#text area
	text_edit = QTextEdit()
	#speak btn
	speak_btn = QPushButton("speak")
	layout = QVBoxLayout()
	layout.addWidget(text_edit)
	layout.addWidget(speak_btn)
	widget.setLayout(layout)
	#signals to handlers
	speech.stateChanged.connect(handle_speech_state)
	speak_btn.clicked.connect( speak_text)
	
	widget.show()
	app.exec()


```
</details>
</details>

## Gtts widget
So, we have seen three engines that we can use (there are more..) and each engines has its own functionality and limitation.
The first widget can be found in the file <a href="https://github.com/ip-repo/guides/blob/main/example-tts-pyside6/gtts_widget_run.py">`gtts_widget_run.py`</a> if you have installed the neccesary modules just run the it.
```console
python gtts_widget_run.py
```
This engine will allow to save text as speech in mp3 or wav format but there are some limitations.
Gtts require internet connection so it wont work offline.
For longer tasks it might be wise to use qrunnables or qthreads.

<img width="451" alt="gtts_widget" src="https://github.com/ip-repo/guides/assets/123945379/0f74706e-d949-4357-aa7a-0237c2f1f31a">

You can listen to the result by gtts.

[lorem.webm](https://github.com/ip-repo/guides/assets/123945379/4c29b97e-ed6f-4e29-a005-59f13b98ff1d)

## QTextToSpeech widget
This widget can found in the file <a href="https://github.com/ip-repo/guides/blob/main/example-tts-pyside6/qt_widget_run.py">`qt_widget_run.py`</a>.
```console
python qt_widget_run.py
```
Qt has a nice text to speech engine but in the current version (6.6.2) it only allow to speak text.
This engine allow to change the pitch ,rate and volume and voices and it also work in offline mode.
It does offer some signals like sayingWord that emit's the current word that the engine speak and this can help us to make more creative programs.

<img width="416" alt="qt_widget" src="https://github.com/ip-repo/guides/assets/123945379/cac24ab2-2e77-48dc-a2e4-4102fd5d45fd">

## Pyttsx3 widget
And this widget is in the file <a href="https://github.com/ip-repo/guides/blob/main/example-tts-pyside6/pyttsx_widget_run.py">`pyttsx_widget_run.py`</a>.
```console
python pyttsx_widget_run.py
```
Pyttsx3 is a simple engine that use locally installed voices and can run offline.
The settings that can be changed are: rate, voice, volume and pitch.
The engine allow user to save text as speech. 

<img width="492" alt="pyttsx3_widget" src="https://github.com/ip-repo/guides/assets/123945379/88937d1d-aafc-47dc-a536-80b60fa86e1a">

You can listen to the result by pyttsx3.

[lorem1.webm](https://github.com/ip-repo/guides/assets/123945379/540565e2-3a17-47f1-b59c-d4b9ed1319ac)

  
You can also explore other text to speech projects on this github:
- <a href="https://github.com/ip-repo/text-to-speech-webpage/blob/main/README.md">Text to Speech webpage</a>
- <a href="https://github.com/ip-repo/conversation-maker/blob/main/README.md">PySide6 Conversation Maker</a>
- <a href="https://github.com/ip-repo/guides/blob/main/gemini-story-to-audio-with-gtts/story-to-audio.md"> Example: generate a story with Gemini and use gtts to create a audio story </a>
