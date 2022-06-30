import re
import json as js
FILE_TARGET = 'script.sql'
JSON_OUTPUT_FILE = 'pickled_db_relations.json'
CURRENT_TABLE = ''
NODES_DIC = {}


def process_line(line):
    global CURRENT_TABLE
    global NODES_DIC
    # If found a table name
    found_table = re.search('(?<=create table if not exists )(\w+)$', line)
    found_reference = re.search(
        '^.+?foreign key \((.+?)\) references (.+?) \((.+?)\),?$', line)
    if found_table:
        #print(f'Table name is {found_table.group()}')
        CURRENT_TABLE = found_table.group()
        if CURRENT_TABLE not in NODES_DIC:
            NODES_DIC[CURRENT_TABLE] = {
                'visited': False, 'adjNodes': {}, 'father_node': None}
    if found_reference:
        fk = found_reference.groups()[0]
        target_table = found_reference.groups()[1]
        if target_table not in NODES_DIC:
            NODES_DIC[target_table] = {
                'visited': False, 'adjNodes': {}, 'father_node': None}
        target_table_fk = found_reference.groups()[2]
        # Add edge from CURRENT_TABLE to target_table
        if target_table not in NODES_DIC[CURRENT_TABLE]:
            NODES_DIC[CURRENT_TABLE]['adjNodes'][target_table] = fk
        # Add way back
        if CURRENT_TABLE not in NODES_DIC[target_table]['adjNodes']:
            NODES_DIC[target_table]['adjNodes'][CURRENT_TABLE] = fk
        print(
            f'Found a reference of table {CURRENT_TABLE}.{fk} to table {target_table}.{target_table_fk}')


def storeNodesList(nodes_list):
    global JSON_OUTPUT_FILE
    nodes_list_str = js.dumps(nodes_list)
    with open(file=JSON_OUTPUT_FILE, mode='w') as f:
        f.write(nodes_list_str)


def read_and_process_lines():
    global NODES_DIC
    # Using readline()
    file1 = open(FILE_TARGET, 'r')
    count = 0

    while True:
        count += 1

        # Get next line from file
        line = file1.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        process_line(line)

        #print("Line{}: {}".format(count, line.strip()))

    file1.close()
    storeNodesList(NODES_DIC)
    print(f"We finished parsing {FILE_TARGET}")


if __name__ == '__main__':
    read_and_process_lines()
