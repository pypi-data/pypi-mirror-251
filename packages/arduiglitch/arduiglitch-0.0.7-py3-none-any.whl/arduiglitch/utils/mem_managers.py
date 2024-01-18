from multiprocessing.managers import BaseManager
from multiprocessing import Queue

class MemManagerSer(BaseManager):
    def __init__(self, address=("", 50000), authkey=b"thisisanautkey"):
        super().__init__(address=address, authkey=authkey)
        self._exp_queue: Queue = Queue()
        self._gui_queue: Queue = Queue()

        MemManagerSer.register("get_exp_queue", lambda: self._exp_queue)
        MemManagerSer.register("get_gui_queue", lambda: self._gui_queue)

class MemManagerCli(BaseManager):
    def __init__(self, address=("", 50000), authkey=b"thisisanautkey"):
        super().__init__(address=address, authkey=authkey)
        self.exp_queue = None
        self.gui_queue = None

        MemManagerCli.register("get_exp_queue")
        MemManagerCli.register("get_gui_queue")