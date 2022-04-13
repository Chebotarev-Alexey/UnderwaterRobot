import robot #интерфейс для управления роботом
import gamepad #интерфейс для общения с геймпадом
from pd import PD
from normalize import normalize_angle, normalize_velocity
import time
import config


# Инициализация геймпада:
gamepad.init()

def printer_function(delay=0.1):
    while 1:
        t = time.time()
        val = None
        while time.time()-t<delay:
            val = yield
        print(str(val))
printer = printer_function()
next(printer)



class Updater: pass

#Абстрактный базовый класс для разных видов поворотов
class RotationUpdater (Updater):
    def __init__(self, joystick, speed=config.rotation_speed):
        self.joystick = joystick
        self.rotation_speed = speed
        self.flag = 0

#Класс, описывающий повороты со стабилизацией по курсу
class YawCorrectionRotationUpdater(RotationUpdater):
    def __init__(self, yaw_k=config.yaw_k, *args, **kwargs):
        self.accepted_rotation = 0
        self.rotation = 0
        self.pd = PD(yaw_k)
        super().__init__(*args, **kwargs)
    def get(self, yaw):
        vector = self.joystick.get()
        if vector.len>0.9:
            self.flag = True
            return vector.angle*self.rotation_speed
        elif vector.len<0.2 and self.flag:
            self.flag = False
            self.rotation = yaw
            self.pd.restart()
            print.send(self.rotation)
        return normalize_velocity(self.keep(yaw))
    def keep(self, yaw):
        normalized_error = normalize_angle(self.rotation - yaw)
        return self.pd.keep(normalized_error)

#Класс, описывающий повороты без стабилизации по курсу
class SimpleRotationUpdater(RotationUpdater):
    def get(self):
        vector = self.joystick.get()
        if vector.len>0.8:
            return normalize_velocity(normalize_angle(90-vector.angle)*self.rotation_speed)
        else:
            return 0

#Класс, описывающий линейное движение в горизонтальной плоскости
class LinearUpdater():
    def __init__(self, joystick):
        self.joystick = joystick
    def get(self):
        return self.joystick.get()*10

#Класс, описывающий погружение и всплытие
class DepthUpdater():
    def __init__(self, up_button, down_button):
        self.up_button = up_button
        self.down_button = down_button
    def get(self):
        return normalize_velocity((self.up_button.get() - self.down_button.get()) * 10)

class ManipulatorUpdater():
    def __init__(self, open_button, close_button):
        self.__open_button = open_button
        self.__close_button = close_button
        self.__actual_val = True
    def get(self):
        if self.__open_button.get():
            self.__actual_val = True
        if self.__close_button.get():
            self.__actual_val = False
        return self.__actual_val

class CameraUpdater():
    def __init__(self, up_button, down_button):
        self.__up_button = up_button
        self.__down_button = down_button
    def get(self):
        return (abs(self.__up_button.get() - self.__down_button.get()), self.__up_button.get()>self.__down_button.get())

#Создаем все нужные элементы геймпада

linear_joystick = gamepad.Joystick(*[gamepad.Axis(*config.linear_axes[name]) for name in ["x", "y"]])

rotation_joystick = gamepad.Joystick(*[gamepad.Axis(*config.rotation_axes[name]) for name in ["x", "y"]])

depth_buttons = [gamepad.Button(config.depth_buttons[name]) for name in ["up", "down"]]

manipulator_buttons = [gamepad.Button(config.manipulator_buttons[name]) for name in ["open", "close"]]

camera_buttons = [gamepad.Button(config.camera_buttons[name]) for name in ["up", "down"]]
#Создаем все апдейтеры:
linear_updater = LinearUpdater(linear_joystick)
rotation_updater = SimpleRotationUpdater(rotation_joystick)
depth_updater = DepthUpdater(*depth_buttons)
manipulator_updater = ManipulatorUpdater(*manipulator_buttons)
camera_updater = CameraUpdater(*camera_buttons)

robot = robot.Robot()
def process():
    #Обновляем данные гемпада:
    gamepad.update()
    
    #Получаем данные о действиях:
    linear_vector = linear_updater.get()
    angular_velocity = rotation_updater.get()
    depth_linear_velocity = depth_updater.get()
    manipulator_value = manipulator_updater.get()
    camera_value = camera_updater.get()

    #Отправляем команды на робота:
    robot.swim(linear_vector, angular_velocity, depth_linear_velocity)

    robot.set_manipulator_to(manipulator_value)
    robot.move_camera(camera_value)
    robot.update()

while 1:
    process()