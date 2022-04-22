import pyodbc
import pandas

class SBD_DataBaseLogger():

    def __init__( self ):
        self.conn = pyodbc.connect( "Driver={SQL Server Native Client 11.0};"
                                    "Server=dbmanage.lab.ki.agh.edu.pl;"
                                    "Database=u_adzieba;"
                                    "uid=u_adzieba;pwd=qazwsxc1")
        
        self.cursor = self.conn.cursor()

    def __del__( self ):
        self.cursor.close()
        self.conn.close()
        
    def showAvailablePlates( self ):  
        return pandas.read_sql_query('select rfid_number from v_find_available_plates', self.conn )

    def showAvailableOrders( self ):  
        return pandas.read_sql_query('select * from forms', self.conn )

    def addAssembly( self, table_db_id, plate_rfid_number ):
        querry = "exec p_add_assembly {}, {}".format( int( table_db_id ), int( plate_rfid_number ) )
        self.cursor.execute( querry )
        self.conn.commit()    

    def removeAssembly( self, plate_rfid_number ):
        querry = "exec p_remove_assembly {}".format( int( plate_rfid_number ) )
        self.cursor.execute( querry )
        self.conn.commit()
    
    def moveAssembly( self, plate_rfid_number, destination_table ):
        querry = "exec p_move_assembly2 {}, {}".format( int( plate_rfid_number ), int( destination_table ))
        self.cursor.execute( querry )
        self.conn.commit()
