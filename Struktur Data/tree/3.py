# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 08:20:06 2023

@author: lenovo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:36:33 2022

@author: RYAN
"""
class nodeTree:
    def __init__(self, dataRoot):
        self.dataRoot = dataRoot
        self.dataPointerKiri = None
        self.dataPointerKanan = None

    
    def insert(self, data):
        print("ini", self.dataRoot, " dan datanya ", data)
        if data < self.dataRoot:
           if self.dataPointerKiri is None:
              self.dataPointerKiri = nodeTree(data)
           else:
              self.dataPointerKiri.insert(data)
        elif data > self.dataRoot:
           if self.dataPointerKanan is None:
              self.dataPointerKanan = nodeTree(data)
           else:
              self.dataPointerKanan.insert(data)
    

    def tampilData(self):
        if self.dataPointerKiri:
            self.dataPointerKiri.tampilData()
        print(self.dataRoot)
        if self.dataPointerKanan:
            self.dataPointerKanan.tampilData()
            

ryan = nodeTree(7) #rootnode
ryan.insert(3)
ryan.insert(6)
ryan.insert(10)
ryan.insert(9)
ryan.insert(1)
ryan.tampilData()