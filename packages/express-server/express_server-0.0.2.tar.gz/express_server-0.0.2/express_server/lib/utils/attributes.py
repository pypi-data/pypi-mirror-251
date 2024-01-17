import os
from ..utils.paths import path_normalizer
from ..utils.files_helper import write_file

class Attributes:
    def setHeader(self,request,headers=[]):
        isContentTypeAvailable = False
        for (key,value) in headers:
            request.send_header(key, value)
            if(key.lower() == "content-type"): isContentTypeAvailable = True
        
        if(not isContentTypeAvailable): request.send_header('Content-Type', 'text/html')

        # end headers 
        request.end_headers()

    # add text response to user 
    def addText(self,text,request):
            request.wfile.write(text.encode("utf-8"))

    def sendfile(self,filepath,request,method,chunk_size = 1024):
            try:
                file_full_path = filepath
                
                # check full path given or not if not so add cwd + path
                file_full_path = path_normalizer(filepath)

                # check path exist and path is correct
                if(not os.path.exists(file_full_path)):
                    request.wfile.write(f"{method} {file_full_path} Not Exists.".encode("utf-8"))
                    return
                    
                # write file in bytes 
                write_file(file_full_path,chunk_size,request)
            except Exception as error:
                    request.wfile.write(f"{error}".encode("utf-8"))