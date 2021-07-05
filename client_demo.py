import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PIL import Image,ImageTk
import emoji
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pickle
from datetime import datetime
import os
import threading
import struct

HOST = '127.0.0.1'
PORT = 80

class Client():	
	def __init__ (self, host, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host,port))
		msg =Tk()
		msg.withdraw()
		self.nickname = simpledialog.askstring("Nickname", "Please choose a Nickname")
		self.gui_done = False
		self.running = True

		gui_thread = threading.Thread(target=self.gui_loop)
		
		receive_thread = threading.Thread(target = self.receive)

		gui_thread.start()
		receive_thread.start()

	def gui_loop(self):
		
		self.win = tkinter.Tk()
		self.win.title('Socket M&T')
		self.win.iconbitmap('icon.ico')
		#self.win.geometry("600x800")
		app = Window(self.win)
		
		

		self.chat_label = tkinter.Label(self.win, text=emoji.emojize(":red_heart:Chat:red_heart:") ,fg="#0098FE", bg="#CCF1FF")
		self.chat_label.config(font=("Transformers Movie",20))
		self.chat_label.pack(padx=20, pady=5)

		self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
		self.text_area.pack(padx=20, pady=5)
		self.text_area.config(state='disabled',fg="#00B7FE")
		self.text_area.configure(bg="white")
		
		self.msg_label = tkinter.Label(self.win, text="Message", bg="#CCF1FF",fg="#0098FE")
		self.msg_label.config(font=("Transformers Movie",20))
		self.msg_label.pack(padx=20, pady=5)

		self.input_area = tkinter.Text(self.win, height=3)
		self.input_area.config(font=("Transformers Movie",10))
		self.input_area.pack(padx=20, pady=5)

		
		self.send_button = tkinter.Button(self.win, text=emoji.emojize("\U000025B6"), command=self.write,fg="#0098FE")
		self.send_button.config(font=( 90))
		self.send_button.pack(padx=20, pady=5)

		self.heart_button = tkinter.Button(self.win,text=emoji.emojize("\U00002665"),command=self.print_heart,fg="red")
		self.heart_button.place(x=500,y=450)
		self.face_button = tkinter.Button(self.win,text=emoji.emojize("\U0001F604"),command=self.print_facesmile)
		self.face_button.place(x=520,y=450)
		self.cry_button = tkinter.Button(self.win,text=emoji.emojize("\U0001F62D"),command=self.print_cry)
		self.cry_button.place(x=540,y=450)
		

		self.gui_done = True

		self.win.protocol("WM_DELETE_WINDOW", self.stop)

		self.win.mainloop()


	def print_heart(self) :
		heart="\U00002665"
		message = f"{self.nickname} : {heart} \n"
		self.sock.send(message.encode('utf-8'))
	def print_facesmile(self) :
		face="\U0001F604"
		message = f"{self.nickname} : {face} \n"
		self.sock.send(message.encode('utf-8'))	
	def print_cry(self) :
		cry="\U0001F62D"
		message = f"{self.nickname} : {cry} \n"
		self.sock.send(message.encode('utf-8'))

	def write(self):
		
		message = f"{self.nickname} : {self.input_area.get('1.0', 'end')}"
		self.sock.send(message.encode('utf-8'))
		self.input_area.delete('1.0', 'end')

	def stop(self):
		self.running = False
		self.win.destroy()
		self.sock.close()
		exit(0)

		

	def receive(self):	
		while self.running:
			try:
				message = self.sock.recv(1024).decode('utf-8')
				if message == 'NICK':
					self.sock.send(self.nickname.encode('utf-8'))
				else:
					if self.gui_done:
						self.text_area.config(state='normal')
						self.text_area.insert('end', message)
						self.text_area.yview('end')
						self.text_area.config(state='disabled')
			except ConnectionAbortedError:
				break
			except:
				print("Error")
				self.sock.close()
				break



class Window(Frame):

    def __init__(self, master=None):
        
        Frame.__init__(self, master)   
               
        self.master = master

        self.init_window()


    def init_window(self):
    
 

       

        menu = Menu(self)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        edit = Menu(menu)
        edit.add_command(label="Red", command=self.showImg1)
        edit.add_command(label="Blue", command=self.showImg2)
        edit.add_command(label="Yellow", command=self.showImg3)
        menu.add_cascade(label="Change Color", menu=edit)

    def showImg1(self):
       self.master.configure(bg="red")

    def showImg2(self):
       self.master.configure(bg="blue")

    def showImg3(self):
       self.master.configure(bg="yellow")


    def client_exit(self):
        exit()



clinet= Client(HOST,PORT)

