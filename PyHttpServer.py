__version__ = "0.1"


import os


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


import tkinter as tk


class LicenseWindow(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        license_text = "\n Author: Douglas Clark," \
                       "\n Contact Info: <coderelease1337@gmail.com>" \
                       "\n \n License Info: " \
                       "\n \n This program utilizes the python 3 web module http.server to allow for"\
                       "\n easy file sharing over http protocol. To make the module easier and more"\
                       "\n accessible to use, this program gives a simple GUI to interact with the"\
                       "\n module."\
                       "\n \n Copyright (C) 2017  Douglas Clark"\
                       "\n \n This program is free software: you can redistribute it and/or modify"\
                       "\n it under the terms of the GNU General Public License as published by"\
                       "\n the Free Software Foundation, under version 3 of the License."\
                       "\n \n This program is distributed in the hope that it will be useful,"\
                       "\n but WITHOUT ANY WARRANTY; without even the implied warranty of"\
                       "\n MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"\
                       "\n GNU General Public License for more details."\
                       "\n \n You should have received a copy of the GNU General Public License"\
                       "\n along with this program.  If not, see <http://www.gnu.org/licenses/>."
        l = tk.Label(self, text=license_text)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

class GeneralInfoWindow(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        general_info_text = "\n Software Version: 0.1"
        l = tk.Label(self, text=general_info_text)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)


from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E
import runpy
import sys
import _thread
import socket


class SimpleServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple HTTP Server GUI")

        self.orig_dir = os.getcwd()
        self.to_dir = None
        self.port = None

        self.message = "Enter a directory to server."
        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(master, textvariable=self.label_text)

        machine_ip = self.get_local_ip()
        self.message3 = "\n ~~~Enter below into Browser~~~\n"\
                        "\n " + machine_ip + ":8000 \n"\
                        "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        self.label_text3 = StringVar()
        self.label_text3.set(self.message3)
        self.label3 = Label(master, textvariable=self.label_text3)

        vcmd = master.register(self.validate_path) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.serve_button = Button(master, text="Run", command=self.run_server, bg="green")
        self.kill_button = Button(master, text="Stop Server", command=self.kill_server, state=DISABLED, bg="red")
        self.info_button = Button(master, text="Info", command=self.open_info_page)
        self.license_button = Button(master, text="License Info", command=self.open_license_page)

        self.label.grid(row=0, column=0, columnspan=2, sticky=W+E)
        self.entry.grid(row=1, column=0, columnspan=2, sticky=W+E)
        self.label3.grid(row=4, column=0, columnspan=2, sticky=W + E)
        self.serve_button.grid(row=5, column=0)
        self.kill_button.grid(row=5, column=1)
        self.info_button.grid(row=6, column=0)
        self.license_button.grid(row=6, column=1)


    def validate_path(self, new_path):
        self.to_dir = new_path
        return True

    def server_thread(self):
        with cd(self.to_dir):
            path4 = os.getcwd()
            print("server_thread: " + path4)
            runpy.run_module("http.server", run_name="__main__", alter_sys=True)

    def run_server(self):
        # Create a thread to launch the server module.
        try:
            _thread.start_new_thread(self.server_thread, ())
        except:
            print("Error: unable to start thread")

        self.serve_button.configure(state=DISABLED)
        self.kill_button.configure(state=NORMAL)

    def kill_server(self):
        print("This is the part were we kill the server.")
        sys.exit()

    def open_license_page(self):
        license_page = tk.Tk()
        main = LicenseWindow(license_page)
        main.pack(side="top", fill="both", expand=True)
        license_page.mainloop()

    def open_info_page(self):
        GI_page = tk.Tk()
        main = GeneralInfoWindow(GI_page)
        main.pack(side="top", fill="both", expand=True)
        GI_page.mainloop()

    def get_local_ip(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        return local_ip


root = Tk()
my_gui = SimpleServerGUI(root)
root.mainloop()