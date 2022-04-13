import time
from serial_server import SerialServer, ask_for_port
from normalize import normalize_velocity
class Robot:
    def __init__(self):
        self.dec_waiting_for_send = [self.chr_from_velocity(0)]*len(self.dec_template)
        self.bin_waiting_for_send = ["0"]*len(self.bin_template)
        self.server = SerialServer(ask_for_port())
        self.server.handler_decorator(self.handler)
        self.server.connect()
    dec_template = {
        "x":0,
        "y":1,
        "z":2,
        "r":3
    }
    bin_template = {
        "m":0,
        "cs":1,
        "cd":2,
    }

    def swim(self, linear_vector, angular_velocity, depth_linear_velocity):
        motors_vector = linear_vector.rotated_clockwise(45)
        self.dec_waiting_for_send[self.dec_template["x"]] = self.chr_from_velocity(motors_vector.x)
        self.dec_waiting_for_send[self.dec_template["y"]] = self.chr_from_velocity(motors_vector.y)
        self.dec_waiting_for_send[self.dec_template["z"]] = self.chr_from_velocity(depth_linear_velocity)
        self.dec_waiting_for_send[self.dec_template["r"]] = self.chr_from_velocity(angular_velocity)
    
    def set_manipulator_to(self, val):
        self.bin_waiting_for_send[self.bin_template['m']] = str(int(val))
    
    def move_camera(self, val):
        self.bin_waiting_for_send[self.bin_template['cs']] = str(val[0])
        self.bin_waiting_for_send[self.bin_template['cd']] = str(int(val[1]))
    @staticmethod
    def chr_from_velocity(vel):
        return chr(44+round(vel))

    @staticmethod
    def chrs_from_bin(bin):
        ascii = ""
        while len(bin)!=0:
            bin_segment = bin[:5]
            bin = bin[5:]
            dec = int(bin_segment, 2)
            ascii += chr(33+dec)
        return ascii

    def handler(self, robot_data):   
        time.sleep(0.05)     
        final = "".join(self.dec_waiting_for_send) + self.chrs_from_bin("".join(self.bin_waiting_for_send))
        return final
        #Включение моторов в каждом из 9 направлений (одна пара моторов - x, вторая - y):
        #(x0,y1)  (x1,y1)  (x1,y0)
        #(x-1,y1) (x0,y0) (x1,y-1)
        #(x-1,y0)(x-1,y-1)(x0,y-1)

        #те моторы:
        #x0y0
        #y1x1
        # звезда - направление моторов
        # *  *
        #/    \
        # 
        #*    *
        # \  /
        # 

        
    
    def update(self):
        self.server.update()
# if __name__ == "__main__":
#     main()