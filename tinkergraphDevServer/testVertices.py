from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

url = 'ws://localhost:8182/gremlin'
remoteConn = DriverRemoteConnection(url, 'g')

g = traversal().withRemote(remoteConn)
g.V('0abe3186-e763-4b4c-a3ed-dfcdf5d8e1b9').addE('knows').to(__.V('aa24c147-68f9-41ee-8099-21a6bd87b9dc')).next()
results = g.V().elementMap().toList()
for result in results:
    print(result)

remoteConn.close()