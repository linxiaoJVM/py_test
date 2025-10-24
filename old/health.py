import httplib

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
import time

class Health(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("UP %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return '{"status":"UP"}'

class Hello(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        # request.setHeader("content-type", "application/json")
        return "Hello, world!"

class Test(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        # request.setHeader("content-type", "application/json")
        print("Hello, this is a test message! %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return "Hello, this is a test message!"

root = resource.Resource()
root.putChild('health', Health())
root.putChild('', Hello())
root.putChild('test', Test())
endpoints.serverFromString(reactor, "tcp:5680").listen(server.Site(root))
reactor.run()
