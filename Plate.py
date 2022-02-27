from tkinter import *
from PIL     import ImageTk, Image
import threading
import queue
import time
from SBD_Application import *
from threading_task_class import *
from track_class import *
from random import randint

class Plate( Button ):

    def __init__( self, table ):
        self.table = table
        self.table.plate_on_table = True
        self.gui = self.table.gui
        self.x_index = self.table.x_index
        self.y_index = self.table.y_index
        self.x_pos   = self.table.x_pos
        self.y_pos   = self.table.y_pos

        self.frame = Frame( self.gui.window_background, height = self.gui.tile_height, width = self.gui.tile_width )
        self.frame.pack_propagate( 0 )
        self.frame.place( x = self.x_pos, y = self.y_pos )
        super().__init__( self.frame )

        # ppm plate
        self.plate_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.plate_menu.add_command( label = "Idź - góra",  command = lambda: self.plate_move( 'up' ))
        self.plate_menu.add_command( label = "Idź - dół ",  command = lambda: self.plate_move( 'down' ))
        self.plate_menu.add_command( label = "Idź - lewo",  command = lambda: self.plate_move( 'left' ))
        self.plate_menu.add_command( label = "Idź - prawo", command = lambda: self.plate_move( 'right' ))
        self.plate_menu.add_separator()
        self.plate_menu.add_command( label = "Zacznij rysować ścieżkę ", command = self.activate_track_creating )
        self.plate_menu.add_separator()
        self.plate_menu.add_command( label = "Usuń płytę", command = self.plate_delete )

        self.plate_track_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.plate_track_menu.add_command( label = "Ścieżka - góra",  command = lambda: self.plate_move( 'up' ))
        self.plate_track_menu.add_command( label = "Ścieżka - dół ",  command = lambda: self.plate_move( 'down' ))
        self.plate_track_menu.add_command( label = "Ścieżka - lewo",  command = lambda: self.plate_move( 'left' ))
        self.plate_track_menu.add_command( label = "Ścieżka - prawo", command = lambda: self.plate_move( 'right' ))
        self.plate_track_menu.add_separator()
        self.plate_track_menu.add_command( label = "Zakończ rysować ścieżkę ", command = lambda: self.deactivate_track_creating( 1 )) 
        self.plate_track_menu.add_command( label = "Anuluj ścieżkę ", command = lambda: self.deactivate_track_creating( 0 ) )
        
        self["image"] = self.gui.table_images[0]
        self["border"] = 0
        self.config( relief = SUNKEN )
        self.bind('<Button-1>', lambda event: self.plate_select())
        self.bind('<Button-3>', self.show_plate_menu )
        self.bind('<Up>',       lambda event: self.plate_move( 'up' ))
        self.bind('<Down>',     lambda event: self.plate_move( 'down' ))
        self.bind('<Left>',     lambda event: self.plate_move( 'left' ))
        self.bind('<Right>',    lambda event: self.plate_move( 'right' ))
        self.pack( fill = BOTH, expand = 1 )
        self.gui.plate_list.append( self )
        self.focus_set()
        self.gui.selected_plate = self

        self.moving_auto = False

    def __del__( self ):
        print("płyta zdjęta")

    def plate_select( self ):

        if not self.gui.track_creating_active:
            self.focus_set()
            self.gui.selected_plate = self
          
    def plate_move_auto( self ): 
        print("lista:", self.gui.task_list)

        if len( self.table.move_directions ) > 0:

            if not self.moving_auto:
                self.thread = ThreadedTask( self )
                self.thread.start()
                self.gui.task_list.append( self.thread )
                self.moving_auto = True
            else:
                if self.thread in self.gui.task_list:
                    self.thread.finish_thread = True
                    print("przed: ", self.gui.task_list)
                    print("usuwam: ", self.thread )
                    self.gui.task_list.remove( self.thread )
                    print("po: ", self.gui.task_list)
                    self.moving_auto = False               

    def plate_move( self, direction ):
        move_allowed = False
        
        if direction in self.table.move_directions:

            if direction == 'up':
                next_table = self.gui.tables_list[ self.y_index - 1 ][ self.x_index ]

                if 'down' in next_table.move_directions:
                    print( type( next_table ))
                    print(next_table.position)
                    next_turntable_need_turn = ( type( next_table ) == TurnTable and next_table.position == "horizontal" )

                    print("actual table: ", self.table, "with type: ", "next table: ", next_table, "with type: ", "is there other plate: ", next_table.plate_on_table )

                    if type( self.table ) == TurnTable:
                        print("ruszam z obrotowego")

                        if self.table.position == "horizontal":
                            self.table.table_turn()
                            print("turning plate")
                        else:

                            if not next_table.plate_on_table:
                                move_allowed = self.plate_go_up()

                    else:
                        
                        if not next_table.plate_on_table:
                            
                            if next_turntable_need_turn:
                                next_table.table_turn()
                            else:
                                move_allowed = self.plate_go_up()

            elif direction == 'down':
                next_table = self.gui.tables_list[ self.y_index + 1 ][ self.x_index ]

                if 'up' in next_table.move_directions:
                    next_turntable_need_turn = ( type( next_table ) == TurnTable and next_table.position == "horizontal" )
                    print("actual table: ", self.table, "with type: ", "next table: ", next_table, "with type: ", "is there other plate: ", next_table.plate_on_table )

                    if type( self.table ) == TurnTable:

                        if self.table.position == "horizontal":
                            self.table.table_turn()
                            print("turning plate")
                        else:

                            if not next_table.plate_on_table:
                                move_allowed = self.plate_go_down()

                    else:
                        if not next_table.plate_on_table:

                            if next_turntable_need_turn:
                                next_table.table_turn()
                            else:
                                move_allowed = self.plate_go_down()

            elif direction == 'left':
                next_table = self.gui.tables_list[ self.y_index ][ self.x_index - 1 ]

                if 'right' in next_table.move_directions:
                    next_turntable_need_turn = ( type( next_table ) == TurnTable and next_table.position == "vertical" )
                    print("actual table: ", self.table, "with type: ", "next table: ", next_table, "with type: ", "is there other plate: ", next_table.plate_on_table )

                    if type( self.table ) == TurnTable:
                        
                        if self.table.position == "vertical":
                            self.table.table_turn()
                            print("turning plate")
                        else:

                            if not next_table.plate_on_table:
                                move_allowed = self.plate_go_left()

                    else:

                        if not next_table.plate_on_table:
                            if next_turntable_need_turn:
                                next_table.table_turn()
                            else:
                                move_allowed = self.plate_go_left()

            elif direction == 'right':
                next_table = self.gui.tables_list[ self.y_index ][ self.x_index + 1 ]

                if 'left' in next_table.move_directions:
                    next_turntable_need_turn = ( type( next_table ) == TurnTable and next_table.position == "vertical" )
                    print("actual table: ", self.table, "with type: ", "next table: ", next_table, "with type: ", "is there other plate: ", next_table.plate_on_table )

                    if type( self.table ) == TurnTable:

                        if self.table.position == "vertical":
                            self.table.table_turn()
                            print("turning plate")
                        else:

                            if not next_table.plate_on_table:
                                move_allowed = self.plate_go_right()

                    else:

                        if not next_table.plate_on_table:
                            
                            if next_turntable_need_turn:
                                next_table.table_turn()
                            else:
                                move_allowed = self.plate_go_right()

            if move_allowed:
                self.table.plate_on_table = False
                self.table = next_table
                self.table.plate_on_table = True
                
                if self.gui.track_creating_active:
                    self.gui.new_track.track_len += 1
                    self.gui.new_track.moves.append( direction )
        else:
            print("brak takiego ruchu")

    def plate_go_up( self ):
        new_y_pos = self.y_pos - self.gui.tile_height

        if new_y_pos >= 0:
            self.frame.place( y = new_y_pos )
            self.y_pos = new_y_pos
            self.y_index = self.y_index - 1
            return True

    def plate_go_down( self ):
        new_y_pos = self.y_pos + self.gui.tile_height

        if new_y_pos <= self.gui.table_area_height - 50:
            self.frame.place( y = new_y_pos )
            self.y_pos = new_y_pos 
            self.y_index = self.y_index + 1
            return True

    def plate_go_left( self ):
        new_x_pos = self.x_pos - self.gui.tile_width

        if new_x_pos >= 0:
            self.frame.place( x = new_x_pos )
            self.x_pos = new_x_pos
            self.x_index = self.x_index - 1
            return True

    def plate_go_right( self ):
        new_x_pos = self.x_pos + self.gui.tile_width

        if new_x_pos <= self.gui.table_area_width - 50:
            self.frame.place( x = new_x_pos )
            self.x_pos = new_x_pos
            self.x_index = self.x_index + 1
            return True

    def show_plate_menu( self, event ):

        if self.gui.track_creating_active:

            if self.gui.selected_plate == self:
                self.plate_track_menu.tk_popup( event.x_root, event.y_root )

        else:
            self.plate_menu.tk_popup( event.x_root, event.y_root )

    def activate_track_creating( self ):
        self.plate_select()
        self.gui.track_creating_active = True
        self.gui.new_track = Track( self.gui, self.table )

    def deactivate_track_creating( self, mode ):
        self.gui.track_creating_active = False

        self.gui.new_track.deactivate_track( mode )

        if mode == 1:
            self.gui.new_track.end_table = self.table
            self.gui.new_track.end_table_x_index = self.table.x_index
            self.gui.new_track.end_table_y_index = self.table.y_index
            self.gui.tracks.append( self.gui.new_track )

            print( self.gui.new_track.start_table, self.gui.new_track.start_table.x_index, self.gui.new_track.start_table.y_index, 
                   self.gui.new_track.end_table,   self.gui.new_track.end_table.x_index,   self.gui.new_track.end_table.y_index )
            
            self.gui.accept_plate_popup()

        elif mode == 0:
            self.gui.new_track = None
       
    def plate_delete( self ):
        self.table.plate_on_table = False
        self.frame.destroy()
        self.plate_menu.destroy()
        self.plate_track_menu.destroy()
        self.destroy()
        self.gui.plate_list.remove( self )