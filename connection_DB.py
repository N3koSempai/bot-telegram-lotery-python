# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 01:10:13 2021

@author: n3ko
"""

import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import re
import psycopg2
#from modules import formats



host = os.environ.get("DATABASE_URL")

result = []

#se requieren dos bases una para jugar otra para la banca
# connection with DB
class DB:
    
    def __ini__(self):
        pass
    
            
    #create the database sqlite3 with the Tables
    def first_start(self):
        
        try:
            
            conexion = psycopg2.connect(host)
            cursor = conexion.cursor()

            cursor.execute('CREATE TABLE Lotery(ID SERIAL PRIMARY KEY, Username VARCHAR(50), NUMEROTOTAL INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Fijo(ID SERIAL PRIMARY KEY, Username VARCHAR(50), FIJO INTEGER, VALUE INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Corrido(ID SERIAL PRIMARY KEY, Username VARCHAR(50), CORRIDO INTEGER, VALUE INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Centena(ID SERIAL PRIMARY KEY, Username VARCHAR(50), CENTENA INTEGER, VALUE INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Parle(ID SERIAL PRIMARY KEY, Username VARCHAR(50), PARLE FLOAT, VALUE INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Rifa(ID SERIAL PRIMARY KEY, Username VARCHAR(50), RIFA INTEGER, VALUE INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Premio(ID SERIAL PRIMARY KEY, Username VARCHAR(50), PREMIO INTEGER, VALUE INTEGER);')
            conexion.commit()
            cursor.execute('CREATE TABLE Banca(ID SERIAL PRIMARY KEY,Username VARCHAR(50),Price INTEGER)')
            conexion.commit()
            conexion.close()
        except psycopg2.ProgrammingError:
            print("las tablas ya existen")

    
    
    
    #for erase the space and other thing
    #for add user. the price is cero by default for modified after 
    def _add_user(self,status, lugar , name, listanum, listaprice):
        conexion = psycopg2.connect(host)
        cursor = conexion.cursor()
        try:

            if lugar == "Corrido" or lugar == "corrido":
                cursor.execute('SELECT VALUE FROM Corrido WHERE Username = %s AND CORRIDO = %s;', ([name,listanum]))
                x = cursor.fetchone()
                if x == [] or x == None:
                    cursor.execute('INSERT INTO Corrido(Username, CORRIDO, VALUE) VALUES (%s,%s,%s);',( name,listanum,listaprice) )
                    conexion.commit()
                else:
                    x = int(x[0]) + int(listaprice)
                    cursor.execute('UPDATE Corrido SET VALUE = %s WHERE Username = %s AND CORRIDO = %s;', ([x,name,listanum]))
                    conexion.commit()
                if status == True:
                    conexion.close()
                return True
            
            elif lugar == "Centena" or lugar == "centena":
                cursor.execute('SELECT VALUE FROM Centena WHERE Username = %s AND CENTENA = %s;', ([name,listanum]))
                x = cursor.fetchone()
                
                if x == [] or x == None: 
                    cursor.execute('INSERT INTO Centena(Username, CENTENA, VALUE) VALUES (%s,%s,%s);',( name,listanum,listaprice) )
                    conexion.commit()
                else:
                    x = int(x[0]) + int(listaprice)
                    cursor.execute('UPDATE Centena SET VALUE = %s WHERE Username = %s AND CENTENA = %s;', ([x,name,listanum]))
                    conexion.commit()
                if status == True:
                    conexion.close()
                return True
            
            elif lugar == "parle" or lugar =="Parle":
                cursor.execute('SELECT VALUE FROM Parle WHERE Username = %s AND PARLE = %s;', ([name,listanum]))
                x = cursor.fetchone()
                if x == [] or x == None: 
                    cursor.execute('INSERT INTO Parle(Username, PARLE, VALUE) VALUES (%s,%s,%s);',( name,listanum,listaprice) )
                    conexion.commit()
                else:
                    x = int(x[0]) + int(listaprice)
                    cursor.execute('UPDATE Parle SET VALUE = %s WHERE Username = %s AND PARLE = %s;', ([x,name,listanum]))
                    conexion.commit()
                if status == True:
                    conexion.close()
                return True
            
            elif lugar == "Rifa" or lugar == "rifa":
                cursor.execute('SELECT VALUE FROM Rifa WHERE Username = %s AND RIFA = %s;', ([name,listanum]))
                x = cursor.fetchone()
                if x == [] or x == None: 
                    cursor.execute('INSERT INTO Rifa(Username, RIFA, VALUE) VALUES (%s,%s,%s);',( name,listanum,listaprice) )
                    conexion.commit()
                else:
                    x = int(x[0]) + int(listaprice)
                    cursor.execute('UPDATE Rifa SET VALUE = %s WHERE Username = %s AND RIFA = %s;', ([x,name,listanum]))
                    conexion.commit()
                if status == True:
                    conexion.close()
                return True
            
            elif lugar == "Fijo" or lugar == "fijo":
                cursor.execute('SELECT VALUE FROM Fijo WHERE Username = %s AND FIJO = %s;', ([name,listanum]))
                x = cursor.fetchone()
                if x == [] or x == None: 
                    cursor.execute('INSERT INTO Fijo(Username, FIJO, VALUE) VALUES (%s,%s,%s);',( name,listanum,listaprice) )
                    conexion.commit()
                else:
                    x = int(x[0]) + int(listaprice)
                    cursor.execute('UPDATE Fijo SET VALUE = %s WHERE Username = %s AND FIJO = %s;', ([x,name,listanum]))
                    conexion.commit()
                if status == True:
                    conexion.close()
                return True
            
            elif lugar == "Banca" or lugar == "banca":
                cursor.execute('SELECT Price FROM Banca WHERE Username = %s;', ([name]))
                x = cursor.fetchone()
            
                if x == [] or x == None:
                   
                    cursor.execute('INSERT INTO Banca(Username, Price) VALUES (%s,%s);',( name,listaprice) )
                    conexion.commit()
                else:
                    x = int(x[0]) + int(listaprice)
                    cursor.execute('UPDATE Banca SET Price = %s WHERE Username = %s;', ([x,name]))
                    conexion.commit()
                if status == True:
                    conexion.close()
                return True
            
            else:
                return False
        except:
            return False
    

    #update the banca and delete the diference    
    def preadduser(self, Username, listaprice):
        global result
        conexion = psycopg2.connect(host)
        cursor = conexion.cursor()
        cursor.execute('SELECT Price FROM Banca WHERE Username = %s;', ([Username]))
        result = cursor.fetchone()
        
        if result != 0 and result != None:
            result = result[0]
            count = 0
            
            for i in listaprice:
                if int(i) <= int(result):
                    count = count + 1
                    result = int(result) - int(i)
                    cursor.execute('UPDATE Banca SET Price = %s WHERE Username = %s;', ([result,Username]))
                    conexion.commit()
                else:
                    conexion.close()
                    return count
            
            conexion.close()    
            return count
        
        else:
            return ("no hay datos de este usario en la banca")
        
    def revertion(self, temp, Username, listaprice):
        global result
        conexion = psycopg2.connect(host)
        cursor = conexion.cursor()
        cursor.execute('SELECT Price FROM Banca WHERE Username = %s;', ([Username]))
        result = cursor.fetchone()
        result = result[0]
        count = 0
        for i in range(temp):
            result = int(result) + int(listaprice[count])
            cursor.execute('UPDATE Banca SET Price = %s WHERE Username = %s;', ([result,Username]))
            conexion.commit()
            count = count + 1
        
        conexion.close()
                

    
        
    def consulting(self,lugar, data):
        conexion = psycopg2.connect(host)
        cursor = conexion.cursor()
        print(data[0])
        #try:
        #x = data[0]
        result = []
        if lugar == "corrido" or lugar == "Corrido":
            cursor.execute('SELECT Username,CORRIDO,VALUE FROM Corrido WHERE CORRIDO = %s;', ([data[0]]))
            result = cursor.fetchall()
        elif lugar == "Centena" or lugar == "centena":
            cursor.execute('SELECT Username,CENTENA,VALUE FROM Centena WHERE CENTENA = %s;', ([data[0]]))
            result = cursor.fetchall()
        elif lugar == "Rifa" or lugar == "rifa":
            cursor.execute('SELECT Username,RIFA,VALUE FROM Rifa WHERE RIFA = %s;', ([data[0]]))
            result = cursor.fetchall()
        elif lugar == "Parle" or lugar == "parle":
            cursor.execute('SELECT Username,PARLE,VALUE FROM Parle WHERE PARLE = %s;', ([data[0]]))
            result = cursor.fetchall()
        elif lugar == "Fijo" or lugar == "fijo":
            cursor.execute('SELECT Username,FIJO,VALUE FROM Fijo WHERE FIJO = %s;', ([data[0]]))
            result = cursor.fetchall()
        elif lugar == "banca" or lugar == "Banca":
            cursor.execute('SELECT Username,Price FROM Banca WHERE Username = %s;', ([data[0]]))
            result = cursor.fetchall()
        elif lugar == 0:
            print(data)
            cursor.execute('SELECT Username,CORRIDO,VALUE FROM Corrido WHERE Username = %s;', ([data]))
            resultc = cursor.fetchall()
            resultc.insert(0, "Corrido:")
            cursor.execute('SELECT Username,CENTENA,VALUE FROM Centena WHERE Username = %s;', ([data]))
            resultce = cursor.fetchall()
            resultce.insert(0,"Centena:")
            cursor.execute('SELECT Username,RIFA,VALUE FROM Rifa WHERE Username = %s;', ([data]))
            resultr = cursor.fetchall()
            resultr.insert(0,"Rifa:")
            cursor.execute('SELECT Username,PARLE,VALUE FROM Parle WHERE Username = %s;', ([data]))
            resultp = cursor.fetchall()
            resultp.insert(0,"Parle")
            cursor.execute('SELECT Username,FIJO,VALUE FROM Fijo WHERE Username = %s;', ([data]))
            resultf = cursor.fetchall()
            resultf.insert(0, "Fijo:")
            cursor.execute('SELECT Username,Price FROM Banca WHERE Username = %s;', ([data]))
            resultb = cursor.fetchall()
            resultb.insert(0,"Banca")
            conexion.commit()
            conexion.close()
            result = (f"""centena: \n {resultce} \n\n corrido: \n {resultc} \n\n
