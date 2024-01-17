from ..utils.attributes import Attributes

# all atributes actions
attributes = Attributes()

class Pages:
    def Send(self,request,route,method):
        request.send_response(200)
        attributes.setHeader(request,route.headers)
        # time.sleep(1)

        # send a file 
        if(route.sendfilepath):
             attributes.sendfile(route.sendfilepath,request,method)
        else:
            attributes.addText(route.text,request)
        
        
    def default(slef,text,request,port=200):
        request.send_response(port)
        attributes.setHeader(request)
        attributes.addText(text,request)

    def show404(slef,request):
        request.send_response(400)
        attributes.setHeader(request)
        attributes.addText('<h2 align="center">404 Not Found !</h2>',request)

    def error(slef,request,error):
        request.send_response(5000)
        attributes.setHeader(request)
        attributes.addText(f"""<h2 style="color: red;text-align: center;">{error}</h2""",request)