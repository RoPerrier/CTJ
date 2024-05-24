# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:56:51 2024

@author: Romain Perrier
"""

import numpy as np
import tkinter as tk
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

def ready(info="", status=None):
    """
    If the assessment is done by the user, create a window to check if the user is ready

    Parameters
    ------
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
    def close():
        close_button.destroy()
        if status is not None :
            skip_button.destroy()
        countdown_label.config(text="The test begin in 3 seconds...")
        countdown(3)

    def countdown(seconds):
        nonlocal Bad_Ending
        if seconds > 0:
            countdown_label.config(text=f"The test begin in {seconds} seconds...")
            root.after(1000, countdown, seconds - 1)
        else:
            Bad_Ending = False
            root.destroy()
    
    def skip_tutorial():
        nonlocal skip
        nonlocal Bad_Ending
        skip = True
        Bad_Ending = False
        root.destroy()

    Bad_Ending = True
    skip = False
    bg_color = "#f0f0f0"
    
    root = tk.Tk()
    root.title("Ready ?")
    try:
        root.wm_attributes("-zoomed", True)
    except tk.TclError :
        root.state('zoomed')
    root.config(bg=bg_color)
    root.option_add("*Font", ("TkDefaultFont", 14))
    root.resizable(False, False)
    
    if status is None:
        t = 'Next Test'
    else:
        t = 'Tutorial'
        
    l = tk.Label(root, padx=10, pady=10, text=info)
    l.config(bg=bg_color)
    l.pack()

    countdown_label = tk.Label(root, padx=10, pady=10, text="", fg="red")
    countdown_label.config(bg=bg_color)
    countdown_label.pack()

    close_button = tk.Button(root, text=t, command=close)
    close_button.pack(pady=10)
    
    if status is not None :
    
        skip_button = tk.Button(root, text="Skip Tutorial", command=skip_tutorial)
        skip_button.pack(pady=10)
    
    root.mainloop()
    
    if Bad_Ending:
        raise Exception("You are not ready.. You must click on the 'Ready' button.")
    return skip

# Example usage
# ready("This is a test message", "tutorial")
