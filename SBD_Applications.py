from tkinter import *
from turtle import screensize
from PIL     import ImageTk, Image
#from Plate import *
from Tables import *
from random import randint
import os, sys, ctypes
import threading
import time
import json

class SBD_Application():

    def __init__( self ):
       
        with open( os.path.join( sys.path[0], "config.json" ), 'r') as config_file:
            self.config_file = json.load( config_file )

        self.task_list    = []
        self.plate_list   = []
        self.tables_list  = []
        self.table_images = []
        self.graphics = [ 
            "plate.png",         #0
            "conveyor_h.png",    #1
            "station_right.png", #2    
            "turntable_h.png",   #3
            "conveyor_v.png",    #4
            "station_left.png",  #5
            "station_up.png",    #6
            "station_down.png",  #7
            "turntable_v.png" ]  #8

        self.track_creating_active = False
        self.new_track = None
        self.tile_width  = self.config_file['window']['tile_width']
        self.tile_height = self.config_file['window']['tile_height']
        self.table_area_width  = self.config_file['window']['table_area_width']
        self.table_area_height = self.config_file['window']['table_area_height']

        self.drawWindow()

        for i in range( len( self.graphics )):
            folder_with_graphics = self.config_file['graphics']['folder']
            img = Image.open( os.path.join( sys.path[0], folder_with_graphics, self.graphics[i] ))
            img = img.resize(( self.tile_width , self.tile_height ))
            self.table_images.append( ImageTk.PhotoImage( img ))

        self.drawTables()

    def drawWindow( self ):

        # place window on screen middle
        user32 = ctypes.windll.user32
        screen_width  = user32.GetSystemMetrics(0) 
        screen_height = user32.GetSystemMetrics(1)
        
        self.window_width  = self.config_file['window']['app_width']
        self.window_height = self.config_file['window']['app_height']
        x_offset = int(( screen_width - self.window_width ) / 2 )
        y_offset = int(( screen_height - self.window_height ) / 2 )
        window_size = "{}x{}+{}+{}".format( self.window_width, self.window_height, x_offset, y_offset )
        
        # draw application window
        self.window = Tk()
        self.window.title( "Application for SBD course" )
        self.window.geometry( window_size )
        self.window.resizable( 0 , 0 ) 
          
        self.window_background = Frame( self.window, bg = 'black' )
        self.window_background.pack_propagate( 0 )
        self.window_background.pack( fill = BOTH, expand = 1 )

        self.visualization_background = Frame( self.window_background, width = self.table_area_width , height = self.table_area_height, bg = 'grey' )
        self.visualization_background.pack_propagate( 0 )
        self.visualization_background.pack( side = TOP, anchor = NW )
                        
        # assign application menu
        menu_bar = Menu( self.window_background )

        file_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='File', menu = file_bar )
        file_bar.add_command( label ='New File', command = None)
        file_bar.add_command( label ='Open...', command = None)
        file_bar.add_command( label ='Save', command = None)
        file_bar.add_separator()
        file_bar.add_command( label ='Exit', command = self.window.destroy )

        edit_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='Użytkownicy', menu = edit_bar )
        edit_bar.add_command( label ='Dodaj', command = None )
        edit_bar.add_command( label ='Edytuj', command = None )
        edit_bar.add_command( label ='Usuń', command = None )
   
        help_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='Zlecenia', menu = help_bar )
        help_bar.add_command( label ='Dodaj', command = None )
        help_bar.add_command( label ='Edytuj', command = None )
        help_bar.add_command( label ='Przeglądaj', command = None )

        self.window.config( menu = menu_bar )

    def drawTables( self ):

        # table array filled with 0
        self.tables_list = [[0] * self.config_file['window']['columns'] for i in range(self.config_file['window']['rows'])]

        # grid filled with table objects
        for table_name in self.config_file['tables']['objects']:
                    
            table_x = self.config_file['tables']['objects'][table_name]['x']
            table_y = self.config_file['tables']['objects'][table_name]['y']
            table_type = self.config_file['tables']['objects'][table_name]['type']
            possible_moves = self.config_file['tables']['objects'][table_name]['move_directions']

            if table_type == "D":
                table = DemouldingTable( self, table_type, possible_moves, table_x, table_y, table_name )
            elif table_type == "M":
                table = MouldingTable( self, table_type, possible_moves, table_x, table_y, table_name )
            elif table_type == "C":
                table = ComposingTable( self, table_type, possible_moves, table_x, table_y, table_name )
            elif table_type == "+":
                table = TurnTable( self, table_type, possible_moves, table_x, table_y, table_name )
            elif table_type == "|" or table_type == "-":
                table = ConveyorTable( self, table_type, possible_moves, table_x, table_y, table_name )
            
            self.tables_list[table_y][table_x] = table

    def run( self ):
        mainloop()

if __name__ == "__main__":
    print("dupa, nie to okno dzbanie")
