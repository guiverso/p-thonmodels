import psycopg2 as p2
from typing import Literal

class SqlVariable:
    def __init__(self,name:str,notnull:bool=False) -> None:
        self.name = name
        self.notnull = notnull
    
    def null(self):
        return 'not null' if self.notnull else ''

class Column(SqlVariable):
    def __init__(self, name: str,typeatr:Literal['varchar','float','int','bool' ],limit=0, notnull: bool = False) -> None:
        super().__init__(name, notnull)
        self.type = typeatr
        self.limit = limit
        if typeatr == 'varchar':
            self.type = f'varchar({self.limit})'
        
    def __str__(self) -> str:
        return f'{self.name} {self.type} {self.null()}'

class Constraint(SqlVariable):
    def __init__(self, name: str,typectr:Literal['FOREIGN','PRIMARY'],atrref:Column,tableref:str = '', notnull: bool = False) -> None:
        super().__init__(name, notnull)
        self.typectr = typectr
        self.atrref = atrref
        self.tableref = tableref
    
    def __str__(self) -> str:
        return f'CONSTRAINT {self.name} {self.typectr} KEY {self.tableref}({self.atrref.name})'

class Database: #um objeto para a database
    def __init__(self,dbname:str,password:str,user:str='postgres',port:str='5432',host:str='localhost'):
        self.namedb = dbname #nome da database
        self.user = user #usuário (postgres por padrão)
        self.password = password #senha
        self.port = port #porta (5432 por padrão)
        self.host = host #host (localhost por padrão)
        
        self.conn = None
        self.curs = None

        try:
            self.conn = p2.connect(dbname=self.namedb,user=self.user,password=self.password,host=self.host,port=self.port)#conexão
            self.curs = self.conn.cursor()#cursor
        except:
            self.conn = p2.connect(dbname='postgres',user=self.user,password=self.password)
            self.conn.autocommit = True
            self.curs = self.conn.cursor()

            self.execute(f'CREATE DATABASE {self.namedb}')
            self.conn = p2.connect(dbname=self.namedb,user=self.user,password=self.password,host=self.host,port=self.port)#conexão
            self.conn.autocommit = True
            self.curs = self.conn.cursor()#cursor

    def save(self):
        self.conn.commit()
        self.conn.close()
    
    def execute(self,sqlcommand:str):
        try:
            self.curs.execute(sqlcommand)
            return True
        except:
            return False

    def create_table(self,tablename:str,atributes:tuple[SqlVariable]):
        collumns = ','.join(str(atribute) for atribute in atributes)
        sqlcmd = f'CREATE TABLE {tablename} ({collumns})'
        return self.execute(sqlcmd)
    
    def getone(self):
        return self.curs.fetchone()
    
    def getall(self):
        return self.curs.fetchall()
    
    def get_from(self,tablename:str,atributename:str='*',Where:bool=False,atrsearch:str='',value:str=''):
        sqlcmd = f'SELECT {atributename} FROM {tablename} {f"WHERE {atrsearch} = {value}" if Where == True else ""} '

        self.execute(sqlcmd)
        return self.getall()

    def insert_in(self,tablename:str,values:tuple[str]):
        value = ''+(','.join(str(val) for val in values))
        sqlcmd = f'INSERT INTO {tablename} VALUES ({value})'
        return self.execute(sqlcmd)

    def delete(self,tablename:str,where:bool=False,atrsearch:str='',value:str=''):
        sqlcmd = f' DELETE FROM {tablename} {f"WHERE {atrsearch} = {value}" if where == True else ""}'
        return self.execute(sqlcmd)