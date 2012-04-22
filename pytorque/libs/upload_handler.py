# -*- coding: utf-8 -*-
import os

__author__ = 'rauch'


class UploadHandler():
    @staticmethod
    def handle(destinationPath, file):
        destination = open(os.path.join(destinationPath, file.name), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()