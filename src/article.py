import time
# from datetime import datetime
import datetime
import copy
from enum import Enum

headerNames = ['uid',
               'title',
               'nickname',
               'year',
               'venue',
               'authors',
               'tags',
               'createTime',
               'lastReadTime',
               'lastModTime',
               'overview',
               'background',
               'pastWork',
               'gap',
               'contribution',
               'mainMethod',
               'myFocus',
               'doubts',
               'miscellaneous']

searchableDomainIndex = [1, 2, 5, 6, 10, 11, 12, 13, 14, 15, 16, 17, 18]

headerDefaultOrder = []


class ReadingProgess(Enum):
    FRESH = 0  # Just added 0-14
    QUEUED = 1  # manually set. once set, restart queued for 14
    READ = 2  # finished reading 0-14
    ARCHIVED = 3  # finished reading 15+
    HOLD = 4  # manually set. once set, restart hold for 14
    STALE = 6  # Just added 15+, or HOLD expired and not refreshed


class ArticleEntry:
    def __init__(self, uid):
        self.parentItem = None
        # useful start
        self.uid = uid  # need a universal ID, will always rank 0th in domains, and will never be moved or shown.
        self._title = ''
        self._nickname = ''
        self._year = 0
        self._venue = ''
        self._authors = []

        self._tags = []
        self._createTime = datetime.datetime.utcnow()
        self._lastReadTime = self._createTime
        self._lastModTime = self._createTime

        self._overview = ''
        self._background = ''
        self._pastWork = ''
        self._gap = ''
        self._contribution = ''
        self._mainMethod = ''
        self._myFocus = ''
        self._doubts = ''
        self._miscellaneous = ''

        # # Needed: reading status,
        # self._last_status_set_time = []
        # self._status = []

    def at(self, i):
        if i == 0:
            return self.uid
        elif i == 1:
            return self._title
        elif i == 2:
            return self._nickname
        elif i == 3:
            return self._year
        elif i == 4:
            return self._venue
        elif i == 5:
            return self._authors
        elif i == 6:
            return self._tags
        elif i == 7:
            return self._createTime
        elif i == 8:
            return self._lastReadTime
        elif i == 9:
            return self._lastModTime
        elif i == 10:
            return self._overview
        elif i == 11:
            return self._background
        elif i == 12:
            return self._pastWork
        elif i == 13:
            return self._gap
        elif i == 14:
            return self._contribution
        elif i == 15:
            return self._mainMethod
        elif i == 16:
            return self._myFocus
        elif i == 17:
            return self._doubts
        elif i == 18:
            return self._miscellaneous

        return None
        # def countDownToStale(self):

    def set(self, i, val):
        if i == 0:
            self.uid = val
        elif i == 1:
            self.title = val
        elif i == 2:
            self.nickname = val
        elif i == 3:
            self.year = val
        elif i == 4:
            self.venue = val
        elif i == 5:
            self.authors = val
        elif i == 6:
            self.tags = val
        elif i == 7:
            self._createTime = val
        elif i == 8:
            self._lastReadTime = val
        elif i == 9:
            self._lastModTime = val
        elif i == 10:
            self.overview = val
        elif i == 11:
            self.background = val
        elif i == 12:
            self.pastWork = val
        elif i == 13:
            self.gap = val
        elif i == 14:
            self.contribution = val
        elif i == 15:
            self.mainMethod = val
        elif i == 16:
            self.myFocus = val
        elif i == 17:
            self.doubts = val
        elif i == 18:
            self.miscellaneous = val

    def modify(func):
        def setModTime(self, *args, **kwargs):
            self._lastModTime = datetime.datetime.utcnow()
            res = func(self, *args, **kwargs)
            return res

        return setModTime

    def test(self):
        print(self._createTime)

    @property
    def title(self):
        return self._title

    @title.setter
    @modify
    def title(self, value):
        self._title = value

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    @modify
    def nickname(self, value):
        self._nickname = value

    @property
    def year(self):
        return self._year

    @year.setter
    @modify
    def year(self, value):
        self._year = value

    @property
    def venue(self):
        return self._venue

    @venue.setter
    @modify
    def venue(self, value):
        self._venue = value

    @property
    def authors(self):
        return self._authors

    @authors.setter
    @modify
    def authors(self, value):
        self._authors = []
        for i, v in enumerate(value):
            self._authors.append(v)

    @property
    def overview(self):
        return self._overview

    @overview.setter
    @modify
    def overview(self, value):
        self._overview = value

    @property
    def background(self):
        return self._background

    @background.setter
    @modify
    def background(self, value):
        self._background = value

    @property
    def pastWork(self):
        return self._pastWork

    @pastWork.setter
    @modify
    def pastWork(self, value):
        self._pastWork = value

    @property
    def gap(self):
        return self._gap

    @gap.setter
    @modify
    def gap(self, value):
        self._gap = value

    @property
    def contribution(self):
        return self._contribution

    @contribution.setter
    @modify
    def contribution(self, value):
        self._contribution = value

    @property
    def mainMethod(self):
        return self._mainMethod

    @mainMethod.setter
    @modify
    def mainMethod(self, value):
        self._mainMethod = value

    @property
    def myFocus(self):
        return self._myFocus

    @myFocus.setter
    @modify
    def myFocus(self, value):
        self._myFocus = value

    @property
    def doubts(self):
        return self._doubts

    @doubts.setter
    @modify
    def doubts(self, value):
        self._doubts = value

    @property
    def miscellaneous(self):
        return self._miscellaneous

    @miscellaneous.setter
    @modify
    def miscellaneous(self, value):
        self._miscellaneous = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    @modify
    def tags(self, value):
        self._tags = []
        for i, v in enumerate(value):
            self._tags.append(v)

    @property
    def lastModTime(self):
        return self._lastModTime

    @property
    def lastReadTime(self):
        return self._lastReadTime

    # @property
    # def createTime(self):
    #     return self._createTime

    def setReadTime(self):
        self._lastReadTime = datetime.datetime.utcnow()


