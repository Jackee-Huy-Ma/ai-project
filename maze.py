from random import randint
from random import choice

import enum
import subprocess
import platform
import time

class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.wall = True
        self.parent = None
        self.neighbors = []
    
    def printNeighbors(self):
        print(len(self.neighbors))
    
    def position(self):
        return (self.i, self.j)
    
class MapGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = (0,0)
        self.myAI = AI((0,1))
        self.walls = self.gen_wall(width, height)
        self.start = (0, 0)
        self.goal = (width-1, height-1)
        self.myNodes = [[Node(i, j) for j in range(self.height)] for i in range(self.width)]


    def gen_wall(self, height, width):
        wall = []

        for i in range(height):
            for j in range(width):
                wall.append((i,j))

        wall.remove((0,0))
        wall.remove((height-1, width-1))
        wall.remove(self.myAI.position)

        return wall
    
    def move_player(self, direction):
        x = self.player[0]
        y = self.player[1]
        posistion = None

        if direction[0] == 'r':
            position = (x + 1, y)

        if direction[0] == 'l':
            position = (x - 1, y)

        if direction[0] == 'u':
            position = (x, y - 1)

        if direction[0] == 'd':
            position = (x, y + 1)

        
        if position not in self.walls and (position[0] >= 0 and position[0] <= self.width - 1) and (position[1] >= 0 and position[1] <= self.height - 1):
            self.player = position

        if posistion == self.goal:
            print("You made it to the end good job!")
    
    def add_neighbors(self):
        for i in range(self.width):
            for j in range(self.height):
                if(i < self.width - 1 and ((i + 1, j) not in self.walls)):
                    self.myNodes[i][j].neighbors.append(self.myNodes[i + 1][j])

                if (i > 0 and (i - 1, j) not in self.walls):
                    self.myNodes[i][j].neighbors.append(self.myNodes[i - 1][j])

                if (j < self.height - 1 and (i, j + 1) not in self.walls):
                    self.myNodes[i][j].neighbors.append(self.myNodes[i][j + 1])

                if(j > 0 and (i, j - 1) not in self.walls):
                    self.myNodes[i][j].neighbors.append(self.myNodes[i][j - 1])
 
def drawGrid(graph, width = 2):
    for y in range(graph.height):
        for x in range(graph.width):
            if (x, y) in graph.walls:
                symbol = 'X'
            elif (x, y) == graph.player:
                symbol = '@'
            elif (x, y) == graph.myAI.position:
                symbol = 'E'
            elif (x, y) == graph.start:
                symbol = '<'
            elif (x, y) == graph.goal:
                symbol = '>'
            else:
                symbol = '.'
            print("%%-%ds" % width % symbol, end="")
        print()
    
def getPath(grid, start, end):
    '''
    for i in range(int(grid.height * grid.width * pct)//2):
        x = randint(1, grid.width - 2)
        y = randint(1, grid.height - 2)

        out.append((x, y))
        out.append((x + choice([-1, 0, 1]), y + choice([-1, 0, 1])))
    
    if((0,0) in out):
        print("yes")
    '''
    while start != end:
        #start position x,y not there yet
        xSign = 1 if end[0] > start[0] else -1
        zSign = 1 if end[1] > start[1] else -1

        if (start[0] != end[0]) and (start[1] != end[1]):
            roll = randint(0,1)
            if roll == 0:
                start = (start[0] + xSign, start[1])
            if roll == 1:
                start = (start[0], start[1] + zSign)

        elif start[0] != end[0]:
            start = (start[0] + xSign, start[1])
        else:
            start = (start[0], start[1] + zSign)
        
        if (start in grid.walls):
            grid.walls.remove(start)
            grid.myNodes[start[0]][start[1]].wall = False

def clear():
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(.01)


class PriorityQueue:
    def __init__(self):
        self.pq = []

    def add(self, item):
        if(len(self.pq) == 0):
            self.pq.append(item)
            return

        min = item
        index = 0

        for i in range(len(self.pq)):
            if((item.i, item.j) == (self.pq[i].i, self.pq[i].j)):
                return
            if min.f <= self.pq[i].f:
                min.f = self.pq[i].f
            index += 1
        self.pq.insert(index, item)
    
    def pop(self):
        if(len(self.pq) != 0):
            return self.pq.pop(0)
    

