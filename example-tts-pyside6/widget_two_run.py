from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtWidgets import (QApplication,QStyleFactory, QWidget,QSpinBox, QFileDialog, QHBoxLayout,QVBoxLayout, 
								QTextEdit, QPushButton, QComboBox,QLabel)
from PySide6.QtGui import QIcon


class TextToSpeech(QWidget):
	def __init__(self, *args, **kargs) -> None:
		super().__init__(*args, **kargs)
		self.init_ui()
		self.init_objects()
		self.init_signals()

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

				

if __name__ == "__main__":
	app = QApplication()
	app.setStyle(QStyleFactory.keys()[2])
	app_widget = TextToSpeech()
	app_widget.show()
	app.exec()
   
