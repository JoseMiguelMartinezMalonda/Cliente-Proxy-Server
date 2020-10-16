import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example


class Intermediary(Example.Intermediary):
    def __init__(self, broker):
        self.communicator = broker

    def send(self, serv, message, current=None):
        proxy = self.communicator().stringToProxy(serv)
        print(serv)
        server = Example.ServerPrx.checkedCast(proxy)

        if not server:
            raise RuntimeError('Invalid proxy')

        server.write(message)
        return 0

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = Intermediary(broker)

        adapter = broker.createObjectAdapter("IntermediaryAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("Intermediary"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))