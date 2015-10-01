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
    # Display repositories
    self.repositoriesList = None
    self.displayRepositoriesList()
    # set icons
    self.setWindowIcon(QtGui.QIcon(icons["subuser-logo"]))
    self.show()
    # Display subusers
    self.displaySubusersList()

  def displaySubusersList(self):
    self.sectionTitle.setText("Subusers")
    subusersDividedDict = subuser.executeGetJson(["list","subusers","--json"])
    subusersDict = {}
    subusersDict.update(subusersDividedDict["locked"])
    subusersDict.update(subusersDividedDict["unlocked"])
    self.listWidget.clear()
    for subuserName,attributes in subusersDict.items():
      if not subuserName.startswith("!"):
        widgetItem = SubuserListWidgetItem(subuserName,attributes)
        def wrapsSelected():
          thisWidgetItem = widgetItem
          def selected():
            self.selectionLabel.setText(thisWidgetItem.name)
            self.tabWidget.clear()
            self.tabWidget.insertTab(0,thisWidgetItem.getActionsWidget(),"Actions")
          return selected
        widgetItem.selected = wrapsSelected()
        self.listWidget.addItem(widgetItem)
    firstItem = self.listWidget.item(0)
    if firstItem:
      self.listWidget.setItemSelected(firstItem,True)

  def displayRepositoriesList(self,displayToListWidget=False):
    if displayToListWidget:
      self.sectionTitle.setText("Repositories")
    self.repositoriesList = subuser.executeGetJson(["list","repositories","--json"])
    repositoriesItem = self.sideBar.topLevelItem(1)
    repositoriesItem.takeChildren()
    repositoryItems=[]
    if displayToListWidget:
      self.listWidget.clear()
    for repositoryName,attributes in self.repositoriesList.items():
      newItem = RepositoryTreeWidgetItem(repositoryName,attributes)
      repositoryItems.append(newItem)
      if displayToListWidget:
        widgetItem = QtGui.QListWidgetItem(newItem.text(0))
        widgetItem.setIcon(QtGui.QIcon(icons["repository"]))
        def wrapsActivated():
          item = newItem
          return (lambda: self.sideBar.setCurrentItem(item))
        widgetItem.activated = wrapsActivated()
        def wrapsSelected():
          item = newItem
          def selected():
            self.selectionLabel.setText(item.displayName)
            self.tabWidget.clear()
            self.tabWidget.insertTab(0,item.getActionsWidget(),"Actions")
          return selected
        widgetItem.selected = wrapsSelected()
        self.listWidget.addItem(widgetItem)
    repositoriesItem.addChildren(repositoryItems)
    if displayToListWidget:
      firstItem = self.listWidget.item(0)
      if firstItem:
        self.listWidget.setItemSelected(firstItem,True)


  def displayRepository(self,repoItem):
    self.sectionTitle.setText(repoItem.displayName)
    self.listWidget.clear()
    imageSources = subuser.executeGetJson(["list","available","--json"])
    for imageSourceName,attributes in imageSources[repoItem.name].items():
      newItem = ImageSourceListWidgetItem(imageSourceName,attributes)
      def wrapsSelected():
        item = newItem
        def selected():
          self.selectionLabel.setText(item.name)
          self.tabWidget.clear()
          self.tabWidget.insertTab(0,item.getActionsWidget(),"Actions")
        return selected
      newItem.selected = wrapsSelected()
      self.listWidget.addItem(newItem)
    firstItem = self.listWidget.item(0)
    if firstItem:
      self.listWidget.setItemSelected(firstItem,True)

  def on_listWidget_itemActivated(self,item):
    try:
      item.activated()
    except AttributeError:
      pass

  def on_listWidget_itemSelectionChanged(self):
    try:
      try:
        item = self.listWidget.selectedItems()[0]
      except IndexError:
        return
      item.selected()
    except AttributeError:
      pass

  @QtCore.pyqtSlot()
  def on_sideBar_itemSelectionChanged(self):
    selection = self.sideBar.currentItem()
    if selection.text(0) == "subusers":
      self.displaySubusersList()
    elif selection.text(0) == "repositories":
      self.displayRepositoriesList(displayToListWidget=True)
    elif type(selection) is RepositoryTreeWidgetItem:
      self.displayRepository(selection)

def main():
  app = QtGui.QApplication(sys.argv)
  ex = MainWindow()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
