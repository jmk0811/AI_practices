
def strToList(str):
    list = []
    list.append([])
    j = 0
    cnt = 0
    for i in str:
        if cnt > 10: break
        if i == ' ': continue
        elif i == '\n': 
            list.append([])
            j += 1
        else: list[j].append(i)
        cnt += 1
    return list

goal_state_str = "1 2 3\n4 5 6\n7 8 B"
goal = strToList(goal_state_str)

f_easy = open("easy.txt", "r", encoding="UTF-8")
easy_str = f_easy.read()
easy = strToList(easy_str)
f_easy.close()

f_hard = open("not_easy.txt", "r", encoding="UTF-8")
hard_str = f_hard.read()
hard = strToList(hard_str)
f_hard.close()

# helper function: find the index of the given number in a grid
def findIndex(s, n): # params: state grid, target number
    for i in range(0, 3):
        for j in range(0, 3):
            if s[i][j] == n:
                return (i, j)
            
# helper function: manhattan distance heuristic
def manhattan(s, n): # params: current state, target number
    gi, gj = findIndex(goal, n)
    ci, cj = findIndex(s, n)
    return abs(ci - gi) + abs(cj - gj)

# helper function: euclidean distance heuristic
def euclidean(s, n): # params: current state, target number
    gi, gj = findIndex(goal, n)
    ci, cj = findIndex(s, n)
    return pow((pow(ci - gi, 2) + pow(cj - gj, 2)), (1 / 2))

# helper function: calculate the heuristic cost
def cost(s, h): # params: current state, heuristic function
    c = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if s[i][j] != 'B': c += h(s, s[i][j])
        
    return c

class Node:
    def __init__(self, state):
        self.state = state
        self.target = " " # number being moved
        self.g = 0 # cost so far (depth)
        self.h = None # cost to go (heuristic cost)
        self.cost = None # total cost (g + h)
        self.children = [] # child nodes
        self.parent = None # parent node
        
    def insert(self, node):
        self.children.append(node)
        
    def toString(self):
        return "" + self.target + " (cost: " + str(self.g) + " + " + str(self.h) + "), "

# helper function: deep copy the given list
def deepcopy(list):
    out = []
    for i in range(0, 3):
        out.append(list[i].copy())
    return out

# helper function: swap the position of the given two elements in a grid
def swap(l, i1, j1, i2, j2):
    temp = l[i1][j1]
    l[i1][j1] = l[i2][j2]
    l[i2][j2] = temp
    
    
