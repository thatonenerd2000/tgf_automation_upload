import urllib.request

class imageScrapper:
    def __init__(self,url,fileName,saveFolder):
        self.url = url
        self.fileName = fileName
        self.saveFolder = saveFolder
        self.fullPath = saveFolder + fileName + ".jpg"

    def saveImage(self):
        urllib.request.urlretrieve(self.url, self.fullPath)