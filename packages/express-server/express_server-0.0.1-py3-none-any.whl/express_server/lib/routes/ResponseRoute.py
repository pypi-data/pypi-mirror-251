class ResponseRoute:
    def __init__(self):
        self.text = ''
        self.sendfilepath = None
        self.headers = []

    def setHeader(self,key,value):
        self.headers.append((key,value))
    
    def setCookie(self,key,value):
        pass

    def send(self,text = ""):
        self.text = text
        return "end"
    
    def sendfile(self,filename):
        self.sendfilepath = filename
        return "end"
    
    def next(self):
        return "next"