from datetime import datetime
import json , sqlite3 , os,subprocess
from debugger import DEBUGGER


logger = DEBUGGER('DB-CONNECTOR')

class initDB :
    def __init__(self , homePath= os.cwd() ) :

        self.db_file = f'{os.environ.get("HOME")}/database/databaseb.db'
        self.disableLog = False

        if not os.path.exists(f'{os.environ.get("HOME")}/debug') :
            os.mkdir(f'{os.environ.get("HOME")}/debug') 

        # if not os.path.exists(f'{os.environ.get("HOME")}/database') :
        #     os.mkdir(f'{os.environ.get("HOME")}/database') 

        self.log = f'{os.environ.get("HOME")}/debug/database_process.log'

    def database_logger(self, log ) :
        logger.info(log)
        # if not self.disableLog :
        #     date = datetime.now()
        #     today = date.today()
        #     datenow = str(today.strftime("%d/%m/%Y"))
        #     now = datetime.now()
        #     timenow = str(now.strftime("%H:%M:%S"))
        #     line = f"{datenow} - {timenow} : {log}\n"
        #     open( self.log  , 'a+').write(line)


    def config_database_path(self,path) :
        self.database_logger(f'Database path set to {path}')
        self.db_file = path

    def fix_database(self) :
        self.database_logger('Fixing Database')
        cli = f"fuser {self.db_file}"
        self.database_logger(cli)
        output = subprocess.getoutput(cli)
        self.database_logger(output)
        output = output.split(': ')[1]
        self.database_logger(f'Kill Process : {output}')
        cli = f'kill -9 {output}'
        self.database_logger(cli)
        output = subprocess.getoutput(cli)
        self.database_logger(cli)
        

    def db_connect(self, timeout=5):
        # self.database_logger(f'DATABASE : Connecting to {self.db_file}')
        try :
            self.con = sqlite3.connect(self.db_file , check_same_thread=False , timeout = timeout)
            self.cur = self.con.cursor()
        except sqlite3.OperationalError:
            self.database_logger('Error : Database Is Locked.')
            self.fix_database()
            self.con = sqlite3.connect(self.db_file , check_same_thread=False , timeout = timeout)
            self.cur = self.con.cursor()

        return self.cur , self.con

    def db_encode(self,db):
        dbf = json.dumps(db)
        return dbf

    def db_decode(self,db) :
        return json.loads(db)



    def execute_dict(self,cli) :
        logger.info(f"execute_dict: {cli}")
        cur , conn = self.db_connect()
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        c = conn.cursor()
        h = c.execute(cli).fetchall()
        if not 'select' in cli.lower() :
            conn.commit()
        # conn.close()
        return h

    def execute(self,cli) :
        self.database_logger(f'INFO DB : Executing : {cli}')
        cur,con = self.db_connect()
        h = cur.execute(cli).fetchall()
        if not 'select' in cli.lower() :
            con.commit()
        con.close()
        return h


    def checkExists(self , cli ) :
        cur , conn = self.db_connect()
        h = cur.execute(cli).fetchall()[0][0]
        if h == 0 :
            conn.close()
            return False
        else : 
            conn.close()
            return True


    def createTable(self,conn, create_table_sql,tableName):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.database_logger(f'Creating Table: {tableName}')
            c = conn.cursor()
            h = c.execute(create_table_sql)
            return h
        except Exception as error:
            self.database_logger(f'Creating Table Error: {error}')


    def insert_to_table(self,table_name , table_headers , table_values , autocommit= True , returncli=False) :
        cur , con = self.db_connect()
        self.database_logger(f'Inserting data into {table_name}'.format(table_name=table_name))
        table_headers = tuple(table_headers)
        table_values = tuple(table_values)

        cli = f"INSERT INTO {table_name} {table_headers} VALUES{table_values}"

        if returncli : 
            return cli

        self.database_logger('INFO DB EXECUTION: '+cli)
        cur.execute(cli)
        if autocommit == True :
            con.commit()

        con.close()
        return cur.lastrowid
            
if __name__ == '__main__' :
    pass