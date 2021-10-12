from tkinter import *
from plate_class import *
from PIL     import ImageTk, Image

class Table( Button ):

    def __init__( self, gui, move_directions, x_index, y_index ):
        self.gui = gui
        self.move_directions = move_directions
        self.x_index = x_index
        self.y_index = y_index
        self.x_pos = self.x_index * self.gui.tile_width
        self.y_pos = self.y_index * self.gui.tile_height
        self.tile_x_center = self.x_pos + self.gui.tile_width  / 2
        self.tile_y_center = self.y_pos + self.gui.tile_height / 2
        self.type  = "default"
        self.position = "default"
        self.plate_on_table = False
        self.callvalue = 0
        self.sendvalue = 0
        
        # ppm moulding table
        self.moulding_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.moulding_menu.add_command( label = "Wyślij płytę", command = None )
        self.moulding_menu.add_separator()
        self.moulding_menu.add_command( label = "Wezwij płytę", command = None ) 
        self.moulding_menu.add_radiobutton( label='A', var = self.callvalue, value = 0 )      
        self.moulding_menu.add_radiobutton( label='B', var = self.callvalue, value = 1 )      
        self.moulding_menu.add_radiobutton( label='C', var = self.callvalue, value = 2 ) 
         
        # ppm demoulding table
        self.demoulding_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.demoulding_menu.add_command( label = "Wezwij płytę", command = None )
        self.demoulding_menu.add_separator()
        self.demoulding_menu.add_command( label = "Wyślij płytę", command = None )        
        self.demoulding_menu.add_radiobutton( label='A', var = self.sendvalue, value = 0 )      
        self.demoulding_menu.add_radiobutton( label='B', var = self.sendvalue, value = 1 )      
        self.demoulding_menu.add_radiobutton( label='C', var = self.sendvalue, value = 2 ) 
       
        # ppm composing table
        self.composing_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.composing_menu.add_command( label = "Nowa płyta", command = self.table_place_new_plate )

        # ppm turntable
        self.turntable_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.turntable_menu.add_command( label = "Obróć stół", command = self.table_turn )
         
        self.frame = Frame( self.gui.window_background, height = self.gui.tile_height, width = self.gui.tile_width )
        self.frame.pack_propagate( 0 )
        self.frame.place( x = self.x_pos, y = self.y_pos )
        super().__init__( self.frame )
        
        if self.gui.tables_config[self.y_index][self.x_index] == "L":
            self.type = "demoulding"
            self["image"] = self.gui.table_images[1]
            self.bind( '<Button-3>', self.show_demoulding_menu )

        elif self.gui.tables_config[self.y_index][self.x_index] == "R":
            self.type = "moulding"
            self["image"] = self.gui.table_images[2]  
            self.bind( '<Button-3>', self.show_moulding_menu )

        elif self.gui.tables_config[self.y_index][self.x_index] == "U":
            self.type = "composing"
            self["image"] = self.gui.table_images[3] 
            self.bind( '<Button-3>', self.show_composing_menu )
            self.gui.composing_tables.append( self )

        elif self.gui.tables_config[self.y_index][self.x_index] == "O":
            self.type = "turntable"
            self.position = "vertical"
            self["image"] = self.gui.table_images[8]
            self.bind( '<Button-3>', self.show_turntable_menu )

        elif self.gui.tables_config[self.y_index][self.x_index] == "H":
            self.type = "conveyor"
            self["image"] = self.gui.table_images[4]
            
        elif self.gui.tables_config[self.y_index][self.x_index] == "V":
            self.type = "conveyor"
            self["image"] = self.gui.table_images[5]
            
        elif self.gui.tables_config[self.y_index][self.x_index] == "P":
            self.type = "press"
            self["image"] = self.gui.table_images[9]
        
        self.config( relief = SUNKEN)
        self.pack( fill = BOTH, expand = 1 )
        
    def show_turntable_menu( self, event ):
        self.turntable_menu.tk_popup( event.x_root, event.y_root )

    def show_composing_menu( self, event ):
        if not self.gui.track_creating_active:
            self.composing_menu.tk_popup( event.x_root, event.y_root )

    def show_moulding_menu( self , event ):
        self.moulding_menu.tk_popup( event.x_root, event.y_root )

    def show_demoulding_menu( self , event ):
        self.demoulding_menu.tk_popup( event.x_root, event.y_root )

    def table_turn( self ):
        print( "Turning table: ", self )

        if self["image"] == "pyimage9":
            self["image"] = self.gui.table_images[7]
            self.position = "horizontal"
        elif self["image"] == "pyimage8":
            self["image"] = self.gui.table_images[8]
            self.position = "vertical"

    def table_place_new_plate( self ):
        plate = Plate( self )