# A* Search
def a_star(state_init, state_goal, h): # params: initial state, goal state, heuristic function
    root = Node(state_init)
    
    node_curr = root # initialize current node to root of the search tree
    state_curr = node_curr.state # initialize current state
    
    candidates = []
    
    cnt = 0
    
    '''
    search start
    '''
    
    while node_curr.state != state_goal:
        # i, j = findIndex(state_curr, 'B')
        
        # check for possible movements, get next state candidates
        for i in range(0, 3):
            for j in range(0, 3):
                target = state_curr[i][j]
                if target != 'B':
                    # move up
                    if i - 1 >= 0 and state_curr[i - 1][j] == 'B':
                        state_next = deepcopy(state_curr) # copy list
                        swap(state_next, i, j, i - 1, j) # move
                        node_next = Node(state_next) # create next node
                        node_next.parent = node_curr # set the parent of the next node
                        node_next.target = target # set the target number (to be moved)
                        node_curr.insert(node_next) # add the node to the tree
                        candidates.append(node_next)
        
                        # batch movement
                        if i == 1:
                            state_next_b = deepcopy(state_next) # copy list
                            swap(state_next_b, i, j, i + 1, j) # move
                            node_next_b = Node(state_next_b) # create next node
                            node_next_b.parent = node_curr # set the parent of the next node
                            target_b = state_curr[i + 1][j] # set the target number (to be moved)
                            node_next_b.target = "(" + target + ", " + target_b + ")"
                            node_curr.insert(node_next_b) # add the node to the tree
                            candidates.append(node_next_b)
                        
                    # move down
                    elif i + 1 <= 2 and state_curr[i + 1][j] == 'B':
                        state_next = deepcopy(state_curr) # copy list
                        swap(state_next, i, j, i + 1, j) # move
                        node_next = Node(state_next) # create next node
                        node_next.parent = node_curr # set the parent of the next node
                        node_next.target = target # set the target number (to be moved)
                        node_curr.insert(node_next) # add the node to the tree
                        candidates.append(node_next)
                        
                        # batch movement
                        if i == 1:
                            state_next_b = deepcopy(state_next) # copy list
                            swap(state_next_b, i, j, i - 1, j) # move
                            node_next_b = Node(state_next_b) # create next node
                            node_next_b.parent = node_curr # set the parent of the next node
                            target_b = state_curr[i - 1][j] # set the target number (to be moved)
                            node_next_b.target = "(" + target + ", " + target_b + ")"
                            node_curr.insert(node_next_b) # add the node to the tree
                            candidates.append(node_next_b)
                        
                    # move right
                    elif j + 1 <= 2 and state_curr[i][j + 1] == 'B':
                        state_next = deepcopy(state_curr) # copy list
                        swap(state_next, i, j, i, j + 1) # move
                        node_next = Node(state_next) # create next node
                        node_next.parent = node_curr # set the parent of the next node
                        node_next.target = target # set the target number (to be moved)
                        node_curr.insert(node_next) # add the node to the tree
                        candidates.append(node_next)
                        
                        # batch movement
                        if j == 1:
                            state_next_b = deepcopy(state_next) # copy list
                            swap(state_next_b, i, j, i, j - 1) # move
                            node_next_b = Node(state_next_b) # create next node
                            node_next_b.parent = node_curr # set the parent of the next node
                            target_b = state_curr[i][j - 1] # set the target number (to be moved)
                            node_next_b.target = "(" + target + ", " + target_b + ")"
                            node_curr.insert(node_next_b) # add the node to the tree
                            candidates.append(node_next_b)
                        
                    # move left
                    elif j - 1 >= 0 and state_curr[i][j - 1] == 'B':
                        state_next = deepcopy(state_curr) # copy list
                        swap(state_next, i, j, i, j - 1) # move
                        node_next = Node(state_next) # create next node
                        node_next.parent = node_curr # set the parent of the next node
                        node_next.target = target # set the target number (to be moved)
                        node_curr.insert(node_next) # add the node to the tree
                        candidates.append(node_next)
                        
                        # batch movement
                        if j == 1:
                            state_next_b = deepcopy(state_next) # copy list
                            swap(state_next_b, i, j, i, j + 1) # move
                            node_next_b = Node(state_next_b) # create next node
                            node_next_b.parent = node_curr # set the parent of the next node
                            target_b = state_curr[i][j + 1] # set the target number (to be moved)
                            node_next_b.target = "(" + target + ", " + target_b + ")"
                            node_curr.insert(node_next_b) # add the node to the tree
                            candidates.append(node_next_b)
        
        # calculate cost of the candidate states
        min = float("inf")
        node_min = None # node with minimum cost
        for node in candidates:
            c = cost(node.state, h)
            node.g += 1
            node.h = c
            node.cost = node.g + node.h # calculate the total cost of the node
            if min > node.cost:
                min = node.cost
                node_min = node
        
        node_curr = node_min # select node with minimum cost
        state_curr = node_curr.state # set current state
        candidates.remove(node_curr) # remove the node in the candidates list
        
        # print(cnt)
        cnt += 1 # for debugging
    
    '''
    search end
    '''
    
    print()
    
    # reverse traverse the search tree to retrieve the optimal path
    out = []
    while node_curr.parent != None:
        out.append(node_curr.toString())
        node_curr = node_curr.parent

    out.reverse()
    
    # print the optimal path
    for i in out:
        print(i)

'''
test run
'''
a_star(easy, goal, manhattan)
# a_star(easy, goal, euclidean)
# a_star(hard, goal, manhattan)
# a_star(hard, goal, euclidean)















    

