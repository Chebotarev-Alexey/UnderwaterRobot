import serial
import time
from myasync import Loop, coroutine, run
import serial.tools.list_ports

class SerialServer(Loop):
    buffer = ""
    def __init__(self, serial):
        super().__init__()
        self.serial = serial
        self._coroutines+=[self.run()]
    def handler_decorator(self, f):
        self.handler = f
    @coroutine
    def run(self):
        while 1:
            while self.serial.in_waiting:
                try:
                    symb = self.serial.read(1).decode()
                except:
                    continue
                if symb == "\n":
                    ans = yield from self.handler(self.buffer)
                    self.send(ans)
                    self.buffer = ""
                else:
                    self.buffer+=symb
            yield
    def send(self, val):
        try:
            self.serial.write(val)
        except TypeError:
            self.serial.write(val.encode())
        self.serial.write(b"\n")

def ask_for_port():
    ports = serial.tools.list_ports.comports()
    ports.sort()
    print("Выберите вариант:")
    for i, port in enumerate(ports):
            print(f"{i+1}. {port}")
               
    return serial.Serial(ports[int(input())-1].name, baudrate=9600)
def main():
    server = SerialServer(ser)

    i = 0
    @server.handler_decorator
    def handler(msg):
        print(f"{time.time()} {msg}")
        # if int(msg)>0:
        #     print("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n")
        # return b"Hello, {msg}"
        return str(i)
        yield
    server.send("1234")
    run(server.run())
