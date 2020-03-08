from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import sys
import datetime

from article import headerNames


class SourceArticleDBModel(QtCore.QAbstractItemModel):
    def __init__(self, db, parent=None):
        super(SourceArticleDBModel, self).__init__(parent)
        self.ADB = db  # TODO: This can be a ArticleDB or a Comparator
        self.hdv = QtWidgets.QHeaderView(QtCore.Qt.Horizontal)
        self.expandedItemUids = set()

        self.dataChanged.connect(self.onDataChanged)

    @pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def onDataChanged(self, topLeft, btmRight):
        # print("data changed!")
        if topLeft.row() == btmRight.row() and topLeft.column() == btmRight.column():
            pass

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return headerNames[section]
        return None

    def columnCount(self, parent=None):
        return len(headerNames)

    def rowCount(self, parent=None):
        # if parent.column() > 0:
        #     return 0
        return self.ADB.entryCount()

    def parent(self, qindex=QtCore.QModelIndex()):
        # if not qindex.isValid():
        #     return QtCore.QModelIndex()
        return QtCore.QModelIndex()

        # parentItem = qindex.internalPointer().parentItem
        # if parentItem == self.ADB:
        #     return QtCore.QModelIndex()
        # return self.createIndex(parentItem.entryList.index(qindex.internalPointer()), 0, parentItem)

        # return None             # TODO: May need a real parent as root

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():  # False for QtCore.QModelIndex()
            parentItem = self.ADB
            entry = parentItem.entries[parentItem.uidList[row]]
            retval = self.createIndex(row, column, entry)
            return retval
        else:
            parentItem = parent.internalPointer()
            return QtCore.QModelIndex()

    def data(self, qindex, role=QtCore.Qt.DisplayRole):
        # print("Accessing data")
        if not qindex.isValid():
            return None

        item = qindex.internalPointer()
        res = item.at(qindex.column())

        if 7 <= qindex.column() <= 9:
            delta = datetime.datetime.now() - datetime.datetime.utcnow()
            timestr = item.at(qindex.column()) + delta
            res = timestr.strftime('%Y-%m-%d %H:%M:%S')

        if role == QtCore.Qt.DisplayRole:
            if 5 <= qindex.column() <= 6:
                return "; ".join(res)
            return res
        elif role == QtCore.Qt.EditRole:
            return res
        elif role == QtCore.Qt.SizeHintRole:  # TODO: hints size need accurate font size
            strlen = len(str(res))
            width = self.hdv.sectionSize(qindex.column())
            if width and item.at(0) in self.expandedItemUids:
                height = min(28 * 3, 7 * 28 * strlen // width)
                # print("Size hint header: (%d, %d, %d)" % (self.hdv.count(), width, height))
                return QtCore.QSize(width, height)
            return QtCore.QSize(100, 28)

        return None

    def setData(self, qindex, dat, role=None):
        if role == QtCore.Qt.EditRole:
            r = qindex.row()
            uid = self.ADB.uidList[r]
            self.ADB.entries[uid].set(qindex.column(), dat)
            self.dataChanged.emit(qindex, qindex, [])
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        # return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row)
        print("Rows changed")
        self.endInsertRows()
        return True

    # add data
    def appendItem(self, entry, parent=QtCore.QModelIndex()):
        oldRowCount = self.rowCount()
        uidCheck = self.ADB.addEntry(entry)
        if not uidCheck:
            print("uidCheck Failure ", uidCheck)
            return False
        self.insertRow(oldRowCount, parent)

        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        uid = self.ADB.uidList[row]
        if uid in self.expandedItemUids:
            self.expandedItemUids.remove(uid)
        self.ADB.removeEntry(uid)
        self.endRemoveRows()
        return True

    # remove data
    def removeItem(self, n):
        if n is None or n >= self.rowCount():
            return False
        self.removeRow(n, QtCore.QModelIndex())
        return True

    def removeItemByUid(self, uid):
        row = self.ADB.getRowByUid(uid)
        return self.removeItem(row)

    def emitItemChangedByUid(self, uid):
        row = self.ADB.getRowByUid(uid)
        if row is not None:
            index0 = self.index(row, 0, QtCore.QModelIndex())
            index1 = self.index(row, len(headerNames) - 1, QtCore.QModelIndex())
            self.dataChanged.emit(index0, index1, [])


class MySortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(MySortFilterProxyModel, self).__init__(parent)
        self.filterDomains = [1, 2, 5, 6, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    def setFilterDomains(self, newDomains):
        self.filterDomains = newDomains

    def filterAcceptsRow(self, sourceRow, sourceParent):
        res = False
        for sect in self.filterDomains:
            idx = self.sourceModel().index(sourceRow, sect, sourceParent)
            res = res or self.filterRegExp().indexIn(str(self.sourceModel().data(idx))) >= 0

        return res

    def lessThan(self, left, right):
        leftData = self.sourceModel().data(left)
        rightData = self.sourceModel().data(right)

        if leftData is None or rightData is None:
            return True
        return leftData < rightData


class ArticleViewer(QtWidgets.QWidget):
    def __init__(self):
        super(ArticleViewer, self).__init__()

        self.proxyModel = MySortFilterProxyModel()

        # When you want to sort immediately after editing
        self.proxyModel.setDynamicSortFilter(True)

        ################################################################################################################
        # Setting the main course
        self.proxyView = QtWidgets.QTreeView()

        # The "Shift, Ctrl select" mode
        self.proxyView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)
        self.proxyView.sortByColumn(1, QtCore.Qt.AscendingOrder)

        # Connect selected signal to a slot, must after `.setModel(xxx)`
        self.proxyView.selectionModel().selectionChanged.connect(self.onSelectTreeItems)
        self.proxyView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.proxyView.setItemsExpandable(False)
        self.proxyView.setWordWrap(True)

        self.proxyView.clicked.connect(self.onSelectionClicked)

        # header issues
        headerView = self.proxyView.header()
        headerView.setSectionsMovable(True)
        # headerView.setFirstSectionMovable(False)
        headerView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        headerView.customContextMenuRequested.connect(self.headerRightClicked)
        headerView.sectionResized.connect(self.saveHeaderState)
        headerView.sectionMoved.connect(self.saveHeaderState)

        self.resHeaderMenu = QtWidgets.QMenu(self)

        proxyLayout = QtWidgets.QGridLayout()
        proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)

        self.setLayout(proxyLayout)

        self.setWindowTitle("Custom Sort/Filter Model")
        self.resize(500, 450)

    def getSelectedItemUids(self):
        visibleHeaderCount = self.proxyView.header().count() - \
                             self.proxyView.header().hiddenSectionCount()
        selectedIdx = self.proxyView.selectedIndexes()
        if len(selectedIdx) == 0 or len(selectedIdx) % visibleHeaderCount > 0:
            return None
        print("=" * 32, "\nSelected Indexes to for uid: from (%d, %d) to (%d, %d)" %
              (selectedIdx[0].row(), selectedIdx[0].column(), selectedIdx[-1].row(), selectedIdx[-1].column()))
        uids = []
        for enRow in range(len(selectedIdx) // visibleHeaderCount):
            idx = selectedIdx[enRow * visibleHeaderCount]
            uidIndex = self.proxyModel.index(idx.row(), 0, idx.parent())
            uid = uidIndex.data()
            uids.append(uid)
        return uids

    # hide/show onRightClickHeader
    @pyqtSlot(bool)
    def resHeaderMenuTriggered(self, tf):
        print('resHeaderMenuTriggered', tf)
        for i, actn in enumerate(self.resHeaderMenu.actions()):
            if not actn.isChecked():
                self.proxyView.header().setSectionHidden(i, True)
            else:
                self.proxyView.header().setSectionHidden(i, False)

            # print("hidden: ", self.proxyView.header().isSectionHidden(i), "index: ", i,
            #       "Visual index: ", self.proxyView.header().visualIndex(i))

    # hide/show onRightClickHeader
    @pyqtSlot(QtCore.QPoint)
    def headerRightClicked(self, QPos):
        parentPosition = self.proxyView.mapToGlobal(QtCore.QPoint(0, 0))
        menuPosition = parentPosition + QPos
        self.resHeaderMenu.move(menuPosition)
        self.resHeaderMenu.show()

    @pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    def onSelectTreeItems(self, newSelection, oldSelection):
        """Purely test"""
        # self.proxyModel.setDynamicSortFilter(True)
        if len(newSelection) < 1:
            return
        print("\n----------------------------\nnew: ", newSelection, "\nold:", oldSelection)
        print("len new: ", len(newSelection), " len old", len(oldSelection))
        # print(self.proxyView.selectedIndexes())
        print(len(self.proxyView.selectedIndexes()))
        #
        # indice=newSelection
        # # print(indice[0].left(),indice[0].right(),indice[0].top(),indice[0].bottom())

        idx = self.proxyView.selectedIndexes()
        idx2 = self.proxyView.currentIndex()
        print("data: ", self.proxyView.model().data(idx2))
        print("proxy column count: %d  row count: %d" % (self.proxyModel.columnCount(), self.proxyModel.rowCount()))
        print("sourc column count: %d  row count: %d" % (self.proxyModel.sourceModel().columnCount(),
                                                         self.proxyModel.sourceModel().rowCount()))
        print("Index of clicked: ", idx2.row(), idx2.column())
        print("Column width: ", self.proxyView.columnWidth(idx2.column()))

        # self.proxyModel.createIndex(1,1,"1")

        # self.proxyModel.sourceModel().data()

        # self.proxyView.setColumnWidth(1,129)
        # self.proxyView.showColumn(1)
        # self.proxyView.model().setData(idx[1], "aa"+self.proxyView.model().data(idx[1]))
        # self.proxyModel.setDynamicSortFilter(True)

    @pyqtSlot(QtCore.QModelIndex)
    def onSelectionClicked(self, idx):
        return
        print("hello")
        print("column count: %d  row count: %d" %
              (self.proxyModel.sourceModel().columnCount(), self.proxyModel.sourceModel().rowCount()))
        print("Index of clicked: ", idx.row(), idx.column())

        # # select programmatically
        # selection = self.proxyView.selectionModel()
        # selection.select(self.proxyView.model().index(2, 0),
        #                  QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)

    def setSourceModel(self, model):
        model.hdv = self.proxyView.header()
        self.proxyModel.setSourceModel(model)

    def setDefaultHeaderView(self):
        """Set default header"""
        for column in range(self.proxyView.model().columnCount()):
            columnName = self.proxyView.model().headerData(column, QtCore.Qt.Horizontal)
            actn = QtWidgets.QAction('%s' % columnName, self.resHeaderMenu, checkable=True)
            actn.setChecked(True)
            actn.triggered.connect(self.resHeaderMenuTriggered)
            self.resHeaderMenu.addAction(actn)
            # print(columnName)

        # uid always invisible
        self.resHeaderMenu.actions()[0].setEnabled(False)

        toUncheck = [0, 8]
        for i in toUncheck:
            self.resHeaderMenu.actions()[i].setChecked(False)
            self.proxyView.header().setSectionHidden(i, True)

        # self.saveHeaderState()

    @pyqtSlot()
    def saveHeaderState(self):
        """When state changes, save it"""
        # print("- Save header")
        self.proxyModel.sourceModel().ADB.headerViewState = self.proxyView.header().saveState()

    @pyqtSlot()
    def loadHeaderState(self):
        if self.proxyModel.sourceModel().ADB.headerViewState:
            header = self.proxyView.header()
            header.restoreState(self.proxyModel.sourceModel().ADB.headerViewState)
            for i in range(header.count()):
                if header.isSectionHidden(i):
                    self.resHeaderMenu.actions()[i].setChecked(False)
            return True

        print("Load from source failed")
        return False

    @pyqtSlot()
    def onClickExpandRows(self):
        uids = self.getSelectedItemUids()
        if uids is None:
            return
        for uid in uids:
            self.proxyModel.sourceModel().expandedItemUids.add(uid)
            self.proxyModel.sourceModel().emitItemChangedByUid(uid)

        # for i in self.proxyModel.sourceModel().expandedItemUids:
        #     print(i, sep="\t")

    @pyqtSlot()
    def onClickCollapseRows(self):
        uids = self.getSelectedItemUids()
        if uids is None:
            return
        for uid in uids:
            if uid in self.proxyModel.sourceModel().expandedItemUids:
                self.proxyModel.sourceModel().expandedItemUids.remove(uid)
                self.proxyModel.sourceModel().emitItemChangedByUid(uid)



if __name__ == "__main__":
    import sys

    # app = QtWidgets.QApplication(sys.argv)
    #
    # window = ArticleViewer()
    # window.setSourceModel(createMailModel(window))
    # window.show()
    #
    # sys.exit(app.exec_())
