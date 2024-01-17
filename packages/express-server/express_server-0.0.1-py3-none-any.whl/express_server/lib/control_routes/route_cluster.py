class RouteCluster:
    def __init__(self,data):
        self.path = data["path"]
        self.method = data["method"]
        self.AllHandlers = [data["handlers"]]
        self.text = ''
        self.headers = []

    def addHandlers(self,newHandler):
        self.AllHandlers.append(newHandler)