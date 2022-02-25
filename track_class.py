class Track():

    def __init__( self, gui, start_table ):
        self.gui = gui
        self.start_table = start_table
        self.start_table_x_index = self.start_table.x_index
        self.start_table_y_index = self.start_table.y_index
        self.end_table = None
        self.end_table_x_index = 0
        self.end_table_y_index = 0
        self.track_len = 0
        self.moves = []
    
    def __del__( self ):
        print("anulowanie trasy")

    def accept_track( self, name ):
        print(name)
        pass

    def cancel_track( self ):
        pass
       