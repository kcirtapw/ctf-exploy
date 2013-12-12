from queue import Queue,Empty

from d3lib.EThread import EThread
from d3lib.PeriodicThread import PeriodicThread2

import telnetlib

class ExploitThread(EThread):
    def __init__(self, queue, exploit, context={}, outstream=None):
        EThread.__init__(self, outstream)
        self._queue = queue
        self._exploit = exploit
        self._queueWait = 1
        self._context = context
        self._tn = telnetlib.Telnet("localhost",50001)
        self._tn.write(b"?S test")

    def _execute(self):
        context = self._context.copy()
        try:
            context.update(self._queue.get(True,self._queueWait)) #blocking
            res = self._exploit.run(**context)
            print(self._tn.read_eager())
            self._tn.write(bytes("?T %s" % context['ip'],encoding="UTF-8"))
            for flag in res.split("\n"):
                self._tn.write(bytes(flag,encoding="UTF-8"))
                print(self._tn.read_eager())
            self._log("flag: %s"%res)
        except Empty:
            pass

def tp_fill(tp, count, queue, exploit, context={}, outstream=None):
    tp.clear()
    for x in range(count):
        t = ExploitThread(queue=queue, exploit=exploit, context=context, outstream=outstream)
        t.daemon = True
        tp.append(t)

def tp_start(tp):
    for x in tp:
        x.start()

def tp_stop(tp):
    for x in tp:
        x.stop()

def tp_stopclean(tp):
    tp_stop(tp)
    for x in tp:
        x.join()
    tp.clear()


