import serial
import time
import serial.tools.list_ports
import config

class SerialServer:
    buffer = ""

    def __init__(self, serial):
        self.serial = serial
        self.connect_flag = True
    def handler_decorator(self, f):
        self.handler = f

    def update(self):
        while self.serial.in_waiting:
            if self.connect_flag:
                self.connect_flag = False
                print("Connected")
            self.last_doing = time.time()
            try:
                symb = self.serial.read(1).decode()
            except:
                continue
            if symb == "\n":
                ans = self.handler(self.buffer)
                self.send(ans)
                self.buffer = ""
            else:
                self.buffer+=symb
        if time.time()-self.last_doing>1:
            self.connect()

    def send(self, val):
        try:
            self.serial.write(val)
        except TypeError:
            self.serial.write(val.encode())
        self.serial.write(b"\n")
    
    def connect(self, msg="1"):
        print("Connecting to robot...")
        self.connect_flag = True
        self.last_doing = time.time()
        self.send(msg)

def ask_for_port():
    ports = serial.tools.list_ports.comports()
    ports.sort()
    print("Выберите вариант:")
    for i, port in enumerate(ports):
            print(f"{i+1}. {port}")
               
    return serial.Serial(ports[int(input())-1].name, baudrate=config.serial_speed)

def main():
    server = SerialServer(ask_for_port())

    i = 0
    @server.handler_decorator
    def handler(msg):
        print(f"{time.time()} {msg}")
        # if int(msg)>0:
        #     print("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n")
        # return b"Hello, {msg}"
        return str(i)
    server.send("1")
    while 1:
        server.update()


if __name__ == "__main__":
    main()