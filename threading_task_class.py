from Plates import *
import os, sys
import threading
import time
from random import randint

class ThreadedTask( threading.Thread ):
    
    def __init__( self, plate ):
        self.plate = plate
        print(" watek dla ", self.plate )
        self.finish_thread = False
        super().__init__()
                
    def run( self ):

        while True:
            if self.finish_thread:
                print("konczenie watku")
                break

            #print( "%s: %s" % ( "czas watku: ", time.ctime( time.time() ) ) )
            if len( self.plate.table.move_directions ) > 0:
                direction_index =  randint( 0, len( self.plate.table.move_directions ) - 1 ) 
                direction = self.plate.table.move_directions[ direction_index ]
                print("kierunek: ", direction)
                self.plate.plate_move( direction )
            time.sleep( 1 )
