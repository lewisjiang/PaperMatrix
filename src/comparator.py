from article import ArticleDB, ArticleEntry, headerNames
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, copy
import time
import pickle


class Comparator(ArticleDB):
    def __init__(self):
        super(Comparator, self).__init__()
        self.name = ""
        self.comment = ""
        self.pinned = False

    def updateFromGiven(self, adb):
        self.entries = copy.copy(adb.entries)
        self.uidList = copy.copy(adb.uidList)
        self.tagDB = copy.deepcopy(adb.tagDB)
        self.authorDB = copy.deepcopy(adb.authorDB)

        self.headerViewState = copy.copy(adb.headerViewState)
        self.createTime = adb.createTime
        self.lastReadTime = adb.lastReadTime
        self.lastModTime = datetime.datetime.utcnow()

        self.pinned = adb.pinned
        self.name = adb.name
        self.comment = adb.comment

    def setName(self, n):
        self.name = n
        self.lastModTime = datetime.datetime.utcnow()

    def setComment(self, s):
        self.comment = s
        self.lastModTime = datetime.datetime.utcnow()


class ComparatorTableModel(QtCore.QAbstractItemModel):
    """will be used in only one place: the main page comparator group
    """
    externalDataLoaded = QtCore.pyqtSignal(bool)

    def __init__(self):
        """have to save all the data together in ONE pickle"""
        super(ComparatorTableModel, self).__init__()
        self.compDB_pinned = []
        self.compDB_unpinned = []
        self.ADB = ArticleDB()  # the comparator containing all the entries

    def emitAllDataChanged(self):
        if self.rowCount() > 0:
            tl = self.index(0, 0)
            br = self.index(self.rowCount() - 1, 1)
            self.dataChanged.emit(tl, br, [])

    def pickleData(self, fpath):
        data = [self.compDB_pinned, self.compDB_unpinned, self.ADB]
        print("pickling: %d %d %d" % (len(self.compDB_pinned), len(self.compDB_unpinned), self.ADB.entryCount()))
        if self.ADB.entryCount() == 0:
            return False
        with open(fpath, 'wb') as f:
            pickle.dump(data, f)
        return True

    def unpickleData(self, fpath):
        data = None
        with open(fpath, 'rb') as f:
            data = pickle.load(f)
        if data and len(data) == 3:
            [self.compDB_pinned, self.compDB_unpinned, self.ADB] = data
            print("unpickling: %d %d %d" %
                  (len(self.compDB_pinned), len(self.compDB_unpinned), self.ADB.entryCount()))
            self.externalDataLoaded.emit(True)
            for r in range(self.rowCount()):
                self.insertRow(r, QtCore.QModelIndex())
            self.emitAllDataChanged()
            return True
        else:
            return False

    def rowCount(self, parent=None):
        return len(self.compDB_pinned) + len(self.compDB_unpinned)

    def columnCount(self, parent=None):
        return 2

    def parent(self, qindex=None):
        # if not qindex.isValid():
        return QtCore.QModelIndex()

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if row < len(self.compDB_pinned):
            return self.createIndex(row, column, self.compDB_pinned[row])
        elif row < len(self.compDB_pinned) + len(self.compDB_unpinned):
            r1 = row - len(self.compDB_pinned)
            return self.createIndex(row, column, self.compDB_unpinned[r1])
        return QtCore.QModelIndex()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if row < len(self.compDB_pinned):
                if col == 0:
                    return "+"
                return self.compDB_pinned[row].name
            elif row < len(self.compDB_pinned) + len(self.compDB_unpinned):
                r1 = row - len(self.compDB_pinned)
                if col == 0:
                    return ""
                return self.compDB_unpinned[r1].name
        return None

    # # Don't need a standard setData()
    # def setData(self, QModelIndex, Any, role=None):
    #     if role == QtCore.Qt.EditRole:
    #         print(QModelIndex)
    #         row = QModelIndex.row()
    #         col = QModelIndex.column()
    #         if col == 0:
    #             return
    #         self.rootItem.childItems[QModelIndex.row()].data[QModelIndex.column()] = Any
    #         self.dataChanged.emit(QModelIndex, QModelIndex, [])  # this signal also triggers rerun sizeHint.
    #         return True
    #
    #     return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, row, count, parent=None):
        self.beginInsertRows(parent, row, row)
        self.endInsertRows()
        return True

    def removeRows(self, pi, count, parent=None):
        self.beginRemoveRows(parent, pi, pi + count - 1)

        if 0 <= pi < len(self.compDB_pinned):
            del self.compDB_pinned[pi]
        elif len(self.compDB_pinned) <= pi < len(self.compDB_unpinned):
            del self.compDB_unpinned[pi - len(self.compDB_pinned)]

        self.endRemoveRows()

        return True

    def addComparator(self, comp):
        self.compDB_unpinned.append(comp)
        self.insertRow(self.rowCount(), QtCore.QModelIndex())
        self.compDB_unpinned.sort(key=lambda x: x.lastModTime, reverse=True)

        self.dataChanged.emit(self.index(len(self.compDB_pinned), 0), self.index(self.rowCount() - 1, 1))

    def removeComparator(self, pi):
        """pi: the row num in pinned"""
        self.removeRow(pi)

    def pinComp(self, pi):
        if pi < len(self.compDB_pinned):
            return False
        upi = pi - len(self.compDB_pinned)
        comp = self.compDB_unpinned[upi]
        del self.compDB_unpinned[upi]
        self.compDB_pinned.insert(0, comp)
        self.emitAllDataChanged()
        return True

    def unpinComp(self, pi):
        if pi >= len(self.compDB_pinned):
            return False
        pi = pi - len(self.compDB_pinned)
        comp = self.compDB_pinned[pi]
        del self.compDB_pinned[pi]
        self.compDB_unpinned.append(comp)
        self.compDB_unpinned.sort(key=lambda x: x.lastModTime, reverse=True)
        self.emitAllDataChanged()
        return True


