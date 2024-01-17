from .route_cluster import RouteCluster

class ControlRoutes:
    def __init__(self):
        self.all_routes = {}
        
    def AddNewRoute(self, resData):
        try:
            # Check if the method key exists, and create an empty list if not
            self.all_routes[resData["method"]]
        except KeyError:
            self.all_routes[resData["method"]] = []

        # Append a new ResRoute instance to the method
        if(len(self.all_routes[resData["method"]]) == 0):
                newResponse = [RouteCluster(resData),0]
                self.all_routes[resData["method"]].append(newResponse)
        else:
             for route in self.all_routes[resData["method"]]:
                  if(resData["path"] == route[0].path):
                       route[0].addHandlers(resData["handlers"])
                       route[1] = route[1]+1
                       break
             else:
                newResponse = [RouteCluster(resData),0]
                self.all_routes[resData["method"]].append(newResponse)