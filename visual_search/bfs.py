from queue import Queue


def bfs(problem):
    start_node = problem.get_start_spot()

    frontier = Queue()
    visited = set()

    path = []
    frontier.put((start_node, path))

    while frontier.qsize() != 0:
        curr_node, final_path = frontier.get()

        if curr_node not in visited:
            curr_node.make_closed()
            visited.add(curr_node)

            for successor in problem.get_successors(curr_node):

                if successor not in visited:

                    if problem.is_goal_state(successor):
                        return final_path

                    successor.make_open()
                    frontier.put((successor, final_path + [successor]))
        problem.draw_board()
