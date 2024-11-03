from queue import PriorityQueue


def ucs(problem):
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

                if successor not in visited:
                    node_index += 1

                    if problem.is_goal_state(successor):
                        return final_path

                    successor.make_open()
                    frontier.put((curr_cost + 1, node_index, (successor, final_path + [successor], curr_cost + 1)))
        problem.draw_board()
