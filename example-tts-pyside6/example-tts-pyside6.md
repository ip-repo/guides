
<img src="output.jpg" ></omg>

# Example: text to speech widgets with gtts and PySide6

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

<details><summary>Quick gtts overview</summary>

Basic usage
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
<details><summary>Example 1: a gtts based widget that can save text as audio file in different languages</summary>
Lets start by importing the necessary objects and creating a class for our widget.

```python
import gtts
import gtts.lang
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtWidgets import (QApplication,QStyleFactory, QWidget,QFileDialog, QHBoxLayout,QVBoxLayout, 
								QTextEdit, QPushButton, QComboBox,QCheckBox)
from PySide6.QtGui import QIcon
import time
import subprocess

class TextToSpeechWidget(QWidget):
	def __init__(self, *args, **kargs) -> None:
		super().__init__(*args, **kargs)
        self.init_objects()
		self.init_ui()
		self.init_signals()

```
Next we will create a method to init the ui.

```python
	def init_ui(self):
		self.setWindowTitle("Welcome to TextToSpeech")
		self.setWindowIcon(QIcon("logo.png"))
		self.setGeometry(0,0, 600,400)
		controls_layout = QHBoxLayout()
		controls_layout.setSpacing(2)
		#select language 
		self.lang_box = QComboBox()
		self.lang_box.addItems(self.reverse_lang_dict.keys())
		#save text
		self.save_text_btn =QPushButton("save text")
		#save speech
		self.save_speech_btn = QPushButton("save audio")
		#set slow speech
		self.slow = QCheckBox("slow")
		controls_layout.addWidget(self.lang_box, 3)
		controls_layout.addWidget(self.slow,1//4)
		controls_layout.addWidget(self.save_text_btn, 1)
		controls_layout.addWidget(self.save_speech_btn, 1)
		main_layout = QVBoxLayout()
		#text container
		self.text_edit = QTextEdit()
		main_layout.addLayout(controls_layout,1)
		main_layout.addWidget(self.text_edit, 10)
		self.setLayout(main_layout)

```
Now can create a text object or a language dictionary
```python
def init_objects(self):
	#this number is the maximum characters that will be processed from text edit widget
	self.text_max_len = 5000
	#languages dictionary for combo box and gtts
	self.lang_dict = gtts.lang.tts_langs()
	self.reverse_lang_dict = {}
	for key in self.lang_dict.keys():
		self.reverse_lang_dict[self.lang_dict[key]] = key
	#file handler
	self.file_dialog = QFileDialog()
```
We have created qt object that has signals and this will help us react to user input.
```python
def init_signals(self):
	#save speech clicked
	self.save_speech_btn.clicked.connect(self.save_speech_btn_clicked)
	#save text clicked
	self.save_text_btn.clicked.connect(self.save_txt_btn_clicked)
```
The signlas are linked to methods that get executed when buttons are clicked.
```python
def save_speech_btn_clicked(self):
	#get the text in the text container
	text = self.text_edit.toPlainText()
	if text:
		#disable widget
		self.setDisabled(True)
		self.setWindowTitle("Working on it....")
		#test if user want a slow speech
		if self.slow.checkState().value == 2:
			slow = True
		else:
			slow = False
		#find out which language to use 
		lang = self.reverse_lang_dict[self.lang_box.currentText()]
		#prepare saving path
		file_name, _ = self.file_dialog.getSaveFileName(None,"Save speech as audio",
		"output.mp3","MP3 (*.mp3);;WAV (*.wav);;")
		if file_name:
			#time to creation time
			t1_start = time.perf_counter()
			#create audio file with gtts-cli
			if slow:
				subprocess.run(["gtts-cli", text[:self.text_max_len],"--slow", "--output", file_name, "-l", lang])
			else:
				subprocess.run(["gtts-cli", text[:self.text_max_len],"--output", file_name, "-l", lang])
			#end time
			t1_stop = time.perf_counter()
			print("exection time:",t1_stop - t1_start, "seconds")
		#enable widget
		self.setEnabled(True)
		self.setWindowTitle("Saved: {}".format(file_name))		
	else:
		self.setWindowTitle("Can't convert nothing....")

def save_txt_btn_clicked(self):
	#disable widget
	self.setDisabled(True)
	#prepare text and cut up to the maximum length
	text = self.text_edit.toPlainText()[:self.text_max_len]
	#prepare saving path
	filename,_ = self.file_dialog.getSaveFileName(None,"Save as text file","output.txt",
	"Text Files (*.txt)")
	if filename:
		#save text file
		with open(filename, "w") as f:
			f.write(text)
		#enable widget
		self.setEnabled(True)
		self.setWindowTitle("Saved: {}".format(filename))
			



```
And now we can create out widget and launch it.
```python 
if __name__ == "__main__":
    #create application instance
	app = QApplication()
    #set application style
	app.setStyle(QStyleFactory.keys()[2])
	app_widget = TextToSpeechWidget()
	#maximum characters length to process to speech 
	app_widget.text_max_len = 10000
	app_widget.show()
	app.exec()
```
If you have created a venv and installed the required libraries you can now Run the file **widget_one_run.py**
```python
(ttsv)python widget_one_run.py
```
This will work well depending on your hardware and can take a long time to process try remaining around 5000 characters.
While the speech is being processed the widget is unavailable.
It might seem surprising but 10000 characters can turn into a audio file of 15 mins.
</details>

