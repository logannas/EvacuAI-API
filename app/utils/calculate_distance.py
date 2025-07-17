import math


def calculate_distance(graph_dict):
    exits = []
    edges = []
    nodes_coordinates = {}
    dec_nodes = {}

    for idx, node in enumerate(graph_dict["nodes"]):
        dec_nodes[node] = idx

        if graph_dict["nodes"][node]["color"] == "green":
            exits.append(idx)

    for i, node in enumerate(graph_dict["layouts"]["nodes"]):
        coordinates = graph_dict["layouts"]["nodes"][node]
        dec_node = dec_nodes[node]
        nodes_coordinates[dec_node] = coordinates

    for edge in graph_dict["edges"]:
        node1_name = graph_dict["edges"][edge]["source"]
        node2_name = graph_dict["edges"][edge]["target"]
        if node1_name in dec_nodes and node2_name in dec_nodes:
            node1 = dec_nodes[node1_name]
            node2 = dec_nodes[node2_name]

            n1x, n1y = (nodes_coordinates[node1]["x"], nodes_coordinates[node1]["y"])
            n2x, n2y = (nodes_coordinates[node2]["x"], nodes_coordinates[node2]["y"])

            d = math.sqrt((n2x - n1x) ** 2 + (n2y - n1y) ** 2)

            edges.append((node1, node2, d))
            edges.append((node2, node1, d))

    graph_dict["graph_filter"] = {
        "exits": exits,
        "edges": edges,
        "node_coordinates": nodes_coordinates,
        "dec_nodes": dec_nodes,
    }
    return graph_dict
