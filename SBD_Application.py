from tkinter import *
from PIL     import ImageTk, Image
#from Plate import *
from Table import *
from random import randint
import os, sys
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
        self.composing_tables = []
        self.tracks = []
        self.table_objects_scheme = []
        self.table_graphics = [ 
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

        self.draw_window()

        for i in range( len( self.table_graphics )):
            img = Image.open( os.path.join( sys.path[0], self.config_file['graphics']['folder'], self.table_graphics[i] ) )
            img = img.resize(( self.tile_width , self.tile_height ))
            self.table_images.append( ImageTk.PhotoImage( img ))

        self.draw_tables()

    def draw_window( self ):
        window_width  = self.config_file['window']['app_width']
        window_height = self.config_file['window']['app_height']
        window_size = "{}x{}+{}+{}".format( window_width, window_height, 200, 0 )
        
        # draw application window
        self.window = Tk()
        self.window.title( "Application for SBD course" )
        self.window.geometry( window_size )
        self.window.resizable( 0 , 0 ) 
          
        self.window_background = Frame( self.window, bg = 'black' )
        self.window_background.pack_propagate( 0 )
        self.window_background.pack( fill = BOTH, expand = 1 )
                        
        # draw application menu
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

    def draw_tables( self ):

        self.tables_list = [[0] * self.config_file['window']['columns'] for i in range(self.config_file['window']['rows'])]

        for table_object in self.config_file['tables']['objects']:
                    
            x = self.config_file['tables']['objects'][table_object]['x']
            y = self.config_file['tables']['objects'][table_object]['y']
            type = self.config_file['tables']['objects'][table_object]['type']
            
            move_directions = self.config_file['tables']['objects'][table_object]['move_directions']
            table = Table( self, type, move_directions, x, y )
            self.tables_list[y][x] = table

    def finish_track_popup( self ):
        popup_width  = 600
        popup_height = 400
        popup_x_root = int( self.window.winfo_x() + self.window_width  / 2 - popup_width  / 2 )
        popup_y_root = int( self.window.winfo_y() + self.window_height / 2 - popup_height / 2 )
        popup_size   = "{}x{}+{}+{}".format( popup_width, popup_height, popup_x_root, popup_y_root )

        popup = Toplevel()
        popup.title("Nazwa ścieżki")
        popup.geometry( popup_size )
        popup.resizable( False, False )
                
        label = Label( popup, text = "Wprowadź nazwę ścieżki:" ).place( x = 40, y = 40 )
        input_box = Entry( popup ).place( x = 40, y = 140 )

        button_save =  Button( popup, text = "Zapisz", command = lambda : self.new_track.accept_track( label.get() )).place( x = 40, y = 240 )
        button_close = Button( popup, text = "Anuluj", command = self.new_track.cancel_track ).place( x = 140, y = 240 )

    def run( self ):
        mainloop()

if __name__ == "__main__":
    print("dupa, nie to okno dzbanie")