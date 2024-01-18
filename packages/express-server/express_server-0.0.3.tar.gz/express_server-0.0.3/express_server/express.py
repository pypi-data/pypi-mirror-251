from .lib.http_server import Server,UserRoutes
from .lib.utils.express import ServerListenerHandler

class express:
    # get request 
    def get(self,path,handlers):
        resData = {"path": path,"method": "GET","handlers": handlers}
        # add routes
        UserRoutes.AddNewRoute(resData)

    # get request 
    def post(self,path,handlers):
        resData = {"path": path,"method": "POST","handlers": handlers}
        # add routes
        UserRoutes.AddNewRoute(resData)

    # express.listen() handle listener
    def listen(self, port, *args):
        ServerListenerHandler(self, port, *args,Server=Server)