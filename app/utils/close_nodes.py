import math


def is_in_direction(direction_vector, direction, tolerance=0.4):
    scalar_product = (direction_vector[0] * direction[0]) + (
        direction_vector[1] * direction[1]
    )
    scalar_product = max(-1.0, min(1.0, scalar_product))
    angle = math.acos(scalar_product)
    return abs(angle) <= tolerance


def find_close_nodes(initial_nodes, nodes):
    close_nodes = []
    for initial_node in initial_nodes:
        initial_node_position = initial_node["position"]
        direction = initial_node["direction"]
        orientation = initial_node["orientation"]
        for number, location in nodes.items():
            delta_x = location[0] - initial_node_position[0]
            delta_y = location[1] - initial_node_position[1]

            magnitude = (delta_x**2 + delta_y**2) ** 0.5
            if magnitude == 0:
                continue

            direction_vector = (delta_x / magnitude, delta_y / magnitude)
            if is_in_direction(direction_vector, direction):
                if magnitude <= orientation:
                    close_nodes.append(number)

    print("Close Nodes: ", close_nodes)
    return close_nodes
