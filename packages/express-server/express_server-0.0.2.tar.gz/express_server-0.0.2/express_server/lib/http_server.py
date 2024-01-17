from http.server import BaseHTTPRequestHandler, HTTPServer
from .control_routes.control_routes import ControlRoutes
from .route_handler.handle_routes import HandleRoutes
from .utils.express import set_host__name,check_port_open
from socketserver import ThreadingMixIn

# all routes 
UserRoutes = ControlRoutes()
routesHandler = HandleRoutes()

class MyRequestHandler(BaseHTTPRequestHandler):
    # get request 
    def do_GET(self):
        routesHandler.handle_get_request(self,UserRoutes)
      
       
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        print(self.rfile.read(length).decode("utf-8"))

    # default server log
    def log_message(self, format, *args):
        # Suppress log messages
        pass
    def handle_error(self, request, client_address):
        pass
    def version_string(self): return 'Express/Python'


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Server():
    def __init__(self, port=3000, host="localhost",listenerHandler=None):
        self.port = port
        self.host = host
        self.running_host = set_host__name(host)
        self._handle_port_open()
        
        # if user not added any callback for server 
        self.listenerHandler = self.DefaultListenerHandler if listenerHandler is None else listenerHandler
        
    # default listener
    def DefaultListenerHandler(self,error):
        # if not error server is running 
        if(not error):
            # server running sucess green msg 
            server_running_success = (f"Server Running At http://{self.running_host}:{self.port}")
            print(f"\033[92m{server_running_success}\033[0m")

    def start(self):
        server_address = (self.host, self.port)
        try:
            httpd = ThreadedHTTPServer(server_address, MyRequestHandler)
            
            # handle server listen 
            self.listenerHandler(None)

            httpd.serve_forever()
        except Exception as error:
            self.listenerHandler(error)
        except KeyboardInterrupt:
                print('\nServer is shutting down...')
                httpd.server_close()
    
    def _handle_port_open(self):
        if (check_port_open(self.running_host,self.port)):
            error_message = f"Error:Address Already In use http://{self.running_host}:{self.port}"
            # red text error 
            print(f"\033[91m{error_message}\033[0m")
            exit(0)