import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtCore import pyqtSignal, pyqtSlot

import re
import sys

from mytreeview import MySortFilterProxyModel, ArticleViewer, SourceArticleDBModel
from comparator import ComparatorTableModel, ComparatorViewer, Comparator
from article import *


class EditTabPageWidget(QtWidgets.QWidget):
    """The tab of addtab2()"""

    def __init__(self, entry=ArticleEntry(-1)):
        super(EditTabPageWidget, self).__init__()

        self.tempArticle = entry
        topFiller = QWidget()
        topFiller.setMaximumWidth(900)  # Max width

        layout = QGridLayout(topFiller)
        # ##############################################################################################################
        # Domain labels
        # qlabel_uid = QLabel('uid')
        qlabel_title = QLabel('title')
        qlabel_nickname = QLabel('nickname')
        qlabel_year = QLabel('year')
        qlabel_venue = QLabel('venue')
        qlabel_authors = QLabel('authors')
        qlabel_tags = QLabel('tags')
        # qlabel_createTime = QLabel('createTime')
        # qlabel_lastReadTime = QLabel('lastReadTime')
        # qlabel_lastModTime = QLabel('lastModTime')
        qlabel_background = QLabel('background')
        qlabel_pastWork = QLabel('pastWork')
        qlabel_gap = QLabel('gap')
        qlabel_contribution = QLabel('contribution')
        qlabel_mainMethod = QLabel('mainMethod')
        qlabel_overview = QLabel('Overview')
        qlabel_myFocus = QLabel('myFocus')
        qlabel_doubts = QLabel('doubts')
        qlabel_miscellaneous = QLabel('miscellaneous')

        qlabel_year.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        qlabel_venue.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        # ##############################################################################################################
        # Their widgets:
        # qLine_uid = QLineEdit()
        self.qLine_title = QLineEdit()
        self.qLine_nickname = QLineEdit()
        self.qSpin_year = QSpinBox()
        self.qSpin_year.setMaximumWidth(100)
        self.qLine_venue = QLineEdit()
        self.qLine_authors = QLineEdit()
        self.qLine_tags = QLineEdit()

        self.qText_overview = QPlainTextEdit()
        self.qText_background = QPlainTextEdit()
        self.qText_pastWork = QPlainTextEdit()
        self.qText_gap = QPlainTextEdit()
        self.qText_contribution = QPlainTextEdit()
        self.qText_mainMethod = QPlainTextEdit()
        self.qText_myFocus = QPlainTextEdit()
        self.qText_doubts = QPlainTextEdit()
        self.qText_miscellaneous = QPlainTextEdit()

        # ##############################################################################################################
        # Layouts
        # layout.addWidget()
        qlabel_title.setBuddy(self.qLine_title)
        layout.addWidget(qlabel_title, 0, 0, 1, 1)
        layout.addWidget(self.qLine_title, 0, 1, 1, 7)

        qlabel_nickname.setBuddy(self.qLine_nickname)
        layout.addWidget(qlabel_nickname, 1, 0, 1, 1)
        layout.addWidget(self.qLine_nickname, 1, 1, 1, 2)

        qlabel_venue.setBuddy(self.qLine_venue)
        layout.addWidget(qlabel_venue, 1, 3, 1, 1)
        layout.addWidget(self.qLine_venue, 1, 4, 1, 2)

        qlabel_year.setBuddy(self.qSpin_year)
        layout.addWidget(qlabel_year, 1, 6, 1, 1)
        layout.addWidget(self.qSpin_year, 1, 7, 1, 1)
        self.qSpin_year.setRange(1950, 2050)
        self.qSpin_year.setValue(datetime.datetime.utcnow().year)

        qlabel_authors.setBuddy(self.qLine_authors)
        layout.addWidget(qlabel_authors, 2, 0, 1, 1)
        layout.addWidget(self.qLine_authors, 2, 1, 1, 7)
        self.qLine_authors.setPlaceholderText("\";\" separated")

        qlabel_tags.setBuddy(self.qLine_tags)
        layout.addWidget(qlabel_tags, 3, 0, 1, 1)
        layout.addWidget(self.qLine_tags, 3, 1, 1, 7)
        self.qLine_tags.setPlaceholderText("\";\" separated")

        qlabel_overview.setBuddy(self.qText_overview)
        self.qText_overview.setTabChangesFocus(True)
        layout.addWidget(qlabel_overview, 4, 0, 1, 1)
        layout.addWidget(self.qText_overview, 4, 1, 1, 7)
        self.qText_overview.setMaximumHeight(240)

        qlabel_background.setBuddy(self.qText_background)
        self.qText_background.setTabChangesFocus(True)
        layout.addWidget(qlabel_background, 5, 0, 1, 1)
        layout.addWidget(self.qText_background, 5, 1, 1, 7)
        self.qText_background.setMaximumHeight(60)

        qlabel_pastWork.setBuddy(self.qText_pastWork)
        self.qText_pastWork.setTabChangesFocus(True)
        layout.addWidget(qlabel_pastWork, 6, 0, 1, 1)
        layout.addWidget(self.qText_pastWork, 6, 1, 1, 7)
        self.qText_pastWork.setMaximumHeight(60)

        qlabel_gap.setBuddy(self.qText_gap)
        self.qText_gap.setTabChangesFocus(True)
        layout.addWidget(qlabel_gap, 8, 0, 1, 1)
        layout.addWidget(self.qText_gap, 8, 1, 1, 7)
        self.qText_gap.setMaximumHeight(240)

        qlabel_contribution.setBuddy(self.qText_contribution)
        self.qText_contribution.setTabChangesFocus(True)
        layout.addWidget(qlabel_contribution, 10, 0, 1, 1)
        layout.addWidget(self.qText_contribution, 10, 1, 1, 7)
        self.qText_contribution.setMaximumHeight(240)

        qlabel_mainMethod.setBuddy(self.qText_mainMethod)
        self.qText_mainMethod.setTabChangesFocus(True)
        layout.addWidget(qlabel_mainMethod, 12, 0, 1, 1)
        layout.addWidget(self.qText_mainMethod, 12, 1, 1, 7)
        self.qText_mainMethod.setMaximumHeight(240)

        qlabel_myFocus.setBuddy(self.qText_myFocus)
        self.qText_myFocus.setTabChangesFocus(True)
        layout.addWidget(qlabel_myFocus, 16, 0, 1, 1)
        layout.addWidget(self.qText_myFocus, 16, 1, 1, 7)
        self.qText_myFocus.setMaximumHeight(240)

        qlabel_doubts.setBuddy(self.qText_doubts)
        self.qText_doubts.setTabChangesFocus(True)
        layout.addWidget(qlabel_doubts, 18, 0, 1, 1)
        layout.addWidget(self.qText_doubts, 18, 1, 1, 7)
        self.qText_doubts.setMaximumHeight(240)

        qlabel_miscellaneous.setBuddy(self.qText_miscellaneous)
        self.qText_miscellaneous.setTabChangesFocus(True)
        layout.addWidget(qlabel_miscellaneous, 20, 0, 1, 1)
        layout.addWidget(self.qText_miscellaneous, 20, 1, 1, 7)
        self.qText_miscellaneous.setMaximumHeight(240)

        # ##############################################################################################################

        # layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        buttonLineFiller = QWidget()
        # layout.addWidget(buttonLineFiller, 8, 0, 1, 3)
        buttonLineLayout = QHBoxLayout(buttonLineFiller)
        # buttonLineLayout.setAlignment(QtCore.Qt.AlignRight)
        # buttonLineLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.btnSave = QPushButton("Save")
        self.btnCancel = QPushButton("Cancel")
        self.btnClose = QPushButton("Close")
        buttonLineLayout.addWidget(self.btnSave)
        buttonLineLayout.addWidget(self.btnCancel)
        buttonLineLayout.addWidget(self.btnClose)

        layout.addWidget(buttonLineFiller, 22, 4, 1, 4)

        scroll = QScrollArea()
        scroll.setWidget(topFiller)
        scroll.setWidgetResizable(True)
        scroll.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)  # set the topFiller's pose in the Area

        vbox = QVBoxLayout()
        vbox.addWidget(scroll)

        self.setLayout(vbox)
        self.setDisplayData()

    def setDisplayData(self):
        if self.tempArticle.uid < 0:
            return

        self.qLine_title.setText(self.tempArticle.title)
        self.qLine_nickname.setText(self.tempArticle.nickname)
        self.qSpin_year.setValue(self.tempArticle.year)
        self.qLine_venue.setText(self.tempArticle.venue)
        self.qLine_authors.setText("; ".join(self.tempArticle.authors))
        self.qLine_tags.setText("; ".join(self.tempArticle.tags))

        self.qText_background.setPlainText(self.tempArticle.background)
        self.qText_pastWork.setPlainText(self.tempArticle.pastWork)
        self.qText_gap.setPlainText(self.tempArticle.gap)
        self.qText_contribution.setPlainText(self.tempArticle.contribution)
        self.qText_mainMethod.setPlainText(self.tempArticle.mainMethod)
        self.qText_overview.setPlainText(self.tempArticle.overview)
        self.qText_myFocus.setPlainText(self.tempArticle.myFocus)
        self.qText_doubts.setPlainText(self.tempArticle.doubts)
        self.qText_miscellaneous.setPlainText(self.tempArticle.miscellaneous)

    def setTitle(self):
        self.tempArticle.title = self.qLine_title.text()

    def setNickname(self):
        self.tempArticle.nickname = self.qLine_nickname.text()

    def setYear(self):
        self.tempArticle.year = self.qSpin_year.value()

    def setVenue(self):
        self.tempArticle.venue = self.qLine_venue.text()

    def setAuthors(self):
        a = self.qLine_authors.text().strip()
        b = re.split("\s*;\s*", a)
        temp = []
        for i in b:
            if i:
                temp.append(i)
        self.tempArticle.authors = temp

    def setTags(self):
        a = self.qLine_tags.text().strip()
        b = re.split("\s*;\s*", a)
        temp = []
        for i in b:
            if i:
                print("TAG")
                temp.append(i)
        self.tempArticle.tags = temp

    def setBackground(self):
        self.tempArticle.background = str(self.qText_background.toPlainText())

    def setPastwork(self):
        self.tempArticle.pastWork = str(self.qText_pastWork.toPlainText())

    def setGap(self):
        self.tempArticle.gap = str(self.qText_gap.toPlainText())

    def setContribution(self):
        self.tempArticle.contribution = str(self.qText_contribution.toPlainText())

    def setMainmethod(self):
        self.tempArticle.mainMethod = str(self.qText_mainMethod.toPlainText())

    def setOverview(self):
        self.tempArticle.overview = str(self.qText_overview.toPlainText())

    def setMyfocus(self):
        self.tempArticle.myFocus = str(self.qText_myFocus.toPlainText())

    def setDoubts(self):
        self.tempArticle.doubts = str(self.qText_doubts.toPlainText())

    def setMiscellaneous(self):
        self.tempArticle.miscellaneous = str(self.qText_miscellaneous.toPlainText())


