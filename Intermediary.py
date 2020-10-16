#!/usr/bin/env python3

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example


class Intermediary(Example.Intermediary):
    def __init__(self, broker):
        self.communicator = broker

    # Si echas un vistazo al fichero Printer.ice, verás que el método send() tiene dos argumentos
    # en el siguiente orden: message, destinationProxy
    # Este es el orden que tienes que utilizar en la definición del método. También es recomendable
    # mantener el nombre de los argumentos porque en Python puedes utilizar ese nombre en la llamada
    def send(self, message, destinationProxy, current=None):

        # "communicator() es un método de la clase Ice.Application() que devuelve un CommunicatorI()
        # Si le pasas "broker" al constructor, le pasas directamente un CommunicatorI()
        # que no tiene método communicator() ni lo necesita porque él ya lo es. Por tanto
        # sólo tienes que usarlo directamente:
        proxy = self.communicator.stringToProxy(destinationProxy)

        print(destinationProxy)

        # De nuevo, en el slice puedes ver la interfaz se llama Printer(), no Server()
        server = Example.PrinterPrx.checkedCast(proxy)

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