Fijo \n {resultf} \n\n  parle: \n {resultp} \n\n banca: \n {resultb}"""
.format(resultce,resultc,resultf,resultp,resultb))
            return result
        conexion.commit()
        conexion.close()

        return result
                
        #except:
            #return False
    
    
    #delete a specific user. 
    def delete(self,lugar, data, number):
        "use lugar for the table and data for the name"
        
        conexion = psycopg2.connect(host)
        cursor = conexion.cursor()
        number = int(number)
        print(number)
        data = str(data[0])
        print(data)
        try:
            if lugar == "corrido" or lugar == "Corrido":
                if number != 0:
                    cursor.execute('DELETE FROM Corrido WHERE Username = %s AND CORRIDO = %s;', ([data,number]))
                elif number == 0:
                    cursor.execute('DELETE FROM Corrido WHERE Username = %s;', ([data]))
            elif lugar == "centena" or lugar == "Centena":
                if number != 0:
                    cursor.execute('DELETE FROM Centena WHERE Username = %s AND CENTENA = %s;', ([data,number]))
                elif number == 0:
                    cursor.execute('DELETE FROM Centena WHERE Username = %s;', ([data]))
            elif lugar == "fijo" or lugar == "Fijo":
                if number != 0:
                    cursor.execute('DELETE FROM Fijo WHERE Username = %s AND FIJO = %s;', ([data,number]))
                elif number == 0:
                    cursor.execute('DELETE FROM Fijo WHERE Username = %s;', ([data]))
            elif lugar == "parle" or lugar == "Parle":
                if number != 0:
                    cursor.execute('DELETE FROM Parle WHERE Username = %s AND PARLE = %s;', ([data,number]))
                elif number == 0:
                    cursor.execute('DELETE FROM Parle WHERE Username = %s;', ([data]))
                
            elif lugar == "rifa" or lugar == "Rifa":
                if number != 0:
                    cursor.execute('DELETE FROM Rifa WHERE Username = %s AND RIFA = %s;', ([data,number]))
                elif number == 0:
                    cursor.execute('DELETE FROM Rifa WHERE Username = %s;', ([data]))
                    
            elif lugar == "banca" or lugar == "Banca":
                cursor.execute('DELETE FROM Banca WHERE Username = %s;', ([data]))
            
            conexion.commit()
            conexion.close()
            return True
        except:
            return False
    
    
    
        #remember fix the error in VALUES is sender with string and not variables
    def deleteall(self):
        conexion = psycopg2.connect(host)
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM Corrido;')
            conexion.commit()
            cursor.execute('DELETE FROM Centena;')
            conexion.commit()
            cursor.execute('DELETE FROM Parle;')
            conexion.commit()
            cursor.execute('DELETE FROM Rifa;')
            conexion.commit()
            cursor.execute('DELETE FROM fijo;')
            conexion.commit()
            cursor.execute('DELETE FROM Premio;')
            conexion.commit()
            cursor.execute('DELETE FROM Lotery;')
            conexion.commit()
            #cursor.execute('DELETE FROM sqlite_sequence') sqlite only
            
            conexion.close()
            return True
        except:
            return False
    
    #clear and sanitize the string
    def clean_string(self, string):
        x = string
        x = re.sub(r"[^A-z0-9@$. ]", "", x)
        if x == " ":
            return False
        y = x.split(" ")
        name = y[0]
        listanum = []
        listaprice = []
        lugar = ""
        for i in y:
            if i == y[1] or i == y[1]:
                try:
                    lugar = i
                    temp = x.split(lugar, 2)
                    temp = temp[1]
                    temp = temp.split("$", 2)
                    listanum = temp[0].split(" ")
                    listanum = list(filter(("").__ne__,listanum))
                    listaprice = temp[1].split(" ")
                    listaprice = list(filter(("").__ne__,listaprice))

                except:
                    return False
            else:
                continue
        if lugar == "Banca" or lugar == "banca":
            status = 0
            listaprice = listaprice[0]
            return self._add_user(status, lugar, name, 0, listaprice)
        
        
        
        elif int(len(listaprice)) != 1 and len(listaprice) == len(listanum) and lugar != "Banca" and lugar != "banca":
            temp = self.preadduser( name, listaprice)
            if temp == None and temp != 0:
                return ("not banca")
            
            if temp == len(listanum):
                
                return self.post_processing(lugar, name ,listanum, listaprice)
            
            elif temp < len(listanum):
                return ("banca no da. solo se pueden realizar con estas condiciones : ",temp,"operaciones. no se realizo ninguna")
            elif temp == 0:
                return ("banca en cero o por debajo de lo requerido")
        
        elif len(listaprice) == 1:
            
            if lugar == "parlec" or lugar == "Parlec":
                listanum = self.parlecombine(listanum)
                print(listanum)
                
            for i in listanum:
                        if len(listaprice) < len(listanum):
                                listaprice.append(listaprice[0])
                  
                        else:
                            temp = self.preadduser(name, listaprice)
                            if temp == None and temp != 0:
                                return ("este usuario aun no tiene cuenta en la banca")
                            
                            elif temp == len(listaprice):
                                return self.post_processing(lugar, name ,listanum, listaprice)
                            elif temp < len(listaprice):
                                print(len(listaprice))
                                self.revertion(temp,name,listaprice)
                                return (f"banca no da. solo se pueden realizar con estas condiciones {temp}  operaciones, cambios cancelados, ")
                            
                            
                            else:
                                return ("banca en cero o por debajo de lo requerido: {temp}")
        else:
            return False
        
        
        
        
    #take a list and name and iterate for make the consulting to database
    def post_processing(self,lugar, name: str, listanum: list, listaprice: list):
       
        
        
        count = len(listaprice)
        status = False
        if lugar == "parlec" or lugar == "Parlec":
            lugar = "Parle"
        try:
            for i in range(count):
                
                if status == False:
                    self._add_user(status, lugar, name,listanum[i],listaprice[i])
                elif status == True:
                    return self._add_user(status, lugar, name,listanum[i],listaprice[i])
                if i == count - 1:
                    status = True
            
        except:
            return False
            
        
        
        #verific a number or a name
    def verificator(self, data):
        data = data.split(" ")
        for i in data:
                if i == "corrido" or i == "Corrido" or i == "Centena" or i == "centena" or i == "parle" or i == "Parle" or i == "Rifa" or i == "rifa" or i == "fijo" or i == "fijo":
                    lugar = i
                    data = list(filter((i).__ne__,data))
                    x = []
                    print(data)
                    if  data != None and data != []:
                        x = self.consulting(lugar, data)
                        return x
                    else:
                        return ("no especificaste usuario, imposible realizar busqueda")
                    break
            
                elif i ==  "Banca" or i == "banca":
                    lugar = i
                    data = list(filter((i).__ne__,data))
                    x = []
                    x = self.consulting(lugar, data)
                    return x
                    break
                
                else:
                    for x in i:
                        if x == "@":
                            lugar = 0
                            x = self.consulting(lugar,i)
                            return x
                        break
                    break
        
    def predelete(self, data):
        data = data.split(" ")
        print(data)
        for i in data:
            i = str(i)
            if i == "corrido" or i == "Corrido" or i == "Centena" or i == "centena" or i == "parle" or i == "Parle" or i == "Rifa" or i == "rifa" or i == "fijo" or i == "fijo":

                lugar = i
                data = list(filter((i).__ne__,data))
                numbers = list(filter((data[0]).__ne__,data))
  
                x = []
                for i in numbers:
                    print(i)
                    x = self.delete(lugar,data, i)
                    return x
                x = self.delete(lugar,data, 0) 
                return x
            elif i == "banca" or i == "Banca":
                lugar = i
                data = list(filter((i).__ne__,data))
                x = self.delete(lugar,data, 0)
                return x
            else:
                return ("no has especificado en que tipo de numero borrar")
    
    
    def parlecombine(self, lista):
        """para combinaciones de parle"""
        temp = ""
        parles = []
        templist = lista.copy()

        for i in lista:
            temp = str(i)
            
            for x in templist:
                if x != i:
                    temp = temp +"." + str(x)
                    parles.append(temp)
                    temp = str(i)
                
                
            templist.remove(i)
    
        return parles


    
    def premiun(self, number):

        count = 0
        centena = ""
        corrido1 = ""
        corrido2 = ""
        m = []
        Fijo = ""
        if len(str(number)) == 7:
            try:
                for i in str(number):
                    m.append(i)
                    if count < 3:
                        centena = centena + i
                    
                    if count >= 1 and count < 3:
                        Fijo = Fijo + i
                    if count > 2 and count <= 4:
                        corrido1 = corrido1 + i
                    if count > 4:
                        corrido2 = corrido2 + i

                    count = count+ 1
                    
                parlet1 = (m[1],m[2],".",m[3],m[4])
                parlet2 = (m[1],m[2],".",m[5],m[6])
                parlet3 = (m[3],m[4],".",m[5],m[6])
                parlet1 = float("".join(parlet1))
                parlet2 = float("".join(parlet2))
                parlet3 = float("".join(parlet3))
            except:
                return False
            centena = centena.split(" ", 1)
            corrido1 = corrido1.split(" ", 1)
            corrido2 = corrido2.split(" ", 1)
            Fijo = Fijo.split(" ", 1)
            conexion = psycopg2.connect(host)
            cursor = conexion.cursor()
            cursor.execute('SELECT Username,CENTENA,VALUE FROM Centena WHERE CENTENA = (%s);', (centena))
            centena =  cursor.fetchall()
            cursor.execute('SELECT Username,CORRIDO,VALUE FROM Corrido WHERE CORRIDO = (%s);', (corrido1))
            corrido1 = cursor.fetchall()
            cursor.execute('SELECT Username,CORRIDO,VALUE FROM Corrido WHERE CORRIDO = (%s);', (corrido2))
            corrido2 = cursor.fetchall()
            cursor.execute('SELECT Username,FIJO,VALUE FROM Fijo WHERE FIJO = (%s);', (Fijo))
            Fijo = cursor.fetchall()
            cursor.execute('SELECT Username,PARLE,VALUE FROM Parle WHERE PARLE = (%s);', ([parlet1]))
            parlet1 = cursor.fetchall()
            cursor.execute('SELECT Username,PARLE,VALUE FROM Parle WHERE PARLE = (%s);', ([parlet2]))
            parlet2 = cursor.fetchall()
            cursor.execute('SELECT Username,PARLE,VALUE FROM Parle WHERE PARLE = (%s);', ([parlet3]))
            parlet3 = cursor.fetchall()
            
            #trait to create a function for make $ inside
            #clio = formats.add_simbol(parlet1)
            #print(clio)
            
            
            
            result = []
            result = (f"""ganadores de la centena: \n {centena} \n\n ganadores del corrido: \n {corrido1} \n\n ganadores del segundo corrido: \n {corrido2} \n\n
ganadores del Fijo \n {Fijo} \n\n ganadores del primer parlet: \n {parlet1} \n\n ganadores del segundo parlet: \n {parlet2} \n\n ganadores del tercer parlet: \n {parlet3} \n\n"""
                      .format(centena,corrido1,corrido2,Fijo,parlet1,parlet2,parlet3))
            
            #print(result)
            #for clean the result

            return result
        elif len(str(number) != 7):
            return ("not len")
        
                
        
                
