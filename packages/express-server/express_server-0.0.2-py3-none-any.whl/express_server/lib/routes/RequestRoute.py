from urllib.parse import urlparse,parse_qs

class RequestRoute:
    def __init__(self,method,request):
        self.request = request
        self.path = request.path.replace("%20"," ")
        self.url = self.originalUrl = self.pathname = self.href = self._raw  = urlparse(self.path).path
        (host, port) = self.request.server.server_address
        self.server_url = f"http://{host}:{port}"
        self.server_full_url = f"http://{host}:{port}"+self.path
        self.method = method
        self._write_row_header(request)
        self._find_query_fragment(self.server_full_url)
        self.ip = request.client_address[0]
        self.user_port = request.client_address[1]
        
        self.headers = []
        self.rawHeaders = []
        self.query: {}
        # this is for /:kjsd like this url 
        self.params: {}
        # post body
        self.body = {}
        # cookie
        self.cookies = []
        cookies = request.headers.get("Cookie")

        # set cookies
        if cookies: self.cookies = [cookie.split("=") for cookie in cookies.split('; ')]

    def get(self,key):
        try:
            for headerKey, value in self.request.headers.items():
                if(headerKey == key):
                    return value
        except:
            pass
        return None
    
    def getCookie(self,key):
        try:
            for cookieKey, value in self.cookies:
                if(cookieKey == key):
                    return value
        except:
            pass
        return None
    
    def _write_row_header(self,request):
        try:
           self.headers = [{key, value} for key, value in request.headers.items()]
           for key, value in request.headers.items():
               self.rawHeaders.extend([key,value])
        except:
            pass

    def find_qeury(self,query):
        for sotredQuery in self.query:
            if(sotredQuery == query):
                return self.query[sotredQuery]
        return None
    
    def _find_query_fragment(self,url):
        parsed_url = urlparse(url)
        self.query = {key: value[0] for key, value in parse_qs(parsed_url.query).items()}

        # set fragment like :- #home
        self.fragment = parsed_url.fragment