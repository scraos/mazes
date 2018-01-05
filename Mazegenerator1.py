from Tkinter import *
import random
import time
import math

class App:
    def __init__(self,master):
        self.w = Canvas(root, width=800, height=500, bg='grey')
        self.w.pack()

        width = int(self.w.cget('width'))
        height = int(self.w.cget('height'))

        w1 = 20
        h1 = 20
        xe = width/w1
        ye = height/h1

        dictgrid = {}

        for i in range(1,xe-1):
            for j in range(1,ye-1):
                dictgrid[(i,j)] = {'walls': {'left': 1, 'right': 1, 'bottom': 1, 'top': 1}, 'visited': False}

        for item in dictgrid:
            if item[0] == 1:
                dictgrid[item]['walls']['left'] = 0
            if item[1] == 1:
                dictgrid[item]['walls']['top'] = 0
            if item[0] == xe - 2:
                dictgrid[item]['walls']['right'] = 0
            if item[1] == ye - 2:
                dictgrid[item]['walls']['bottom'] = 0

        for i in range(1, xe - 1):
            for j in range(1, ye - 1):
                if dictgrid[(i,j)]['walls']['top'] == 1 or dictgrid[(i,j)]['walls']['top'] == 0:
                    #top
                    self.w.create_line(i*w1,j*h1,(i+1)*w1,j*h1)
                if dictgrid[(i,j)]['walls']['left'] == 1 or dictgrid[(i,j)]['walls']['left'] == 0:
                    #left
                    self.w.create_line(i*w1,j*h1,i*w1,(j+1)*h1)
                if dictgrid[(i, j)]['walls']['bottom'] == 1 or dictgrid[(i, j)]['walls']['bottom'] == 0:
                    #bottom
                    self.w.create_line(i*w1,(j+1)*h1,(i+1)*w1,(j+1)*h1)
                if dictgrid[(i,j)]['walls']['right'] == 1 or dictgrid[(i,j)]['walls']['right'] == 0:
                    #right
                    self.w.create_line((i+1)*w1,j*h1,(i+1)*w1,(j+1)*h1)

        coords = sorted(dictgrid)


        def neighbors(i):
            neighbs = []
            neighbs.append((i[0],i[1]+1))
            neighbs.append((i[0]+1,i[1]))
            neighbs.append((i[0]-1,i[1]))
            neighbs.append((i[0],i[1]-1))
            if i[0] == 1:
                neighbs.remove((i[0]-1,i[1]))
            if i[1] == 1:
                neighbs.remove((i[0],i[1]-1))
            if i[0] == xe - 2:
                neighbs.remove((i[0]+1,i[1]))
            if i[1] == ye - 2:
                neighbs.remove((i[0],i[1]+1))
            return neighbs

        def checkneighbors(n):
            unvneighbs = []
            for i in neighbors(n):
                if not dictgrid[i]['visited']:
                    unvneighbs.append(i)
            return unvneighbs

        def removeWalls(self,current,next):
            if current[0] < next[0]:
                self.w.create_line((current[0]+1)*w1,current[1]*h1,(current[0]+1)*w1,(current[1]+1)*h1, fill='grey')
                dictgrid[current]['walls']['right'] = 2
                dictgrid[next]['walls']['left'] = 2
            if current[0] > next[0]:
                self.w.create_line((current[0])*w1,current[1]*h1,(current[0])*w1,(current[1]+1)*h1, fill='grey')
                dictgrid[current]['walls']['left'] = 2
                dictgrid[next]['walls']['right'] = 2
            if current[1] < next[1]:
                self.w.create_line((current[0])*w1,(current[1]+1)*h1,(current[0]+1)*w1,(current[1]+1)*h1, fill='grey')
                dictgrid[current]['walls']['bottom'] = 2
                dictgrid[next]['walls']['top'] = 2
            if current[1] > next[1]:
                self.w.create_line((current[0])*w1,(current[1])*h1,(current[0]+1)*w1,(current[1])*h1, fill='grey')
                dictgrid[current]['walls']['top'] = 2
                dictgrid[next]['walls']['bottom'] = 2
            self.w.update()

        #n = coords, m = dictgrid
        def mazegen(n,m):
            stack = []
            cur = n[0]
            m[cur]['visited'] = True
            unvisited = []
            for item in dictgrid:
                if not m[item]['visited']:
                    unvisited.append(item)
            while len(unvisited) > 0:
                cur_n = checkneighbors(cur)
                if len(cur_n) > 0:
                    nxt = random.choice(cur_n)
                    stack.append(cur)
                    removeWalls(self,cur, nxt)
                    cur = nxt
                    m[cur]['visited'] = True
                    unvisited.remove(cur)
                elif len(stack) > 0:
                    new_cur = random.choice(stack)
                    stack.remove(new_cur)
                    cur = new_cur
            return

        mazegen(coords,dictgrid)

        def heur(n):
            dx = abs(xe - 2 - n[0])
            dy = abs(ye - 2 - n[1])
            return round(math.sqrt(dx ** 2 + dy ** 2), 3)

        for item in dictgrid:
            dictgrid[item]['visited'] = False
            dictgrid[item]['g'] = 10e9
            dictgrid[item]['h'] = heur(item)
            dictgrid[item]['f'] = 10e9

        # def newneighb(n):
        #     totalneighbs = []
        #     totalneighbs.append((i[0], i[1] + 1))
        #     totalneighbs.append((i[0] + 1, i[1]))
        #     totalneighbs.append((i[0] - 1, i[1]))
        #     totalneighbs.append((i[0], i[1] - 1))
        #     for item in dictgrid[n]['walls']:
        #         if dictgrid[n]['walls'][item] != 1:
        #             totalneighbs.

        def reconstruct_path(a, b):
            total_path = [b]
            while b in a.keys():
                b = a[b]
                total_path.append(b)
            return total_path

        def Astar(self, start, goal):
            begintime = time.clock()
            openSet = [start]
            closedSet = []
            cameFrom = {}
            dictgrid[start]['g'] = 0
            dictgrid[start]['f'] = dictgrid[start]['h']
            while len(openSet) > 0:
                current1 = min(openSet, key=lambda o: dictgrid[o]['f'])
                if current1 == goal:
                    endtime = time.clock()
                    print endtime - begintime
                    print "Done"
                    return reconstruct_path(cameFrom, current1)
                    break

                openSet.remove(current1)
                closedSet.append(current1)
                for item in dictgrid[current1]['neighb']:
                    if item in closedSet:
                        continue
                    if item not in openSet:
                        openSet.append(item)

                    tentG = dictgrid[current1]['g'] + 1
                    if tentG >= dictgrid[item]['g']:
                        self.w.create_rectangle(w1 * item[0] + 1, h1 * item[1] + 1, w1 * (item[0] + 1) - 1, h1 * (item[1] + 1) - 1,
                                           fill="#ff3300", bd="#ff3300")
                        continue

                    cameFrom[item] = current1
                    self.w.create_rectangle(w1 * item[0] + 1, h1 * item[1] + 1, w1 * (item[0] + 1) - 1, h1 * (item[1] + 1) - 1,
                                       fill="#0080ff", bd="#0080ff")
                    dictgrid[item]['g'] = tentG
                    dictgrid[item]['f'] = dictgrid[item]['g'] + dictgrid[item]['h']
                    root.update()
            if len(openSet) == 0:
                endtime = time.clock()
                print endtime - begintime
                print "No solution"
                return []

            print "were ready aswell"

            result2 = Astar((1,1), (xe-2,ye-2))

            for item in result2:
                self.w.create_rectangle(w1 * item[0] + 1, h1 * item[1] + 1, w1 * (item[0] + 1) - 1, h1 * (item[1] + 1) - 1, fill="#33cc33", bd="#33cc33")

root = Tk()
app = App(root)

root.mainloop()