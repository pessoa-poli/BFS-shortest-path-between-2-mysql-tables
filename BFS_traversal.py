import json as js

TARGET_JSON_FILE = './pickled_db_relations.json'
TARGET_OUTPUT_FILE = 'output_with_fathers.json'
ORIGIN_NODE = 'TBMarca'
TARGET_NODE = 'TBProduto'


def load_nodes_dic_from_json(target_json_file):
    with open(target_json_file, 'r') as f:
        dic_str = f.read()
        dic_dic = js.loads(dic_str)
    return dic_dic


def storeNodesList(nodes_list: dict, output_file: str):
    nodes_list_str = js.dumps(nodes_list)
    with open(file=output_file, mode='w') as f:
        f.write(nodes_list_str)


def buildPathString(dic: dict, origin_node: str, target_node: str):
    path = f'{target_node}'
    path_found = False
    while not path_found:
        print(f'Current path is:\n{path}\n{"#"*20}')
        node_father = dic[target_node]['father_node']
        if not node_father:
            break
        if node_father == origin_node:
            path_found = True
        path = f'{node_father}->'+path
        target_node = node_father
    if not path_found:
        print('Path not found.')
        return ''
    return path


def BFS_Traversal(origin_node: str, target_node: str):
    dic = load_nodes_dic_from_json(TARGET_JSON_FILE)
    queue = []
    # Add origin_node to queue
    queue.append({origin_node: dic[origin_node]})
    # Mark added node as visited
    dic[origin_node]['visited'] = True

    # While queue is not empty do
    while queue:
        print(f'queue is:\n {queue}\n{"#"*20}')
        node_of_the_turn = queue.pop(0)
        for key in node_of_the_turn:  # There will be only one key
            # Node is a dictionary of tableNames
            for node in node_of_the_turn[key]['adjNodes']:
                if not dic[node]['visited']:
                    dic[node]['visited'] = True
                    queue.append({node: dic[node]})
                    dic[node]['father_node'] = key
    return dic


if __name__ == '__main__':
    dic = BFS_Traversal(ORIGIN_NODE, TARGET_NODE)
    path = buildPathString(dic, ORIGIN_NODE, TARGET_NODE)
    print(path)
