from tkinter import *

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
    
    def add_move_to_track( self, direction ):
        self.moves.append( direction )
        self.track_len = len( self.moves )

    def cancel_track( self ):
        self.gui.new_track = None

    def accept_track_popup( self, end_table ):
        self.end_table = end_table
        self.end_table_x_index = self.end_table.x_index
        self.end_table_y_index = self.end_table.y_index

        self.gui.showTrackPopup()

    def accept_track( self, track_name ):
        self.gui.new_track = None

    def showTrackPopup( self ):
        popup_width  = 600
        popup_height = 400
        popup_x_root = int( self.window.winfo_x() + self.window_width  / 2 - popup_width  / 2 )
        popup_y_root = int( self.window.winfo_y() + self.window_height / 2 - popup_height / 2 )
        popup_size   = "{}x{}+{}+{}".format( popup_width, popup_height, popup_x_root, popup_y_root )

        popup = Toplevel()
        popup.title("Nazwa ścieżki")
        popup.geometry( popup_size )
        popup.resizable( False, False )
        trackPopupEntry = StringVar( popup )     

        label_start_table = Label( popup, text = "Początek ścieżki: " + str( self.new_track.start_table.name )).place( x = 40, y = 20 )
        label_end_table   = Label( popup, text = "Koniec ścieżki: "   + str( self.new_track.end_table.name )).place( x = 40, y = 50 )
        label_track_len   = Label( popup, text = "Długość ścieżki: "  + str( self.new_track.track_len ) + str( self.new_track.moves ) ).place( x = 40, y = 80 )
        label             = Label( popup, text = "Wprowadź nazwę ścieżki:" ).place( x = 40, y = 110 )
        input_box         = Entry( popup, textvariable = trackPopupEntry ).place( x = 40, y = 140 ) 

        button_save =  Button( popup, text = "Zapisz", command = lambda : self.SaveButtonAction  ( popup, trackPopupEntry.get() )).place( x = 40,  y = 240 )
        button_close = Button( popup, text = "Anuluj", command = lambda : self.CancelButtonAction( popup )).place( x = 90,  y = 240 )

    def SaveButtonAction( self, widget, track_name ):
        self.new_track.accept_track( track_name )
        widget.destroy()
    
    def CancelButtonAction( self, widget ):
        self.new_track.cancel_track()
        widget.destroy()
       