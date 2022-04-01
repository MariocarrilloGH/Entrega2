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
        self.cars_tunnel = [Value('i',0), Value('i',0)]
        self.cars_waiting = [Value('i', 0), Value('i',0)]
        self.mutex = Lock()
        self.can_go = Condition(self.mutex)
        self.direction = -1
    def turn_change(self,t):
        self.turn.value = t.value
        self.turn.value = (self.turn.value + 1)%2
    def neutral_turn(self):
        self.turn.value=-1
    def car_turn(self):
        return(self.turn.value==self.direction)
    def can_change_turn(self):
        self.mutex.acquire()
        self.can_go.wait_for(self.nobody_tunel)
        self.mutex.release()
    def nobody_tunel(self):
        return (self.cars_tunnel[(self.direction+1)%2].value==0 and self.cars_tunnel[(self.direction+1)%2].value==0)
    def wants_enter(self, direction):
        self.mutex.acquire()
        self.cars_waiting[direction].value += 1 
        self.direction = direction
        self.can_go.wait_for(self.car_turn) 
        self.cars_tunnel[direction].value += 1
        self.mutex.release()
    
    def leaves_tunnel(self, direction):
        self.mutex.acquire()
        self.cars_waiting[direction].value -= 1
        self.cars_tunnel[direction].value -= 1
        self.can_go.notify_all()
        self.mutex.release()
 
def delay(n=3):
    time.sleep(random.random()*n) 
def car(cid, direction,t, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the tunnel")
    delay(3)
    print(f"car {cid} heading {direction} leaving the tunnel")
    print(f"car {cid} heading {direction} out of the tunnel")
    monitor.leaves_tunnel(direction)
def turn(t,monitor):
    while(True):
        monitor.turn_change(t)
        t.value = monitor.turn.value
        print(f"{t.value}")
        if t.value == 1:
            time.sleep(10)
        if t.value == 0:
            time.sleep(10)
        monitor.neutral_turn()
        print(f"{monitor.turn.value}")
        monitor.can_change_turn()
        print("Nadie en el túnel")
def main():
    monitor = Monitor()
    cid = 0 
    t = Value('i',0)
    s = Process(target = turn,args=(t,monitor))
    s.start()
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1 else SOUTH 
        cid += 1
        p = Process(target=car, args=(cid, direction,t, monitor))
        p.start()
        time.sleep(random.expovariate(1/0.5)) 
if __name__ == '__main__':
    main()