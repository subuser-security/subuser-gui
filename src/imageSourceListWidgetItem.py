#external modules
import PyQt4.QtGui as QtGui
#internal modules
from paths import icons

class ImageSourceListWidgetItem(QtGui.QListWidgetItem):
  def __init__(self,imageSourceName,imageSourceAttributes):
    super(ImageSourceListWidgetItem, self).__init__()
    self.imageSourceName = imageSourceName
    self.imageSourceAttributes = imageSourceAttributes
    self.setText(self.imageSourceName)
    self.setIcon(QtGui.QIcon(icons["image-source"]))
