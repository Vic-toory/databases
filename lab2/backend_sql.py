from psycopg2 import sql

def insert_into(cursor,table, columns , values):
    try:
        str= "INSERT INTO "
        str=str + table +' ('
        str=str+columns+') '
        str=str+' VALUES '+ values
          
        cursor.execute(sql.SQL(str))
        return True
    except Exception as err:
        print("Error {} ".format(err))
        return False


def update(cursor,table,set,where_cond):
     try:
        str="UPDATE "
        str= str + table
        str= str + ' set ' + set
        str= str + ' where '+ where_cond 
        cursor.execute(sql.SQL(str))
        return True
     except Exception as err:
        print("Error {} ".format(err))
        return False


def delete(cursor, table, condition):
    try:
        str='DELETE FROM '+ table +' where '+ condition
        cursor.execute(sql.SQL(str))
        return True
    except Exception as err:
        print("Error {} ".format(err))
        return False


def rand_data_driver(cursor,conn,n_rows):
    x=0
    while x < n_rows:
        x= r_d_d(cursor,x,conn)
        x=x+1
    print('exit')
    return True


def r_d_d(cursor,x,conn):
    try:
        str_ind=""" select setval('\"Driver_DriverID_seq\"',(select max(\"DriverID\") from \"Driver\"));"""
        str_rand="""
        insert into "Driver" ("Rating","Experience","Name")
        values (
        (random()*5),
        (random()*10),
        (substr(md5(random()::name), 0, 6)));"""
        cursor.execute(sql.SQL(str_ind + str_rand))
    except Exception as err:
        conn.rollback()
        return x-1
    else:
        conn.commit()
    return x
 
def rand_data_car(cursor,conn,n_rows):
        x=0
        while x < n_rows:
            x= r_d_c(cursor,x,conn)
            x=x+1
        return True
 
def r_d_c(cursor,x,conn):
    try:
        str_ind=""" select setval('Car_License_plate_seq',(select max(\"License plate\") from \"Car\"));"""
        str_rand="""
        insert into "Car" ("Model","Class","Number of seats","Color","DriverIDFK")
        values (
        (select substr(md5(random()::varchar), 0, 6)),
        (select substr(md5(random()::varchar), 0, 10)),
        (select random()*5),
        (select substr(md5(random()::varchar), 0, 10)),
        (SELECT "DriverID" FROM "Driver" 
		 OFFSET floor(random()*(select count("DriverID") from "Driver")) LIMIT 1));"""
        cursor.execute(sql.SQL(str_rand + str_ind))
    except Exception as err:
        conn.rollback()
        return x-1
    else:
        conn.commit()
    return x


def select(cursor,conn, columns , tables, condition):
    try:
        str= "SELECT " + columns
        str = str + " FROM " + tables
        str = str + " WHERE " +condition
        cursor.execute(sql.SQL(str)) 
        return cursor
    except Exception as err:
        print("Error {} ".format(err))
        conn.rollback()
        return []


def tables(cursor):
    try:
        str= """
            SELECT DISTINCT TABLE_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_CATALOG = 'lab1' AND TABLE_SCHEMA = 'public'
            """
        cursor.execute(sql.SQL(str))
        return cursor
    except Exception as err:
        print("Error {} ".format(err))


def columns_in_tab(cursor,table):
    try:
        str= """
            SELECT column_name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = """ + table
            
        cursor.execute(sql.SQL(str))
        return cursor
    except Exception as err:
        print("Error {} ".format(err))