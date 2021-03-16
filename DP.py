#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 26 10:34:18 2021

@author: nada 
"""


import sys
import time
import threading

class Phil(object):
    
    def __init__(self, initial):
        self.lock = threading.Condition(threading.Lock())
        self.v = initial

    def pup(self):
        with self.lock:
            self.v += 1
            self.lock.notify()

    def pdown(self):
        with self.lock:
            while self.v == 0:
                self.lock.wait()
            self.v-= 1
            
            


class Philosopher (threading.Thread):

    def __init__(self, N , L, R, B): # B butler
        
        
        
        threading.Thread.__init__(self)
       
        self.right = R
        self.B = B
        self.number = N   
        self.left = L

    def run(self):
        for i in range(20):
            self.B.pdown() 
            time.sleep(0.5)                
            self.left.picked(self.number)    
            time.sleep(0.5)                 
            self.right.picked(self.number)    
            time.sleep(0.5)                 
            self.right.putdown(self.number)   
            self.left.putdown(self.number)     
            self.B.pup()                
        
        
        sys.stdout.write("Philosopher [%s] finished thinking and eating\n" % self.number)



class Chop(object):

    def __init__(self, number):
        self.number = number           # chopstick 
        self.user = -1                 #  the philosopher 
        self.lock = threading.Condition(threading.Lock())
        self.taken = False




    def picked(self, user):         
        with self.lock:
            while self.taken == True:
                self.lock.wait()
            self.user = user
            self.taken = True
            sys.stdout.write("Philosopher [%s] picked up chopstick [%s]\n" % (user, self.number))
            self.lock.notify()
            
              

    def putdown(self, user):       
        with self.lock:
            while self.taken == False:
                self.lock.wait()
            self.user = -1
            self.taken = False
        
        
            sys.stdout.write("Philosopher [%s] put down chopstick [%s]\n" % (user, self.number))
            self.lock.notifyAll()

def main():
    num = 5
    chopsticks = [Chop(i) for i in range(num)]

    B = Phil(num-1)
    
    philso = [Philosopher(i, chopsticks[i], chopsticks[(i+1)%num], B) for i in range(num)]


    for i in range(num):
        philso[i].start()


if __name__ == "__main__":
    main()