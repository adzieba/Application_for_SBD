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
        self.table.plate_on_table = True
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
        self.framebackground.bind('<Button-1>', lambda event: self.selectPlate())
        self.framebackground.bind('<Button-3>', self.showPlateMenu )
        self.framebackground.bind('<Up>',       lambda event: self.movePlate( 'up' ))
        self.framebackground.bind('<Down>',     lambda event: self.movePlate( 'down' ))
        self.framebackground.bind('<Left>',     lambda event: self.movePlate( 'left' ))
        self.framebackground.bind('<Right>',    lambda event: self.movePlate( 'right' ))

        self.label = Label( self.frame, height = 1, width=2, text = '123', bg='grey')
        self.label.place( relx = 0.05, rely = 0.05 )
        self.label.bind('<Button-1>', lambda event: self.selectPlate())
        self.label.bind('<Button-3>', self.showPlateMenu )
        self.framebackground.focus_set( )
        self.menu = None

        self.gui.selected_plate = self
        self.path_to_follow = None
        self.following_path = False
        self.follow_thread = None

    def __del__( self ):
        print("plyta - koniec")

    def showPlateMenu( self, event ):

        if self.menu != None:
            self.menu.destroy()

        if self.gui.selected_plate == self:

            if self.gui.track_creating_active:
                self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
                self.menu.add_command( label = "Ścieżka - góra",  command = lambda: self.movePlate( 'up' ))
                self.menu.add_command( label = "Ścieżka - dół ",  command = lambda: self.movePlate( 'down' ))
                self.menu.add_command( label = "Ścieżka - lewo",  command = lambda: self.movePlate( 'left' ))
                self.menu.add_command( label = "Ścieżka - prawo", command = lambda: self.movePlate( 'right' ))
                self.menu.add_separator()
                self.menu.add_command( label = "Zaakceptuj ścieżkę ", command = lambda: self.gui.new_track.acceptTrack( self.table )) 
                self.menu.add_command( label = "Anuluj ścieżkę ",     command = lambda: self.gui.new_track.cancelTrack() )
                self.menu.tk_popup( event.x_root, event.y_root )
            else:
                # ppm plate
                self.menu = Menu( self.gui.visualization_background, tearoff = 0 )
                self.menu.add_command( label = "Idź - góra",  command = lambda: self.movePlate( 'up' ))
                self.menu.add_command( label = "Idź - dół ",  command = lambda: self.movePlate( 'down' ))
                self.menu.add_command( label = "Idź - lewo",  command = lambda: self.movePlate( 'left' ))
                self.menu.add_command( label = "Idź - prawo", command = lambda: self.movePlate( 'right' ))

                paths = self.table.getPaths( 1 )            
               
                if paths:
                    self.menu.add_separator()

                    for path in paths:
                        sub_menu = Menu( self.menu, tearoff = 0 )
                        sub_menu.add_command( label = "Wyślij", command = lambda: self.startFollowingPath( paths[path] ) )
                        self.menu.add_cascade( label = str( path ),  menu = sub_menu )

                self.menu.add_separator()
                self.menu.add_command( label = "Zacznij rysować ścieżkę ", command = self.newTrackForPlate )
                self.menu.add_separator()
                self.menu.add_command( label = "Usuń płytę", command = self.deletePlate )
                self.menu.tk_popup( event.x_root, event.y_root )

    def newTrackForPlate( self ):
        self.selectPlate()
        self.gui.new_track = None
        self.gui.new_track = Track( self.gui, self.table )

    def deletePlate( self ):
        self.table.plate_on_table = False
        self.gui.selected_plate = None
        self.frame.destroy()
        self.menu.destroy()
        
    def selectPlate( self ):

        if not self.gui.track_creating_active:
            self.framebackground.focus_set()
            self.gui.selected_plate = self
          
    def startFollowingPath( self, path ): 
       
        if not self.following_path:
            self.following_path = True
            self.path_to_follow = path['moves']
            self.follow_thread = FollowPathThread( self, self.path_to_follow )
            self.follow_thread.run()
           

        # if len( self.table.move_directions ) > 0:

            # if not self.moving_auto:
            #     self.thread = ThreadedTask( self )
            #     self.thread.start()
            #     self.gui.task_list.append( self.thread )
            #     self.moving_auto = True
            # else:
            #     if self.thread in self.gui.task_list:
            #         self.thread.finish_thread = True
            #         print("przed: ", self.gui.task_list)
            #         print("usuwam: ", self.thread )
            #         self.gui.task_list.remove( self.thread )
            #         print("po: ", self.gui.task_list)
            #         self.moving_auto = False               

    def finishFollowingPath( self ):
        self.following_path = False
        self.path_to_follow = None
        self.follow_thread  = None

    def movePlate( self, direction ):
        move_allowed = False
        
        if direction in self.table.move_directions:

            if direction == 'up':
                next_table = self.gui.tables_list[ self.y_index - 1 ][ self.x_index ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'down' in next_table.move_directions:
                    next_turntable_need_turn = is_nexttable_turntable and next_table.position == "horizontal" 
                   
                    if not next_table.plate_on_table:

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):
                                
                                if self.table.position == "horizontal":
                                    self.table.turnTable()
                                else:
                                    move_allowed = self.movePlateUp()

                            else:

                                if next_turntable_need_turn:
                                    next_table.turnTable()
                                else:
                                    move_allowed = self.movePlateUp()

                        else:
                            move_allowed = self.movePlateUp()                


            elif direction == 'down':
                next_table = self.gui.tables_list[ self.y_index + 1 ][ self.x_index ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'up' in next_table.move_directions:
                    next_turntable_need_turn = is_nexttable_turntable and next_table.position == "horizontal" 
                    
                    if not next_table.plate_on_table:

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):

                                if self.table.position == "horizontal":
                                    self.table.turnTable()
                                else:
                                    move_allowed = self.movePlateDown()

                            else:

                                if next_turntable_need_turn: 
                                    next_table.turnTable()
                                else:
                                    move_allowed = self.movePlateDown()

                        else:
                            move_allowed = self.movePlateDown()

            elif direction == 'left':
                next_table = self.gui.tables_list[ self.y_index ][ self.x_index - 1 ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'right' in next_table.move_directions:
                    next_turntable_need_turn = is_nexttable_turntable and next_table.position == "vertical" 
                    
                    if not next_table.plate_on_table:

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):
                                
                                if self.table.position == "vertical":
                                    self.table.turnTable()
                                else:
                                    move_allowed = self.movePlateLeft()

                            else:

                                if next_turntable_need_turn:
                                    next_table.turnTable()
                                else:
                                    move_allowed = self.movePlateLeft()

                        else:
                            move_allowed = self.movePlateLeft()


            elif direction == 'right':
                next_table = self.gui.tables_list[ self.y_index ][ self.x_index + 1 ]
                is_nexttable_turntable = isinstance( next_table, Tables.TurnTable )

                if 'left' in next_table.move_directions:
                    next_turntable_need_turn = ( is_nexttable_turntable and next_table.position == "vertical" )
                    
                    if not next_table.plate_on_table:

                        if not self.gui.track_creating_active:

                            if isinstance( self.table, Tables.TurnTable ):

                                if self.table.position == "vertical":
                                    self.table.turnTable()
                                else:
                                    move_allowed = self.movePlateRight()

                            else:
                               
                                if next_turntable_need_turn :
                                    next_table.turnTable()
                                else:
                                    move_allowed = self.movePlateRight()

                        else:
                            move_allowed = self.movePlateRight()

            if move_allowed:
                self.table.plate_on_table = False
                self.table = next_table
                self.table.plate_on_table = True
                
                if self.gui.track_creating_active:
                    self.gui.new_track.addMove( direction )

            return move_allowed
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
