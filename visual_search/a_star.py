from queue import PriorityQueue

def heuristics(problem, curr_state):
    x1, y1 = curr_state.get_pos()
    x2, y2 = problem.get_goal_state().get_pos()

    return abs(x1 - x2) + abs(y1 - y2)


def a_star(problem):
    start_node = problem.get_start_spot()

    frontier = PriorityQueue()
    visited = set()
    node_index = 0

    path = []
    frontier.put((0, node_index, (start_node, path, 1)))

    while frontier.qsize() != 0:
        _, _, (curr_node, final_path, curr_cost) = frontier.get()

        if curr_node not in visited:
            curr_node.make_closed()
            visited.add(curr_node)

            for successor in problem.get_successors(curr_node):
                new_cost = curr_cost + 1

                total_cost = new_cost + heuristics(problem, successor)

                if successor not in visited:
                    #node_index += 1

                    if problem.is_goal_state(successor):
                        return final_path

                    successor.make_open()
                    frontier.put((total_cost, node_index, (successor, final_path + [successor], new_cost)))
        problem.draw_board()
