import heapq


class priorityQueue:
    def __init__(self):
        self.cities = []

    def push(self, city, cost):
        heapq.heappush(self.cities, (cost, city))

    def pop(self):
        return heapq.heappop(self.cities)[1]

    def isEmpty(self):
        if (self.cities == []):
            return True
        else:
            return False

    def frontair(self):
        print("Frontier : ",self.cities)



class ctNode:
    def __init__(self, city, distance):
        self.city = str(city)
        self.distance = str(distance)


mc = {}


def makedict():
    file = open("mc.txt", 'r')
    for string in file:
        line = string.split(',')
        ct1 = line[0]
        ct2 = line[1]
        dist = int(line[2])
        mc.setdefault(ct1, []).append(ctNode(ct2, dist))
        mc.setdefault(ct2, []).append(ctNode(ct1, dist))


def makehuristikdict():
    h = {}
    with open("mch.txt", 'r') as file:
        for line in file:
            line = line.strip().split(",")
            node = line[0].strip()
            sld = int(line[1].strip())
            h[node] = sld
    return h


def heuristic(node, values):
    return values[node]


def astar(start, end):
    explored=[]
    path = {}
    distance = {}
    q = priorityQueue()
    h = makehuristikdict() # dictionary of the heuristics


    q.push(start, 0)
    distance[start] = 0
    path[start] = None
    expandedList = []
    step=0
    while (q.isEmpty() == False):

        step= step+1
        current = q.pop()
        expandedList.append(current)
        explored.append(current)
        print("Next node: ", current)
        print("------------------------")
        print("Step: ",step)
        print("------------------------")
        print("Current Node: ",current)
        print("Explored Cities : ",explored)

        if (current == end):
            break
        print("Children of "+current + " = ", end =" ")
        for new in mc[current]:
            print(new.city, end=" ")
        print("")
        for new in mc[current]:
            if new.city not in explored:
                g_cost = distance[current] + int(new.distance)

                #print(new.city, new.distance, "now : " + str(distance[current]), g_cost)
                print("f("+new.city+")"+" = "+"h("+new.city+")"+" = " + str(heuristic(new.city, h)))

                if (new.city not in distance or g_cost < distance[new.city]):
                    distance[new.city] = g_cost
                    f_cost = h[new.city]
                    q.push(new.city, f_cost)

                    path[new.city] = current
        q.frontair()

    printoutput(start, end, path, distance, expandedList)


def printoutput(start, end, path, distance, expandedlist):
    finalpath = []
    i = end

    while (path.get(i) != None):
        finalpath.append(i)
        i = path[i]
    finalpath.append(start)
    finalpath.reverse()


    print("=======================================================")
    print("the final path\t: " + str(finalpath))
    print("Total cost \t\t\t\t\t\t: " + str(distance[end]))


def main():
    src = "1"
    dst = "12"
    makedict()
    astar(src, dst)


if __name__ == "__main__":
    main()
