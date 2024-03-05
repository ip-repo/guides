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
