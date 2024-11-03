from queue import PriorityQueue


def dijkstra(problem):
    start_node = problem.get_start_spot()
    frontier = PriorityQueue()
    visited = set()

    path = []
    initial_cost = 0
    frontier.put((initial_cost, (start_node, path)))

    cost_so_far = {start_node: initial_cost}

    while not frontier.empty():
        current_cost, (curr_node, final_path) = frontier.get()

        if curr_node not in visited:
            curr_node.make_closed()
            visited.add(curr_node)

            for successor in problem.get_successors(curr_node):
                new_cost = current_cost + 1

                if successor not in visited or new_cost < cost_so_far.get(successor, float('inf')):
                    if problem.is_goal_state(successor):
                        return final_path + [successor]

                    cost_so_far[successor] = new_cost
                    successor.make_open()
                    frontier.put((new_cost, (successor, final_path + [curr_node])))

        problem.draw_board()
