import threading
from rabbit import *


class ToUpper(Worker):
    def __init__(self):
        super(ToUpper, self).__init__('ToUpper', 'my_queue', 'upper')

    def work(self, message):
        self.write(message.upper())


class Printer(Consumer):
    def __init__(self):
        super(Printer, self).__init__('Printer', 'upper')

    def work(self, message):
        print(message)


def launch(SeviceClass):
    service = SeviceClass()
    def run():
        service.start()
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    return t


thread1 = launch(Printer)
thread2 = launch(ToUpper)

# Wait for the threads to finish
thread1.join()
thread2.join()
print('Workflow done.')

