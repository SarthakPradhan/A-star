# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 14:32:45 2016

@author: SARTHAK
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:28:23 2016

@author: SARTHAK
"""

import cv2
import numpy as np
from math import *
imag=cv2.imread('C:\Users\SARTHAK\.spyder2\maze.png',1)
cv2.imshow('Orig maze',imag)
cv2.waitKey(1)
imag = cv2.resize(imag,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
img=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
#print img
cv2.waitKey(0)
cv2.destroyAllWindows()
class Node:
    def __init__(self,i,j,thres):
        self.posR=i
        self.posC=j      
        self.state=thres[i,j]
    def setFs(self,g,h,parent):
        self.parentPosR=parent.posR
        self.parentPosC=parent.posC
        self.g=g
        self.h=h
        self.f=g+h
    def resetF(self,g):
        self.g=g
        self.f=g+self.h
    

k,l=img.shape

ret,thres = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

closedList=[]
openList=[]
closCol=150
visCol=80
destCol=200
starCol=40

def distance(o1,o2):
    dist=(o1.posR-o2.posR)**2+(o1.posC-o2.posC)**2
    dist=cos(dist)+sin(dist)
    return dist
start=[4,5]
goal=[k-50,l-100]
thres[2,10]=150
def printPath():
    m=goal[0]
    n=goal[1]
    eh=False
    
    while(not eh ):

        for z in closedList:
            if z.posR==m and z.posC==n:
                break
        
        m=z.parentPosR
        n=z.parentPosC
        #print "m,n" , m ,n
        imag[z.posR,z.posC]=[0,0,255]
        if (m == start[0] and n == start[1]):
            eh= True
        

thres[start[0],start[1]]=starCol
thres[goal[0],goal[1]]=destCol
s = Node(start[0],start[1],thres)
go = Node(goal[0],goal[1],thres)
s.setFs(0,distance(s,go),s)
openList.append(s)
#it=1
print "start"
while True:
#    print "it",it
#    it=it+1
    openList.sort(key=lambda x: (x.f, x.h))
    
#    for x in openList:
#        print "openlist ",x.posR," ",x.posC
#    for x in closedList:
#        print x.posR," ",x.posC 
#    print "closed list" ,len(closedList),"open list" ,len(openList)
    current=openList[0]
    closedList.append(current)
    openList.remove(current)
    if (current.posR==goal[0] and current.posC==goal[1]):
        print "found"
        printPath()
        break
    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    for i, j in neighbors:
        
        a=current.posR+i
        b=current.posC+j
#        for x in closedList:
#            print x.posR," ",x.posC
        boo=False
        for z in closedList:
                if (z.posR==a and z.posC==b):
                    boo=True           

#        print boo
        if ((0 <= a < k) and (0 <= b < l) and thres[a,b] != 0 and (not boo) ):           
                                
#            print "a =" ,a," b = ",b

            Oboo=False
            if openList:       
                for z in openList:
                    if (z.posR==a and z.posC==b):
                        Oboo=True
                        temp=z
                        break

            
            if ( Oboo and temp.g>(current.g+distance(temp,current))):
                
                ga=(current.g+distance(temp,current))
                temp.resetF(ga)
                temp.parentPosR=current.posR
                temp.parentPosC=current.posC
            if not Oboo:                
                temp=Node(a,b,thres)
                temp.setFs(current.g+distance(temp,current),distance(temp,go),current)
                openList.append(temp)
                thres[a,b]=visCol
    cv2.imshow('thres maze',thres)
    cv2.waitKey(1)
        

    
cv2.imshow('thres maze',thres)
imag = cv2.resize(imag,None,fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
cv2.imshow('maze',imag)
cv2.waitKey(0)
cv2.destroyAllWindows()