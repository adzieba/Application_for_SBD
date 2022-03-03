from tkinter import *
from Plates import *
from PIL     import ImageTk, Image
import sys, os, json

class Table():

    def __init__( self, gui, type, move_directions, x_index, y_index, name ):
        self.gui = gui
        self.move_directions = move_directions
        self.x_index = x_index
        self.y_index = y_index
        self.name = name
        self.x_pos = self.x_index * self.gui.tile_width
        self.y_pos = self.y_index * self.gui.tile_height
        self.tile_x_center = self.x_pos + self.gui.tile_width  / 2
        self.tile_y_center = self.y_pos + self.gui.tile_height / 2

        self.label = None
        self.plate_on_table = False
        self.callvalue = 0
        self.sendvalue = 0
        self.menu = None

        self.frame = Frame( self.gui.visualization_background, height = self.gui.tile_height, width = self.gui.tile_width )
        self.frame.pack_propagate( 0 )
        self.frame.place( x = self.x_pos, y = self.y_pos )
        
        self.framebackground = Label( self.frame )
        self.framebackground.pack( fill = BOTH )
   
    def getPaths( self, mode ):

        with open( os.path.join( sys.path[0], "config.json" ), 'r') as infile:
            config_file = json.load( infile ) 

            if 'paths' in config_file['tables']['objects'][self.name] and len( config_file['tables']['objects'][self.name] ) > 0 :
                
                paths = {}
                
                for path in config_file['tables']['objects'][self.name]['paths']:

                    destination_table_x = config_file['tables']['objects'][self.name]['paths'][path]['destination']['x']
                    destination_table_y = config_file['tables']['objects'][self.name]['paths'][path]['destination']['y']
                    
                    if mode == 0:
                        if self.gui.tables_list[destination_table_y][destination_table_x].plate_on_table:
                            paths[ path ] = config_file['tables']['objects'][self.name]['paths'][path]

                    elif mode == 1:
                        if not self.gui.tables_list[destination_table_y][ destination_table_x].plate_on_table:
                            paths[ path ] = config_file['tables']['objects'][self.name]['paths'][path]
                        else:
                            if 'queued' in config_file['tables']['objects'][self.name]['paths'][path]:
                                paths[ path ] = config_file['tables']['objects'][self.name]['paths'][path]

                    elif mode == 2:
                        paths[ path ] = config_file['tables']['objects'][self.name]['paths'][path]

                return paths

            else:
                return False
    
    def deletePath( self, path_name ):

        with open( os.path.join( sys.path[0], "config.json" ), 'r') as infile:
            config_file = json.load( infile )

        if path_name in config_file['tables']['objects'][self.name]['paths']:
            del config_file['tables']['objects'][self.name]['paths'][path_name]
            
        if len( config_file['tables']['objects'][self.name]['paths'] ) == 0:
            del config_file['tables']['objects'][self.name]['paths']

        with open( os.path.join( sys.path[0], "config.json" ), 'w') as outfile:
            json.dump( config_file, outfile, indent = 4 )

    def setOccupied( self ):
        self.plate_on_table = True

    def setFree( self ):
        self.plate_on_table = False

    def isFree( self ):
        return not self.plate_on_table

