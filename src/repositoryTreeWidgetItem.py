#external modules
import PyQt4.QtGui as QtGui
#internal modules
from paths import icons

class RepositoryTreeWidgetItem(QtGui.QTreeWidgetItem):
  def __init__(self,repositoryName,repositoryAttributes):
    super(RepositoryTreeWidgetItem, self).__init__()
    self.name = repositoryName
    self.attributes = repositoryAttributes
    if self.attributes["temporary"]:
      try:
        self.displayName = self.attributes["source-dir"]
      except KeyError:
        self.displayName = self.attributes["git-origin"]
    else:
      self.displayName = self.name
    self.setText(0,self.displayName)
    self.setIcon(0,QtGui.QIcon(icons["repository"]))

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
