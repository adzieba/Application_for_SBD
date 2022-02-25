import os, sys, json

# script generates json file with basic config for application

# check if linelayout file has correct structure
def import_layout_file( file ):
    columns_length_error = False

    #open file with tables layout
    with open( os.path.join( sys.path[0], file ), "r" ) as f:
        layout = f.readlines()
        rows = len( layout )

    for i in range( rows ):

        #remove spaces
        layout[i] = layout[i].rstrip()

        if i == 0:
            # columns = character count in first line
            columns = len( layout[i] )
        else:
            if len( layout[i] ) != columns:
                columns_length_error = True
                print( "columns count error in line: ", i )

    if rows > 0 and columns > 0 and not columns_length_error:
        return [ rows, columns, layout]
    else:
        return False

def check_moves( line_layout, column, row ):
    
    move_directions = []
    type_move_directions = []
    table_type = line_layout[row][column]

    if table_type in config_file['tables']['types']:
        type_move_directions = config_file['tables']['types'][table_type]['moves']
    
    for direction in type_move_directions:
        
        table_type = line_layout[row][column]
        up_table_type    = False
        down_table_type  = False
        left_table_type  = False
        right_table_type = False

        if row - 1 >= 0:
            if line_layout[row - 1][column] != '.':
                up_table_type = line_layout[row - 1][column]

        if row + 1 <= rows:   
            if line_layout[row + 1][column] != '.':
                down_table_type = line_layout[row + 1][column]

        if column - 1 >= 0:    
            if line_layout[row][column - 1] != '.':
                left_table_type = line_layout[row][column - 1]

        if column + 1 <= columns:    
            if line_layout[row][column + 1] != '.':
                right_table_type = line_layout[row][column + 1]

        if direction == "up":
            if up_table_type:
                if ( table_type in ['M','D','C' ] and not up_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                    if "down" in config_file['tables']['types'][up_table_type]['moves']:
                        
                        if ( table_type in ['M','D','C' ] and up_table_type == '|' ):
                            move_directions = []
                            move_directions.append( 'up' )
                            break

                        move_directions.append( 'up' )
        
        if direction == "down":
            if down_table_type:
                if ( table_type in ['M','D','C' ] and not down_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                    if "up" in config_file['tables']['types'][down_table_type]['moves']:

                        if ( table_type in ['M','D','C' ] and down_table_type == '|' ):
                            move_directions = []
                            move_directions.append( 'down' )
                            break

                        move_directions.append( 'down' )

        if direction == "left":
            if left_table_type: 
                if ( table_type in ['M','D','C' ] and not left_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                    if "right" in config_file['tables']['types'][left_table_type]['moves']:
                     
                     if ( table_type in ['M','D','C' ] and left_table_type == '-' ):
                            move_directions = []
                            move_directions.append( 'left' )
                            break
                     
                     move_directions.append( 'left' )


        if direction == "right":
            if right_table_type: 
                if ( table_type in ['M','D','C' ] and not right_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                    if "left" in config_file['tables']['types'][right_table_type]['moves']:

                        if ( table_type in ['M','D','C' ] and right_table_type == '-' ):
                            move_directions = []
                            move_directions.append( 'right' )
                            break

                        move_directions.append( 'right' )

    return move_directions

results = import_layout_file( "linelayout.txt" )

if not results:
    print("layout file error")
else:
    rows    = results[0]
    columns = results[1]
    layout  = results[2]

    config_file = {}
    tile_width  = 50
    tile_height = 50

    config_file['layout'] = layout
    config_file['window'] = { 'rows':rows, 'columns':columns, 'tile_width':tile_width, 'tile_height':tile_height,
                              'table_area_width':columns * tile_width, 'table_area_height':rows * tile_height, 
                              'app_width':columns * tile_width + 200, 'app_height':rows * tile_height + 200 }
      
    config_file['graphics'] = { 'folder':'Graphics2' }
    
    config_file['tables'] = {}
    config_file['tables']['types'] = {}
    config_file['tables']['types']['.'] = { 'name':'blank'}
    config_file['tables']['types']['|'] = { 'name':'conveyor_v', 'moves':[ 'up', 'down' ], 'picture':'conveyor.png' }
    config_file['tables']['types']['-'] = { 'name':'conveyor_h', 'moves':[ 'left', 'right' ], 'picture':'conveyor.png' }
    config_file['tables']['types']['+'] = { 'name':'turntable' , 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'turntable.png' }
    config_file['tables']['types']['D'] = { 'name':'moulding'  , 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'station.png' }
    config_file['tables']['types']['M'] = { 'name':'demoulding', 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'station.png' }
    config_file['tables']['types']['C'] = { 'name':'composing' , 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'station.png' }

    table_num = 0
    config_file['tables']['objects'] = {}

    for y in range( rows ):

        for x in range( columns ):

            if layout[y][x] in config_file['tables']['types']:

                if "moves" in config_file['tables']['types'][layout[y][x]]:

                    move_directions = []
                    move_directions = check_moves( layout, x, y ) 
                                    
                    if len( move_directions ) > 0:
                        table_name = config_file['tables']['types'][layout[y][x]]['name'] + str( table_num )
                        config_file['tables']['objects'][table_name] = { 'type':layout[y][x], 'x':x, 'y':y, 'move_directions':move_directions }
                        table_num += 1

            else:
                print( layout[y][x], " is unknown type, script killed")
                sys.exit()

    with open( os.path.join( sys.path[0], "config.json" ), 'w') as outfile:
        json.dump(config_file, outfile, indent = 4 )
