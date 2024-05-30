# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:24:08 2024

@author: Romain Perrier
"""

import tkinter as tk
import os

from PIL import Image, ImageTk

###############################         FUNCTIONS       ############################################


def rubric_assessment_method(item, nb_assessment, window):
    """
    Generate a window to let the user make the Rubric assessment.

    Parameters
    ----------
    item : string
        A strings representing the item being assessed.
    nb_assessment : int
        The number of assessment done.
    window : WindowManager
        an object to manage human assessments.
        
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
    def exit_program():
        nonlocal testing, BadEnding
        testing = False
        BadEnding = True
        
    def close():
        nonlocal item_value
        nonlocal testing
        item_value = entry.get()
        testing = False
    
    def validate_entry(input):
        if input.isdigit() or input == "":
            return True
        else:
            return False
        
    item_value = None
    testing = True
    BadEnding = False

    # Check if root and window.bgcolor are already defined
    window.create_window("Rubric")
    
    # Create text block
    l = tk.Label (padx=10, pady=10, text = "Please enter the value of this item :")
    l.config(bg=window.bgcolor)
    l.pack ()
    
    frame = tk.Frame(window.root, bg=window.bgcolor)
    frame.pack(padx=10, pady=10)
    
    # Load images dynamically based on list elements
    
    image_path = item + ".png"
    
    if not os.path.exists(image_path):
        testing = False
        window.root.destroy()
        raise Exception(image_path + " not in directory.")
    
    image = resize_image(image_path, (window.root.winfo_screenwidth() * 0.9)//3,window.root.winfo_screenheight() * 0.6)
    
    label = tk.Label(frame, image=image, bg=window.bgcolor)
    label.grid(row=0, column=0, padx=10, pady=10)
    
    # Entry only for int
    vcmd = window.root.register(validate_entry)
    entry = tk.Entry(window.root, validate="key", validatecommand=(vcmd, '%P'))
    entry.pack(padx=10, pady=10)
    
    close_button = tk.Button(window.root, text="Next", command=close)
    close_button.pack(pady=10)
    
    assessment_label = tk.Label(window.root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=window.bgcolor)
    assessment_label.pack(side=tk.BOTTOM, pady=10)
    
    window.root.protocol("WM_DELETE_WINDOW", exit_program)

    while testing:
        window.root.update()
    for widget in window.root.winfo_children():
        widget.destroy()
    if BadEnding:
        window.root.destroy()
        raise Exception("Assessment not done !")
        
    return int(item_value)

def acj_assessment_method(id_judge, pair, nb_assessment, window):
    """
    Generate a window to let the user make the ACJ assessment.

    Parameters
    ----------
    id_judge : int
        The id of the judge making the assessment.
    pair : list of string
        A list of strings representing the pair of items being assessed.
    nb_assessment : int
        The number of assessments done.
    window : WindowManager
        an object to manage human assessments.

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
    def exit_program():
        nonlocal testing, BadEnding
        testing = False
        BadEnding = True
        
    def close(element):
        nonlocal sort, testing
        sort = sorted(pair, key=lambda x: x != element)
        testing = False
        
    sort = []
    testing = True
    BadEnding = False

    window.create_window("ACJ")
        
    # Create text block
    l = tk.Label (padx=10, pady=10, text = "Judge " + str(id_judge+1) + "\nPlease select the best item :")
    l.config(bg=window.bgcolor)
    l.pack ()
    
    frame = tk.Frame(window.root, bg=window.bgcolor)
    frame.pack(padx=10, pady=10)
    
    # Load images dynamically based on list elements
    images = []
    
    for image_name in pair:
        image_path = image_name + ".png"
        
        if not os.path.exists(image_path):
            window.root.destroy()
            testing = False
            raise Exception(image_path + " not in directory.")
    
        images.append(resize_image(image_path, (window.root.winfo_screenwidth() * 0.9)//3, window.root.winfo_screenheight() * 0.6))
                      
    label1 = tk.Label(frame, image=images[0], bg=window.bgcolor)
    label1.grid(row=0, column=0, padx=10, pady=10)
    label1.bind("<Button-1>", lambda event: close(pair[0]))
    
    label2 = tk.Label(frame, image=images[1], bg=window.bgcolor)
    label2.grid(row=0, column=1, padx=10, pady=10)
    label2.bind("<Button-1>", lambda event: close(pair[1]))
    
    assessment_label = tk.Label(window.root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=window.bgcolor)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    window.root.protocol("WM_DELETE_WINDOW", exit_program)
    
    while testing:
        window.root.update()
    for widget in window.root.winfo_children():
        widget.destroy()
    if BadEnding:
        window.root.destroy()
        raise Exception("Assessment not done !")
    
    return sort
def ctj_assessment_method(slider_range, trio, nb_assessment, window):
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
    window : WindowManager
        an object to manage human assessments.
        
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
    def exit_program():
        nonlocal testing
        nonlocal BadEnding
        testing = False
        BadEnding = True
        
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
        nonlocal testing
        permutation = [trio[i] for i in range(len(trio))]
        dist = slider.get()
        if dist >= slider_range:
            dist = slider_range - 1
        if dist <= -1:
            dist = 0 
        testing = False
    
    permutation = []
    dist = -1
    testing = True
    BadEnding = False

    window.create_window("CTJ")

    #create text block
    l = tk.Label (padx=10, pady=10, text = "Please sort the item, the best to the worst, then choose the distance betwwen the middle one and the others : \n(To permuting two item, clic the first one then the second)")
    l.config(bg=window.bgcolor)
    l.pack ()

    frame = tk.Frame(window.root, bg=window.bgcolor)
    frame.pack(padx=10, pady=10)

    images = []
    
    for image_name in trio:
        image_path = image_name + ".png"
        
        if not os.path.exists(image_path):
            testing = False
            window.root.destroy()
            raise Exception(image_path + " not in directory.")

        images.append(resize_image(image_path, (window.root.winfo_screenwidth() * 0.9)//3,window.root.winfo_screenheight() * 0.6))
    
    image_labels = [tk.Label(frame, image=image) for image in images]

    for i, label in enumerate(image_labels):
        label.grid(row=0, column=i, padx=10, pady=10)
        label.bind("<Button-1>", lambda event, idx=i: swap_images(event, idx))

    selected_index = None
    
    slider = tk.Scale(frame, from_=0, to=slider_range, orient=tk.HORIZONTAL, length=400, bg=window.bgcolor)
    slider.grid(row=1, column=0, columnspan=len(trio), pady=10)

    close_button = tk.Button(window.root, text="Next", command=close)
    close_button.pack(pady=10)
    
    assessment_label = tk.Label(window.root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=window.bgcolor)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    window.root.protocol("WM_DELETE_WINDOW", exit_program)
    
    while testing :
        window.root.update()
    for widget in window.root.winfo_children():
        widget.destroy()
    if BadEnding :
        window.root.destroy()
        raise Exception("Assessment not done !")

    return permutation,dist

def resize_image(image_path, width, height):
    """
    Resize an image while preserving its aspect ratio using Pillow.

    Parameters
    ----------
    image_path : string
        Path to the image file.
    width : int
        The maximum width of images displayed.
    width : int
        The height width of images displayed.

    Returns
    -------
    resized_image : tk.PhotoImage
        Resized image as a Tkinter PhotoImage object.
    """
        
    original_image = Image.open(image_path)
    
    # Use the thumbnail method to resize the image in place
    original_image.thumbnail((width, height), Image.Resampling.LANCZOS)
    
    # Convert the resized image to a Tkinter PhotoImage object
    resized_image = ImageTk.PhotoImage(original_image)
    
    return resized_image