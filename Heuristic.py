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

    def frontier(self):
        print("Frontier: ",self.cities)



class ctNode:
    def __init__(self, city, distance):
        self.city = str(city)
        self.distance = str(distance)


romania = {}


def makedict():
    file = open("romania.txt", 'r')
    for string in file:
        line = string.split(',')
        ct1 = line[0]
        ct2 = line[1]
        dist = int(line[2])
        romania.setdefault(ct1, []).append(ctNode(ct2, dist))
def makedict():
    file = open("usa.txt", 'r')
    for string in file:
        line = string.split(',')
        ct1 = line[0]
        ct2 = line[1]
        dist = int(line[2])
        romania.setdefault(ct1, []).append(ctNode(ct2, dist))




def makehuristikdict():
    h = {}
    with open("usah.txt", 'r') as file:
        for line in file:
            line = line.strip().split(" ")
            node = line[0].strip()
            sld = int(line[1].strip())
            h[node] = sld
    return h


def heuristic(node, values):
    return values[node]

def check(a,b,c):
    if a<=b+c:
        return "Yes"
    else:
        return "False"

def consistency(start, end):
    h = makehuristikdict()
    for k,v in romania.items():
        for i in v:
            print("-------------")
            print(k,i.city)
            print("-------------")
            print("h("+k+"): "+str(h[k])+"  h("+i.city+"): "+str(h[i.city])+"   c("+k+", a, " +i.city+"): "+ str(i.distance))
            print("Is "+"h("+k+")"+"<=" + "  h("+i.city+") + "+ " c("+k+", a, " +i.city+") ?" )
            print(check(h[k],h[i.city],int(i.distance)))
            print()

def astar(start, end):
    '''for k,v in romania.items():
        print(k,v)'''
    explored=[]
    path = {}
    distance = {}
    q = priorityQueue()
    h = makehuristikdict() # dictionary of the heuristics
    finalcost={}

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
        if (current == end):
            break

        for new in romania[current]:
            if new.city not in explored:
                g_cost = distance[current] + int(new.distance)


                #print("f("+new.city+")"+" = "+"g("+new.city+") + "+"h("+new.city+")"+" = "+ str(distance[current])+" + " + new.distance +" + " + str(heuristic(new.city, h)) + " = " +str(g_cost + heuristic(new.city, h)))

                if (new.city not in distance or g_cost < distance[new.city]):
                    distance[new.city] = g_cost
                    f_cost = g_cost + heuristic(new.city, h)
                    q.push(new.city, f_cost)
                    finalcost[new.city]=f_cost
                    path[new.city] = current

        final_path = []
        i = end

        while (path.get(i) != None):
            final_path.append(i)
            i = path[i]
        final_path.append(start)
        for i in final_path.reverse():
            print(final_path)



def main():
    src = "Seattle"
    dst = "Dallas"
    makedict()
    consistency(src, dst)


if __name__ == "__main__":
    main()
