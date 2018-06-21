import sys
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from picamera import PiCamera
from pyzbar.pyzbar import decode

class VideoRecorder(QtCore.QObject):
	# To take a snapshot one at a time then emit out in term on numpy ndarray
	image_data = QtCore.pyqtSignal(np.ndarray)
	
	def __init__(self, camera_port=0, parent=None):
		super().__init__(parent)
		self.resolution = (320,240)		
		
		self.camera = PiCamera() 
		self.camera.resolution=self.resolution

		self.timer = QtCore.QBasicTimer()

	def start_recording(self):
		self.timer.start(0, self)

	def timerEvent(self, event):
		if (event.timerId() != self.timer.timerId()):
			return
		
		frame = np.empty((self.resolution[1],self.resolution[0],3),dtype=np.uint8)	
		#capture image

		self.camera.capture(frame,'rgb')
		#emit image out 
		self.image_data.emit(frame)


class DecoderWidget(QtWidgets.QWidget):
	#To display image array and do decoding
	
	def __init__(self,  parent=None):
		super().__init__(parent)
		self.qr_data = []
		self.image = QtGui.QImage()
		self._red = (0, 0, 255)
		self._width = 2
		self._min_size = (30, 30)

	def _decode(self):
		if self.qr_data != [] :
			msg = QtWidgets.QMessageBox()
			msg.setIcon(QtWidgets.QMessageBox.Information)
			msg.setWindowTitle("QR Code Data ")
			msg.setDetailedText(self.qr_data[0].data.decode('utf-8'))
			retval = msg.exec_()
		
		
	
	def image_data_slot(self, image_data: np.ndarray):
		self.qr_data = decode(image_data)
		self.image = self.get_qimage(image_data)
		if self.image.size() != self.size():
			self.setFixedSize(self.image.size())

		self.update()

	def get_qimage(self, image: np.ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3 * width
		QImage = QtGui.QImage
		image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
		image = image.rgbSwapped()
		return image

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawImage(0, 0, self.image)
		self.image = QtGui.QImage()
		
		if self.qr_data != [] :
			col = QtGui.QColor(200, 0, 0)
			col.setNamedColor('#d4d4d4')
			painter.setPen(col)
		
			#painter.setBrush(QtGui.QColor(200, 0, 0))
			rect = self.qr_data[0].rect
			painter.drawRect(rect.left, rect.top, rect.width, rect.height)
		
		

class MainWidget(QtWidgets.QWidget):
	def __init__(self,  parent=None):
		super().__init__(parent)
		self.decoder_widget = DecoderWidget()

		self.recorder = VideoRecorder()
		
		image_data_slot = self.decoder_widget.image_data_slot
		
		self.recorder.image_data.connect(image_data_slot)
		
		layout = QtWidgets.QVBoxLayout()

		layout.addWidget(self.decoder_widget)
		self.run_button = QtWidgets.QPushButton('Decode')
		layout.addWidget(self.run_button)

		self.run_button.clicked.connect(self.decoder_widget._decode)
		self.setLayout(layout)
		self.recorder.start_recording()
		
def main():
	app = QtWidgets.QApplication(sys.argv)

	main_window = QtWidgets.QMainWindow()
	main_widget = MainWidget()
	main_window.setCentralWidget(main_widget)
	main_window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()    		
