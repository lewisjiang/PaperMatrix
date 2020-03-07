import random
import re
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtCore import pyqtSignal, pyqtSlot

from mytreeview import MySortFilterProxyModel, ArticleViewer, SourceArticleDBModel
from comparator import ComparatorTableModel, ComparatorViewer, Comparator
from article import *
from tabpagewidgets import EditTabPageWidget, ComparatorTabPageWidget


class MainWindow(QMainWindow):
    def __init__(self, ):
        super(QMainWindow, self).__init__()

        rec = QApplication.desktop().screenGeometry()
        self.monitor_height = rec.height()
        self.monitor_width = rec.width()

        self.tabWidget = QTabWidget(tabsClosable=True)
        self.tabWidget.tabCloseRequested.connect(self.CloseTab)
        # self.tabWidget.setMovable(True)
        self.setCentralWidget(self.tabWidget)

        self.statusBar().showMessage("Ready")
        self.createMenu()

        self.compTableModel = ComparatorTableModel()  # TODO: set data

        self.addTab0()

        self.btnCreateNew.clicked.connect(self.onClicked_CreateNewEntry)

        self.editorPool = dict()

        self.resize(750, 600)

    def createMenu(self):
        self.menu0 = self.menuBar().addMenu("&File")
        self.menu1 = self.menuBar().addMenu("&Edit")

        self.menu0.addAction('&Add new entry', self.onClicked_CreateNewEntry)
        self.menu0.addAction('&Save database', lambda: self.compTableModel.pickleData("pm.db"))
        self.menu0.addAction('&Load database', lambda: self.compTableModel.unpickleData("pm.db"))
        self.menu0.addAction('&Exit', self.close)

    @pyqtSlot(bool)
    def loadData(self, b):
        if b:
            self.qMainTreev.setSourceModel(SourceArticleDBModel(self.compTableModel.ADB))
            self.qMainTreev.loadHeaderState()
            print("loaded data entry count: ", self.compTableModel.ADB.entryCount())

    def addTab0(self):
        """Add the main window tab"""

        hbox = QHBoxLayout()
        gbox = QGridLayout()

        # Deal with the side bar
        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.StyledPanel)
        leftFrame.setMinimumSize(200, 600)
        leftFrame.setMaximumWidth(250)  # Max width
        leftFrame.setLayout(gbox)

        self.btnExpandSelected = QPushButton(leftFrame)
        self.btnCollapseSelected = QPushButton(leftFrame)
        self.btnExpandSelected.setText("Expand")
        self.btnCollapseSelected.setText("Collapse")
        gbox.addWidget(self.btnExpandSelected, 2, 0, 1, 2)
        gbox.addWidget(self.btnCollapseSelected, 2, 2, 1, 2)

        self.btnCreateNew = QPushButton(leftFrame)
        self.btnCreateNew.setText("New Entry")
        gbox.addWidget(self.btnCreateNew, 3, 0, 1, 2)

        self.btnDeleteEntry = QPushButton(leftFrame)
        self.btnDeleteEntry.setText("Delete")
        gbox.addWidget(self.btnDeleteEntry, 3, 2, 1, 2)

        # Show current comparators, a table view maybe.
        groupComparators = QGroupBox("Comparators", leftFrame)
        self.compTableView = ComparatorViewer(self.compTableModel)
        groupCLayout = QGridLayout()
        groupCLayout.addWidget(self.compTableView, 0, 0, 1, 2)

        self.btnAddToComparator = QPushButton(leftFrame)
        self.btnAddToComparator.setText("Add to comparator")
        # self.btnAddToComparator.setEnabled(False)
        groupCLayout.addWidget(self.btnAddToComparator, 1, 0, 1, 2)

        self.btnAddToNew = QPushButton(leftFrame)
        self.btnAddToNew.setText("New")
        groupCLayout.addWidget(self.btnAddToNew, 2, 0, 1, 1)

        self.btnDelComp = QPushButton(leftFrame)
        self.btnDelComp.setText("Delete")
        groupCLayout.addWidget(self.btnDelComp, 2, 1, 1, 1)

        self.btnPinComp = QPushButton(leftFrame)
        self.btnPinComp.setText("Pin")
        groupCLayout.addWidget(self.btnPinComp, 3, 0, 1, 1)

        self.btnUnPinComp = QPushButton(leftFrame)
        self.btnUnPinComp.setText("Unpin")
        groupCLayout.addWidget(self.btnUnPinComp, 3, 1, 1, 1)

        groupComparators.setLayout(groupCLayout)
        # filler0 = QWidget()
        gbox.addWidget(groupComparators, 0, 0, 1, 4)

        groupFilter = QGroupBox("Entry Filter", leftFrame)
        groupFilter.setMaximumHeight(250)
        groupGridLayout = QGridLayout()
        groupFilter.setLayout(groupGridLayout)
        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox("Case sensitive")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.filterSyntaxCheckBox = QtWidgets.QCheckBox("Use Regex")
        self.filterSyntaxCheckBox.setChecked(True)
        self.filterPatternLineEdit = QtWidgets.QLineEdit()
        # self.filterPatternLineEdit.setText("")

        self.filterDomainCombo = QtWidgets.QComboBox()
        self.filterDomainCombo.addItem("All", searchableDomainIndex)
        for i in searchableDomainIndex:
            self.filterDomainCombo.addItem(headerNames[i], [i])
        filterComboLabel = QtWidgets.QLabel("Filter Domain:")
        filterComboLabel.setBuddy(self.filterDomainCombo)
        groupGridLayout.addWidget(filterComboLabel, 0, 0, 1, 4)
        groupGridLayout.addWidget(self.filterDomainCombo, 1, 0, 1, 4)

        filterPatternLabel = QtWidgets.QLabel("&Filter pattern:")
        filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        groupGridLayout.addWidget(filterPatternLabel, 2, 0, 1, 4)
        groupGridLayout.addWidget(self.filterPatternLineEdit, 3, 0, 1, 4)

        groupGridLayout.addWidget(self.filterCaseSensitivityCheckBox, 4, 0, 1, 4)
        groupGridLayout.addWidget(self.filterSyntaxCheckBox, 5, 0, 1, 4)
        gbox.addWidget(groupFilter, 1, 0, 1, 4)

        # deal with the main tree view
        self.qMainTreev = ArticleViewer()
        srcModel = SourceArticleDBModel(self.compTableModel.ADB)

        self.qMainTreev.setSourceModel(srcModel)
        self.qMainTreev.setDefaultHeaderView()

        self.compTableModel.externalDataLoaded.connect(self.loadData)

        # the splitter
        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(leftFrame)
        # splitter1.addWidget(self.proxyView)
        splitter1.addWidget(self.qMainTreev)
        splitter1.setSizes([100, 200])

        hbox.addWidget(splitter1)

        tab = QWidget()
        tab.setLayout(hbox)
        self.tabWidget.addTab(tab, "Main")
        self.tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)

        self.btnExpandSelected.clicked.connect(self.qMainTreev.onClickExpandRows)
        self.btnCollapseSelected.clicked.connect(self.qMainTreev.onClickCollapseRows)

        self.qMainTreev.proxyView.doubleClicked.connect(self.onDoubleClicked_EditEntry)
        self.btnDeleteEntry.clicked.connect(self.deleteSelectedEntries)

        self.filterPatternLineEdit.textChanged.connect(self.textFilterChanged)
        self.filterSyntaxCheckBox.toggled.connect(self.textFilterChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.textFilterChanged)
        self.filterDomainCombo.currentIndexChanged.connect(self.textFilterDomainChanged)

        self.btnAddToNew.clicked.connect(self.onClicked_CreateNewComparator)
        self.btnPinComp.clicked.connect(self.pinComparator)
        self.btnUnPinComp.clicked.connect(self.unpinComparator)
        self.btnDelComp.clicked.connect(self.delComparator)

        self.compTableView.view.doubleClicked.connect(self.addTab1_Open)
        self.btnAddToComparator.clicked.connect(self.addTab1_Append)

    def pinComparator(self):
        selected = self.compTableView.view.selectedIndexes()
        if selected:
            row = selected[0].row()
            self.compTableModel.pinComp(row)
            self.compTableView.view.clearSelection()

    def unpinComparator(self):
        selected = self.compTableView.view.selectedIndexes()
        if selected:
            row = selected[0].row()
            self.compTableModel.unpinComp(row)
            self.compTableView.view.clearSelection()

    def delComparator(self):
        selected = self.compTableView.view.selectedIndexes()
        if selected:
            row = selected[0].row()
            comp = self.compTableModel.index(row, 0).internalPointer()

            tabIndex = self.checkIfCompOpened(comp.name)
            if tabIndex > 0:
                self.tabWidget.removeTab(tabIndex)

            self.compTableView.view.clearSelection()
            self.compTableModel.removeComparator(row)

    def deleteSelectedEntries(self):
        uids = self.qMainTreev.getSelectedItemUids()
        if uids:
            self.qMainTreev.proxyView.clearSelection()
            for uid in uids:
                srcRow = self.qMainTreev.proxyModel.sourceModel().ADB.getRowByUid(uid)
                self.qMainTreev.proxyModel.sourceModel().removeItem(srcRow)

                entryEditTabIndex = self.checkIfEntryOpened(uid)
                if entryEditTabIndex > 0:
                    self.tabWidget.removeTab(entryEditTabIndex)

                for comp in self.compTableModel.compDB_pinned + self.compTableModel.compDB_unpinned:
                    compTabIndex = self.checkIfCompOpened(comp.name)
                    if compTabIndex > 0:
                        compTab = self.tabWidget.widget(compTabIndex)
                        compTab.qCompViewer.proxyModel.sourceModel().removeItemByUid(uid)
                    comp.removeEntry(uid)
        return True

    def textFilterDomainChanged(self):
        nd = self.filterDomainCombo.itemData(self.filterDomainCombo.currentIndex())
        self.qMainTreev.proxyModel.setFilterDomains(nd)
        self.textFilterChanged()

    def textFilterChanged(self):
        if self.filterSyntaxCheckBox.isChecked():
            syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.RegExp)
        else:
            syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.FixedString)

        caseSensitivity = (
                self.filterCaseSensitivityCheckBox.isChecked()
                and QtCore.Qt.CaseSensitive or QtCore.Qt.CaseInsensitive)
        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(), caseSensitivity, syntax)
        self.qMainTreev.proxyModel.setFilterRegExp(regExp)

    def onClicked_CreateNewComparator(self):
        toAddUids = self.qMainTreev.getSelectedItemUids()
        if toAddUids:
            comp = Comparator()
            for uid in toAddUids:
                entry = self.compTableModel.ADB.getEntryByUid(uid)
                comp.addEntry(entry)
            self.addTab1_new(comp)

    def validateComparatorName(self):
        currentCTab = self.tabWidget.currentWidget()
        name = currentCTab.compNameLineEdit.text()
        valid = len(name) > 0

        exception = currentCTab.comp.name

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setFixedHeight(100)
        msg.setFixedWidth(100)
        msg.setWindowTitle("Cannot save")

        msg.setText("The Comparator doesn't have a name!")
        if not valid:
            msg.setText("The Comparator doesn't have a name!")
            retval = msg.exec_()
            return False

        for n in self.compTableModel.compDB_pinned:
            if not valid:
                break
            valid = valid and (name != n.name or exception == n.name)
        for n in self.compTableModel.compDB_unpinned:
            if not valid:
                break
            valid = valid and (name != n.name or exception == n.name)

        if not valid:
            msg.setText("A Comparator with the same name exists already!")
            retval = msg.exec_()
            return False

        return True

    def onClicked_SaveComparator_New(self):
        currentCTab = self.tabWidget.currentWidget()
        name = currentCTab.compNameLineEdit.text()
        if not self.validateComparatorName():
            return

        currentCTab.comp.setName(currentCTab.compNameLineEdit.text())
        currentCTab.comp.setComment(currentCTab.compCommentText.toPlainText())
        if currentCTab.originalComp is None:
            print("Create comparator ", name)
            currentCTab.originalComp = Comparator()
            currentCTab.originalComp.updateFromGiven(currentCTab.comp)
            self.compTableModel.addComparator(currentCTab.originalComp)
        else:
            print("Update comparator ", name)
            currentCTab.originalComp.updateFromGiven(currentCTab.comp)
        self.compTableModel.emitAllDataChanged()

    def addTab1_new(self, comp):
        """Add the new comparator tab"""
        tab = ComparatorTabPageWidget()
        tab.setComparatorToShow(comp)
        tab.originalComp = None

        newidx = self.tabWidget.addTab(tab, "New Comparator")
        self.tabWidget.setCurrentIndex(newidx)

        tab.btnCancel.clicked.connect(self.closeCurrentTab)
        tab.btnSave.clicked.connect(self.onClicked_SaveComparator_New)
        tab.qCompViewer.proxyView.doubleClicked.connect(self.onDoubleClicked_EditCompEntry)

        tab.compNameLineEdit.textChanged.connect(self.setCurrentComparatorTabLabel)

    # def onClicked_SaveComparator_Open(self):

    def onClicked_SaveComparator_OpenAppend(self):
        currentCTab = self.tabWidget.currentWidget()
        name = currentCTab.compNameLineEdit.text()
        if not self.validateComparatorName():
            return

        print("-- OA Save comparator ", name)

        theComp = currentCTab.comp
        theComp.setName(currentCTab.compNameLineEdit.text())
        theComp.setComment(currentCTab.compCommentText.toPlainText())

        original = currentCTab.originalComp
        original.updateFromGiven(theComp)
        self.compTableModel.emitAllDataChanged()

    def addTab1_Open(self):  # TODO: slot collecting 2 signals (double click and btn click) for different p
        """open addTab1 when double clicked on the compTableView"""
        if len(self.compTableView.view.selectedIndexes()) < 1:
            return
        original = self.compTableView.view.selectedIndexes()[0].internalPointer()

        tabIndex = self.checkIfCompOpened(original.name)
        if tabIndex > 0:
            self.tabWidget.setCurrentIndex(tabIndex)
            return

        tab = ComparatorTabPageWidget()
        tab.setComparatorToShow(original)

        newidx = self.tabWidget.addTab(tab, "New Comparator")
        self.tabWidget.setCurrentIndex(newidx)

        tab.btnCancel.clicked.connect(self.closeCurrentTab)
        tab.btnSave.clicked.connect(self.onClicked_SaveComparator_OpenAppend)
        tab.qCompViewer.proxyView.doubleClicked.connect(self.onDoubleClicked_EditCompEntry)

        tab.compNameLineEdit.textChanged.connect(self.setCurrentComparatorTabLabel)
        self.setCurrentComparatorTabLabel()

    def addTab1_Append(self):
        if len(self.compTableView.view.selectedIndexes()) < 1:
            return
        original = self.compTableView.view.selectedIndexes()[0].internalPointer()
        uids = self.qMainTreev.getSelectedItemUids()
        if not uids:
            return

        tabIndex = self.checkIfCompOpened(original.name)
        if tabIndex > 0:
            tgtTab = self.tabWidget.widget(tabIndex)
            for uid in uids:
                entry = self.compTableModel.ADB.getEntryByUid(uid)
                tgtTab.qCompViewer.proxyModel.sourceModel().appendItem(entry)
            self.tabWidget.setCurrentIndex(tabIndex)
            return

        theComp = Comparator()
        theComp.updateFromGiven(original)

        for uid in uids:
            entry = self.compTableModel.ADB.getEntryByUid(uid)
            theComp.addEntry(entry)

        tab = ComparatorTabPageWidget()
        tab.setComparatorToShow(theComp)
        tab.originalComp = original

        newidx = self.tabWidget.addTab(tab, theComp.name[:16] if len(theComp.name) < 16 else theComp.name[:13] + "..")
        self.tabWidget.setCurrentIndex(newidx)

        tab.btnCancel.clicked.connect(self.closeCurrentTab)
        tab.btnSave.clicked.connect(self.onClicked_SaveComparator_OpenAppend)
        tab.qCompViewer.proxyView.doubleClicked.connect(self.onDoubleClicked_EditCompEntry)

        tab.compNameLineEdit.textChanged.connect(self.setCurrentComparatorTabLabel)
        self.setCurrentComparatorTabLabel()

    @pyqtSlot()
    def onClicked_SaveEdit(self):
        currentEditTab = self.tabWidget.currentWidget()
        currentEditTab.setTitle()
        currentEditTab.setNickname()
        currentEditTab.setYear()
        currentEditTab.setVenue()
        currentEditTab.setAuthors()
        currentEditTab.setTags()

        currentEditTab.setOverview()
        currentEditTab.setBackground()
        currentEditTab.setPastwork()
        currentEditTab.setGap()
        currentEditTab.setContribution()
        currentEditTab.setMainmethod()
        currentEditTab.setMyfocus()
        currentEditTab.setDoubts()
        currentEditTab.setMiscellaneous()

        entry = currentEditTab.tempArticle
        print(type(entry))
        if entry.uid == -1:
            # TODO: How to set a unique ID for each article when created???
            lastUid = self.qMainTreev.proxyModel.sourceModel().ADB.getUidByRow(
                self.compTableModel.ADB.entryCount() - 1)
            if lastUid is None:
                entry.uid = 0
            else:
                entry.uid = lastUid + 1

            self.qMainTreev.proxyModel.sourceModel().appendItem(entry)
            print("Saving new edit: ", entry.uid)
        else:
            sourceModel = self.qMainTreev.proxyModel.sourceModel()
            rowNum = sourceModel.ADB.getRowByUid(entry.uid)
            print("Saving: ", sourceModel.ADB.entryCount())
            for i in range(1, len(headerNames)):
                sourceModel.setData(sourceModel.index(rowNum, i, QtCore.QModelIndex()), entry.at(i), QtCore.Qt.EditRole)

    @pyqtSlot()
    def onClicked_CreateNewEntry(self):
        tempEntry = ArticleEntry(-1)
        self.addTab2(tempEntry)

    @pyqtSlot()
    def onDoubleClicked_EditCompEntry(self):
        visibleHeaderCount = self.tabWidget.currentWidget().qCompViewer.proxyView.header().count() - \
                             self.tabWidget.currentWidget().qCompViewer.proxyView.header().hiddenSectionCount()
        print("=" * 32 + "\nvisible cols: ", visibleHeaderCount)
        if len(self.tabWidget.currentWidget().qCompViewer.proxyView.selectedIndexes()) != visibleHeaderCount:
            return
        idx = self.tabWidget.currentWidget().qCompViewer.proxyView.selectedIndexes()[0]
        uidIndex = self.tabWidget.currentWidget().qCompViewer.proxyModel.index(idx.row(), 0, idx.parent())
        uid = uidIndex.data()
        print("uid: ", uid)

        tabIdx = self.checkIfEntryOpened(uid)
        if tabIdx > 0:
            self.tabWidget.setCurrentIndex(tabIdx)
            return

        tempEntry = self.tabWidget.currentWidget().qCompViewer.proxyModel.sourceModel().ADB.getEntryByUid(uid)
        copie = copy.deepcopy(tempEntry)
        print(copie.uid)
        self.addTab2(copie)

    @pyqtSlot()
    def onDoubleClicked_EditEntry(self):
        visibleHeaderCount = self.qMainTreev.proxyView.header().count() - \
                             self.qMainTreev.proxyView.header().hiddenSectionCount()
        print("=" * 32 + "\nvisible cols: ", visibleHeaderCount)
        if len(self.qMainTreev.proxyView.selectedIndexes()) != visibleHeaderCount:
            return
        idx = self.qMainTreev.proxyView.selectedIndexes()[0]
        uidIndex = self.qMainTreev.proxyModel.index(idx.row(), 0, idx.parent())
        uid = uidIndex.data()
        print("uid: ", uid)

        tabIdx = self.checkIfEntryOpened(uid)
        if tabIdx > 0:
            self.tabWidget.setCurrentIndex(tabIdx)
            return

        tempEntry = self.qMainTreev.proxyModel.sourceModel().ADB.getEntryByUid(uid)  # TODO: on double clicked
        copie = copy.deepcopy(tempEntry)
        print(copie.uid)
        self.addTab2(copie)

    def addTab2(self, entry):
        """Add the editor tab"""

        tab = EditTabPageWidget(entry)

        if tab.tempArticle.uid >= 0:
            if len(tab.tempArticle.nickname) <= 10:
                newidx = self.tabWidget.addTab(tab, tab.tempArticle.nickname)
            else:
                newidx = self.tabWidget.addTab(tab, tab.tempArticle.title[:15])
        else:
            newidx = self.tabWidget.addTab(tab, "New Edit")
        self.tabWidget.setCurrentIndex(newidx)

        # connect signals
        tab.btnClose.clicked.connect(self.closeCurrentTab)
        tab.btnSave.clicked.connect(self.onClicked_SaveEdit)

        tab.qLine_nickname.textChanged.connect(self.setCurrentEditTabLabel)

    def CloseTab(self, i):
        self.tabWidget.removeTab(i)

    @pyqtSlot()
    def setCurrentEditTabLabel(self):
        txt = self.tabWidget.currentWidget().qLine_nickname.text()
        if len(txt) < 10:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), txt)
        else:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), txt[:10] + "..")

    @pyqtSlot()
    def setCurrentComparatorTabLabel(self):
        if not isinstance(self.tabWidget.currentWidget(), ComparatorTabPageWidget):
            return
        txt = self.tabWidget.currentWidget().compNameLineEdit.text()
        if len(txt) < 16:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), txt)
        else:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), txt[:15] + "..")

    def closeCurrentTab(self):
        self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def checkIfEntryOpened(self, uid):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)
            if isinstance(tab, EditTabPageWidget):
                if tab.tempArticle.uid == uid:
                    return i
        return -1

    def checkIfCompOpened(self, name):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)
            if isinstance(tab, ComparatorTabPageWidget):
                if tab.originalComp.name == name:
                    return i
        return -1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setWindowTitle("PaperMatrix")
    mainwindow.show()
    sys.exit(app.exec_())
