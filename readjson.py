import json

with open('sample.json', 'r') as infile:
    tables = json.load( infile )

for index in tables:
    print(index)
    print(type(index))
    print( tables[ index ] )

tables['t6'] = { 'name':'table6', 'type':'turn_table', 'x':1, 'y':6 } 

with open('sample.json', 'w') as outfile:
    json.dump(tables, outfile, indent = 4 )
