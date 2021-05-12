def parse_rules():
    adjacency_matrix = {}

    with open("rules.txt") as f:
        rule = f.readline()
        while rule != "":
            rule_words = rule.split(" ")
            parent_color = " ".join(rule_words[:2])

            if parent_color not in adjacency_matrix:
                adjacency_matrix[parent_color] = {} # create a list to hold the children of this color
            if "no other bags" not in rule:
                n_children = int((len(rule_words) - 4) / 4) # strip out the "x y bags contain...", then each rule is a 4 word string of the form "n x y bag(s)"
                for a in range(n_children):
                    child_color = " ".join(rule_words[4 * (a + 1) + 1: 4 * (a + 1) + 3])
                    if child_color not in adjacency_matrix:
                        adjacency_matrix[child_color] = {}
                    # children_map[parent_color][" ".join(rule_words[4 * (a + 1) + 1: 4 * (a + 1) + 3])] = int(rule_words[4 * (a + 1)])
                    adjacency_matrix[parent_color][child_color] = 1 # 1 means the first color contains the second color
                    adjacency_matrix[child_color][parent_color] = -1 # -1 means the first color is contained by the second color
            rule = f.readline()

    return adjacency_matrix


def remove_edge_between(adjacency_matrix, color_1, color_2):
    adjacency_matrix[color_1][color_2] = 0
    adjacency_matrix[color_2][color_1] = 0


def main():
    adjacency_matrix = parse_rules()
    source_nodes = [color for color in adjacency_matrix]
    for parent_color in adjacency_matrix:
        for other_parent_color in adjacency_matrix:
            if parent_color in adjacency_matrix[other_parent_color] and adjacency_matrix[parent_color][other_parent_color] == -1: # this means that other_parent_color can contain parent_color
                source_nodes.remove(parent_color)
                break # once we know parent_color isn't a source node, we can stop looking

    # kahn's algorithm
    sorted_nodes = []
    while len(source_nodes) > 0:
        source_color = source_nodes.pop()
        sorted_nodes.append(source_color)
        for child_color in adjacency_matrix[source_color]:
            if adjacency_matrix[source_color][child_color] == 1: # if source color contains the child color...
                remove_edge_between(adjacency_matrix, source_color, child_color)

            if child_color not in sorted_nodes:
                child_color_still_has_incoming_edges = False
                for connected_color in adjacency_matrix[child_color]:
                    if adjacency_matrix[child_color][connected_color] == -1:
                        child_color_still_has_incoming_edges = True
                        break

                if not child_color_still_has_incoming_edges: # if there are no edges still incoming to the child color...
                    source_nodes.append(child_color) # then it's a new source color

    print(sorted_nodes)


if __name__ == '__main__':
    main()
