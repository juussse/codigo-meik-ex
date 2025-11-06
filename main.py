import novapi
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
 
from mbuild import gamepad
 
import math
from time import ticks_ms
 
 
class PID:
    def __init__(self, Kp, Ki, Kd, setPoint=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setPoint = setPoint
        self.error = 0  
        self.dt = 0  
        self.u = 0  
        self.proporcional = 0  
        self.integral = 0  
        self.derivativo = 0  
       
        self.last_time = -0.1  
        self.last_error = 0  
       
    def fix_setPoint(self,new_setPoint):  
        self.setPoint = new_setPoint  
    #calcula la correcccion final (solicita la posicion actual y el dt)
    def final(self, pos, dt):  
        self.error = self.setPoint-pos  
        
        self.dt = dt
       
        self.proporcional = self.error*self.Kp  
       
        self.integral += self.error * self.dt  
        try:
            self.derivativo = ((self.error-self.last_error)/(self.dt)) * self.Kd  
        except ZeroDivisionError:
            pass
        
        self.last_error = self.error  
       
        self.u = self.proporcional + (self.integral * self.Ki) + self.derivativo  
       
        return self.u
       
 
tel = encoder_motor_class("M1","INDEX1")
 
pidTel = PID(0.5,0,5)
 
t = 0
 
Br = "DC1"
Fr = "DC2"
Bl = "DC3"
Fl = "DC4"
 
 
 
pos = 0
 
 
b = False
 
ang = 0
 
 
paso = 630
 
nivelAct = 0
 
posiciones = [0]
 
for i in range(4):
    posiciones.append(posiciones[-1]+paso)
 
angAct = 0
 
bAnt = False
 
temporizadorGripper = 0
 
while True:
    dt = (ticks_ms() - t)
    t = ticks_ms()
    
    
    if (gamepad.is_key_pressed ("N1")):
        motor.set_power(100)
        temporizadorGripper = 0
    temporizadorGripper+=dt
    
    if(temporizadorGripper>200):
        motor.set_power(0)
        
        
    
    bAnt = b
    b = gamepad.is_key_pressed("N2")
    
    if(not bAnt and b):
        nivelAct+=1
        ang = posiciones[nivelAct%5]
    
        
        
    pidTel.fix_setPoint(ang)
    
    anguloTel = tel.get_value("angle")
    
    uTel = pidTel.final(anguloTel, dt)
    
    tel.set_power(uTel)
    
    Rx = gamepad.get_joystick("Rx")  
    Lx = gamepad.get_joystick("Lx")  
    Ly = gamepad.get_joystick("Ly")  
 
    power_expand_board.set_power(Fl, (Ly+Lx+Rx))   
    power_expand_board.set_power(Fr, (Ly-Lx)-Rx)   
    power_expand_board.set_power(Br, (Ly+Lx-Rx))   
    power_expand_board.set_power(Bl, -(Ly-Lx+Rx))
