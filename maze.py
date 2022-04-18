from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
		# For example, when parsing raw_data, you may create several Node objects.  
		# Then you can store these objects into self.nodes.  
		# Finally, add to nd_dictionary by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        
            
        self.nd_dict = dict()  # key: index, value: the correspond node
        self.ends_dict=dict()
        self.ends=[]
        self.v_ends=[]
        self.str=""
        for row in self.raw_data:
            # print(row[0])
            nd=Node(row[0])
            k=0
            for i in range(4):
                if row[i+1]>=1:
                    k+=1
                    if i+1 == 1:
                        nd.setSuccessor(row[i+1], 1, row[i+5])
                    elif i+1 == 2:
                        nd.setSuccessor(row[i+1], 3, row[i+5])
                    elif i+1 == 3:
                        nd.setSuccessor(row[i+1], 2, row[i+5])
                    elif i+1 == 4:
                        nd.setSuccessor(row[i+1], 4, row[i+5])
            if k==1:
                self.ends_dict[nd.getIndex()]=nd
                self.ends.append(nd.getIndex())
            self.nodes.append(nd)
            self.nd_dict[nd.getIndex()]=nd

        self.BFS_2(self.nd_dict[1], self.nd_dict[6])
        print(self.str)
        self.str=""
        self.v_ends.append(1)
        # a=1
        # while self.ends:
        #     self.ends.remove(a)
        #     a=self.BFS(self.nd_dict[a])
        #     print(self.str)
        #     self.str=""
        #self.nd_dict[vi_end]=[]

        #self.nd_dict[queue]=[]
    def getEnds(self):
        return self.ends

    def getStr(self):
        stemp=self.str
        self.str=""
        return stemp

    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.nd_dict[1]

    def getNodeDict(self):
        return self.nd_dict

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        visited = [] # List for visited nodes.
        queue = []     #Initialize a queue
        pi = []
         
        visited.append(nd.getIndex())
        queue.append(nd.getIndex())
        pi.append(-1)
        k=-1
        stop=False 
        while queue:
                     # Creating loop to visit each node
            m = queue.pop(0)
            k+=1
            #print("pp")
            #print(m, end = "\n")
            # print(visited)
            # print(queue)
            #print(k)
            if m in self.ends and m not in self.v_ends:
                self.v_ends.append(m)
                # print("Node ", nd.getIndex(), " to the nearest end ", m)
                break 
            for neighbour in self.nd_dict[m].getSuccessors():
                #print("su is ", neighbour)
                if neighbour[0] not in visited:
                    visited.append(neighbour[0])
                    queue.append(neighbour[0])
                    pi.append(k)
                    
        inverse_order=[]

        # print(visited[k])
        inverse_order.append(visited[k])
        i=k
        itr=1
        while pi[i] != -1:
            # print (visited[pi[i]])
            inverse_order.append(visited[pi[i]])
            itr+=1
            #print("yy")
            i=pi[i]

        # print("sect 1")
        car_dir = 1
        for neighbour in self.nd_dict[inverse_order[itr-1]].getSuccessors():
            if self.nd_dict[inverse_order[itr-2]].getIndex() == neighbour[0]:
                car_dir = neighbour[1]

        for j in range (1, itr):
            # print(inverse_order[itr-j-1])
            action, car_dir = self.getAction(car_dir, self.nd_dict[inverse_order[itr-j]], self.nd_dict[inverse_order[itr-j-1]])
            self.str=self.str+(action)
        return visited[k]

    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        visited = [] # List for visited nodes.
        queue = []     #Initialize a queue
        pi = []
         
        visited.append(nd_from.getIndex())
        queue.append(nd_from.getIndex())
        pi.append(-1)
        k=-1
        stop=False 
        while queue:
                     # Creating loop to visit each node
            m = queue.pop(0)
            k+=1
            #print("pp")
            #print(m, end = "\n")
            # print(visited)
            # print(queue)
            #print(k)
            if m == nd_to.getIndex():
                break 
            for neighbour in self.nd_dict[m].getSuccessors():
                #print("su is ", neighbour)
                if neighbour[0] not in visited:
                    visited.append(neighbour[0])
                    queue.append(neighbour[0])
                    pi.append(k)
                    
        inverse_order=[]

        print(visited[k])
        inverse_order.append(visited[k])
        i=k
        itr=1
        while pi[i] != -1:
            # print (visited[pi[i]])
            inverse_order.append(visited[pi[i]])
            itr+=1
            #print("yy")
            i=pi[i]

        # print("sect 1")
        car_dir = 1
        for j in range (1, itr):
            # print(inverse_order[itr-j-1])
            action, car_dir = self.getAction(car_dir, self.nd_dict[inverse_order[itr-j]], self.nd_dict[inverse_order[itr-j-1]])
            self.str=self.str+(action)
        return None

    def getAction(self, car_dir, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_from
		# If not, print error message and return 0
        is_in = False
        for neighbour in nd_from.getSuccessors():
            if nd_to.getIndex() == neighbour[0]:
                is_in = True
                #print(" Car_dir is: ", car_dir, ", from node ", nd_from.getIndex(), " to ", nd_to.getIndex(), " on the ", neighbour[1])
                if neighbour[1] - car_dir == 1 or neighbour[1] -  car_dir == -3:
                    # print("From ", nd_from.getIndex(), " to ", nd_to.getIndex(), ", TURN_LEFT")
                    return "l", neighbour[1]
                elif neighbour[1] - car_dir == -1 or neighbour[1] - car_dir == 3:
                    # print("From ", nd_from.getIndex(), " to ", nd_to.getIndex(), ", TURN_RIGHT")
                    return "r", neighbour[1]
                elif neighbour[1] - car_dir == 2 or neighbour[1] - car_dir == -2:
                    # print("From ", nd_from.getIndex(), " to ", nd_to.getIndex(), ", U_TURN")
                    return "b", neighbour[1]
                else:
                    # print("From ", nd_from.getIndex(), " to ", nd_to.getIndex(), ", ADVANCE")
                    return "f", neighbour[1]

        if is_in == False:
            print(nd_to.getIndex(), " not a Successor ", nd_to.getIndex())
        return None

    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)