class ArticleDB:
    """Article database"""

    def __init__(self):
        self.tagDB = dict()
        self.authorDB = dict()
        # FIXME
        self.entries = dict()   # {uid: entry}
        self.uidList = []       # [uid, ..., ]

        # Not needed
        self.domainOrder = [i for i in range(len(headerNames))]  # negative for hidden
        self.columnWidths = [40 for i in headerNames]  # used for srcModel's sizehints

        self.headerViewState = None  # QHeaderView()'s state for

        self.createTime = datetime.datetime.utcnow()
        self.lastReadTime = self.createTime
        self.lastModTime = self.createTime

    def entryCount(self):
        return len(self.uidList)

    def modify(func):
        def setModTime(self, *args, **kwargs):
            self._lastModTime = datetime.datetime.utcnow()
            retval = func(self, *args, **kwargs)
            return retval

        return setModTime

    def getEntryByUid(self, uid):
        if uid in self.entries.keys():
            return self.entries[uid]
        return None

    def getEntryByRow(self, r):
        if 0 <= r < self.entryCount():
            return self.entries[self.uidList[r]]
        return None

    def getUidByRow(self, r):
        if 0 <= r < self.entryCount():
            return self.uidList[r]
        return None

    def getRowByUid(self, iid):
        if iid not in self.entries.keys():
            return None
        for i, uid in enumerate(self.uidList):
            if uid == iid:
                return i
        return None

    @modify
    def addEntry(self, articleEntry):
        if articleEntry.uid in self.entries.keys():
            print("Already exist")
            return False
        self.entries[articleEntry.uid] = articleEntry
        self.uidList.append(articleEntry.uid)
        for t in articleEntry.tags:
            if t in self.tagDB.keys():
                self.tagDB[t] += [articleEntry.uid]
            else:
                self.tagDB[t] = [articleEntry.uid]
        for t in articleEntry.authors:
            if t in self.authorDB.keys():
                self.authorDB[t] += [articleEntry.uid]
            else:
                self.authorDB[t] = [articleEntry.uid]
        return True

    @modify
    def removeEntry(self, uid):
        if uid not in self.entries.keys():
            print("uid not exist")
            return False
        articleEntry = self.entries[uid]
        # print("before remove: ", self.tagDB)
        for t in articleEntry.tags:
            self.tagDB[t].remove(uid)
            if len(self.tagDB[t]) == 0:
                del self.tagDB[t]
        for t in articleEntry.authors:
            self.authorDB[t].remove(uid)
            if len(self.authorDB[t]) == 0:
                del self.authorDB[t]
        # print("after remove: ", self.tagDB)
        del self.uidList[self.uidList.index(uid)]
        del self.entries[uid]
        return True



if __name__ == "__main__":
    a = ArticleEntry(-1)
    print(a)
