from queue import PriorityQueue

adj_matrix = [
    [0, 3, 0, 1, 0],
    [2, 0, 4, 0, 0],
    [0, 4, 0, 5, 1],
    [100, 0, 5, 0, 3],
    [0, 0, 1, 3, 0]
]

def visitedNode(node, path):
    for i in range(len(path)):
        if (node == path[i]):
            return False
    return True

def UCS (matrix, start, goal):
    q= PriorityQueue()
    path = []
    path.append(start)
    q.put((0, start, path))

    while not q.empty():
        cost, currNode, currPath = q.get()

        if(currNode==goal):
            return cost, currPath
        
        # Generate neighbors of the current node from adjacency matrix
        neighbors=[]
        for i in range(len(matrix[currNode])):
            if(matrix[currNode][i]!=0):
                neighbors.append(i)

        for neighbor in neighbors:
            if(visitedNode(neighbor, currPath)):
                # If neighbor is not visited before, push it to the priority queue with its cost and path
                new_cost = cost + matrix[currNode][neighbor]  
                new_path = currPath + [neighbor]
                # Calculate cost to reach neighbor from current node
                q.put((new_cost, neighbor,new_path))

    return None

#debug
start_node = 0
goal_node = 4
path = UCS(adj_matrix, start_node, goal_node)
if path:
    print(f"Shortest path from node {start_node} to node {goal_node}: {path}")
else:
    print(f"No path found from node {start_node} to node {goal_node}")