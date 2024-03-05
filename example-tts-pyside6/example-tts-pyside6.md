
<img src="output.jpg" >





# Example: text to speech widget with different engines

You can try to listen to a conversation between two people trying to figure out how to create tts widgets.

[summary_speech.webm](https://github.com/ip-repo/guides/assets/123945379/14f7f8b5-6822-48ce-bb91-b3de7bcd3596)

<details><summary>Before we start</summary>

First we need to install to python libraries: PySide6 and gtts.
```
#python 3.12
git clone https://github.com/ip-repo/guides.git
cd example-tts-pyside6
python -m venv ttsv
ttsv\Scripts\activate
pip install PySide6 #6.6.2
pip install gtts #2.5.1
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
String to speech 
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
	text = " " .join(sys.argv[4:])
	#speak
	engine.say(text)
	engine.runAndWait()
if __name__ == "__main__":
	main()
```
Now we can use it from terminal.
```console
python pytts_cli.py 150 10.0 1 hello world

```
</details>
<details>
	<summary>QTextToSpeech</summary>
	
A quick text to speech widget with.

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

So, we have seen three engines that we can use (there are more..) and each engines has its own functionality and limitation.
The first widget can be found in the file `gtts_widget_run.py` if you have installed the neccesary modules just run the it.
```console
python gtts_widget_run.py
```
This widget will allow to save text as speech in mp3 or wav format but there are some limitations.
Gtts require internet connection so it wont work offline.
For longer tasks it might be wise to user qrunnables or qthreads.

<img width="451" alt="gtts_widget" src="https://github.com/ip-repo/guides/assets/123945379/0f74706e-d949-4357-aa7a-0237c2f1f31a">

You can listen to a text to speech by gtts.

[lorem.webm](https://github.com/ip-repo/guides/assets/123945379/4c29b97e-ed6f-4e29-a005-59f13b98ff1d)





