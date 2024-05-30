# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:56:51 2024

@author: Romain Perrier
"""

import numpy as np
import tkinter as tk

from tkinter import colorchooser
from sklearn.preprocessing import MinMaxScaler

###############################         FUNCTIONS       ############################################

def Rescale (Min,Max,estimated_values):
    """
    Rescaling the estimated_values between Min and Max.

    Parameters
    ----------
    Min : int
        The minimum value of items.
    Max : int
        The maximum value of items.
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.

    Returns
    -------
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.

    """
    scaler = MinMaxScaler(feature_range=(Min, Max))
    estimated_values = scaler.fit_transform(np.array(estimated_values).reshape(-1, 1)).flatten().astype(type(Min)).tolist()
    return estimated_values

def SSR (true_values,estimated_values):
    """
    Calculate the sum of squared residuals, a mesure of similarity between true value and predicted value. Near 0 the value are not similar, Near 1 the values are similar

    Parameters
    ----------
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.

    Returns
    -------
    SSR : float
        The sum of squared residuals, a mesure of similarity between true value and predicted value. Near 0 the value are not similar, Near 1 the values are similar.

    """
    estimated_STD = np.std(estimated_values)
    MSE = np.square(np.subtract(true_values, estimated_values)).mean()
    true_STD_squared = estimated_STD**2 - MSE
    SSR = true_STD_squared / (estimated_STD**2+ np.finfo(float).eps)
    if SSR < 0:
        SSR=0;
    elif SSR > 1:
        SSR=1
    return SSR

def ready(window, info="", status=None):
    """
    If the assessment is done by the user, create a window to check if the user is ready

    Parameters
    ------
    window : windowManager
        windowManager object
    info : string
        A string for display information.
    status : string 
        Set if we are in a tutorial or not
        
    Raises
    ------
    Exception
        The window was not destroy in the correct way.

    Returns
    -------
    skip : bool
        True if the user skip the tutorial.

    """
    def exit_program():
        nonlocal testing
        nonlocal BadEnding
        testing = False
        BadEnding = True
            
    def close():
        close_button.destroy()
        if status is not None :
            skip_button.destroy()
        countdown_label.config(text="The test begin in 3 seconds...")
        countdown(3)

    def countdown(seconds):
        nonlocal testing
        if seconds > 0:
            countdown_label.config(text=f"The test begin in {seconds} seconds...")
            window.root.after(1000, countdown, seconds - 1)
        else:
            testing = False
    
    def skip_tutorial():
        nonlocal skip
        nonlocal testing
        skip = True
        testing = False
    
    skip = False
    testing = True
    BadEnding = False
    
    window.create_window("Ready ?")

    if status is None:
        t = 'Next Test'
    else:
        t = 'Tutorial'
        
    l = tk.Label(window.root, padx=10, pady=10, text=info)
    l.config(bg=window.bgcolor)
    l.pack()

    countdown_label = tk.Label(window.root, padx=10, pady=10, text="", fg="red")
    countdown_label.config(bg=window.bgcolor)
    countdown_label.pack()

    close_button = tk.Button(window.root, text=t, command=close)
    close_button.pack(pady=10)
    
    if status is not None :
    
        skip_button = tk.Button(window.root, text="Skip Tutorial", command=skip_tutorial)
        skip_button.pack(pady=10)
    
    window.root.protocol("WM_DELETE_WINDOW", exit_program)
    
    while testing :
        window.root.update()
    for widget in window.root.winfo_children():
        widget.destroy()
    if BadEnding :
        window.root.destroy()
        raise Exception("You are not ready.. You must click on the 'Ready' button.")

    return skip


class WindowManager():
    def __init__(self):
        self._root = None
        self._bgcolor = '#f0f0f0'
    
    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self, value):
        self._root = value
    
    @property
    def bgcolor(self):
        return self._bgcolor
    
    @bgcolor.setter
    def bgcolor(self, value):
        self._bgcolor = value
    
    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bgcolor = color
            self.root.config(bg=self.bgcolor)
    
    def destroy(self):
        if self.root is not None :
            self.root.destroy()
        
                
    def create_window(self, title):
                
        if self.root is None:
            self.root = tk.Tk()
            self.root.title(title)
            try:
                self.root.wm_attributes("-zoomed", True)
            except tk.TclError:
                self.root.state('zoomed')
            self.root.config(bg=self.bgcolor)
            self.root.option_add("*Font", ("TkDefaultFont", 14))
            self.root.resizable(False, False)
            
            menu_bar = tk.Menu(self.root)
            self.root.config(menu=menu_bar)
            parameters_menu = tk.Menu(menu_bar, tearoff=0)
            menu_bar.add_cascade(label="Parameters", menu=parameters_menu)
            parameters_menu.add_command(label="Change Background Color", command=self.change_bg_color)

        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.root.title(title)
            menu_bar = tk.Menu(self.root)
            self.root.config(menu=menu_bar)
            parameters_menu = tk.Menu(menu_bar, tearoff=0)
            menu_bar.add_cascade(label="Parameters", menu=parameters_menu)
            parameters_menu.add_command(label="Change Background Color", command=self.change_bg_color)
