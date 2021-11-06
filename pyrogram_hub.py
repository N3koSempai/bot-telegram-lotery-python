# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 15:58:45 2021

@author: n3ko
"""
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))



from connection_DB import DB
from pyrogram import Client, filters


#set the workdirectory


#instance the db module
db = DB()
db.first_start()


#acces data for account
ids = os.environ["T_id"]
hashs = os.environ["T_hash"]
tokens = os.environ["TB_token"]


id_owner = ["", ""] #add your admin user here
TARGET = "" #add your target group
MENTION = "[{}](tg://user?id={})"
MESSAGE = "{} Bienvenido al grupo  {}"
last_command = ""
current = 0
P_MESSAGE = ("""Hola. esta es una lista de opciones para ti \n /agregar :usa este comando para agregar usuarios
/eliminar :con este puede eliminar usuarios agregados por error \n /verificar :para verificar un usuario por nombre o por tipos
/premio :con este comando puedes agregar el premio y se realizaran los calculos necesarios
/Reiniciar :reinicia todas las jugadas a cero CUIDADO.
/c :este comando usalo en cualquer momento para que el bot cancele lo que este haciendo
/author :about the developer""")
author = "author: @N3koSenpai . Este bot es un programa estadistico con base de datos. No me hago responsable del uso del bot por terceras partes"

#configuration of provilage with a external file
app = Client("Lotery_bot", api_id= int(ids), api_hash= str(hashs), bot_token = str(tokens))



    #welcome
    #@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
    #def welcome(client, message):
        #new_members = [u.mention for u in message.new_chat_members]
        #text = f"{} "emoji.SPARKLES, ", ".join(new_members))
        #message.reply_text(text, disable_web_page_preview = True)



    
#receive comand in private
@app.on_message(filters.private & filters.command(["start" ,"agregar" ,  "eliminar", "verificar", "premio"
                                                   ,"Reiniciar", "author"]))
def main(client, msg):
    #set the id of actual member
    global current
    current = msg.from_user.username
    global last_command
    #defiden if is the owner
    for i in id_owner:
        if current == i:
            if msg.text == "/start":
                msg.reply(P_MESSAGE)
                
            elif msg.text == "/agregar":
                msg.reply_text("escribe en el siguiente orden : @ejemplo corrido 2 1 2 $10 20 30 ")
                last_command = msg.text
                
        
            elif msg.text== "/eliminar":
                last_command = msg.text
                msg.reply_text("escribe el usuario seguido por los numeros")
            
            
            elif msg.text== "/verificar":
                last_command = msg.text
                msg.reply_text("Escribe primero el tipo de numero y luego el nombre ex: corrido @fermin. si no pones el tipo de numero se mostraran todo para ese nombre")
                              
        
            elif msg.text== "/premio":
                last_command = msg.text
                msg.reply_text("introduce el numero del premio y recibe los ganadores")
                
            elif msg.text== "/Reiniciar":
                last_command = msg.text
                msg.reply_text("Esta punto de borrar todas las jugadas.escriba cualquier cosa para continuar o use el comando /c para cancelar")
            
            elif msg.text== "/ReiniciarBanca":
                last_command = msg.text
                msg.reply_text("Reiniciada la banca de todos a 0")
            
            elif msg.text== "/author":
                last_command = msg.text
                msg.reply_text(author)
            
            
        

    
@app.on_message(filters.private & filters.regex("/c"))
def cancel_function(client, msg):
    global last_command
    last_command = msg.text
    current = msg.from_user.username
    if msg.text == "/c":
        app.send_message(current, "comando cancelado")
        app.send_message(current, "preciona /start para ver opciones")
    else:
        pass

    
    
@app.on_message(filters.private & filters.text)
def aswer_for_text(client, msg):
    current = msg.from_user.username
    if last_command == "/agregar":
        valid = db.clean_string(msg.text)
        
        if valid == True or valid == None:
            msg.reply_text("ejecutado correctamente")
        elif valid == False:
            msg.reply_text("error, imposible continuar,verifique")
        elif valid == "not banca":
            msg.reply_text("")
        
            
            
    if last_command == "/eliminar" :
        valid = db.predelete(msg.text)
        if valid == True:
            msg.reply_text("usuario eliminado")
        elif valid == False:
            msg.reply_text("error. verifique la informacion")
        
    elif last_command == "/verificar" :
        app.send_message(current, "verificando usuario...tenga paciencia, puede demorar")
        valid = db.verificator(msg.text)
        msg.reply_text(valid)
 
    elif last_command == "/Reiniciar":
        valid = db.deleteall()
        if valid == True:
            app.send_message(current, "Todo en cero")
        else:
            app.send_message(current,"a ocurrido un error")

        
        
    elif last_command == "/premio":
        valid = db.premiun(msg.text)
        if valid != False and valid != "not len":
            msg.reply_text(valid)
        elif valid == False:
            msg.reply_text("error en procesado. revise que todos sean numeros")
        elif valid == "not len":
            msg.reply_text("cantidad de digitos incorrecta . el numero tiene que ser de 7 digitos")
                
        
        
        
    elif last_command == "/no factible":
        app.send_message(current, "")
    elif last_command == "/c":
        app.send_message(current, "selecciona un comando")
        app.send_message(current, P_MESSAGE)
        
    else:
        pass

app.run()
