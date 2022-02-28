from tkinter import *
from Plates import *
from PIL     import ImageTk, Image

class Table( Button ):

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
        self.frame = Frame( self.gui.visualization_background, height = self.gui.tile_height, width = self.gui.tile_width )
        self.frame.pack_propagate( 0 )
        self.frame.place( x = self.x_pos, y = self.y_pos )
        super().__init__( self.frame )
        self.config( relief = FLAT, borderwidth = 0 )        
        self.pack( fill = BOTH, expand = 1 )

class DemouldingTable( Table ):

    def __init__(self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__(gui, type, move_directions, x_index, y_index, name )

        if 'right' in self.move_directions: 
            self["image"] = self.gui.table_images[2]
        elif 'left' in self.move_directions:
            self["image"] = self.gui.table_images[5]
        elif 'up' in self.move_directions:
            self["image"] = self.gui.table_images[6]
        elif 'down' in self.move_directions:
            self["image"] = self.gui.table_images[7]

        self.bind( '<Button-3>', self.showMenu )

    def showMenu( self, event ):
        menu = Menu( self.gui.visualization_background, tearoff = 0 )
        menu.add_command( label = "Wezwij płytę", command = None )
        menu.add_separator()
        menu.add_command( label = "Wyślij płytę", command = None )        
        menu.add_radiobutton( label = 'A', var = self.sendvalue, value = 0 )      
        menu.add_radiobutton( label = 'B', var = self.sendvalue, value = 1 )      
        menu.add_radiobutton( label = 'C', var = self.sendvalue, value = 2 ) 
        menu.tk_popup( event.x_root, event.y_root )

class MouldingTable( Table ):

    def __init__(self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__(gui, type, move_directions, x_index, y_index, name )
        
        if 'right' in self.move_directions: 
            self["image"] = self.gui.table_images[2]
        elif 'left' in self.move_directions:
            self["image"] = self.gui.table_images[5]
        elif 'up' in self.move_directions:
            self["image"] = self.gui.table_images[6]
        elif 'down' in self.move_directions:
            self["image"] = self.gui.table_images[7]  

        self.bind( '<Button-3>', self.showMenu )

    def showMenu( self, event ):
        menu = Menu( self.gui.visualization_background, tearoff = 0 )
        menu.add_command( label = "Wyślij płytę", command = None )
        menu.add_separator()
        menu.add_command( label = "Wezwij płytę", command = None ) 
        menu.add_radiobutton( label = 'A', var = self.callvalue, value = 0 )      
        menu.add_radiobutton( label = 'B', var = self.callvalue, value = 1 )      
        menu.add_radiobutton( label = 'C', var = self.callvalue, value = 2 ) 
        menu.tk_popup( event.x_root, event.y_root )

class ComposingTable( Table ):

    def __init__(self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__(gui, type, move_directions, x_index, y_index, name )
    
        if 'right' in self.move_directions: 
            self["image"] = self.gui.table_images[2]
        elif 'left' in self.move_directions:
            self["image"] = self.gui.table_images[5]
        elif 'up' in self.move_directions:
            self["image"] = self.gui.table_images[6]
        elif 'down' in self.move_directions:
            self["image"] = self.gui.table_images[7]

        self.bind( '<Button-3>', self.showMenu )
        self.gui.composing_tables.append( self )

    def showMenu( self, event ):
        menu = Menu( self.gui.visualization_background, tearoff = 0 )
        menu.add_command( label = "Nowa płyta", command = self.startNewPlate )
        menu.tk_popup( event.x_root, event.y_root )

    def startNewPlate( self ):
        plate = Plate( self )

class TurnTable( Table ):

    def __init__(self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__(gui, type, move_directions, x_index, y_index, name )
        self.position = "horizontal"
        self["image"] = self.gui.table_images[3]
        self.bind( '<Button-3>', self.showMenu )

    def showMenu( self, event ):
        menu = Menu( self.gui.visualization_background, tearoff = 0 )
        menu.add_command( label = "Obróć stół", command = self.turnTable )
        menu.tk_popup( event.x_root, event.y_root )

    def turnTable( self ):
        
        if self.position == "horizontal":
            self["image"] = self.gui.table_images[8]
            self.position = "vertical"
        elif self.position == "vertical":
            self["image"] = self.gui.table_images[3]
            self.position = "horizontal"

class ConveyorTable( Table ):

    def __init__(self, gui, type, move_directions, x_index, y_index, name ):
        super().__init__(gui, type, move_directions, x_index, y_index, name )

        if type == "|":
            self["image"] = self.gui.table_images[4]
            
        elif type == "-":
            self["image"] = self.gui.table_images[1]