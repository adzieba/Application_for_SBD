from Plates import *
import threading
import time


class FollowPathThread( threading.Thread ):
    
    def __init__( self, plate, path ):
        self.plate = plate
        self.path_to_follow = path
        print("początek podążania, płyta: ", self.plate )
        self.path_len = len( path )
        self.finish_thread = False
        super().__init__()
        self.move_index = 0

    def __del__( self ):
        print("koniec podążania")  

    def run( self ):

        while True:
            print( self.path_to_follow[self.move_index] )
            if self.plate.movePlate( self.path_to_follow[self.move_index] ):
                self.move_index += 1
                self.plate.gui.window.update()

            if self.move_index >= self.path_len:
                self.plate.finishFollowingPath()
                break
            time.sleep( 1 )