class ComparatorTabPageWidget(QtWidgets.QWidget):
    """The tab of addtab1"""

    def __init__(self):
        super(ComparatorTabPageWidget, self).__init__()

        hbox = QHBoxLayout()
        gbox = QGridLayout()

        # Deal with the side bar
        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.StyledPanel)
        leftFrame.setMinimumSize(200, 600)
        leftFrame.setMaximumWidth(300)  # Max width
        leftFrame.setLayout(gbox)

        compNameLabel = QtWidgets.QLabel("&Comparator Name:")
        self.compNameLineEdit = QtWidgets.QLineEdit()
        self.compNameLineEdit.setMaxLength(32)
        compNameLabel.setBuddy(self.compNameLineEdit)
        gbox.addWidget(compNameLabel, 0, 0, 1, 2)
        gbox.addWidget(self.compNameLineEdit, 1, 0, 1, 2)

        compCommentLabel = QtWidgets.QLabel("My Comment:")
        self.compCommentText = QPlainTextEdit()
        self.compCommentText.setTabChangesFocus(True)
        compNameLabel.setBuddy(self.compCommentText)
        gbox.addWidget(compCommentLabel, 2, 0, 1, 2)
        gbox.addWidget(self.compCommentText, 3, 0, 1, 2)

        groupFilter = QGroupBox("Entry Filter", leftFrame)
        groupFilter.setMaximumHeight(250)
        groupGridLayout = QGridLayout()
        groupFilter.setLayout(groupGridLayout)
        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox("Case sensitive")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.filterSyntaxCheckBox = QtWidgets.QCheckBox("Use Regex")
        self.filterSyntaxCheckBox.setChecked(True)
        self.filterPatternLineEdit = QtWidgets.QLineEdit()

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
        gbox.addWidget(groupFilter, 4, 0, 1, 2)

        self.btnRemove = QPushButton("Remove from comparator")
        self.btnExpandSelected = QPushButton("Expand")
        self.btnCollapseSelected = QPushButton("Collapse")
        self.btnMoveUp = QPushButton("Move up")
        self.btnMoveDown = QPushButton("Move Down")
        self.btnSave = QPushButton("Save")
        self.btnCancel = QPushButton("Cancel")

        gbox.addWidget(self.btnRemove, 5, 0, 1, 2)
        gbox.addWidget(self.btnExpandSelected, 6, 0, 1, 1)
        gbox.addWidget(self.btnCollapseSelected, 6, 1, 1, 1)
        gbox.addWidget(self.btnMoveUp, 8, 0, 1, 1)
        gbox.addWidget(self.btnMoveDown, 8, 1, 1, 1)
        gbox.addWidget(self.btnSave, 9, 0, 1, 1)
        gbox.addWidget(self.btnCancel, 9, 1, 1, 1)

        # deal with the main tree view
        # TODO: think about reset data/load data
        self.qCompViewer = ArticleViewer()
        self.comp = Comparator()
        self.originalComp = None
        srcModel = SourceArticleDBModel(self.comp)
        self.qCompViewer.setSourceModel(srcModel)
        self.qCompViewer.setDefaultHeaderView()
        self.qCompViewer.proxyModel.setDynamicSortFilter(False)

        # finally the splitter
        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(leftFrame)
        splitter1.addWidget(self.qCompViewer)
        splitter1.setSizes([100, 200])

        hbox.addWidget(splitter1)

        self.setLayout(hbox)

        self.filterPatternLineEdit.textChanged.connect(self.textFilterChanged)
        self.filterSyntaxCheckBox.toggled.connect(self.textFilterChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.textFilterChanged)

        self.btnExpandSelected.clicked.connect(self.qCompViewer.onClickExpandRows)
        self.btnCollapseSelected.clicked.connect(self.qCompViewer.onClickCollapseRows)
        self.btnRemove.clicked.connect(self.onClicked_RemoveFromComparator)
        # self.btnMoveUp.clicked.connect(self.onClicked_MoveUp)  # FIXME

    def setComparatorToShow(self, cp):
        if cp:
            self.comp = Comparator()  # The one to be modified
            self.originalComp = cp  # The pointer to the original Comparator
            self.comp.updateFromGiven(cp)

            srcModel = SourceArticleDBModel(self.comp)

            self.qCompViewer.setSourceModel(srcModel)
            self.qCompViewer.loadHeaderState()

            self.compNameLineEdit.setText(self.comp.name)
            self.compCommentText.setPlainText(self.comp.comment)

    def textFilterDomainChanged(self):
        nd = self.filterDomainCombo.itemData(self.filterDomainCombo.currentIndex())
        self.qCompViewer.proxyModel.setFilterDomains(nd)
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
        self.qCompViewer.proxyModel.setFilterRegExp(regExp)

    # @pyqtSlot()
    # def onClicked_MoveUp(self):
    #     indexes = self.qCompViewer.proxyView.selectedIndexes()
    #     rowsToMove = set()
    #     for idx in indexes:
    #         rowsToMove.add(idx.row())
    #     itemIndexes = sorted(list(rowsToMove))
    #     for no, itemIndex in enumerate(itemIndexes):
    #         if itemIndex == 0:
    #             continue
    #         if no == 0 or itemIndexes[no - 1] < itemIndex - 1:
    #             dest = itemIndex - 1
    #         else:
    #             dest = itemIndex
    #         self.qCompViewer.proxyModel.beginMoveRows(QtCore.QModelIndex(), itemIndex, itemIndex,
    #                                                   QtCore.QModelIndex(), dest)
    #         self.qCompViewer.proxyModel.moveRow(QtCore.QModelIndex(), itemIndex, QtCore.QModelIndex(), dest)
    #         self.qCompViewer.proxyModel.endMoveRows()

    @pyqtSlot()
    def onClicked_RemoveFromComparator(self):
        uids = self.qCompViewer.getSelectedItemUids()
        if uids:
            self.qCompViewer.proxyView.clearSelection()
            for uid in uids:
                srcRow = self.qCompViewer.proxyModel.sourceModel().ADB.uidList.index(uid)
                self.qCompViewer.proxyModel.sourceModel().removeItem(srcRow)
        return
