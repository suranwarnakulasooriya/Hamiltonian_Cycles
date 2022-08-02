# ==============================================================================================================================
# HamCycleCode.py

# =============================================================================================
# INITIALIZE

import itertools # itertools.product is used to find all possible paths
import matplotlib.pyplot as plt # used to plot cycles

# =============================================================================================

# ==========================================================================================================================
# HAMCYCLES

def HamSquares(m): # main function to find all hamcycles in a square grid with sidelength m

    # =================================================================================================================
    # DOC

    ''''Find and plot hamiltonian cycles within a square grid of sidelength m.'''

    # =================================================================================================================

    # =================================================================================================================
    # FALLBACK

    try: # see if input is an integer
        int(m)
    except:
        return None # return none of input is not integer

    m = int(m) # convert input to integer

    if m%2 == 1 or m < 1: # if the sidelength is odd, there are no hamiltonian cycles
        print(f'There are no Hamiltonian cycles in a square grid of side length {m}.')
        return None # so return none

    # =================================================================================================================

    # =================================================================================================================
    # IF SIDELENGTH IS A POSITIVE EVEN INTEGER, FIND HAMCYCLES

    else:

    # =========================================================================================
    # INITIALIZE GRID

        grid = [] # grid starts empty
        n = [i for i in range(1,m**2+1)] # list of natural numbers up to m**2
        tempRow = [] # temporary row starts empty
        for j in range(len(n)): # cycle through n
            tempRow.append(n[j]) # add to the current row

            if n[j]%m == 0: # if at the end of the row:
                grid.append(tempRow) # append row to grid
                tempRow = [] # clear row

    # =========================================================================================
    # =================================================================================================================

    # =================================================================================================================
    # UDFs

    # =========================================================================================
    # CLEANLY DISPLAY A LIST OF LISTS

        def display(lst): # display a given list of lists list by list
            for i in lst: # print each element one at a time
                print(i)

    # =========================================================================================
    # =========================================================================================
    # REVERSE FUNCTION

        def reverse(lst): # returns all list elements in reversed order
            rev = [] # reversed version of list starts empty
            for n in range(1,len(lst)+1): # move from the last element to the first
                rev.append(lst[-n]) # add to reversed list
            return rev

    # the built in list.reverse() returns None and reverses the list itself,
    # so I made my own function
    # =========================================================================================
    # =========================================================================================
    # NEIGHBOR FUNCTIONS

        def N(r,c): # find north neighbor given a row and column

            if -1 < c < m and -1 <  r-1 < m: # check if neighbor is out of bounds
                return grid[r-1][c] # return neighbor if within bounds

            else:
                return None # return none if out of bounds

        def S(r,c): # find south neighbor, same method as N
            if -1 < c < m and -1 < r+1< m:
                return grid[r+1][c]
            else:
                return None

        def E(r,c): # find east neighbor, same method as N
            if -1 < c+1 < m and -1 < r < m:
                return grid[r][c+1]
            else:
                return None

        def W(r,c): # find west neighbor, same method as N
            if -1 < c-1 < m and -1 < r < m:
                return grid[r][c-1]
            else:
                return None

    # =========================================================================================
    # =========================================================================================
    # FIND TYPE OF NODE (CORNER, EDGE, CENTER)

        def nodeType(r,c): # find type of node given

            fcns = [N, S, E, W] # list of neighbor functions
            score = 0 # number of neighbors starts as 0

            for fcn in fcns: # look in all four directions
                if fcn(r,c):
                    score += 1 # if a neighbor exists, the number of neighbors increases

            if score == 2: # nodes with two neighbors are corners
                return 'corner'

            elif score == 3: # nodes with 3 neighbors are edges
                return 'edge'

            elif score == 4: # nodes with 4 neighbors are centers
                return 'center'

    # =========================================================================================
    # =========================================================================================
    # CHECK IF LIST CONTAINS ALL UNIQUE ELEMENTS

        def checkUnique(lst): # find if a given list contains all unique elements (no repeats)
            seen = [] # list of seen elements starts empty
            for element in lst: # cycle through list

                if element in seen: # if the element has been seen, there are duplicate elements
                    return False # so the list does not contain unique elements

                else: # is the element has not been seen, append it to the list of seen elements
                    seen.append(element)

            return True # if False was not returned, return True, since the lack
                        # of returning False means that the list has all unique elements

    # =========================================================================================
    # =================================================================================================================

    # =================================================================================================================
    # CREATE TREE DICT

    # =========================================================================================
    # INITIALIZE

        fcns = [N, S, E, W] # list of neighbor functions
        dests = [] # nodes to travel to
        starts = n # starting nodes

    # =========================================================================================
    # =========================================================================================
    # CREATE DICT

        for row in range(m): # cycle through rows
            for column in range(m): # cycle through columns

                neighbors = [] # lists of neighbors stars empty

                for fcn in fcns: # cycle through function list

                    if fcn(row,column): # if neighbor exists:
                        neighbors.append(fcn(row,column)) # add neighbor to list of neighbors

                dests.append(neighbors) # neighbors are the possible destinations

        tree = dict(zip(starts,dests)) # zip start and end points into dict

    # =========================================================================================
    # =================================================================================================================

    # =================================================================================================================
    # LIST ALL POSSIBLE PATHS IN M**2 MOVES

    # =========================================================================================
    # CREATE LIST OF NUMBERS OF NEIGHBORS

        neighbornums = [] # list of number of places to travel to from a given node starts empty

        for row in range(m): # cycle through row
            for column in range(m): # cycle through columns

                if nodeType(row,column) == 'corner': # if the node is a corner:
                    neighbornums.append([0,1]) # it has two neighbors

                elif nodeType(row,column) == 'edge': # if the node is an edge:
                    neighbornums.append([0,1,2]) # it has three neighbors

                elif nodeType(row,column) == 'center': # if the node is a center:
                    neighbornums.append([0,1,2,3]) # it has four neighbors

    # =========================================================================================
    # =========================================================================================
    # LIST ALL PATHS

        paths = list(itertools.product(*neighbornums)) # this is the only call of itertools

    # =========================================================================================
    # =================================================================================================================

    # =================================================================================================================
    # FIND HAMILTONIAN CYCLES

        hamcycles = [] # list of found hamcycles starts empty

        for pth in paths: # cycle through paths

            path = list(pth)
            simptree = {} # the simplified tree is a 1:1 version of the tree, meaning on specific node...
                          # you can only travel to exactly one other node

            for node in range(1,m**2+1): # cycle through range 1-m**2
                simptree[node] = tree[node][path[node-1]] # create simplified tree

            node = 1 # starting node is always 1
            # (if the path the a hamcycle, the starting node is irrelevant since it's a closed shape)

            queue = [node] # the queue starts with the first node (the queue is an individual path)
            for move in range((m**2)): # preform m**2 moves
                node = simptree[node] # travel to next node
                queue.append(node) # queue next node

            if checkUnique(queue[1:]) == True: # check if queue passes each point one
                if queue[-1] == 1: # check if last node is 1 (meaning that it cycles back)
                    if reverse(queue) in hamcycles: # if the reveres of the queue is in the current list,
                                                    # it is a version of an already found cycle in reverse...
                                                    # the cycles are undirected graphs so the current queue and its reverse
                                                    # will look the same when plotted
                                                    # so the queue can be discarded
                        pass

                    else:
                        hamcycles.append(queue) # if the queue is not a repeat, append it to hamcycles

            else: # if the queue does not meet at least one of these requierments, it is not a hamcycle
                pass

    # =================================================================================================================

    # =================================================================================================================
    # PLOT HAMCYCLES

        plots = 0 # number of plotted cycles stars as 0

        for cycle in hamcycles: # go through each hamcycle
            plots += 1 # number of plotted cycles increases

            x = [] # x positions star empty
            y = [] # y positions start empty
            for node in cycle: # go through each node in the cycle
                for row in range(m): # go through the graph to find the x and y of that node
                    for column in range(m):
                        if grid[row][column] == node:
                            x.append(row) # add x of the node
                            y.append(column) # add y of the node

            plt.plot(x,y,color='#b07bff') # plot the path
            plt.plot(x,y,'o',color='black') # plot the nodes
            plt.xlim(-min(x)-1,max(x)+1) # x and y limits are 1 away from the farthest node in that direction
            plt.ylim(-min(y)-1,max(y)+1) # ^
            plt.xticks([]) # remove tickmarks
            plt.yticks([]) # ^
            plt.gca().set_aspect('equal', adjustable='box') # set ratio to square
            plt.savefig(f'/Users/user/Desktop/{m}-{plots}') # save figure as Users/user/Desktop/m-plots.png
            plt.clf() # clear figure for next plot

    # =================================================================================================================

    # =================================================================================================================
    # RETURN HAMCYCLES

        if len(hamcycles) > 1:
            print(f"There are {str(len(hamcycles))} Hamiltonian cycles in a square grid if side length {str(m)}.")
        else:
            print(f"There is 1 Hamiltonian Cycle in a square grid of side length {str(m)}.")

        return display(hamcycles)

    # =================================================================================================================

    # =================================================================================================================

# END
# ==========================================================================================================================
# ==============================================================================================================================
