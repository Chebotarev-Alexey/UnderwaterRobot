linear_axes = {'x':(False, 2), 'y':(True, 4)}
rotation_axes = {'x':(False, 0), 'y':(True, 1)}
depth_buttons = {'up':6, 'down':8}
manipulator_buttons = {'open':7, 'close':5}
camera_buttons = {'up':1, 'down':3}

serial_speed = 9600

#коэффициэнты для выравнивания по курсу в режиме YawCorrectionRotation - п и д:
yaw_k = (0.4, 0.5)

#скорость поворота вычисляется как angle*ROTATOIN_SPEED, где angle - угол поворота джойстика (скорость от -10 до 10):
rotation_speed = 0.07
