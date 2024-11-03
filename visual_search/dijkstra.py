from queue import PriorityQueue

def dijkstra(problem):
    start_node = problem.get_start_spot()
    goal_node = problem.get_goal_state()

    frontier = PriorityQueue()
    visited = set()

    frontier.put((0, start_node))
    path = []

    cost_so_far = {start_node: 0}
    parent_map = {start_node: None}

    while not frontier.empty():
        current_cost, curr_node = frontier.get()

        if curr_node in visited:
            continue

        curr_node.make_closed()
        visited.add(curr_node)

        if curr_node == goal_node:
            step = curr_node
            while step is not None:
                path.append(step)
                step = parent_map[step]
            path.reverse()

        for successor in problem.get_successors(curr_node):
            new_cost = current_cost + 1

            if successor not in visited or new_cost < cost_so_far.get(successor, float('inf')):
                cost_so_far[successor] = new_cost
                parent_map[successor] = curr_node
                frontier.put((new_cost, successor))
                successor.make_open()

        problem.draw_board()

    return path
