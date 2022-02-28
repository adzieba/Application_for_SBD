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

    def cancel_track_creating( self ):
        self.gui.new_track = None

    def accept_track( self, end_table ):
        self.gui.track_creating_active = False

        self.end_table = end_table
        self.end_table_x_index = self.end_table.x_index
        self.end_table_y_index = self.end_table.y_index
        #self.gui.tracks.append( self.gui.new_track )

        print( "poczatek trasy: ", self.start_table, self.start_table.x_index, self.start_table.y_index ) 
        print( "koniec trasy :",   self.end_table,   self.end_table.x_index,   self.end_table.y_index )
        
        self.gui.finish_track_popup()

       