import imghdr
from tkinter import *
from PIL     import ImageTk, Image
import threading
import queue
import time
import Tables
from SBD_Applications import *
from FollowPathThread import *
from Tracks import *
from random import randint
import sys

#class Plate( Button ):
class Plate():

    def __init__( self, table ):
        print("plyta - poczatek")
        self.table = table
        self.table.setOccupied( self )
        self.gui = self.table.gui
        self.x_index = self.table.x_index
        self.y_index = self.table.y_index
        self.x_pos   = self.table.x_pos
        self.y_pos   = self.table.y_pos
    
        self.frame = Frame( self.gui.visualization_background, height = self.gui.tile_height, width = self.gui.tile_width )
        self.frame.pack_propagate( 0 )
        self.frame.place( x = self.x_pos, y = self.y_pos )
        
        self.framebackground = Label( self.frame, image = self.gui.table_images[0] )
        self.framebackground.pack( fill = BOTH )
        self.framebackground.bind('<Button-1>', lambda event: self.setFocusOnPlate())
        self.framebackground.bind('<Button-3>', self.showPlateMenu )
        self.framebackground.bind('<Up>',       lambda event: self.manualMovePlate( 'up' ))
        self.framebackground.bind('<Down>',     lambda event: self.manualMovePlate( 'down' ))
        self.framebackground.bind('<Left>',     lambda event: self.manualMovePlate( 'left' ))
        self.framebackground.bind('<Right>',    lambda event: self.manualMovePlate( 'right' ))

        self.label = Label( self.frame, height = 1, width=2, text = '123', bg='grey')
        self.label.place( relx = 0.05, rely = 0.05 )
        self.label.bind('<Button-1>', lambda event: self.setFocusOnPlate())
        self.label.bind('<Button-3>', self.showPlateMenu )
        
        self.setFocusOnPlate()
        self.menu = None
        self.path_to_follow = None
        self.following_path = False
        self.follow_thread = None

    def __del__( self ):
        print("plyta - koniec")

    def showPlateMenu( self, event ):

        if self.menu != None:
            self.menu.destroy()
   
        self.setFocusOnPlate()

        if self.gui.track_creating_active:
            self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
            self.menu.add_command( label = "Ścieżka - góra",  command = lambda: self.manualMovePlate( 'up' ))
            self.menu.add_command( label = "Ścieżka - dół ",  command = lambda: self.manualMovePlate( 'down' ))
            self.menu.add_command( label = "Ścieżka - lewo",  command = lambda: self.manualMovePlate( 'left' ))
            self.menu.add_command( label = "Ścieżka - prawo", command = lambda: self.manualMovePlate( 'right' ))
            self.menu.add_separator()
            self.menu.add_command( label = "Zaakceptuj ścieżkę ", command = lambda: self.gui.new_track.acceptTrack( self.table )) 
            self.menu.add_command( label = "Anuluj ścieżkę ",     command = lambda: self.gui.new_track.cancelTrack() )
            self.menu.tk_popup( event.x_root, event.y_root )
        else:
            # ppm plate
            self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
            self.menu.add_command( label = "Idź - góra",  command = lambda: self.manualMovePlate( 'up' ))
            self.menu.add_command( label = "Idź - dół ",  command = lambda: self.manualMovePlate( 'down' ))
            self.menu.add_command( label = "Idź - lewo",  command = lambda: self.manualMovePlate( 'left' ))
            self.menu.add_command( label = "Idź - prawo", command = lambda: self.manualMovePlate( 'right' ))

            paths = self.table.getPaths( 1 )            
            
            if paths:
                self.menu.add_separator()
                send_menu = Menu( self.menu, tearoff = 0 )

                for path_name in paths:
                    moves = paths[path_name]['moves']
                    send_menu.add_command( label = path_name, command = lambda moves=moves: self.startFollowingPath( moves ))
                    
                self.menu.add_cascade( label = "Wyślij płytę do:", menu = send_menu )

            if not self.following_path:
                self.menu.add_separator()
                self.menu.add_command( label = "Zacznij rysować ścieżkę", command = self.startNewTrackForPlate )
                self.menu.add_separator()
                self.menu.add_command( label = "Usuń płytę", command = self.deletePlate )
            else:
                self.menu.add_command( label = "Zatrzymaj płytę", command = self.finishFollowingPath )

            self.menu.tk_popup( event.x_root, event.y_root )

    def startNewTrackForPlate( self ):
        self.setFocusOnPlate()
        self.gui.new_track = None
        self.gui.new_track = Track( self.gui, self.table )

    def deletePlate( self ):
        self.table.setFree()
        self.gui.selected_plate = None
        self.frame.destroy()
        self.menu.destroy()
        
    def setFocusOnPlate( self ):
        self.framebackground.focus_set()
        self.gui.selected_plate = self
          
    def startFollowingPath( self, moves ): 
       
        if not self.following_path:
            self.following_path = True
            self.moves_to_follow = moves
            self.follow_thread = FollowPathThread( self, self.moves_to_follow )
            self.follow_thread.start()          

    def finishFollowingPath( self ):
        self.following_path = False
        self.path_to_follow = None
        self.follow_thread  = None

    def manualMovePlate( self, direction ):
        if not self.following_path:
            self.movePlate( direction )

    def movePlate( self, direction ):
        move_done = False
        
        if direction in self.table.move_directions:

            if direction == 'up':
                next_table = self.gui.tables_list[ self.y_index - 1 ][ self.x_index ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'down' in next_table.move_directions:
                    next_turntable_need_turn = is_nexttable_turntable and next_table.position == "horizontal" 
                   
                    if next_table.isFree():

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):
                                
                                if self.table.position == "horizontal":
                                    self.table.turnTable()
                                else:
                                    move_done = self.movePlateUp()

                            else:

                                if next_turntable_need_turn:
                                    next_table.turnTable()
                                else:
                                    move_done = self.movePlateUp()

                        else:
                            move_done = self.movePlateUp()                


            elif direction == 'down':
                next_table = self.gui.tables_list[ self.y_index + 1 ][ self.x_index ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'up' in next_table.move_directions:
                    next_turntable_need_turn = is_nexttable_turntable and next_table.position == "horizontal" 
                    
                    if next_table.isFree():

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):

                                if self.table.position == "horizontal":
                                    self.table.turnTable()
                                else:
                                    move_done = self.movePlateDown()

                            else:

                                if next_turntable_need_turn: 
                                    next_table.turnTable()
                                else:
                                    move_done = self.movePlateDown()

                        else:
                            move_done = self.movePlateDown()

            elif direction == 'left':
                next_table = self.gui.tables_list[ self.y_index ][ self.x_index - 1 ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'right' in next_table.move_directions:
                    next_turntable_need_turn = is_nexttable_turntable and next_table.position == "vertical" 
                    
                    if next_table.isFree():    

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):
                                
                                if self.table.position == "vertical":
                                    self.table.turnTable()
                                else:
                                    move_done = self.movePlateLeft()

                            else:

                                if next_turntable_need_turn:
                                    next_table.turnTable()
                                else:
                                    move_done = self.movePlateLeft()

                        else:
                            move_done = self.movePlateLeft()


            elif direction == 'right':
                next_table = self.gui.tables_list[ self.y_index ][ self.x_index + 1 ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'left' in next_table.move_directions:
                    next_turntable_need_turn = ( is_nexttable_turntable and next_table.position == "vertical" )
                    
                    if next_table.isFree():

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):

                                if self.table.position == "vertical":
                                    self.table.turnTable()
                                else:
                                    move_done = self.movePlateRight()

                            else:
                               
                                if next_turntable_need_turn :
                                    next_table.turnTable()
                                else:
                                    move_done = self.movePlateRight()

                        else:
                            move_done = self.movePlateRight()

            if move_done:
                self.table.setFree()
                self.table = next_table
                self.table.setOccupied( self )
                                
                if self.gui.track_creating_active:
                    self.gui.new_track.addMove( direction )

            return move_done
        else:
            print("brak takiego ruchu")
            return False

    def movePlateUp( self ):
        new_y_pos = self.y_pos - self.gui.tile_height

        if new_y_pos >= 0:
            self.frame.place( y = new_y_pos )
            self.y_pos = new_y_pos
            self.y_index = self.y_index - 1
            return True

    def movePlateDown( self ):
        new_y_pos = self.y_pos + self.gui.tile_height

        if new_y_pos <= self.gui.table_area_height - 50:
            self.frame.place( y = new_y_pos )
            self.y_pos = new_y_pos 
            self.y_index = self.y_index + 1
            return True

    def movePlateLeft( self ):
        new_x_pos = self.x_pos - self.gui.tile_width

        if new_x_pos >= 0:
            self.frame.place( x = new_x_pos )
            self.x_pos = new_x_pos
            self.x_index = self.x_index - 1
            return True

    def movePlateRight( self ):
        new_x_pos = self.x_pos + self.gui.tile_width

        if new_x_pos <= self.gui.table_area_width - 50:
            self.frame.place( x = new_x_pos )
            self.x_pos = new_x_pos
            self.x_index = self.x_index + 1
            return True