class ComparatorViewer(QtWidgets.QWidget):
    def __init__(self, sourceModel):
        super(ComparatorViewer, self).__init__()
        # self.setMinimumSize(500, 500)

        self.view = QtWidgets.QTableView()
        self.view.setModel(sourceModel)
        self.view.verticalHeader().hide()
        self.view.horizontalHeader().hide()
        self.view.horizontalHeader().setStretchLastSection(True)

        self.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.view.setShowGrid(False)

        # self.view.setColumnWidth(0, 15)

        vheader = self.view.verticalHeader()
        vheader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        # print(vheader.minimumSectionSize())
        vheader.setMinimumSectionSize(20)
        vheader.setDefaultSectionSize(20)

        hheader = self.view.horizontalHeader()
        # hheader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        hheader.setMinimumSectionSize(20)
        self.view.setColumnWidth(0, 20)

        self.view.clicked.connect(self.onSelectionClicked)

        sourceLayout = QtWidgets.QHBoxLayout()
        sourceLayout.addWidget(self.view)
        self.setLayout(sourceLayout)

    def onSelectionClicked(self, idx):
        print("Index of clicked: ", idx.row(), idx.column())
        # r = idx.row()
        # pins = len(self.view.model().compDB_pinned)
        # if r < pins:
        #     cmp = self.view.model().compDB_pinned[r]
        #     for atc in cmp.uidList:
        #         print(cmp.entries[atc].title)
        #     self.view.model().unpinComp(idx.row())
        # else:
        #     cmp = self.view.model().compDB_unpinned[r - pins]
        #     for atc in cmp.uidList:
        #         print(cmp.entries[atc].title)
        #     self.view.model().pinComp(idx.row())

        # self.view.clearSelection()
        # self.view.verticalHeader().setDefaultSectionSize(9)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    model = ComparatorTableModel()

    for i in range(10):
        temp = Comparator()
        for j in range(i):
            temparticle = ArticleEntry(i * 100 + j)
            temparticle.title = "testing %d + %d" % (i, j)
            temp.addEntry(temparticle)
        # with open("aa%d.pkl"%i,'wb') as f:
        #     pickle.dump(temp, f)

        # with open("aa%d.pkl"%i,'rb') as f:
        #     temp = pickle.load(f)

        temp.setName("article %d" % i)
        model.addComparator(temp)
        # time.sleep(0.1)

    # with open("pinned.pkl",'wb') as f:
    #     pickle.dump(model.compDB_pinned,f)
    # with open("unpinned.pkl", 'wb') as f:
    #     pickle.dump(model.compDB_unpinned, f)

    # with open("pinned.pkl", 'rb') as f:
    #     model.compDB_pinned = pickle.load(f)
    # with open("unpinned.pkl", 'rb') as f:
    #     model.compDB_unpinned = pickle.load(f)

    view = ComparatorViewer(model)
    view.show()

    sys.exit(app.exec_())
