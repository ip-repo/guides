import gtts
import gtts.lang
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtWidgets import (QApplication,QStyleFactory, QWidget,QFileDialog, QHBoxLayout,QVBoxLayout, 
								QTextEdit, QPushButton, QComboBox,QCheckBox,)
from PySide6.QtGui import QIcon
import time
import subprocess


class TextToSpeechGtts(QWidget):
	def __init__(self, *args, **kargs) -> None:
		super().__init__(*args, **kargs)
		self.init_objects()
		self.init_ui()
		self.init_signals()

	def init_ui(self):
		self.setWindowTitle("Welcome to TextToSpeech")
		self.setWindowIcon(QIcon("logo.png"))
		self.setGeometry(0,0, 600,400)
		controls_layout = QHBoxLayout()
		controls_layout.setSpacing(2)
		self.lang_box = QComboBox()
		self.lang_box.addItems(self.reverse_lang_dict.keys())
		self.save_text_btn =QPushButton("save text")
		self.save_speech_btn = QPushButton("save audio")
		self.slow = QCheckBox("slow")
		controls_layout.addWidget(self.lang_box, 3)
		controls_layout.addWidget(self.slow,1//4)
		controls_layout.addWidget(self.save_text_btn, 1)
		controls_layout.addWidget(self.save_speech_btn, 1)
		main_layout = QVBoxLayout()
		self.text_edit = QTextEdit()
		main_layout.addLayout(controls_layout,1)
		main_layout.addWidget(self.text_edit, 10)
		self.setLayout(main_layout)

	def init_objects(self):
		self.text_max_len = 5000
		self.lang_dict = gtts.lang.tts_langs()
		self.reverse_lang_dict = {}
		for key in self.lang_dict.keys():
			self.reverse_lang_dict[self.lang_dict[key]] = key
		self.tts = QTextToSpeech()
		self.tts.setVoice(self.tts.availableVoices()[0])
		self.tts.setVolume(1.0)
		self.file_dialog = QFileDialog()
		
	def init_signals(self):
		self.save_speech_btn.clicked.connect(self.save_speech_btn_clicked)
		self.save_text_btn.clicked.connect(self.save_txt_btn_clicked)
		
	def save_speech_btn_clicked(self):
		text = self.text_edit.toPlainText()
		if text:
			self.setDisabled(True)
			self.setWindowTitle("Working on it....")
			if self.slow.checkState().value == 2:
				slow = True
			else:
				slow = False
			lang = self.reverse_lang_dict[self.lang_box.currentText()]

			file_name, _ = self.file_dialog.getSaveFileName(None,"Save speech as audio","output.mp3",
												   "MP3 (*.mp3);;WAV (*.wav);;")
			if file_name:
				t1_start = time.perf_counter() 
				if slow:
					subprocess.run(["gtts-cli", text[:self.text_max_len],"--slow", "--output", file_name, "-l", lang])
				else:
					subprocess.run(["gtts-cli", text[:self.text_max_len],"--output", file_name, "-l", lang])
				t1_stop = time.perf_counter()
				print("exection time:",t1_stop - t1_start, "seconds")
			self.setEnabled(True)
			self.setWindowTitle("Saved: {}".format(file_name))	
		else:
			self.setWindowTitle("Can't convert nothing....")
	
	def save_txt_btn_clicked(self):
		self.setDisabled(True)
		text = self.text_edit.toPlainText()[:self.text_max_len]
		filename,_ = self.file_dialog.getSaveFileName(None,"Save as text file","output.txt",
												"Text Files (*.txt)")
		if filename:
			with open(filename, "w") as f:
				f.write(text)
			self.setEnabled(True)
			self.setWindowTitle("Saved: {}".format(filename))
		
			





if __name__ == "__main__":
	app = QApplication()
	app.setStyle(QStyleFactory.keys()[2])
	#print(QStyleFactory.keys())
	app_widget = TextToSpeechGtts()
	#maximum characters length to process as speech 
	app_widget.text_max_len = 10000
	
	app_widget.show()
	app.exec()
   
