import backend_sql as bs
import sys, os
import time

class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def tables(self):
        self.model.cursor=self.model.table()
        cur=self.model.cursor
        self.view.show_tables(cur)

    def columns_in_tab(self,table):
        tab = "\'" + table +"\'"
        self.model.cursor=self.model.columns_in_tab(tab)
        cur=self.model.cursor
        self.view.show_table_columns(cur,table)

    def insert(self,table,columns,values,count):
       try:
            tab = "\"" + table +"\""
            col=""
            val=""
            for x in range(len(columns)):
                if x==len(columns)-1:
                    col=col+"\"" + columns[x] + "\""
                else:
                    col=col+"\"" + columns[x] + "\""+", "
            for x in range(len(values)):
                if isinstance(values[x], str):
                    values[x]="\'" + values[x] + "\'"
            tmp=0
            ind=int(len(values)/count)
            for i in range(ind):
                val=val+'('
                for x in range(count):
                    if x==count-1:
                        val=val + values[tmp+x]
                    else:
                        val=val + values[tmp+x] +","
                if i ==ind-1:
                    val=val+')'
                else:
                    val=val+'),'
                tmp=tmp+count
            self.view.show_insert(table,columns,values,self.model.insert(tab,col,val))
       except:
            return
            
        

    def update(self,table,columns,values,condition):
        if len(condition)==0:
            condition="\'t\'"
        tab = "\"" + table +"\""
        set=""
        for x in range(len(values)):
            if isinstance(values[x], str):
                values[x]="\'" + values[x] + "\'"
        for x in range(len(columns)):
            if x==len(columns)-1:
                set=set+"\"" + columns[x] + "\""+"="+  values[x]
            else:
                set=set+"\"" + columns[x] + "\""+"="+ values[x] +", "
        
        
        self.view.show_update(table,set,condition,self.model.update(tab,set,condition))

    def delete(self,table,condition):
        table="\""+table+"\""
        if table == "\"Driver\"":
            flag=self.delete_driver(table, condition)
        elif table == "\"Car\"":
            flag=self.delete_car(table, condition)
        elif table == "\"Order\"":
            flag=self.delete_order(table, condition)
        elif table == "\"Passenger\"":
            flag=self.delete_passenger(table, condition)
        else:
            flag=False
           
        self.view.display_delete(table, condition,flag)

    def delete_driver(self,table, condition):
        try:
            f1=self.model.delete("\"Car\"","\"DriverIDFK\" in (select \"DriverID\" from \"Driver\" where "+condition+")")
            f2=self.model.delete("\"Order\"","\"DriverIDFK\" in (select \"DriverID\" from \"Driver\" where "+condition+")")
            if f1 and f2:
                return self.model.delete("\"Driver\"",condition)
            else:
                return False
        except:
            return False;

    def delete_order(self,table, condition):
        try:
            return self.model.delete("\"Order\"",condition)
        except:
            return False;

    def delete_car(self,table, condition):
        try:
           return self.model.delete("\"Car\"",condition)
        except:
            return False;

    def delete_passenger(self,table, condition):
        try:
            f1=self.model.delete("\"Order\"","\"NumberFK\" in (select \"Number\" from \"Passenger\" where "+condition+")")
            if f1:
                return self.model.delete("\"Passenger\"",condition)
            else:
                return False
        except:
            return False;

    def rand_data(self,table,n_rows):
        if table == "Driver":
            fl=self.model.rand_data_driver(n_rows)
        elif table == "Car":
            fl=self.model.rand_data_car(n_rows)
        else:
            fl=False 
        self.view.rand_data(table,n_rows,fl)

    def select(self, columns , tables, condition):
            col=""
            tab=""
            for x in range(len(columns)):
                if x==len(columns)-1:
                    if columns[0]=="*":
                        col=columns[0]
                    else:
                        col=col+"\"" + columns[x] + "\""
                else:
                    col=col+"\"" + columns[x] + "\""+", "
            for x in range(len(tables)):
                if x==len(tables)-1:
                    tab=tab + "\""+ tables[x]+ "\""
                else:
                    tab=tab + "\""+ tables[x]+ "\"" +","
            if len(condition)== 0:
                condition="\'t\'"

            col_view=[]
            if columns[0]=="*":
                for x in tables:
                    t = "\'" + x +"\'"
                    for y in self.model.columns_in_tab(t):
                        col_view.append(y[0])
            else:
                col_view=columns
            
            start_time = time.time()
            self.view.select(col_view , tab,self.model.select(col,tab, condition),time.time() - start_time)
