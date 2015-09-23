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
        labelText = self.attributes["source-dir"]
      except KeyError:
        labelText = self.attributes["git-origin"]
    else:
      labelText = self.name
    self.setText(0,labelText)
    self.setIcon(0,QtGui.QIcon(icons["repository"]))
