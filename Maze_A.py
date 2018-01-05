from Tkinter import *
import random
import math
import time

root = Tk()

w = Canvas(root, width=1000, height=600)
w.pack()

width = int(w.cget('width'))
height = int(w.cget('height'))
h1 = 5
w1 = 5

Spots = {}

map1 = [[1]*(width/w1) for i in range(height/h1)]

rows = len(map1)
columns = len(map1[0])

xe = columns - 1
ye = rows - 1

bp = random.randint((rows)*(columns)/4, (rows)*(columns)/3)

while bp >= 0:
    y = random.randint(0, rows - 1)
    x = random.randint(0, columns - 1)
    if map1[y][x] == 1:
        map1[y][x] = 0
    bp = bp - 1

map1[0][0] = 1
map1[height/h1 - 1][width/w1 - 1] = 1

def heur(n):
    dx = abs(xe - n[0])
    dy = abs(ye - n[1])
    return round(math.sqrt(dx**2+dy**2),3)

for i in range(rows):
    for j in range(columns):
        if map1[i][j] == 1:
            w.create_rectangle(j*w1, i*h1, (j+1)*w1, (i+1)*h1, fill='white')
            Spots[(j,i)] = {}
            Spots[(j,i)]['white'] = True
        if map1[i][j] == 0:
            w.create_rectangle(j * w1, i * h1, (j+1) * w1, (i+1) * h1, fill='#404040')
            Spots[(j, i)] = {}
            Spots[(j, i)]['white'] = False

# y = n[0] and x = n[1]

def neighb(n):
    neigbhs = []
    if n[1] <= ye and n[1] >= 0 and n[0] <= xe and n[0] >= 0:
        if n[1] - 1 >= 0 and Spots[(n[0], n[1] - 1)]['white']:
            neigbhs.append((n[0], n[1] - 1))
        if n[1] + 1  <= ye and Spots[(n[0], n[1] + 1)]['white']:
            neigbhs.append((n[0], n[1] + 1))
        if n[0] - 1 >= 0 and Spots[(n[0] - 1, n[1])]['white']:
            neigbhs.append((n[0] - 1, n[1]))
        if n[0] + 1 <= xe and Spots[(n[0] + 1, n[1])]['white']:
            neigbhs.append((n[0] + 1, n[1]))
    return neigbhs

for item in Spots:
    Spots[item]['h'] = heur(item)
    Spots[item]['f'] = xe*ye*10e6
    Spots[item]['g'] = xe*ye*10e6
    Spots[item]['neighb'] = neighb(item)

def reconstruct_path(a,b):
    total_path = [b]
    while b in a.keys():
        b = a[b]
        total_path.append(b)
    return total_path


def Astar(start, goal):
    begintime = time.clock()
    openSet = [start]
    closedSet = []
    cameFrom = {}
    Spots[start]['g'] = 0
    Spots[start]['f'] = Spots[start]['h']
    while len(openSet) > 0:
        current = min(openSet, key = lambda i: Spots[i]['f'])
        if current == goal:
            endtime = time.clock()
            print endtime - begintime
            print "Done"
            return reconstruct_path(cameFrom, current)
            break

        openSet.remove(current)
        closedSet.append(current)
        for item in Spots[current]['neighb']:
            if item in closedSet:
                continue
            if item not in openSet:
                openSet.append(item)

            tentG = Spots[current]['g'] + 1
            if tentG >= Spots[item]['g']:
                w.create_rectangle(w1 * item[0], h1 * item[1], w1 * (item[0] + 1), h1 * (item[1] + 1), fill="#ff3300")
                continue

            cameFrom[item] = current
            w.create_rectangle(w1*item[0],h1*item[1],w1*(item[0]+1),h1*(item[1]+1), fill = "#0080ff")
            Spots[item]['g'] = tentG
            Spots[item]['f'] = Spots[item]['g'] + Spots[item]['h']
        root.update()
    if len(openSet) == 0:
        endtime = time.clock()
        print endtime - begintime
        print "No solution"
        return []

for item in Astar((0,0),(xe,ye)):
    w.create_rectangle(w1*item[0],h1*item[1],w1*(item[0]+1),h1*(item[1]+1), fill = "#33cc33")
