#Written by Fiona Shyne and London Lowmanstone
#properties and methods should be lowercase with underscores in-between words
#for example: def say_hello()

#imports

#variables
MAX_ANGLE = 40
MIN_ANGLE = - MAX_ANGLE
FOCAL_LENGTH = 35 #mm 
OBJECT_WIDTH = 40 #mm
VADER_DISTANCE = 100 #distance from ball to relese the convader belt
VADER_GO = 20 #distance from ball to turn on the vader
VADER_OFF = 0 #distance from ball to turn vader off
MAX_THROTTLE = 100 # the highest throttle level
MIN_THROTTLE = 0 #the lowest throttle level

#prop is short for proportion
#prop ranges from -1 to 1
#returns a value between low and high based on prop
#-1 will give low, 1 will give high
#function is linear
def value_from_prop(prop, low, high):
    #runs the function y=mx+b where slope is m=(high-1ow)/2 and y-intercept is b=(low+high)/2
    return (((high-low)/2.0)*prop) + ((low+high)/2)
        

#TODO make this all nice and split up the different tests into the correct files
#make sure that the program is only run if the file is being run, not just imported
if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    ping = PingPongBall()
    vader = Vader()
    propeller = Propeller(MAX_THROTTLE, MIN_THROTTLE)
    rutter = Rutter(MAX_ANGLE, MIN_ANGLE)
     
    
    # using webcam print the result of is_left to determine wether the boat should go left or right and how much
    for i in range(100):
        
        #find the frame of the webcam and find the is_left value
        ret,frame = cam.read()
        value = is_left(frame)
        print("VALUE:{}" .format(value))
        
        #find the biggest contour
        contours = ping.process(frame)
        if not len(contours) == 0:
            mas_area = 0
            best_contour= 0
            for i in contours:
                area = cv2.contourArea(i)
                if area > mas_area:
                    mas_area = area
                    best_contour = i
        else:
            best_contour = [] 
                  
        #find distance to ball
        distance = find_distance(FOCAL_LENGTH, OBJECT_WIDTH, best_contour)
        print("DISTANCE: {}" .format(distance))

        # if it finds the ball turn the motor
        if value == "can't find ball":
            pass
        else: 
            motor_control(value, distance,vader,propeller,rutter)
        
        ''' #draws what it sees
        #put a green outline for the contours of the ball
        contours = ping.process(frame)
        middle = 480 / 2
        if not len(contours) == 0:
            mas_area = 0
            best_contour= 0
            for i in contours:
                area = cv2.contourArea(i)
                if area > mas_area:
                    mas_area = area
                    best_contour= i
            for i in best_contour:
                frame[i[0][1], i[0][0]] = [0,255,0]
        # display the frame     
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
            
        (x,y),radius = cv2.minEnclosingCircle(best_contour)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(frame,center,radius,(0,255,0),2)
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''
        
        #time.sleep(0.5)
