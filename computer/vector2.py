from normalize import normalize_angle
import math
class Vector2:
    def __init__(self, cartesian=None, polar=None):
        if cartesian:
            self.x, self.y = cartesian
            self.angle = math.degrees(math.atan2(self.y,self.x))
            self.len = math.sqrt(self.x**2+self.y**2)
        elif polar:
            self.angle, self.len = polar
            self.angle = self.angle
            rad = math.radians(self.angle)
            self.y, self.x = math.sin(rad)*self.len, math.cos(rad)*self.len
        else:
            raise TypeError("укажите значение ветора в одной из систем координат: декартова, полярная")
    def __add__(self, other):

        return type(self)(cartesian=(self.x+other.x, self.y+other.y))
    def __mul__(self, other):
        try:
            return type(self)(cartesian=(self.x*other.x, self.y*other.y))
        except AttributeError:
            return self*type(self)(cartesian=[other]*2)

    def rotated_clockwise(self, angle):
        new_angle = normalize_angle(self.angle-angle)
        return type(self)(polar=(new_angle, self.len))
    def __iter__(self):
        return (self.x, self.y).__iter__()

def main():
    v = Vector2(polar=(45, 2))
    print(v.x, v.y)
    v.rotate(45)
    print(v.x, v.y)

if __name__ == "__main__":
    main()