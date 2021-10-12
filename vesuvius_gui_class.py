from tkinter import *
from PIL     import ImageTk, Image
from plate_class import *
from table_class import *
from random import randint
import os, sys
import threading
import time

class Vesuvius_gui():

    def __init__( self ):
        self.tile_height  = 50
        self.tile_width   = 50
        self.task_list    = []
        self.plate_list   = []
        self.table_images = []
        self.composing_tables = []
        self.tracks = []
        self.table_objects_scheme = []
        self.table_graphics_dir = [ 
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\station_down.png",    #0  # pyimage1
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\station_left.png",    #1  # pyimage2
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\station_right.png",   #2  # pyimage3
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\station_up.png",      #3  # pyimage4
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\transport_h.png",     #4  # pyimage5
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\transport_h_v.png",   #5  # pyimage6
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\turntable_45deg.png", #6  # pyimage7
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\turntable_h.png",     #7  # pyimage8
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\turntable_v.png",     #8  # pyimage9
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\press.png",           #9  # pyimage10
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\plyta.png",           #10 # pyimage11
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\arrow_up.png",        #11 # pyimage12
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\arrow_down.png",      #12 # pyimage13
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\arrow_left.png",      #13 # pyimage14
            r"C:\Users\azieba\Desktop\Projekty\python\vesuviusgui\Graphics\arrow_right.png" ]    #14 # pyimage15

        self.track_creating_active = False
        self.new_track = None


        if self.import_tables_config():
            self.make_window()
            self.draw_tables()
        else:
            print( "error on entry" )

    def import_tables_config( self ):
        File_len_error = False

        with open( os.path.join(sys.path[0], "rozstaw.txt"),"r", encoding = 'utf8' ) as f:
            self.tables_config = f.readlines()
            self.rows_of_tiles = len( self.tables_config )

        for i in range( len( self.tables_config ) ):
            self.tables_config[i] = self.tables_config[i].rstrip()

            if i == 0:
                self.columns_of_tiles = len( self.tables_config[i] )
            else:
                if len( self.tables_config[i] ) != self.columns_of_tiles:
                    File_len_error = True
                    print( "file line length error" )

        if self.rows_of_tiles > 0 and self.columns_of_tiles > 0 and not File_len_error:
            return True
        else:
            return False

    def make_window( self ):
        self.table_area_width = self.tile_width  * self.columns_of_tiles
        self.table_area_height = self.tile_height * self.rows_of_tiles
        self.window_width  = self.table_area_width + 150
        self.window_height = self.table_area_height + 150
        self.window_size = "{}x{}".format( self.window_width, self.window_height )
        
        self.window = Tk()
        self.window.title( "Vesuvius scheme" )
        self.window.geometry( self.window_size )
        self.window.resizable( 0 , 0 ) 
          
        self.window_background = Frame( self.window, bg = 'black' )
        self.window_background.pack_propagate( 0 )
        self.window_background.pack( fill = BOTH, expand = 1 )

        for i in range( len( self.table_graphics_dir ) ):
            img = Image.open(self.table_graphics_dir[i])
            img = img.resize( (self.tile_width, self.tile_height ), Image.ANTIALIAS )
            self.table_images.append( ImageTk.PhotoImage( img ) )

        # rysuj menu górne
        menu_bar = Menu( self.window_background )

        file_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='File', menu = file_bar )
        file_bar.add_command( label ='New File', command = None)
        file_bar.add_command( label ='Open...', command = None)
        file_bar.add_command( label ='Save', command = None)
        file_bar.add_separator()
        file_bar.add_command( label ='Exit', command = self.window.destroy)

        edit_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='Edit', menu = edit_bar )
        edit_bar.add_command( label ='Cut', command = None )
        edit_bar.add_command( label ='Copy', command = None )
        edit_bar.add_command( label ='Paste', command = None )
        edit_bar.add_command( label ='Select All', command = None )
        edit_bar.add_separator()
        edit_bar.add_command( label ='Find...', command = None )
        edit_bar.add_command( label ='Find again', command = None )

        help_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='Help', menu = help_bar )
        help_bar.add_command( label ='Tk Help', command = None )
        help_bar.add_command( label ='Demo', command = None )
        help_bar.add_separator()
        help_bar.add_command( label ='About Tk', command = None )

        self.window.config( menu = menu_bar )

    def draw_tables( self ):

        for y in range( self.rows_of_tiles ):
            table_objects_row = []

            for x in range( self.columns_of_tiles ):
                move_directions = []

                if self.tables_config[y][x] != ".":

                    if y - 1 >= 0:
                        if self.tables_config[y - 1][x] != ".":
                            move_directions.append( 1 )

                    if y + 1 <= self.rows_of_tiles:
                        if self.tables_config[y + 1][x] != ".":
                            move_directions.append( 2 )

                    if x - 1 >= 0: 
                        if self.tables_config[y][x - 1] != ".":
                            move_directions.append( 3 )

                    if x + 1 <= self.columns_of_tiles: 
                        if self.tables_config[y][x + 1] != ".":
                            move_directions.append( 4 )
                    
                    table = Table( self, move_directions, x, y )
                    table_objects_row.append( table )
                    
                else:
                    table_objects_row.append( "0" )                       

            self.table_objects_scheme.append( table_objects_row )   

    def new_button( self, root, button_height, button_width, x_pos, y_pos, graphic ):
        frame = self.new_frame( root, button_height, button_width, x_pos, y_pos )
        button = Button( frame )
        button["image"] = graphic
        button.pack( fill = BOTH, expand = 1 )
        return button

    def new_frame( self, root, button_height , button_width, x_pos, y_pos ):
        frame = Frame( root, height = button_height, width = button_width )
        frame.pack_propagate( 0 )
        frame.place( x = x_pos, y = y_pos )
        return frame
        
    def main( self ):
        mainloop()

if __name__ == "__main__":
    print("dupa, nie to okno dzbanie")