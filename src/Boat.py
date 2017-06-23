#TODO finish
# turns the motor based on the value is_left returns
def motor_control(value, distance, vader, propeller, rutter):
    global  VADER_DISTANCE, VADER_GO, VADER_OFF
    angle = value * rutter.max_angle
    if angle < 0.1 and angle > -0.1:
        angle = 0 
    rutter.turn_rutter(angle)

    if distance > VADER_DISTANCE:
        propeller.set_throttle(propeller.max_throttle)

    elif distance <VADER_DISTANCE and distance > VADER_GO:
        propeller.set_throttle(propeller.max_throttle/2)
        if vader.lowered == False: 
            vader.lower()
    elif distance < VADER_GO and distance > VADER_OFF:
        propeller.set_throttle(propeller.max_throttle/4)
        if vader.on == False:
            vader.turn_on()
        if vader.lowered == False: 
            vader.lower()
    elif distance <= VADER_OFF:
        propeller.set_throttle(propeller.min_throttle)
        if vader.on == True: 
            vader.turn_off()
        if vader.lowered == True: 
            vader.higher() 
    
    #TODO make this a list of commands to run
    command = None   
    if not(command is None):
        print("running the following command {}".format(command))