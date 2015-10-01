#external modules
import PyQt4.QtGui as QtGui
#internal modules
from paths import icons
import subuser

class SubuserListWidgetItem(QtGui.QListWidgetItem):
  def __init__(self,subuserName,subuserAttributes):
    super(SubuserListWidgetItem, self).__init__()
    self.name = subuserName
    self.attributes = subuserAttributes
    self.setText(self.name)
    self.setIcon(QtGui.QIcon(icons["subuser"]))

  def activated(self):
    subuser.execute(["run",self.name])

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
