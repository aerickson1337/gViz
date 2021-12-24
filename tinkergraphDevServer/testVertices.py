from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

url = 'ws://localhost:8182/gremlin'
remoteConn = DriverRemoteConnection(url, 'g')

g = traversal().withRemote(remoteConn)

g.addV('person').properties('name', 'paul').iterate()
g.addV('person').properties('name', 'fred').iterate()
g.addV('person').properties('name', 'tim').iterate()

results = g.V().elementMap().toList()
for result in results:
    print(result)

remoteConn.close()