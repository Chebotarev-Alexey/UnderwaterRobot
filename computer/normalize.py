def normalize_angle(angle):
    while 1:
        if angle > 180:
            angle = -360+angle
        elif angle < -180:
            angle = 360+angle
        else:
            break
    return angle

def normalize_velocity(velocity):
    if velocity > 10:
        velocity = 10
    elif velocity < -10:
        velocity = -10
    return velocity