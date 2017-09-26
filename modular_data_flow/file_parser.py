from modular_data_flow import modular_testing as m


def get_lines_of_file_as_lists(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def populate_current_nodes_and_links_dicts(lines):
    info_type = ''
    for i in range(len(lines)):
        line = lines[i].lower()  # get each line, make sure it is all lowercase
        if line == 'nodes' and info_type == '':
            info_type = 'n'  # to determine whether we are looking at node or link assignment

        elif line == 'links' and info_type == 'n':
            info_type = 'l'  # to determine whether we are looking at node or link assignment

        elif info_type == 'n':  # looking at node assignment
            line = line.split()
    # there must be 2 or 3 values in this line (one integer followed by one or two words)
            if 2 <= len(line) <= 3:
                k, kind = line[0], line[1]
    # first value must be unique integer that has not been used
                if k.isdigit() and k not in current_nodes_dict:
                    key = k  # will be key in current_nodes_dict
    # second value must be the name of a node kind that can be made
                    if kind in all_nodes_dict:
                        temp_object = all_nodes_dict[kind]  # this is either an empty string or another dictionary
    # either: temp_object must be an empty string
                        if temp_object == '':
                            value = m.get_node(kind)  # this node instance will go into current_nodes_dict
    # or: temp_object must be a dictionary
                        elif isinstance(temp_object, dict):
    # then there must be three values in this line and the third must be a valid category name
                            if len(line) == 3 and line[2] in temp_object:
                                value = m.get_node(kind + ' ' + line[2]) # node instance will go into current_nodes_dict
                            else:
                                raise Exception("Expecting valid node category after node kind, in line " + str(i + 1))
                    else:
                        raise Exception("Expecting valid node kind after integer, in line " + str(i+1))
                else:
                    raise Exception("Expecting new unique integer at beginning of line " + str(i+1))
            else:
                raise Exception("Expecting an integer and one or two words in line " + str(i + 1))
            current_nodes_dict[key] = value  # if we get this far, add above assigned key/value to current_nodes_dict

        elif info_type == 'l':  # looking at link assignment
            line = line.split()
    # there must be exactly two integers in each line
            if len(line) == 2:
                from_node, to_node = line[0], line[1]
    # each integer must represent a node that was assigned earlier in the file
                if from_node in current_nodes_dict and to_node in current_nodes_dict:
                    current_links_dict[from_node] = to_node  # add the link connection (ints for each node) to a dict
                else:
                    raise Exception("Attempting link with/to node that was not instantiated, in line " + str(i+1))
            else:
                raise Exception("Expecting two integers separated by a space (describing a link), in line " + str(i+1))

        else:
            raise Exception("Syntax error in line " + str(i+1))

# what about duplicate entries/lines in links


def link_up_nodes():
    for frm, to in current_links_dict.items():
        frm_node = current_nodes_dict[frm]
        to_node = current_nodes_dict[to]
        frm_node.assign_output_node(to_node)
        to_node.assign_input_node(frm_node)


all_nodes_dict, current_nodes_dict, current_links_dict = m.get_modules_dict(), {}, {}
file_lines = get_lines_of_file_as_lists('test.txt')
populate_current_nodes_and_links_dicts(file_lines)

link_up_nodes()

done = False
while not done:
    done_counter = 0
    for key, node in current_nodes_dict.items():
        if not node.is_done():
            node.do_work()
        else:
            done_counter += 1
    if done_counter == len(current_nodes_dict):
        done = True

#print(current_nodes_dict)
#print(current_links_dict)
