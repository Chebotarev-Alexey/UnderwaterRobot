import pygame
import sys

pygame.init()
if(pygame.joystick.get_count()<1):
    print("Геймпад не найден")
    sys.exit()
print("Геймпад обнаружен!")
j = pygame.joystick.Joystick(0)
j.init()
a = j.get_axis
b = j.get_button
h = j.get_hat

while 1:
    pygame.event.get()
    Buttons = []
    Hats = []
    Axes = []
    for button in range(j.get_numbuttons()):
        Buttons.append(int(b(button)))
    for hat in range(j.get_numhats()):
        Hats.append(h(hat))
    for axis in range(j.get_numaxes()):
        Axes.append(int(a(axis)*10))
    print({
        "axes": Axes,
        "hats": Hats,
        "butt": Buttons
        })