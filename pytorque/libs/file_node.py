# -*- coding: utf-8 -*-
import os
import jsonpickle
import time
from hurry import filesize

__author__ = 'rauch'

class Metadata():
    id = None
    rel = None
    size = None
    modifiedDate = None

    def __init__(self, id):
        self.id = id


class FileNode():
    __kilo = 1024
    __datetime_format = "%d-%m-%Y  %H:%M"
    children = []
    _fullName = None
    attr = None
    state = None
    data = None
    _isDirectory = False

    def __init__(self, fullName, parent=None):
        self._fullName = os.path.abspath(fullName)
        self.attr = Metadata(self._fullName)
        self.attr.dateModified = time.strftime(self.__datetime_format, time.gmtime(os.path.getmtime(fullName)))

        self.data = os.path.basename(self._fullName)
        self._isDirectory = os.path.isdir(fullName)
        if self._isDirectory:
            self.state = "closed"
            self.attr.rel = "folder"
            self.attr.size = filesize.size(FileNode.getsize(self._fullName))
        else:
            self.attr.rel = "file"
            self.attr.size = filesize.size(os.path.getsize(self._fullName))
        self.children = []

    def getFullName(self):
        return self._fullName

    def getShortName(self):
        return self.data

    def addChild(self, child):
        self.children.append(child)

    def isDirectory(self):
        return self._isDirectory

    def setIsDirectory(self, isDirectory):
        self._isDirectory = isDirectory

    def hasChildren(self):
        return not(self.children is None) and len(self.children) > 0

    def getChildren(self):
        return self.children

    @staticmethod
    def getsize(start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    currentFileSize = os.path.getsize(fp)
                except OSError:
                    currentFileSize = 0
                total_size += currentFileSize
        return total_size


    @staticmethod
    def _listdir_nohidden(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                yield f

    @staticmethod
    def createDirectoryNode(fullDirName):
        currentFileNode = FileNode(fullDirName)

        for currentFileName in FileNode._listdir_nohidden(fullDirName):
            currentNode = FileNode(os.path.join(fullDirName, currentFileName), currentFileNode)
            currentFileNode.addChild(currentNode)

        return currentFileNode


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

if __name__ == "__main__":
    fileNode = FileNode.createDirectoryNode("/home/rauch/Diploma")

    print(time.strftime("%d-%m-%Y %M:%H", time.gmtime(os.path.getmtime("/home/rauch/Diploma"))))

    print(jsonpickle.encode(fileNode, unpicklable=False))

    resultJSON = {
        "Result": "OK",#ERROR could be here -> Message
        "Records": [
                {"JobId": 1, "Name": "Benjamin Button", "State": 17, "SubmitDate": "/Date(1320259705710)/"},
                {"JobId": 2, "Name": "Douglas Adams", "State": 42, "SubmitDate": "/Date(1320259705710)/"},
                {"JobId": 3, "Name": "Isaac Asimov", "State": 26, "SubmitDate": "/Date(1320259705710)/"},
                {"JobId": 4, "Name": "Thomas More", "State": 65, "SubmitDate": "/Date(1320259705710)/"}
        ]
    }
    print(jsonpickle.encode(resultJSON))
