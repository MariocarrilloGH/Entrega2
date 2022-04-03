<<<<<<< HEAD
"""
Entrega 2
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value
NORTH = 0
SOUTH = 1

NCARS = 100
inicio=time.time()
class Monitor():
    def __init__(self):
        self.turn = Value('i',0)
        self.cars_tunnel = Value('i',0) #Numero de coches en el tunel#
        self.cars_waiting = Value('i', 0)#Numero de coches esperando#
        self.mutex = Lock()#semaforo#
        self.can_go = Condition(self.mutex)
        self.direction = -1
    def turn_change(self,t):#Cambia a la otra direccion#
        self.turn.value = t.value
        self.turn.value = (self.turn.value + 1)%2
    def neutral_turn(self): #En rojo para los dos lados#
        self.turn.value=-1
    def car_turn(self):#Devuelve True si esta en verde el lado de la direccion#
        return(self.turn.value==self.direction)
    def can_change_turn(self):#Espera a que no queden coches dentro#
        self.mutex.acquire()
        self.can_go.wait_for(self.nobody_tunel)
        self.mutex.release()
    def nobody_tunel(self):#Devulve si hay coches dentro#
        return (self.cars_tunnel.value==0)
    def wants_enter(self, direction):#El coche entrara si su lado esta en verde.#
        self.mutex.acquire()
        self.cars_waiting.value += 1 
        self.direction = direction
        self.can_go.wait_for(self.car_turn) 
        self.cars_tunnel.value += 1
        self.mutex.release()
    
    def leaves_tunnel(self, direction):#Sale el coche#
        self.mutex.acquire()
        self.cars_waiting.value -= 1
        self.cars_tunnel.value -= 1
        self.can_go.notify_all()
        self.mutex.release()
 
def delay(n=3):
    time.sleep(random.random()*n) 
def car(cid, direction,t, monitor):
    print(f"car {cid} direction {direction} created")
    delay(5)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    print(f"car {cid} heading {direction} out of the tunnel")
    monitor.leaves_tunnel(direction)
def turn(t,monitor):#Este proceso hace de semaforo poniendose en verde y rojo todo el tiempo#
    while(True):
        monitor.turn_change(t)
        t.value = monitor.turn.value
        print(f"{t.value}")
        if t.value == 1:#Para ajustar los tiempos de cada lado#
            time.sleep(10)
        if t.value == 0:
            time.sleep(10)
        monitor.neutral_turn()
        print(f"{monitor.turn.value}")
        monitor.can_change_turn()
        print("Nobody in the tunnel")
def main():
    monitor = Monitor()
    cid = 0 
    t = Value('i',0)
    s = Process(target = turn,args=(t,monitor))#El semaforo#
    s.start()
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1 else SOUTH 
        cid += 1
        p = Process(target=car, args=(cid, direction,t, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) 
if __name__ == '__main__':
    main()
=======
"""
Practica 2
"""

import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

NORTH = 0
SOUTH = 1

NCARS = 100

class Monitor():
    def __init__(self):
        self.cars_tunnel = [Value('i',0), Value('i',0)]
        self.cars_waiting = [Value('i', 0), Value('i',0)]
        self.mutex = Lock()
        self.can_go = Condition(self.mutex)
        self.direction = -1
        self.turn = Value('i',0)
    
    def tunnel_condition(self):
        empty = self.cars_tunnel[(self.direction + 1) % 2].value == 0
        turn = self.turn.value == self.direction
        return (empty and turn)
    
    def wants_enter(self, direction):
        self.mutex.acquire()
        self.cars_waiting[direction].value += 1 
        self.direction = direction
        self.can_go.wait_for(self.tunnel_condition) 
        self.cars_tunnel[direction].value += 1
        self.mutex.release()
    
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        self.cars_waiting[direction].value -= 1
        self.cars_tunnel[direction].value -= 1
        self.turn.value = (direction + 1) % 2
        self.can_go.notify_all()
        self.mutex.release()

def delay(n=3):
    time.sleep(random.random()*n)

def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    monitor.leaves_tunnel(direction)
    print(f"car {cid} heading {direction} out of the tunnel")

def main():
    monitor = Monitor()
    cid = 0 
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1 else SOUTH 
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) 

if __name__ == '__main__':
    main()

>>>>>>> d0aae0d732d7be3a7ca85220e9dd725711b24d18
