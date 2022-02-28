import os, sys, json

class ConfigGenerator():
    
    def __init__( self ):
        print("Generator init")

        if self.import_layout_file( "linelayout.txt" ):
            self.generate_config()
        else:
            print("layout file error")

    def __del__( self ):
        print("Generator del")

    def import_layout_file( self, file ):
        columns_length_error = False

        #open file with tables layout
        with open( os.path.join( sys.path[0], file ), "r" ) as f:
            self.line_layout = f.readlines()
            self.rows = len( self.line_layout )

        for i in range( self.rows ):

            #remove spaces
            self.line_layout[i] = self.line_layout[i].rstrip()

            if i == 0:
                # columns = character count in first line
                self.columns = len( self.line_layout[i] )
            else:
                if len( self.line_layout[i] ) != self.columns:
                    columns_length_error = True
                    print( "columns count error in line: ", i )

        if self.rows > 0 and self.columns > 0 and not columns_length_error:
            return True
        else:
            return False

    def generate_config( self ):

        self.config_file = {}
        self.tile_width  = 50
        self.tile_height = 50
        self.app_extra_width = 400
        self.app_extra_height = 300

        self.config_file['layout'] = self.line_layout
        self.config_file['window'] = { 'rows':self.rows, 'columns':self.columns, 'tile_width':self.tile_width, 'tile_height':self.tile_height,
                                       'table_area_width':self.columns * self.tile_width, 'table_area_height':self.rows * self.tile_height,
                                       'app_extra_width': self.app_extra_width, 'app_extra_height':self.app_extra_height,  
                                       'app_width':self.columns * self.tile_width + self.app_extra_width, 'app_height':self.rows * self.tile_height + self.app_extra_height }
        
        self.config_file['graphics'] = { 'folder':'Graphics' }
        
        self.config_file['tables'] = {}
        self.config_file['tables']['types'] = {}
        self.config_file['tables']['types']['.'] = { 'name':'blank'}
        self.config_file['tables']['types']['|'] = { 'name':'conveyor_v', 'moves':[ 'up', 'down' ], 'picture':'conveyor.png' }
        self.config_file['tables']['types']['-'] = { 'name':'conveyor_h', 'moves':[ 'left', 'right' ], 'picture':'conveyor.png' }
        self.config_file['tables']['types']['+'] = { 'name':'turntable' , 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'turntable.png' }
        self.config_file['tables']['types']['D'] = { 'name':'moulding'  , 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'station.png' }
        self.config_file['tables']['types']['M'] = { 'name':'demoulding', 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'station.png' }
        self.config_file['tables']['types']['C'] = { 'name':'composing' , 'moves':[ 'up', 'down', 'left', 'right' ], 'picture':'station.png' }

        table_num = 0
        self.config_file['tables']['objects'] = {}

        for y in range( self.rows ):

            for x in range( self.columns ):

                if self.line_layout[y][x] in self.config_file['tables']['types']:

                    if "moves" in self.config_file['tables']['types'][self.line_layout[y][x]]:

                        move_directions = []
                        move_directions = self.check_moves( x, y ) 
                                        
                        if len( move_directions ) > 0:
                            table_name = self.config_file['tables']['types'][self.line_layout[y][x]]['name'] + str( table_num )
                            self.config_file['tables']['objects'][table_name] = { 'type':self.line_layout[y][x], 'x':x, 'y':y, 'move_directions':move_directions }
                            table_num += 1

                else:
                    print( self.line_layout[y][x], " is unknown type, finish creating")
                    sys.exit()

        with open( os.path.join( sys.path[0], "config.json" ), 'w') as outfile:
            json.dump( self.config_file, outfile, indent = 4 )
        
        print("Config generated")

    def check_moves( self, x, y ):
        
        move_directions = []
        type_move_directions = []
        table_type = self.line_layout[y][x]

        if table_type in self.config_file['tables']['types']:
            type_move_directions = self.config_file['tables']['types'][table_type]['moves']
        
        for direction in type_move_directions:
            
            table_type = self.line_layout[y][x]
            up_table_type    = False
            down_table_type  = False
            left_table_type  = False
            right_table_type = False

            if y - 1 >= 0:
                if self.line_layout[y - 1][x] != '.':
                    up_table_type = self.line_layout[y - 1][x]

            if y + 1 <= self.rows:   
                if self.line_layout[y + 1][x] != '.':
                    down_table_type = self.line_layout[y + 1][x]

            if x - 1 >= 0:    
                if self.line_layout[y][x - 1] != '.':
                    left_table_type = self.line_layout[y][x - 1]

            if x + 1 <= self.columns:    
                if self.line_layout[y][x + 1] != '.':
                    right_table_type = self.line_layout[y][x + 1]

            if direction == "up":
                if up_table_type:
                    if ( table_type in ['M','D','C' ] and not up_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                        if "down" in self.config_file['tables']['types'][up_table_type]['moves']:
                            
                            if ( table_type in ['M','D','C' ] and up_table_type == '|' ):
                                move_directions = []
                                move_directions.append( 'up' )
                                break

                            move_directions.append( 'up' )
            
            if direction == "down":
                if down_table_type:
                    if ( table_type in ['M','D','C' ] and not down_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                        if "up" in self.config_file['tables']['types'][down_table_type]['moves']:

                            if ( table_type in ['M','D','C' ] and down_table_type == '|' ):
                                move_directions = []
                                move_directions.append( 'down' )
                                break

                            move_directions.append( 'down' )

            if direction == "left":
                if left_table_type: 
                    if ( table_type in ['M','D','C' ] and not left_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                        if "right" in self.config_file['tables']['types'][left_table_type]['moves']:
                        
                            if ( table_type in ['M','D','C' ] and left_table_type == '-' ):
                                move_directions = []
                                move_directions.append( 'left' )
                                break
                        
                        move_directions.append( 'left' )

            if direction == "right":
                if right_table_type: 
                    if ( table_type in ['M','D','C' ] and not right_table_type in ['M','D','C' ]) or not table_type in ['M','D','C' ]:
                        if "left" in self.config_file['tables']['types'][right_table_type]['moves']:

                            if ( table_type in ['M','D','C' ] and right_table_type == '-' ):
                                move_directions = []
                                move_directions.append( 'right' )
                                break

                            move_directions.append( 'right' )

        return move_directions

config = ConfigGenerator()