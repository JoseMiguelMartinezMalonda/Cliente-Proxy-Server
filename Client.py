#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        print(argv[1])
        intermediary = Example.IntermediaryPrx.checkedCast(proxy)

        if not intermediary:
            raise RuntimeError('Invalid proxy')

        intermediary.send(argv[3], argv[2])

        return 0


sys.exit(Client().main(sys.argv))
