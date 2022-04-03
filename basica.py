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
        self.cars_tunnel = [Value('i',0), Value('i',0)]#Lista con los coches en el túnel separados por dirección#
        self.cars_waiting = [Value('i', 0), Value('i',0)]#Lista con los coches esperando separados por dirección#
        self.mutex = Lock() #Semaforo#
        self.can_go = Condition(self.mutex)
        self.direction = -1 #Se actualiza con cada coche.#
        self.turn = Value('i',0)#1 o 0 dependiendo de la direccion qque pueda pasar en el momento.#
    
    def tunnel_condition(self):#Podra entrar si es su turno y no hay coches en la direccion contraria#
        empty = self.cars_tunnel[(self.direction + 1) % 2].value == 0
        turn = self.turn.value == self.direction
        return (empty and turn)
    
    def wants_enter(self, direction):#Entrara cuando se cumpla tunnel_condition#
        self.mutex.acquire()
        self.cars_waiting[direction].value += 1 
        self.direction = direction
        self.can_go.wait_for(self.tunnel_condition) 
        self.cars_tunnel[direction].value += 1
        self.mutex.release()
    
    def leaves_tunnel(self, direction):#Cuando un coche sale cambia la direccion para que entren los del otro lado cuando no queden coches. #
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