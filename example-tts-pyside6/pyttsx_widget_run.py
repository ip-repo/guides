
from PySide6.QtWidgets import (QApplication,QStyleFactory, QWidget,QSpinBox, QFileDialog, QHBoxLayout,QVBoxLayout, 
								QTextEdit, QPushButton, QComboBox,QLabel)
from PySide6.QtGui import QIcon
import pyttsx3

class TextToSpeechPyttsx3(QWidget):
	def __init__(self, *args, **kargs) -> None:
		super().__init__(*args, **kargs)
		self.init_ui()
		self.init_objects()
		self.init_signals()
	
	def init_ui(self):
		self.setWindowTitle("Welcome to TextToSpeech")
		self.setWindowIcon(QIcon("logo.png"))
		top_layout = QHBoxLayout()
		self.voice_box = QComboBox()
		self.pitch_box = QSpinBox()
		self.pitch_box.setPrefix("pitch: ")
		self.pitch_box.setRange(-10,10)
		self.pitch_box.setValue(0)
		self.rate_box = QSpinBox()
		self.rate_box.setPrefix("rate: ")
		self.rate_box.setRange(1,1000)
		self.rate_box.setValue(200)
		self.volume_box = QSpinBox()
		self.volume_box.setPrefix("volume: ")
		self.volume_box.setRange(0,10)
		self.volume_box.setValue(10)
		self.save_btn = QPushButton("save")
		top_layout.addWidget(self.voice_box)
		top_layout.addWidget(self.pitch_box)
		top_layout.addWidget(self.rate_box)
		top_layout.addWidget(self.volume_box)
		top_layout.addWidget(self.save_btn)
		self.text_edit = QTextEdit()
		main_layout = QVBoxLayout()
		main_layout.addLayout(top_layout)
		main_layout.addWidget(self.text_edit)
		self.setLayout(main_layout)
	
	def init_objects(self):
		self.engine = pyttsx3.init()
		
		voices = self.engine.getProperty("voices")
		self.voices_dict = {}
		
		for i, voice in enumerate(voices):
			self.voices_dict[voice.name] = voice.id
			self.voice_box.addItem(voice.name)
			if i == 0:
				self.engine.setProperty("voice", voice.id)

		self.file_dialog = QFileDialog()

	def init_signals(self):
		self.save_btn.clicked.connect(self.save)
	
	def save(self):
		text = self.text_edit.toPlainText()
		self.engine.setProperty('pitch', (self.pitch_box.value() // 10.0))
		self.engine.setProperty('rate', self.rate_box.value())
		self.engine.setProperty('volume', (self.volume_box.value() // 10.0))
		if text:
			self.setDisabled(True)
			self.engine.setProperty("voice",self.voices_dict[self.voice_box.currentText()])
			file_name, _ = self.file_dialog.getSaveFileName(None,"Save speech as audio","output.mp3",
												   "MP3 (*.mp3);;WAV (*.wav);;")
			if file_name:
				self.engine.save_to_file(text,file_name)
				self.engine.runAndWait()
			self.setEnabled(True)
			
if __name__ == "__main__":
	app = QApplication()
	app.setStyle(QStyleFactory.keys()[2])
	app_widget = TextToSpeechPyttsx3()
	app_widget.show()
	app.exec()
   