<details>
	<summary>Example 2: QTextToSpeech based widget that read text aloud and can be tweaked to some degree</summary>
Lets start by importing the necessary objects and creating a class for our widget.
	
```python
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtWidgets import (QApplication,QStyleFactory, QWidget,QSpinBox, QFileDialog, QHBoxLayout,QVBoxLayout, 
								QTextEdit, QPushButton, QComboBox,QLabel)
from PySide6.QtGui import QIcon

class TextToSpeetQt(QWidget):
	def __init__(self, *args, **kargs) -> None:
		super().__init__(*args, **kargs)
		self.init_ui()
		self.init_objects()
		self.init_signals()

```
Next we will create a method to init the ui.
```python
def init_ui(self):
		self.setWindowTitle("Welcome to TextToSpeech")
		self.setWindowIcon(QIcon("logo.png"))
		main_layout = QVBoxLayout()
		controls_layout = QHBoxLayout()
		self.open_text_btn = QPushButton("Open")
		self.pitch_box = QSpinBox()
		self.pitch_box.setRange(-10,10)
		self.rate_box = QSpinBox()
		self.rate_box.setRange(-10,10)
		self.volume_box = QSpinBox()
		self.volume_box.setValue(1)
		self.volume_box.setRange(0	,10)
		self.say_btn = QPushButton("say")
		self.voice_box = QComboBox()
		self.label1 = QLabel("")
		controls_layout.addWidget(self.open_text_btn)
		controls_layout.addWidget(self.pitch_box)
		controls_layout.addWidget(self.rate_box)
		controls_layout.addWidget(self.volume_box)
		controls_layout.addWidget(self.voice_box)
		controls_layout.addWidget(self.say_btn)

		self.text_edit = QTextEdit()
		main_layout.addLayout(controls_layout, 1)
		main_layout.addWidget(self.text_edit, 9)
		main_layout.addWidget(self.label1,1//3)
		self.setLayout(main_layout)	
```
 Its to create the init_signals and objects methods.
 ```python
def init_signals(self):
		self.open_text_btn.clicked.connect(self.open_text_file)
		self.say_btn.clicked.connect(self.say)
		self.tts.stateChanged.connect(self.update_state)
		self.tts.sayingWord.connect(self.current_word)

def init_objects(self):
	self.file_dialog = QFileDialog()
	self.tts = QTextToSpeech()
	self.last_10_word = []
	self.voice_dict = {}
	for i, voice in enumerate(self.tts.availableVoices()):
		name = voice.name()
		gender = voice.gender()
		if name and gender:
			self.voice_dict[i] = [name, gender, voice.genderName(gender)]
			self.voice_box.addItem(name)
			
	self.tts.setVoice(self.tts.availableVoices()[2])
	self.tts.setVolume(1.0)
	self.tts.setRate(0.0)
	self.tts.setPitch(0.0)
```

```python
def open_text_file(self):
	file_name, _ = self.file_dialog.getOpenFileName(
						parent=None,
						caption="Open a text file",
						dir=".",
						filter="Text files (*.txt)"
					)
	if file_name:
		with open(file_name, "r") as f:
			text = f.read()
			self.text_edit.setText(text)
			self.setWindowTitle(file_name)
	else:
		self.setWindowTitle("Welcom to Text To Speech")
```
```python
def say(self):
	if self.say_btn.text() == "say":
		current_voice = self.voice_box.currentText()
		for  voice in self.tts.availableVoices():
			if voice.name() == current_voice:
				self.tts.setVoice(voice)
		self.tts.setPitch(self.pitch_box.value()/10.0)
		self.tts.setRate(self.rate_box.value()/10.0)
		self.tts.setVolume(self.volume_box.value()/10.0)

		self.tts.say(self.text_edit.toPlainText())
		self.say_btn.setText("stop")	
	else:
		self.tts.stop()
		self.say_btn.setText("say")
```

```python
def update_state(self, *args):
	if self.tts.state() == QTextToSpeech.State.Ready:
		self.say_btn.setText("say")
						
def current_word(self, *args):
	if len(self.last_10_word) < 3:
		self.last_10_word.append(args[0])
		self.create_nice_html(args[0])
	else:
		self.last_10_word.insert(0, args[0])

		self.last_10_word.pop(-1)
		self.create_nice_html(args[0])
```

```python
def create_nice_html(self,current: str, color: str="yellow",words_color: str="white"):
	current_word = "<font color={}>{}</font>"
	res = ""
	for word in self.last_10_word:
		if word == current:
			current_word = "<font color={}>{} </font>".format(color, current)
			res+=current_word + " "
		else:
			other_word = "<font color={}>{}</font>".format(words_color, word)
			res+=other_word + " "
	self.label1.setText(res)
```

```python
if __name__ == "__main__":
	app = QApplication()
	app.setStyle(QStyleFactory.keys()[2])
	app_widget = TextToSpeetQt()
	app_widget.show()
	app.exec()
   

```

</details>

