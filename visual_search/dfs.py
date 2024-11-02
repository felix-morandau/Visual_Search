from collections import deque


def dfs(problem):
    start_node = problem.get_start_spot()

    frontier = deque()
    visited = set()

    path = []
    frontier.append((start_node, path))

    while len(frontier) != 0:
        curr_node, final_path = frontier.pop()

        if curr_node not in visited:
            curr_node.make_closed()
            visited.add(curr_node)

            for successor in problem.get_successors(curr_node):

                if successor not in visited:

                    if problem.is_goal_state(successor):
                        return final_path

                    successor.make_open()
                    frontier.append((successor, final_path + [successor]))
        problem.draw_board()
