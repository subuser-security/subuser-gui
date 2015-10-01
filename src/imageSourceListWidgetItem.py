#external modules
import PyQt4.QtGui as QtGui
#internal modules
from paths import icons

class ImageSourceListWidgetItem(QtGui.QListWidgetItem):
  def __init__(self,imageSourceName,imageSourceAttributes):
    super(ImageSourceListWidgetItem, self).__init__()
    self.name = imageSourceName
    self.attributes = imageSourceAttributes
    self.setText(self.name)
    self.setIcon(QtGui.QIcon(icons["image-source"]))

  def getActionsWidget(self):
    layout = QtGui.QVBoxLayout()
    attributesLabel = QtGui.QLabel()
    attributesLabel.setText(str(self.attributes))
    layout.addWidget(attributesLabel)
    #layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
    frame = QtGui.QFrame()
    frame.setLayout(layout)
    scrollArea = QtGui.QScrollArea()
    scrollArea.setWidget(frame)
    return scrollArea
