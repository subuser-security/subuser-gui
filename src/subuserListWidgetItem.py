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
    subuser.execute("run "+self.name+" &")