def aStar(node, start, end):
    openQ = PriorityQueue()
    closeQ = PriorityQueue()
    a = set()
    calculateFn(node, start, end)

    #print(f"Node:[{node.i}][{node.j}] added to PriorityQueue!")
    openQ.add(node)
    a.add((node.i, node.j))
    while openQ:
        # Returns first node. Assumes first node fn is smallest.
        q = openQ.pop()
        #print(f"Node:[{q.i}][{q.j}] pop from PriorityQueue!")
        #minNode = q.neighbors[0]
        minNode = q.neighbors[0]
        #print(f"Set first neighbor as minNode. Node[{minNode.i}][{minNode.j}]")
       
        # Loop through neighbors. Note Wall nodes are removed and not checked.
        #print(f"length:{len(q.neighbors)}")
        #print("Start Looping through Q neighbours")
        for i in range(len(q.neighbors)):
            # Checks if node is equal to end goal
            #print(f"i:{i}")
            #print(f"In While Loop length:{len(q.neighbors)}")
            if(q.neighbors[i].i == end[0] and q.neighbors[i].j == end[1]):
                closeQ.add(q)
                PathPriorityQueue = PriorityQueue()
                path = set()
                parentA = closeQ.pq[len(closeQ.pq) - 1]
                PathPriorityQueue.add(parentA)
                path.add((parentA.i, parentA.j))
                while(parentA.parent is not None):
                    parentA = parentA.parent
                    if((parentA.i,parentA.j) not in path):
                        path.add((parentA.i, parentA.j))
                        PathPriorityQueue.add(parentA)
                        
                return PathPriorityQueue

            calculateFn(q.neighbors[i], start, end)             
            if(minNode.f <= q.neighbors[i].f):
                minNode = q.neighbors[i]
                if ((minNode.i, minNode.j) not in a):
                    minNode.parent = q
                    openQ.add(minNode)
                    a.add((minNode.i, minNode.j))

                    
        
        closeQ.add(q)
        #print(f"position: [{q.i}][{q.j}]")
    
    return

# Helper function that calculates F(n) = g(n) + h(n)
def calculateFn(node, start, end):
    node.g = abs(node.i - start[0] + node.j - start[1])
    node.h = abs((node.i - end[0]) + (node.j - end[1]))
    node.f = node.g + node.h

class AI:
    def __init__(self, position):
        self.position = position

def main():
    grid = MapGrid(10, 10)
    getPath(grid, (0,0), (grid.height -1, grid.width - 1))
    getPath(grid, grid.myAI.position, (grid.height -1, grid.width - 1))
    grid.add_neighbors()
    
    '''
    for i in range(grid.height):
        for j in range(grid.width):
            print(f"Node:{i},{j}:{grid.myNodes[i][j].i},{grid.myNodes[i][j].j}")
    '''

    for i in range(10):
        getPath(grid, (randint(0,9), randint(0,9)), (randint(0,9), randint(0,9)))
    
   
    myPriorityQueue = PriorityQueue()
    
    #print(f"position of gridAI{grid.myAI[0]}, {grid.myAI[1]}")
    myPriorityQueue = aStar(grid.myNodes[grid.myAI.position[0]][grid.myAI.position[1]], (grid.myAI.position), (grid.height - 1, grid.width - 1))
    #myPriorityQueue = aStar(grid.myNodes[grid.player[0]][grid.player[1]], grid.player, (grid.height - 1, grid.width - 1))
    myPriorityQueue.pq.reverse() 
    '''
    for i in range(len(myPriorityQueue.pq)):
        print((myPriorityQueue.pq[i].i, myPriorityQueue.pq[i].j))
    #print(len(myPriorityQueue.pq))
    '''

    #To-do - reverse
    while grid.player != grid.goal:
        #print(len(grid.myNodes[grid.player[0]][grid.player[1]].neighbors))
        drawGrid(grid)
        direction = input("Which direction? (r,l,u,d)")
        grid.move_player(direction)
        tempNode = myPriorityQueue.pop().position()
        if(tempNode == grid.myAI):
            grid.myAI.position = myPriorityQueue.pop().position()
        else:
            grid.myAI.position = tempNode
        clear()
    print("End")

if __name__ == '__main__':
    main()
