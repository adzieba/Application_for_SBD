from tkinter import *
from PIL     import ImageTk, Image
import threading
import queue
import time
from vesuvius_gui_class import *
from threading_task_class import *
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

        # ppm plate
        self.plate_menu = Menu( self.gui.window_background, tearoff = 0 )
        self.plate_menu.add_command( label = "Usuń płytę", command = self.plate_delete )

        self.frame = Frame( self.gui.window_background, height = self.gui.tile_height, width = self.gui.tile_width )
        self.frame.pack_propagate( 0 )
        self.frame.place( x = self.x_pos, y = self.y_pos )
        super().__init__( self.frame )

        self["image"] = self.gui.table_images[10]
        self["border"] = 0
        self.config( relief = SUNKEN )
        self.bind('<Button-1>', lambda event: self.plate_move_manual())
        #self.bind('<Button-3>', lambda event: self.plate_move_auto())
        self.bind('<Button-3>', self.show_plate_menu )
        self.bind('<Up>',       lambda event: self.plate_move( 1 ))
        self.bind('<Down>',     lambda event: self.plate_move( 2 ))
        self.bind('<Left>',     lambda event: self.plate_move( 3 ))
        self.bind('<Right>',    lambda event: self.plate_move( 4 ))
        self.pack( fill = BOTH, expand = 1 )
        self.gui.plate_list.append( self )
        self.focus_set()
        self.gui.selected_plate = self

        self.moving_auto = False

    def plate_move_manual( self ):
        self.focus_set()
        self.gui.selected_plate = self
          
        #if len( self.table.move_directions ) > 0:
        #    direction_index =  randint( 0, len( self.table.move_directions ) - 1 ) 
        #    direction = self.table.move_directions[ direction_index ]
        #    self.plate_move( direction )   

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

            if direction == 1:
                next_table = self.gui.table_objects_scheme[ self.y_index - 1 ][ self.x_index ]
                next_turntable_need_turn = ( next_table.type == "turntable" and next_table.position == "horizontal" )
                print("actual table: ", self.table, "with type: ", self.table.type, "next table: ", next_table, "with type: ", next_table.type, "is there other plate: ", next_table.plate_on_table )

                if self.table.type == "turntable":
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

            elif direction == 2:
                next_table = self.gui.table_objects_scheme[ self.y_index + 1 ][ self.x_index ]
                next_turntable_need_turn = ( next_table.type == "turntable" and next_table.position == "horizontal" )
                print("actual table: ", self.table, "with type: ", self.table.type, "next table: ", next_table, "with type: ", next_table.type, "is there other plate: ", next_table.plate_on_table )

                if self.table.type == "turntable":

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

            elif direction == 3:
                next_table = self.gui.table_objects_scheme[ self.y_index ][ self.x_index - 1 ]
                next_turntable_need_turn = ( next_table.type == "turntable" and next_table.position == "vertical" )
                print("actual table: ", self.table, "with type: ", self.table.type, "next table: ", next_table, "with type: ", next_table.type, "is there other plate: ", next_table.plate_on_table )

                if self.table.type == "turntable":
                    
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

            elif direction == 4:
                next_table = self.gui.table_objects_scheme[ self.y_index ][ self.x_index + 1 ]
                next_turntable_need_turn = ( next_table.type == "turntable" and next_table.position == "vertical" )
                print("actual table: ", self.table, "with type: ", self.table.type, "next table: ", next_table, "with type: ", next_table.type, "is there other plate: ", next_table.plate_on_table )

                if self.table.type == "turntable":

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
        self.plate_menu.tk_popup( event.x_root, event.y_root )

    def plate_delete( self ):
        self.table.plate_on_table = False
        self.frame.destroy()
        self.plate_menu.destroy()
        self.destroy()