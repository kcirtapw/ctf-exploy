#!/usr/bin/env python

from exploy import *
from exploit import Exploit
import time
import random
import hashlib
import io

def testfiller(o):
    i = random.randint(1,8)
    o._log("filling with %s\n" % i)
    q.put({"ip":i})

class MyExploit(Exploit):
    def run(self, ip, port, *args, **kwargs):
        print("exploiting %s:%s\n" % (ip,port))
        h=hashlib.md5()
        h.update(bytes(str(random.random()),encoding="UTF-8"))
        return ("%s=" % (h.hexdigest()[:9]))

if __name__ == "__main__":
    logfile = io.open("test.log",'w+')
    ex = MyExploit()
    q = Queue()
    tp = [] #threadpool
    tp_fill(tp, count=3, exploit=ex, queue=q, context={'port':5001},outstream=logfile)
    filler = PeriodicThread2(5,testfiller,outstream=logfile)
    filler.daemon=True
    filler.start()
    tp_start(tp)
    try:
      input()
    except EOFError:
      print("shutting down...\n")
    except KeyboardInterrupt:
      print("shutting down...\n")
    logfile.close()

    """
    try:
        import bpython
        bpython.embed(locals())
    except AttributeError:
        print("Not started with `bpython` - no interactivity")
    """

