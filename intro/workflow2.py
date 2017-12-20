import time
import threading
from rabbit import Worker, Consumer

class ToUpper(Worker):
    def __init__(self, name):
        super(ToUpper, self).__init__(name, 'my_queue', 'upper')

    def work(self, message):
        print(self.name + ": " + message)
        time.sleep(1)
        self.write(message.upper())


class Printer(Consumer):
    def __init__(self, name):
        super(Printer, self).__init__(name, 'upper')

    def work(self, message):
        time.sleep(2)
        print(self.name + ': ' + message)


threads = []
def launch(SeviceClass, name):
    service = SeviceClass(name)
    def run():
        try:
            service.start()
        except Exception as e:
            print(e)

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    threads.append(t)

launch(Printer, 'P1')
launch(Printer, 'P2')
launch(ToUpper, 'T1')

# Wait for the threads to finish
for t in threads:
    t.join()


