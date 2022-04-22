from tkinter import *
from tkinter.ttk import Combobox
from turtle import screensize
from PIL     import ImageTk, Image
#from Plate import *
from Tables import *
from random import randint
import os, sys, ctypes
import threading
import time
import json

class SBD_Application():

    def __init__( self ):
       
        with open( os.path.join( sys.path[0], "config.json" ), 'r') as config_file:
            self.config_file = json.load( config_file )

        self.task_list    = []
        self.plate_list   = []
        self.tables_list  = []
        self.table_images = []
        self.graphics = [ 
            "plate.png",         #0
            "conveyor_h.png",    #1
            "station_right.png", #2    
            "turntable_h.png",   #3
            "conveyor_v.png",    #4
            "station_left.png",  #5
            "station_up.png",    #6
            "station_down.png",  #7
            "turntable_v.png" ]  #8

        self.track_creating_active = False
        self.new_track = None
        self.selected_plate = None
        self.tile_width  = self.config_file['window']['tile_width']
        self.tile_height = self.config_file['window']['tile_height']
        self.table_area_width  = self.config_file['window']['table_area_width']
        self.table_area_height = self.config_file['window']['table_area_height']

        self.userLogged = False
        self.userRole = 0

        self.drawWindow()

        for i in range( len( self.graphics )):
            folder_with_graphics = self.config_file['graphics']['folder']
            img = Image.open( os.path.join( sys.path[0], folder_with_graphics, self.graphics[i] ))
            img = img.resize(( self.tile_width , self.tile_height ))
            self.table_images.append( ImageTk.PhotoImage( img ))

        self.drawTables()

    def drawWindow( self ):

        # place window on screen middle
        user32 = ctypes.windll.user32
        screen_width  = user32.GetSystemMetrics(0) 
        screen_height = user32.GetSystemMetrics(1)
        
        self.window_width  = self.config_file['window']['app_width']
        self.window_height = self.config_file['window']['app_height']
        x_offset = int(( screen_width - self.window_width ) / 2 )
        y_offset = int(( screen_height - self.window_height ) / 2 )
        window_size = "{}x{}+{}+{}".format( self.window_width, self.window_height, x_offset, y_offset )
        
        # draw application window
        self.window = Tk()
        self.window.title( "Application for SBD course" )
        self.window.geometry( window_size )
        self.window.resizable( 0 , 0 ) 
          
        self.window_background = Frame( self.window, bg = 'black' )
        self.window_background.pack_propagate( 0 )
        self.window_background.pack( fill = BOTH, expand = 1 )

        self.visualization_background = Frame( self.window_background, width = self.table_area_width , height = self.table_area_height, bg = 'grey' )
        self.visualization_background.pack_propagate( 0 )
        self.visualization_background.pack( side = TOP, anchor = NW )
                        
        # assign application menu
        menu_bar = Menu( self.window_background )

        file_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='File', menu = file_bar )
        file_bar.add_command( label ='New File', command = None)
        file_bar.add_command( label ='Open...', command = None)
        file_bar.add_command( label ='Save', command = None)
        file_bar.add_separator()
        file_bar.add_command( label ='Exit', command = self.window.destroy )

        edit_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='Użytkownicy', menu = edit_bar )
        edit_bar.add_command( label ='Zaloguj', command = self.showUserLogInMenu )
        edit_bar.add_command( label ='Wyloguj', command = self.userLogOut )
        edit_bar.add_command( label ='Dodaj', command = None )
        edit_bar.add_command( label ='Edytuj', command = self.showUserChooseMenu )
   
        help_bar = Menu( menu_bar, tearoff = 0 )
        menu_bar.add_cascade( label ='Zlecenia', menu = help_bar )
        help_bar.add_command( label ='Dodaj', command = None )
        help_bar.add_command( label ='Edytuj', command = None )
        help_bar.add_command( label ='Przeglądaj', command = None )

        self.window.config( menu = menu_bar )

    def drawTables( self ):


        # table array filled with 0
        self.tables_list = [[0] * self.config_file['window']['columns'] for i in range(self.config_file['window']['rows'])]

        # grid filled with table objects
        for table_name in self.config_file['tables']['objects']:
                    
            table_x = self.config_file['tables']['objects'][table_name]['x']
            table_y = self.config_file['tables']['objects'][table_name]['y']
            table_type = self.config_file['tables']['objects'][table_name]['type']
            table_db_id = self.config_file['tables']['objects'][table_name]['db_id']
            possible_moves = self.config_file['tables']['objects'][table_name]['move_directions']

            if table_type == "D":
                table = DemouldingTable( self, table_type, possible_moves, table_x, table_y, table_name, table_db_id )
            elif table_type == "M":
                table = MouldingTable( self, table_type, possible_moves, table_x, table_y, table_name, table_db_id )
            elif table_type == "C":
                table = ComposingTable( self, table_type, possible_moves, table_x, table_y, table_name, table_db_id )
            elif table_type == "+":
                table = TurnTable( self, table_type, possible_moves, table_x, table_y, table_name, table_db_id )
            elif table_type == "|" or table_type == "-":
                table = ConveyorTable( self, table_type, possible_moves, table_x, table_y, table_name, table_db_id )
            
            self.tables_list[table_y][table_x] = table

    def showUserLogInMenu( self ):

        popup_width  = 400
        popup_height = 200
        popup_x_root = int( self.window.winfo_x() + self.window_width  / 2 - popup_width  / 2 )
        popup_y_root = int( self.window.winfo_y() + self.window_height / 2 - popup_height / 2 )
        popup_size   = "{}x{}+{}+{}".format( popup_width, popup_height, popup_x_root, popup_y_root )
        popup = Toplevel()
        popup.title("Logowanie")
        popup.geometry( popup_size )
        popup.resizable( False, False )

        login = StringVar( popup )     
        password = StringVar( popup )

        label_login = Label( popup, text = "Login: " ).place( x = 20, y = 20 )
        input_login = Entry( popup, textvariable = login ).place( x = 120, y = 20 ) 

        label_password = Label( popup, text = "Hasło: " ).place( x = 20, y = 50 )
        input_password = Entry( popup, textvariable = password ).place( x = 120, y = 50 ) 

        button_accept =  Button( popup, text = "Zaloguj", command = lambda : self.menuLogInAccept( popup, login.get(), password.get() ) ).place( x = 20,  y = 100 )
        button_cancel = Button( popup, text = "Anuluj",  command = lambda : self.menuLogInCancel( popup ) ).place( x = 120,  y = 100 )

    def menuLogInAccept( self, widget, login, password ):
        db_read = SBD_DataBaseLogger()

        if db_read.userLogIn( login, password ):
            self.userLogged = True
            self.userRole = 1
            widget.destroy()       

    def userLogOut( self ):
        self.userLogged = False
        self.userRole = 0 
        pass

    def menuLogInCancel( self, widget ):
        widget.destroy()

    def showUserChooseMenu( self ):

        #if self.userRole == 0:
        #    return 0

        popup_width  = 600
        popup_height = 600
        popup_x_root = int( self.window.winfo_x() + self.window_width  / 2 - popup_width  / 2 )
        popup_y_root = int( self.window.winfo_y() + self.window_height / 2 - popup_height / 2 )
        popup_size   = "{}x{}+{}+{}".format( popup_width, popup_height, popup_x_root, popup_y_root )
        popup = Toplevel()
        popup.title("Edytuj użytkowników")
        popup.geometry( popup_size )
        popup.resizable( False, False )

        db_read = SBD_DataBaseLogger()
        df = db_read.usersShow()

        background = Frame( popup, width = 600 , height = 500 )
        background.pack_propagate( 0 )
        background.place( x = 0, y = 50 )
        
        pt = pandastable.Table(background, dataframe = df )
        pt.show()

        login = StringVar( popup )     
        password = StringVar( popup )

        label_login = Label( popup, text = "Wybierz użytkownika: " ).place( x = 20, y = 20 )

        button_update =  Button( popup, text = "Wybierz", command = lambda : self.menuEditUserChoose( popup, pt ) ).place( x = 20,  y = 550 )
        button_delete =  Button( popup, text = "Usuń", command = lambda : self.menuEditUserDelete( popup, pt ) ).place( x = 100,  y = 550 )
        button_cancel =  Button( popup, text = "Anuluj", command = lambda : self.menuEditUserCancel( popup ) ).place( x = 150,  y = 550 )

    def menuEditUserChoose( self, widget, pt ):
        row = pt.getSelectedRows()
        self.menuEditUser( row.iloc[0] )
        widget.destroy() 

    def menuEditUserDelete( self, widget, pt ):
        row = pt.getSelectedRows()
        user_id = row.iloc[0]['user_id'] 

        db_read = SBD_DataBaseLogger()
        db_read.userDelete( user_id )

        widget.destroy() 
        self.showUserChooseMenu()

    def menuEditUserCancel( self, widget ):
        widget.destroy() 

    def menuEditUser( self, row ):
        popup_width  = 400
        popup_height = 600
        popup_x_root = int( self.window.winfo_x() + self.window_width  / 2 - popup_width  / 2 )
        popup_y_root = int( self.window.winfo_y() + self.window_height / 2 - popup_height / 2 )
        popup_size   = "{}x{}+{}+{}".format( popup_width, popup_height, popup_x_root, popup_y_root )
        popup = Toplevel()
        popup.title("Modyfikuj użytkownika")
        popup.geometry( popup_size )
        popup.resizable( False, False )

        db_read = SBD_DataBaseLogger()
        df = db_read.getUserRoles()
        roles = []

        for i in range(len(df)) :
            roles.append( df.iloc[i, 1] ) 
            
        text_login     = StringVar( popup, row['login'] )
        text_password  = StringVar( popup, row['password'] )
        text_firstname = StringVar( popup, row['firstname'] )
        text_lastname  = StringVar( popup, row['lastname'] )
        text_email     = StringVar( popup, row['email'] )
        text_role      = StringVar( popup, row['name'] )

        input_login     = Entry( popup, textvariable = text_login     ).place( x = 20, y = 20 ) 
        input_password  = Entry( popup, textvariable = text_password  ).place( x = 20, y = 40 ) 
        input_firstname = Entry( popup, textvariable = text_firstname ).place( x = 20, y = 60 ) 
        input_lastname  = Entry( popup, textvariable = text_lastname  ).place( x = 20, y = 80 ) 
        input_email     = Entry( popup, textvariable = text_email     ).place( x = 20, y = 100 ) 
        input_role   = Combobox( popup, textvariable = text_role, values = roles ).place( x = 20, y = 140 )
     
        button_accept =  Button( popup, text = "Zmień",   command = lambda : self.menuEditAccept( popup, row, text_login.get(), 
                                                                                                              text_password.get(), 
                                                                                                              text_firstname.get(), 
                                                                                                              text_lastname.get(), 
                                                                                                              text_email.get(),
                                                                                                              text_role.get(),
                                                                                                              df )).place( x = 20, y = 170 )

        button_cancel =  Button( popup, text = "Anuluj",  command = lambda : self.menuEditCancel( popup ) ).place( x = 120, y = 170 )

    def menuEditAccept( self, widget, row, new_login, new_password, new_firstname, new_lastname, new_email, new_role_name, df ):

        if ( row['login'] != new_login
             or row['password'] != new_password 
             or row['firstname'] != new_firstname 
             or row['lastname'] != new_lastname 
             or row['email'] != new_email 
             or row['name'] != new_role_name ):
            
            sub_df = df[df['name'] == new_role_name ]
            new_role_id = sub_df.values[0][0] 
            
            db_read = SBD_DataBaseLogger()
            db_read.userModify( row['user_id'], new_login, new_password, new_firstname, new_lastname, new_email, new_role_id )
        else:
            print('bez zmian')

        widget.destroy() 
        self.showUserChooseMenu()

    def menuEditCancel( self, widget ):
        widget.destroy() 
        self.showUserChooseMenu()

    def run( self ):
        mainloop()

if __name__ == "__main__":
    print("dupa, nie to okno dzbanie")
