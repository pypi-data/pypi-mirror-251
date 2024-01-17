from ..utils.pages import Pages
from ..routes.RequestRoute import RequestRoute
from ..routes.ResponseRoute import ResponseRoute
import traceback 

# add new pages 
pages = Pages()
class HandleRoutes:
    def handle_next_handler(self,index,request,routes,method):
        # add new request data here and send to user 
        RequestData = RequestRoute(method,request)
        requestPath = RequestData.url
        
        # this is our cluster routes like app.route()
        for routeIndex in range(0,len(routes.all_routes[method])):
                currentRoute = routes.all_routes[method][routeIndex]
                route = currentRoute[0]

                # match the path 
                if (requestPath != (route.path).replace("%20"," ")):continue
                try:
                    # if path match send user resonse actions 
                    ResopnseData = ResponseRoute()

                    # send callback to user 
                    ResponseState = route.AllHandlers[index](RequestData,ResopnseData,ResopnseData.next)
                    
                    # finnaly send response 
                    if(ResponseState == "end"):
                        try:
                            pages.Send(request,ResopnseData,method)
                        except:
                            pages.show404(request)
                            pass
                        return True
                    elif(ResponseState == "next"):
                        if(index<currentRoute[1]):
                            self.handle_next_handler(index+1,request,routes,method)
                        else:
                            pages.error(request,f"<------- Thare Is Not Any Next() Response -------> ")
                        return True
                    else:
                        pages.error(request,f"<------- Add A Response Handler Here ------->")
                        return True
                except Exception as error:
                    traceback.print_exc()  # Print the full traceback of error
                    # show error page 
                    pages.error(request,f"Internal Server Error:{error} \n <---- Handle This Error")
                    return True
        
        # send False if there is not any route 
        return False
    
    def handle_get_request(self,request,routes):
        try:
            if len(routes.all_routes)<=0:
                pages.show404(request)
                
            elif not self.handle_next_handler(0,request,routes,"GET"):
                # if route not available send 404 page
                pages.show404(request)
        except Exception as error:
            print(error)
            pages.default("Internal Server Error",request,500)
            return None 