from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .manage_user_routes.manage_routes import MangaeRoutes
from .route_handler.handle_routes import HandleRoutes
from .utils.express import set_host__name,check_port_open
from .utils import styles

# < -- user defind routes add and manage -- >
UserRoutes = MangaeRoutes()

# < -- route request handler -- >
routesHandler = HandleRoutes()

class MyRequestHandler(BaseHTTPRequestHandler):
    # < -- client get request recived  -- >
    def do_GET(self):
        # < -- handle get request by routesHandler Object -- >
        routesHandler.handle_get_request(self,UserRoutes)
      
    # < -- client post request recived  -- >
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        print(self.rfile.read(length).decode("utf-8"))

    # < -- default server log -- >
    def log_message(self, format, *args):
        # Suppress log messages
        pass
    
    # < -- handle anknown error -- >
    def handle_error(self, request, client_address):
        pass

    # < -- set header of Server String  Ex:- Server: Express/Python -- >
    def version_string(self): return 'Express/Python'


class Server():
    def __init__(self, port=3000, host="localhost",listenerHandler=None):
        # < -- init -- >
        self.port = port
        self.host = host
        self.running_host = set_host__name(host)
        self._handle_port_open()
        
        # < -- if user not added any callback for server listener then added custom listener  -- >
        self.listenerHandler = self.DefaultListenerHandler if listenerHandler is None else listenerHandler
        
    # < -- default listener -- >
    def DefaultListenerHandler(self,error):
        # if not error server is running 
        if(not error):
            # server running sucess green msg 
            server_running_success = (f"Server Running At http://{self.running_host}:{self.port}")
            styles.greenText(server_running_success)

    # < -- start server -- >
    def start(self):
        # < -- client host and port -- >
        server_address = (self.host, self.port)

        
        # < -- build http threading server  -- >
        try:
            httpd = ThreadingHTTPServer(server_address, MyRequestHandler)
            
            # handle server listen 
            self.listenerHandler(None)

            httpd.serve_forever()
        except Exception as error:
            self.listenerHandler(error)
        except KeyboardInterrupt:
                print('\nServer is shutting down...')
                httpd.server_close()
    
    # < -- handle port related errors -- >
    def _handle_port_open(self):
        if (check_port_open(self.running_host,self.port)):
            # < -- custom port open error -- >
            error_message = f"Error:Address Already In use http://{self.running_host}:{self.port}"
            # < -- if port alrady open then show error -- >
            styles.redText(error_message)
            exit(0)
