# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:24:08 2024

@author: Romain Perrier
"""

import tkinter as tk
import importlib as il
import os

from tkinter import colorchooser

bg_color = '#f0f0f0'

###############################         FUNCTIONS       ############################################


def _rubric_assessment_method(item, nb_assessment):
    """
    Generate a window to let the user make the Rubric assessment.

    Parameters
    ----------
    item : string
        A strings representing the item being assessed.
    nb_assessment : int
        The number of assessment done.

    Raises
    ------
    Exception
        No file in directory.
    Exception
        The assessment was not done.

    Returns
    -------
    int
        The estimated value made by the user for this item.

    """
    def close():
        nonlocal item_value
        item_value = entry.get()
        root.destroy()
    
    def validate_entry(input):
        if input.isdigit() or input == "":
            return True
        else:
            return False

    
    def change_bg_color():
        color = colorchooser.askcolor()[1]
        if color:
            global bg_color
            bg_color = color
            root.config(bg=bg_color)
            frame.config(bg=bg_color)
            l.config(bg=bg_color)
            label.config(bg=bg_color)
        
    il.reload(tk)
        
    item_value = None

    root = tk.Tk()
    root.title("Rubric")
    try:
        root.wm_attributes("-zoomed", True)
    except tk.TclError :
        root.state('zoomed')
    root.config(bg=bg_color)
    root.option_add("*Font", ("TkDefaultFont", 14))
    root.resizable(False, False)
    
    #create menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    parameters_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Parameters", menu=parameters_menu)
    parameters_menu.add_command(label="Change Background Color", command=change_bg_color)
    
    #create text block
    l = tk.Label (padx=10, pady=10, text = "Please enter the value of this item :")
    l.config(bg=bg_color)
    l.pack ()
    
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(padx=10, pady=10)
    
    # Load images dynamically based on list elements
    
    image_path = item + ".png"
    
    if not os.path.exists(image_path):
        root.destroy()
        raise Exception(image_path + " not in directory.")
    
    image = resize_image(image_path, (root.winfo_screenwidth() * 0.9)//3)
    
    label = tk.Label(frame, image=image, bg=bg_color)
    label.grid(row=0, column=0, padx=10, pady=10)
    
    # Entry only for int
    vcmd = root.register(validate_entry)
    entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry.pack(padx=10, pady=10)
    
    close_button = tk.Button(root, text="Next", command=close)
    close_button.pack(pady=10)
    
    assessment_label = tk.Label(root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=bg_color)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
    
    if (item_value is None) or (item_value == "") :
        raise Exception("Assessment not done !")
        
    
    return int(item_value)

def _acj_assessment_method(id_judge, pair, nb_assessment):
    """
    Generate a window to let the user make the ACJ assessment.

    Parameters
    ----------
    id_judge : int
        The id of the judge making the assessment.
    pair : list of string
        A list of strings representing the pair of items being assessed.
    nb_assessment : int
        The number of assessment done.

    Raises
    ------
    Exception
        No file in directory.
    Exception
        The assessment was not done.

    Returns
    -------
    list
        A list of string containing the assessment results in the format [Max, Min].

    """
    def close(element):
        nonlocal sort
        sort = sorted(pair, key=lambda x: x != element)
        root.destroy()
    
    def change_bg_color():
        color = colorchooser.askcolor()[1]
        if color:
            global bg_color
            bg_color = color
            root.config(bg=bg_color)
            frame.config(bg=bg_color)
            l.config(bg=bg_color)
            label1.config(bg=bg_color)
            label2.config(bg=bg_color)
        
    il.reload(tk)
        
    sort = []

    root = tk.Tk()
    root.title("ACJ")
    try:
        root.wm_attributes("-zoomed", True)
    except tk.TclError :
        root.state('zoomed')
    root.config(bg=bg_color)
    root.option_add("*Font", ("TkDefaultFont", 14))
    root.resizable(False, False)
    
    #create menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    parameters_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Parameters", menu=parameters_menu)
    parameters_menu.add_command(label="Change Background Color", command=change_bg_color)
    
    #create text block
    l = tk.Label (padx=10, pady=10, text = "Judge " + str(id_judge+1) + "\nPlease select the best item :")
    l.config(bg=bg_color)
    l.pack ()
    
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(padx=10, pady=10)
    
    # Load images dynamically based on list elements
    images = []
    
    for image_name in pair:
        image_path = image_name + ".png"
        
        if not os.path.exists(image_path):
            root.destroy()
            raise Exception(image_path + " not in directory.")
    
        images.append(resize_image(image_path, (root.winfo_screenwidth() * 0.9)//3))
                      
    label1 = tk.Label(frame, image=images[0], bg=bg_color)
    label1.grid(row=0, column=0, padx=10, pady=10)
    label1.bind("<Button-1>", lambda event: close(pair[0]))
    
    label2 = tk.Label(frame, image=images[1], bg=bg_color)
    label2.grid(row=0, column=1, padx=10, pady=10)
    label2.bind("<Button-1>", lambda event: close(pair[1]))
    
    assessment_label = tk.Label(root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=bg_color)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
    
    if len(sort) != 2 :
        raise Exception("Assessment not done !")
    
    return sort

def _ctj_assessment_method(slider_range, trio, nb_assessment):
    """
    Generate a window to let the user make the CTJ assessment.

    Parameters
    ----------
    slider_range : int
        The range of the slider.
    trio : list of string
        A list of strings representing the trio of items being assessed.
    nb_assessment : int
        The number of assessment done.
        
    Raises
    ------
    Exception
        No file in directory.
    Exception
        The assessment was not done.

    Returns
    -------
    
        A tuple containing the assessment results (Max,(dist,Average),Min).In the format (int, (int, int), int).
    """
    def swap_images(event, index):
        nonlocal selected_index, images, image_labels
        if selected_index is None:
            selected_index = index
        else:
            images[index], images[selected_index] = images[selected_index], images[index]
            trio[index], trio[selected_index] = trio[selected_index], trio[index]
            
            image_labels[index].config(image=images[index])
            image_labels[selected_index].config(image=images[selected_index])
            
            selected_index = None

    def close():
        nonlocal permutation
        nonlocal dist
        permutation = [trio[i] for i in range(len(trio))]
        dist = slider.get()
        if dist >= slider_range:
            dist = slider_range - 1
        if dist <= -1:
            dist = 0 
        root.destroy()
    
    def change_bg_color():
        color = colorchooser.askcolor()[1]
        if color:
            global bg_color
            bg_color = color
            root.config(bg=bg_color)
            frame.config(bg=bg_color)
            l.config(bg=bg_color)
        
    il.reload(tk)
    
    permutation = []
    dist = -1

    root = tk.Tk()
    root.title("CTJ")
    try:
        root.wm_attributes("-zoomed", True)
    except tk.TclError :
        root.state('zoomed')
    root.config(bg=bg_color)
    root.option_add("*Font", ("TkDefaultFont", 14))
    root.resizable(False, False)
        
    #create menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    parameters_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Parameters", menu=parameters_menu)
    parameters_menu.add_command(label="Change Background Color", command=change_bg_color)
    
    #create text block
    l = tk.Label (padx=10, pady=10, text = "Please sort the item, the best to the worst, then choose the distance betwwen the middle one and the others : \n(To permuting two item, clic the first one then the second)")
    l.config(bg=bg_color)
    l.pack ()

    frame = tk.Frame(root, bg=bg_color)
    frame.pack(padx=10, pady=10)

    images = []
    
    for image_name in trio:
        image_path = image_name + ".png"
        
        if not os.path.exists(image_path):
            root.destroy()
            raise Exception(image_path + " not in directory.")

        images.append(resize_image(image_path, (root.winfo_screenwidth() * 0.9)//3))
    
    image_labels = [tk.Label(frame, image=image) for image in images]

    for i, label in enumerate(image_labels):
        label.grid(row=0, column=i, padx=10, pady=10)
        label.bind("<Button-1>", lambda event, idx=i: swap_images(event, idx))

    selected_index = None
    
    slider = tk.Scale(frame, from_=0, to=slider_range, orient=tk.HORIZONTAL, length=400)
    slider.grid(row=1, column=0, columnspan=len(trio), pady=10)

    close_button = tk.Button(root, text="Next", command=close)
    close_button.pack(pady=10)
    
    assessment_label = tk.Label(root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=bg_color)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
    
    if len(permutation) != 3 :
        raise Exception("Assessment not done !")

    return permutation,dist

from PIL import Image, ImageTk

def resize_image(image_path, width):
    """
    Resize an image while preserving its aspect ratio using Pillow.

    Parameters
    ----------
    image_path : string
        Path to the image file.
    width : int
        The maximum width of images displayed.

    Returns
    -------
    resized_image : tk.PhotoImage
        Resized image as a Tkinter PhotoImage object.
    """
        
    original_image = Image.open(image_path)
    original_width, original_height = original_image.size
    
    # Calculate aspect ratio
    aspect_ratio = original_width / original_height
    
    # Calculate new dimensions while preserving aspect ratio
    new_width = width
    new_height = int(width / aspect_ratio)
    
    # Resize the image using Pillow
    resized_image = original_image.resize((int(new_width), int(new_height)))
    
    # Convert the resized image to a Tkinter PhotoImage object
    resized_photo = ImageTk.PhotoImage(resized_image)
    
    return resized_photo