class DemouldingTable( Table ):

    def __init__( self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__( gui, type, move_directions, x_index, y_index, name )

        if 'right' in self.move_directions: 
            self.framebackground["image"] = self.gui.table_images[2]
        elif 'left' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[5]
        elif 'up' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[6]
        elif 'down' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[7]

        self.framebackground.bind( '<Button-3>', self.showMenu )

    def showMenu( self, event ):

        if self.menu != None:
            self.menu.destroy()
        
        paths = self.getPaths( 0 ) 

        self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
                
        if paths:
            
            call_menu = Menu( self.menu, tearoff = 0 )

            for path in paths:
                call_menu.add_command( label = path, command = None ) 
                
            self.menu.add_cascade( label = "Przywołaj z ",  menu = call_menu )

        paths2 = self.getPaths( 2 )

        if paths2:   
            self.menu.add_separator()

            for path in paths2:
                sub_menu = Menu( self.menu, tearoff = 0 )
                sub_menu.add_command(  label = "Usuń", command = lambda path=path: self.deletePath( path ) )
                sub_menu.add_command(  label = "Zmień nazwę" )
                self.menu.add_cascade( label = str( path ),  menu = sub_menu )  

        self.menu.tk_popup( event.x_root, event.y_root )

class MouldingTable( Table ):

    def __init__( self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__( gui, type, move_directions, x_index, y_index, name )
        
        if 'right' in self.move_directions: 
            self.framebackground["image"] = self.gui.table_images[2]
        elif 'left' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[5]
        elif 'up' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[6]
        elif 'down' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[7]  

        self.framebackground.bind( '<Button-3>', self.showMenu )

    def showMenu( self, event ):

        if self.menu != None:
            self.menu.destroy()

        self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
                
        paths = self.getPaths( 0 ) 
        
        if paths:
            
            call_menu = Menu( self.menu, tearoff = 0 )

            for path in paths:
                call_menu.add_command( label = path, command = None ) 
                
            self.menu.add_cascade( label = "Przywołaj z ",  menu = call_menu )   

        paths2 = self.getPaths( 2 )

        if paths2:   
            self.menu.add_separator()

            for path in paths2:
                sub_menu = Menu( self.menu, tearoff = 0 )
                sub_menu.add_command(  label = "Usuń", command = lambda path=path: self.deletePath( path ) )
                sub_menu.add_command(  label = "Zmień nazwę" )
                self.menu.add_cascade( label = str( path ),  menu = sub_menu )  

        self.menu.tk_popup( event.x_root, event.y_root )

class ComposingTable( Table ):

    def __init__( self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__( gui, type, move_directions, x_index, y_index, name )
    
        if 'right' in self.move_directions: 
            self.framebackground["image"] = self.gui.table_images[2]
        elif 'left' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[5]
        elif 'up' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[6]
        elif 'down' in self.move_directions:
            self.framebackground["image"] = self.gui.table_images[7]

        self.framebackground.bind( '<Button-3>', self.showMenu )
        
    def showMenu( self, event ):

        if self.menu != None:
            self.menu.destroy()

        self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
        self.menu.add_command( label = "Nowa płyta", command = self.startNewPlate )
        
        paths = self.getPaths( 0 ) 
        
        if paths:
            
            call_menu = Menu( self.menu, tearoff = 0 )

            for path in paths:
                call_menu.add_command( label = path, command = None ) 
                
            self.menu.add_cascade( label = "Przywołaj z ",  menu = call_menu )    

        paths2 = self.getPaths( 2 )

        if paths2:   
            self.menu.add_separator()

            for path in paths2:
                sub_menu = Menu( self.menu, tearoff = 0 )
                sub_menu.add_command(  label = "Usuń", command = lambda path=path: self.deletePath( path ))
                sub_menu.add_command(  label = "Zmień nazwę" )
                self.menu.add_cascade( label = str( path ),  menu = sub_menu )  

        self.menu.tk_popup( event.x_root, event.y_root )

    def startNewPlate( self ):
        plate = Plate( self )

class TurnTable( Table ):

    def __init__( self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__( gui, type, move_directions, x_index, y_index, name )
        self.position = "horizontal"
        self.framebackground["image"] = self.gui.table_images[3]
        self.framebackground.bind( '<Button-3>', self.showMenu )

    def showMenu( self, event ):

        if self.menu != None:
            self.menu.destroy()
        
        self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
        self.menu.add_command( label = "Obróć stół", command = self.turnTable )

        paths = self.getPaths( 0 ) 

        if paths:
            
            call_menu = Menu( self.menu, tearoff = 0 )

            for path in paths:
                call_menu.add_command( label = path, command = None ) 
                
            self.menu.add_cascade( label = "Przywołaj z ",  menu = call_menu )   

        paths2 = self.getPaths( 2 )

        if paths2:   
            self.menu.add_separator()

            for path in paths2:
                sub_menu = Menu( self.menu, tearoff = 0 )
                sub_menu.add_command(  label = "Usuń", command = lambda path=path: self.deletePath( path ) )
                sub_menu.add_command(  label = "Zmień nazwę" )
                self.menu.add_cascade( label = str( path ),  menu = sub_menu )  

        self.menu.tk_popup( event.x_root, event.y_root )

    def turnTable( self ):
        
        if self.position == "horizontal":
            self.framebackground["image"] = self.gui.table_images[8]
            self.position = "vertical"
        elif self.position == "vertical":
            self.framebackground["image"] = self.gui.table_images[3]
            self.position = "horizontal"

class ConveyorTable( Table ):

    def __init__( self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__( gui, type, move_directions, x_index, y_index, name )

        if type == "|":
            self.framebackground["image"] = self.gui.table_images[4]
            
        elif type == "-":
            self.framebackground["image"] = self.gui.table_images[1]