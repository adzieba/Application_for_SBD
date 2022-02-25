import json

tables = { 't1': { 'name':'table1', 'type':'conveyor',   'x':1, 'y':1, 'move_directions':[1,2] },
           't2': { 'name':'table2', 'type':'turn_table', 'x':1, 'y':2 } }

tables['t3'] = {}
tables['t3']['name'] = 'table3'
tables['t3']['type'] = 'demoulding station'
tables['t3']['x'] = 1
tables['t3']['y'] = 3

index = 't4'

tables[index] = {}
tables[index]['name'] = 'table4'
tables[index]['type'] = 'moulding station'
tables[index]['x'] = 1
tables[index]['y'] = 4

tables['t5'] = { 'name':'table5', 'type':'turn_table', 'x':1, 'y':5 }

print(tables)

with open('sample.json', 'w') as outfile:
    json.dump(tables, outfile, indent = 4 )
    