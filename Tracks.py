from tkinter import *
import os, sys, json

class Track():

    def __init__( self, gui, start_table ):
        print("tworzenie trasy - poczatek")
        self.gui = gui
        self.gui.track_creating_active = True
        self.start_table = start_table
        self.start_table_x_index = self.start_table.x_index
        self.start_table_y_index = self.start_table.y_index
        self.end_table = None
        self.end_table_x_index = 0
        self.end_table_y_index = 0
        self.track_len = 0
        self.moves = []
       
    def __del__( self ):
        print("tworzenie trasy - koniec")
        self.gui.track_creating_active = False
    
    def addMove( self, direction ):
        self.moves.append( direction )
        self.track_len = len( self.moves )

    def cancelTrack( self ):
        self.gui.new_track = None

    def acceptTrack( self, end_table ):
        self.end_table = end_table
        self.end_table_x_index = self.end_table.x_index
        self.end_table_y_index = self.end_table.y_index
        
        popup_width  = 600
        popup_height = 400
        popup_x_root = int( self.gui.window.winfo_x() + self.gui.window_width  / 2 - popup_width  / 2 )
        popup_y_root = int( self.gui.window.winfo_y() + self.gui.window_height / 2 - popup_height / 2 )
        popup_size   = "{}x{}+{}+{}".format( popup_width, popup_height, popup_x_root, popup_y_root )
        popup = Toplevel()
        popup.title("Nazwa ścieżki")
        popup.geometry( popup_size )
        popup.resizable( False, False )
        trackNameStartTable  = StringVar( popup )     
        trackNameForEndTable = StringVar( popup )
        can_be_queued = IntVar( popup )

        label_start_table = Label( popup, text = "Stół - początek: " + str( self.start_table.name )).place( x = 40, y = 20 )
        label_end_table   = Label( popup, text = "Stół - koniec: "   + str( self.end_table.name )).place( x = 40, y = 50 )
        label_track_len   = Label( popup, text = "Długość ścieżki: "  + str( self.track_len ) + str( self.moves ) ).place( x = 40, y = 80 )
        label1            = Label( popup, text = "Nazwa ścieżki dla stołu początkowego: " ).place( x = 40, y = 110 )
        input_box         = Entry( popup, textvariable = trackNameStartTable ).place( x = 40, y = 140 ) 
        
        if self.end_table.name != self.start_table.name:
            label2            = Label( popup, text = "Czy płyty na ścieżce mogą się kolejkować? " ).place( x = 40, y = 170 )
            confirm_add_end   = Checkbutton( popup, variable = can_be_queued, onvalue = 1 , offvalue = 0 ). place( x = 300, y = 170 )
            label3            = Label( popup, text = "Nazwa ścieżki dla stołu końcowego:  " ).place( x = 40, y = 200 )
            input_box         = Entry( popup, textvariable = trackNameForEndTable ).place( x = 40, y = 230 ) 

        button_save =  Button( popup, text = "Zapisz", command = lambda : self.popupSaveButton( popup, trackNameStartTable.get(), can_be_queued.get(), trackNameForEndTable.get() )).place( x = 40,  y = 260 )
        button_close = Button( popup, text = "Anuluj", command = lambda : self.popupCancelButton( popup )).place( x = 90,  y = 260 )

    def popupSaveButton( self, widget, start_table_track_name, path_queued, end_table_track_name ):

        start_table_name_ok = False
        end_table_track_name_ok = False
        include_end_table = False

        if len( start_table_track_name ) > 0:
            start_table_name_ok = True
        
        if len( end_table_track_name ) > 0:            
                include_end_table = True
                end_table_track_name_ok = True
        else:
            end_table_track_name_ok = True

        if start_table_name_ok and end_table_track_name_ok:

            with open( os.path.join( sys.path[0], "config.json" ), 'r') as infile:
                config_file = json.load( infile )

            if not 'paths' in config_file['tables']['objects'][self.start_table.name]:
                config_file['tables']['objects'][self.start_table.name]['paths'] = {}
    
            config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name] = {}
            config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name]['moves'] = self.moves

            if path_queued:
                config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name]['queued'] = 'yes'

            config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name]['destination'] = {}
            config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name]['destination']['name'] = self.end_table.name
            config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name]['destination']['x'] = self.end_table.x_index
            config_file['tables']['objects'][self.start_table.name]['paths'][start_table_track_name]['destination']['y'] = self.end_table.y_index

            if include_end_table:
                if not 'paths' in config_file['tables']['objects'][self.end_table.name]:
                    config_file['tables']['objects'][self.end_table.name]['paths'] = {}
    
                config_file['tables']['objects'][self.end_table.name]['paths'][end_table_track_name] = {}

                reversed_moves = list( reversed( self.moves ))
               
                for move in range( len(reversed_moves)):
                    print(move)
                    print("przed: ", reversed_moves[move])

                    if reversed_moves[move] == 'up':
                        reversed_moves[move] = 'down'
                        continue

                    if reversed_moves[move] == 'down':
                        reversed_moves[move] = 'up'
                        continue

                    if reversed_moves[move] == 'left':
                        reversed_moves[move] = 'right'
                        continue
                    
                    if reversed_moves[move] == 'right':
                        reversed_moves[move] = 'left'     
                        continue             

                config_file['tables']['objects'][self.end_table.name]['paths'][end_table_track_name]['moves'] = reversed_moves
                config_file['tables']['objects'][self.end_table.name]['paths'][end_table_track_name]['destination'] = {}
                config_file['tables']['objects'][self.end_table.name]['paths'][end_table_track_name]['destination']['name'] = self.start_table.name
                config_file['tables']['objects'][self.end_table.name]['paths'][end_table_track_name]['destination']['x'] = self.start_table.x_index
                config_file['tables']['objects'][self.end_table.name]['paths'][end_table_track_name]['destination']['y'] = self.start_table.y_index

            with open( os.path.join( sys.path[0], "config.json" ), 'w') as outfile:
                json.dump( config_file, outfile, indent = 4 )

            self.cancelTrack()
            widget.destroy()
    
    def popupCancelButton( self, widget ):
        self.cancelTrack()
        widget.destroy()
       