#!/usr/bin/python

#external modules
import sys
import os
import shutil
import PyQt4.Qt as Qt
import PyQt4.uic
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from paths import *
#internal modules
from repositoryTreeWidgetItem import RepositoryTreeWidgetItem
from subuserListWidgetItem import SubuserListWidgetItem
from imageSourceListWidgetItem import ImageSourceListWidgetItem
import subuser

class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    # Load subuser logo
    PyQt4.uic.loadUi(os.path.join(sourceDir,"data/subuser.ui"), self)
    subuserIconPixmap = QtGui.QPixmap(icons["subuser-logo"])
    self.subuserIcon.setPixmap(subuserIconPixmap)
    # Load repositories
    self.repositoriesList = None
    self.loadRepositoriesList()
    # hook up event handlers
    #self.listWidget.itemActivated.connect(self.on_listWidget_itemActivated)
    # set icons
    self.setWindowIcon(QtGui.QIcon(icons["subuser-logo"]))
    self.show()
    # Load subusers
    self.loadSubusersList()

  def loadSubusersList(self):
    subusersDividedDict = subuser.executeGetJson("list subusers --json")
    subusersDict = {}
    subusersDict.update(subusersDividedDict["locked"])
    subusersDict.update(subusersDividedDict["unlocked"])
    self.listWidget.clear()
    for subuserName,attributes in subusersDict.items():
      if not subuserName.startswith("!"):
        widgetItem = SubuserListWidgetItem(subuserName,attributes)
        self.listWidget.addItem(widgetItem)

  def loadRepositoriesList(self,loadToListWidget=False):
    self.repositoriesList = subuser.executeGetJson("list repositories --json")
    repositoriesItem = self.sideBar.topLevelItem(1)
    repositoriesItem.takeChildren()
    repositoryItems=[]
    if loadToListWidget:
      self.listWidget.clear()
    for repositoryName,attributes in self.repositoriesList.items():
      newItem = RepositoryTreeWidgetItem(repositoryName,attributes)
      repositoryItems.append(newItem)
      if loadToListWidget:
        widgetItem = QtGui.QListWidgetItem(newItem.text(0))
        widgetItem.setIcon(QtGui.QIcon(icons["repository"]))
        def createSelector():
          item = newItem
          return (lambda: self.sideBar.setCurrentItem(item))
        widgetItem.activated = createSelector()
        self.listWidget.addItem(widgetItem)
    repositoriesItem.addChildren(repositoryItems)

  def on_listWidget_itemActivated(self,item):
    try:
      item.activated()
    except AttributeError:
      pass

  @QtCore.pyqtSlot()
  def on_sideBar_itemSelectionChanged(self):
    selection = self.sideBar.currentItem()
    if selection.text(0) == "subusers":
      self.loadSubusersList()
    elif selection.text(0) == "repositories":
      self.loadRepositoriesList(loadToListWidget=True)
    elif type(selection) is RepositoryTreeWidgetItem:
      self.listWidget.clear()
      imageSources = subuser.executeGetJson("list available --json")
      for imageSourceName,attributes in imageSources[selection.name].items():
        self.listWidget.addItem(ImageSourceListWidgetItem(imageSourceName,attributes))

  def closeEvent(self,event):
    shutil.rmtree(communicationsDir)

def main():
  app = QtGui.QApplication(sys.argv)
  ex = MainWindow()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
