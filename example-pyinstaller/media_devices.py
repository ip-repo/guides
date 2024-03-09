import sys
import os
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import QApplication, QWidget,QHBoxLayout,QLabel,QVBoxLayout
from PySide6.QtGui import QPixmap


def resource_path(relative_path):
    """ Get absolute path to resource """

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MultimediaDeviceInfoWidget(QWidget):
    def __init__(self, img: str, info: str) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.image_label = QLabel()
        pic = QPixmap(img)
        self.image_label.setPixmap(pic)
        self.label = QLabel()
        self.label.setText(info)
        layout.addWidget(self.image_label,1)
        layout.addWidget(self.label,1)
        layout.addWidget(QLabel(),2)
        self.setLayout(layout)

class MultimediaInfoWidget(QWidget):
    
    def __init__(self, widgets_list: list) -> None:
        super().__init__()
        self.setWindowTitle("Multimedia Devices")
        self.setFixedWidth(500)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        for widget in widgets_list:
            layout.addWidget(widget, 1)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication()

    app.setStyleSheet("QWidget{color:white; font-size:12pt;background-color:black;}")
    widgets = []
 
    for device in  QMediaDevices.videoInputs():
        video_input_text = ""
        video_input_text += "Device description: " + device.description() +"\n"
       
        if device.isDefault():
            video_input_text += "Is device default(may not be correct): " + "True\n"
        else: 
            video_input_text += "Is device default(may not be correct): " + "False\n"

        widgets.append(MultimediaDeviceInfoWidget(resource_path("assets\\cam.png"), video_input_text))
    
    for device in  QMediaDevices.audioInputs():
        audio_input_text = ""
        audio_input_text += "Device description: " + device.description() +"\n"
       
        if device.isDefault():
           audio_input_text += "Is device default(may not be correct): " + "True\n"
        else: 
            audio_input_text += "Is device default(may not be correct): " + "False\n"

        audio_input_text += "Device mode: " + device.mode().name + "\n"
        audio_input_text += "Channel count: from {} to {}".format(device.minimumChannelCount(), device.maximumChannelCount()) + "\n"
        audio_input_text += "Sample rate: from {} to {}".format(device.minimumSampleRate(), device.maximumSampleRate()) + "\n"
        widgets.append(MultimediaDeviceInfoWidget(resource_path("assets\\mic.png"), audio_input_text))
    
    for device in  QMediaDevices.audioOutputs():
        audio_out_text = ""

        audio_out_text += "Device description: " + device.description() +"\n"
       
        if device.isDefault():
            audio_out_text += "Is device default(may not be correct): " + "True\n"
        else: 
            audio_out_text += "Is device default(may not be correct): " + "False\n"

        audio_out_text += "Device mode: " + device.mode().name + "\n"
        audio_out_text += "Channel count: from {} to {}".format(device.minimumChannelCount(), device.maximumChannelCount()) + "\n"
        audio_out_text += "Sample rate: from {} to {}".format(device.minimumSampleRate(), device.maximumSampleRate()) + "\n"
        widgets.append(MultimediaDeviceInfoWidget(resource_path("assets\\speak.png") ,audio_out_text))
        
    
    
    window = MultimediaInfoWidget(widgets_list=widgets)
    window.show()
    app.exec()

    
