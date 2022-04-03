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

