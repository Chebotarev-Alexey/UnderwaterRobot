import pygame #интерфейс для опроса геймпада
from vector2 import Vector2

_gamepad = None

def update():
    pygame.event.get()
def init():
    global _gamepad
    pygame.init()
    try:
        _gamepad = pygame.joystick.Joystick(0)
    except Exception as e:
        raise type(e)("геймпад не найден")
    _gamepad.init()


class GamepadElement:
    def __init__(self, num):
        global _gamepad
        if not _gamepad:
            raise Exception("Сначала требуется инициализировать геймпад")
        self._gamepad = _gamepad
        self._num = num
    def get(self): pass

class Axis(GamepadElement):
    def __init__(self, reverse=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse = reverse
    def get(self):
        if not self.reverse:
            return self._gamepad.get_axis(self._num)
        else:
            return -self._gamepad.get_axis(self._num)

class Button(GamepadElement):
    def get(self):
        return self._gamepad.get_button(self._num-1)

class Hat(GamepadElement):
    def get(self):
        return self._gamepad.get_hat(self._num)

class Joystick(GamepadElement):
    def __init__(self, x_axis, y_axis): 
        self.__x_axis = x_axis
        self.__y_axis = y_axis

    def get(self):
        vector = Vector2(cartesian=(self.__x_axis.get(), self.__y_axis.get()))
        abs_x = abs(vector.x)
        abs_y = abs(vector.y)
        if max(abs_x, abs_y):
            if abs_x<abs_y:
                new_y = 10
                new_x = vector.x*(new_y/abs_y)
            else:
                new_x = 10
                new_y = vector.y*(new_x/abs_x)
            new_vector = Vector2((new_x, new_y))
            normalized_vector = vector*(10/new_vector.len)
            return normalized_vector
        return vector