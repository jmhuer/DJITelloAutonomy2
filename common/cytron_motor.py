import serial

class Cytron_Motor:
    
    def __init__(self, baud):
        self.ser = serial.Serial(
            #port='COM3', #uncomment for windows
            port='/dev/ttyUSB0',
            baudrate=baud
            )
    
    # setspeed: sets the speed of the robot given the desired speed as percentage.
    # robot continues to move unless
    # stop is called.
    # inputs:
    #   speed: a number from 0-100 denoting the speed of the robot as a 
    #          percentage.
    def setspeed(self, speed):

        #record speed for future uses
        self.prevSpeed = speed
        
        #1 is forward and 0 is backward
        direction = 1 if speed >= 0 else 0

        #calculate the speed section
        speedBits = int(63 * (abs(speed)/100))
        
        if direction:
            leftMotor = 0b00000000
            rightMotor = 0b10000000
        else:
            leftMotor = 0b01000000
            rightMotor = 0b11000000
        
        #set final byte values for both motors
        leftMotor = leftMotor | speedBits
        rightMotor = rightMotor | speedBits

        #construct bytearray
        arr = bytearray()
        arr.append(leftMotor)
        arr.append(rightMotor)

        self.ser.write(arr)
        arr.clear()

    
    #stop the robot from moving
    def stop(self):
        leftMotor = 0b00000000
        rightMotor = 0b10000000
        #construct bytearray
        arr = bytearray()
        arr.append(leftMotor)
        arr.append(rightMotor)

        self.ser.write(arr)
        arr.clear()

    # turnRight: turns the robot towards the right side given a turning speed.
    #            the turn is a rotation and not a steer.
    #            robot continues to turn/rotate unless
    #            stop is called.
    # inputs:
    #   speed: a number from 0-100 denoting the turning speed of the robot as a 
    #          percentage.
    def turnRight(self, speed):
        
        #input correction
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0

        #record speed for future uses
        self.prevSpeed = speed
        
        #1 is right and left is backward
        direction = 1 if speed >= 0 else 0

        #calculate the speed section
        speedBits = int(63 * (abs(speed)/100))
        
        if direction:
            leftMotor = 0b00000000
            rightMotor = 0b11000000
        else:
            leftMotor = 0b01000000
            rightMotor = 0b10000000
        
        
        #set final byte values for both motors
        leftMotor = leftMotor | speedBits
        rightMotor = rightMotor | speedBits

        #construct bytearray
        arr = bytearray()
        arr.append(leftMotor)
        arr.append(rightMotor)

        self.ser.write(arr)
        arr.clear()


    # turnLeft: turns the robot towards the left side given a turning speed.
    #            the turn is a rotation and not a steer.
    #            robot continues to turn/rotate unless
    #            stop is called.
    # inputs:
    #   speed: a number from 0-100 denoting the turning speed of the robot as a 
    #          percentage.
    def turnLeft(self, speed):
        
        #input correction
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0

        #record speed for future uses
        self.prevSpeed = speed
        
        #1 is right and left is backward
        direction = 1 if speed >= 0 else 0

        #calculate the speed section
        speedBits = int(63 * (abs(speed)/100))
        
        if direction:
            leftMotor = 0b01000000
            rightMotor = 0b10000000
        else:
            leftMotor = 0b00000000
            rightMotor = 0b11000000
        
        #set final byte values for both motors
        leftMotor = leftMotor | speedBits
        rightMotor = rightMotor | speedBits

        #construct bytearray
        arr = bytearray()
        arr.append(leftMotor)
        arr.append(rightMotor)

        self.ser.write(arr)
        arr.clear()

    def steerMove(self, speed, steer):
        
        #input correction
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100
        if steer > 100:
            steer = 100
        if steer < -100:
            steer = -100

        #record speed for future uses
        self.prevSpeed = speed
        self.prevSteer = steer

        leftMotorSpeed = speed
        rightMotorSpeed = speed

        absSteer = abs(steer)

        #calculate left and right motor speeds based on steer
        if steer >= 0:
            leftMotorSpeed = leftMotorSpeed + (absSteer / 2)
            rightMotorSpeed = rightMotorSpeed - (absSteer/2)
        else:
            leftMotorSpeed = leftMotorSpeed - (absSteer / 2)
            rightMotorSpeed = rightMotorSpeed + (absSteer/2)

        #value limit correction
        if leftMotorSpeed > 100:
            leftMotorSpeed = 100
        #elif leftMotorSpeed < 0:
            #leftMotorSpeed = 0
        
        if rightMotorSpeed > 100:
            rightMotorSpeed = 100
        #elif rightMotorSpeed < 0:
        #    rightMotorSpeed = 0
            
        
        #1 is right and left is backward
        direction = 1 if speed >= 0 else 0

        #calculate the speed section for both motors
        speedBitsRight = int(63 * (abs(rightMotorSpeed)/100))
        speedBitsLeft = int(63 * (abs(leftMotorSpeed)/100))
        
        if (rightMotorSpeed * leftMotorSpeed) < 0:
            if rightMotorSpeed > 0:
                leftMotor = 0b00000000
                rightMotor = 0b11000000
            else:
                leftMotor = 0b01000000
                rightMotor = 0b10000000
        elif direction:
            leftMotor = 0b00000000
            rightMotor = 0b10000000
        else:
            leftMotor = 0b01000000
            rightMotor = 0b11000000
        
        #set final byte values for both motors
        leftMotor = leftMotor | speedBitsLeft
        rightMotor = rightMotor | speedBitsRight

        #construct bytearray
        arr = bytearray()
        arr.append(leftMotor)
        arr.append(rightMotor)

        self.ser.write(arr)
        arr.clear()
