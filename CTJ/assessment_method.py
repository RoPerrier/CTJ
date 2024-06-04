# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:24:08 2024

@author: Romain Perrier
"""

try:
    import tkinter as tk
except ImportError:
    raise Exception("tkinter is not installed, for more information refer to : https://github.com/RoPerrier/CTJ/blob/main/fix_import_error_tkinter.md")

from PIL import Image, ImageTk
    
import os

###############################         FUNCTIONS       ############################################

class AssessmentManager:
    """
    A class to manage various assessment-related operations such as sorting elements, 
    handling user inputs, and managing the state of the assessment process.

    Attributes:
    -----------
    _testing : bool
        Indicates if the assessment is currently in testing mode. Default is True.
    _bad_ending : bool
        Indicates if the assessment ended in an error state. Default is False.
    _sort : list
        A list used for storing sorted elements.
    _sort_label : list
        A list of labels corresponding to the sorted elements.
    _selected_index : int or None
        The currently selected index in the sorting process. Default is None.
    _dist : int
        A distance metric used in the CTJ assessment process. Or the value entered by the user in Rubric assessment. Default is -1.

    Methods:
    --------
    testing() -> bool:
        Property to get the testing status.
    testing(value: bool):
        Property to set the testing status.
    bad_ending() -> bool:
        Property to get the bad ending status.
    bad_ending(value: bool):
        Property to set the bad ending status.
    sort() -> list:
        Property to get the sorted elements list.
    sort(value: list):
        Property to set the sorted elements list.
    sort_label() -> list:
        Property to get the sorted labels list.
    sort_label(value: list):
        Property to set the sorted labels list.
    selected_index() -> int or None:
        Property to get the selected index.
    selected_index(value: int or None):
        Property to set the selected index.
    dist() -> int:
        Property to get the distance metric.
    dist(value: int):
        Property to set the distance metric.
    exit_program():
        Sets the testing status to False and bad ending status to True.
    rubric_close(entry):
        Sets the distance metric from the given entry and sets the testing status to False.
    validate_entry(input: str) -> bool:
        Validates the user input, allowing only digits or an empty string.
    acj_close(element, pair):
        Sorts the pair of elements based on a condition and sets the testing status to False.
    swap_images(event, index: int, trio: list):
        Swaps images in the trio based on the selected index.
    ctj_close(trio: list, slider, slider_range: int):
        Configures the sorted elements and distance metric based on the trio and slider values, and sets the testing status to False.
    """

    def __init__(self):
        self._testing = True
        self._bad_ending = False
        self._sort = []
        self._sort_label = []
        self._selected_index = None
        self._dist = -1
    
    @property
    def testing(self):
        return self._testing
    
    @testing.setter
    def testing(self, value):
        self._testing = value
    
    @property
    def bad_ending(self):
        return self._bad_ending
    
    @bad_ending.setter
    def bad_ending(self, value):
        self._bad_ending = value
    
    @property
    def sort(self):
        return self._sort

    @sort.setter
    def sort(self, value):
        self._sort = value
        
    @property
    def sort_label(self):
        return self._sort_label

    @sort_label.setter
    def sort_label(self, value):
        self._sort_label = value
        
    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        self._selected_index = value
    
    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value
    
    def exit_program(self):
        """
        Sets the testing status to False and bad ending status to True.
        """
        self.testing = False
        self.bad_ending = True
        
    def rubric_close(self, entry):
        """
        Sets the distance metric from the given entry and sets the testing status to False.
        
        Parameters:
        -----------
        entry : Entry
            The entry widget containing the distance metric.
        """
        self.dist = entry.get()
        self.testing = False
        
    def validate_entry(self, input):
        """
        Validates the user input, allowing only digits or an empty string.
        
        Parameters:
        -----------
        input : str
            The user input to be validated.
        
        Returns:
        --------
        bool
            True if the input is valid, False otherwise.
        """
        if input.isdigit() or input == "":
            return True
        else:
            return False

    def acj_close(self, element, pair):
        """
        Sorts the pair of elements based on a condition and sets the testing status to False.
        
        Parameters:
        -----------
        element : any
            The element to be used as a key for sorting.
        pair : list
            The list of elements to be sorted.
        """
        self.sort = sorted(pair, key=lambda x: x != element)
        self.testing = False
        
    def swap_images(self, event, index, trio):
        """
        Swaps images in the trio based on the selected index.
        
        Parameters:
        -----------
        event : Event
            The event that triggered the swap.
        index : int
            The index of the image to be swapped.
        trio : list
            The list containing the images.
        """
        if self.selected_index is None:
            self.selected_index = index
        else:
            self.sort[index],  self.sort[self.selected_index] =  self.sort[self.selected_index],  self.sort[index]
            trio[index], trio[self.selected_index] = trio[self.selected_index], trio[index]
            
            self.sort_label[index].config(image=self.sort[index])
            self.sort_label[self.selected_index].config(image=self.sort[self.selected_index])
            
            self.selected_index = None
    
    def ctj_close(self, trio, slider, slider_range):
        """
        Configures the sorted elements and distance metric based on the trio and slider values, and sets the testing status to False.
        
        Parameters:
        -----------
        trio : list
            The list of elements to be sorted.
        slider : Scale
            The slider widget to get the distance metric.
        slider_range : int
            The range of the slider.
        """
        self.sort = [trio[i] for i in range(len(trio))]
        self.dist = slider.get()
        if self.dist >= slider_range:
            self.dist = slider_range - 1
        if self.dist <= -1:
            self.dist = 0 
        self.testing = False


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
    item_value : int
        The estimated value made by the user for this item.

    """
    
    rubric_assessment  = AssessmentManager()
        
    item_value = None

    # Check if root and window.bgcolor are already defined
    window.create_window("Rubric")
    
    # Create text block
    l = tk.Label (padx=10, pady=10, text = "Please enter the value of this item :")
    l.config(bg=window.bgcolor)
    l.pack ()
    
    # Load images dynamically based on list elements
    
    image_path = item + ".png"
    
    if not os.path.exists(image_path):
        rubric_assessment.testing = False
        window.root.destroy()
        raise Exception(image_path + " not in directory.")
    
    image = resize_image(image_path, (window.root.winfo_screenwidth() * 0.9)//3,window.root.winfo_screenheight() * 0.6)
    
    label_frame = tk.Frame(window.root, bg=window.bgcolor)
    label_frame.pack(padx=10, pady=10)
    
    label = tk.Label(label_frame, image=image, bg=window.bgcolor)
    label.grid(row=0, column=0, padx=10, pady=10)
    
    # Entry only for int
    entry_frame = tk.Frame(window.root, bg=window.bgcolor)
    entry_frame.pack(padx=10, pady=10)
    
    vcmd = window.root.register(rubric_assessment.validate_entry)
    entry = tk.Entry(entry_frame, validate="key", validatecommand=(vcmd, '%P'))
    entry.pack(padx=10, pady=10)
    
    window.root.update_idletasks() #For macOs
    
    close_button = tk.Button(window.root, text="Next", command = lambda: rubric_assessment.rubric_close(entry))
    close_button.pack(pady=10)
    
    assessment_label = tk.Label(window.root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=window.bgcolor)
    assessment_label.pack(side=tk.BOTTOM, pady=10)
    
    window.root.protocol("WM_DELETE_WINDOW", rubric_assessment.exit_program)
    
    while rubric_assessment.testing:
        window.root.update()
    for widget in window.root.winfo_children():
        widget.destroy()
    if rubric_assessment.bad_ending or rubric_assessment.dist == "":
        window.root.destroy()
        raise Exception("Assessment not done !")
    
    item_value = int(rubric_assessment.dist)
    
    return item_value

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
    sort : list
        A list of string containing the assessment results in the format [Max, Min].
    """
    
    acj_assessment = AssessmentManager()

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
            acj_assessment.testing = False
            raise Exception(image_path + " not in directory.")
    
        images.append(resize_image(image_path, (window.root.winfo_screenwidth() * 0.9)//3, window.root.winfo_screenheight() * 0.6))
                      
    label1 = tk.Label(frame, image=images[0], bg=window.bgcolor)
    label1.grid(row=0, column=0, padx=10, pady=10)
    label1.bind("<Button-1>", lambda event: acj_assessment.acj_close(pair[0], pair))
    
    label2 = tk.Label(frame, image=images[1], bg=window.bgcolor)
    label2.grid(row=0, column=1, padx=10, pady=10)
    label2.bind("<Button-1>", lambda event: acj_assessment.acj_close(pair[1], pair))
    
    assessment_label = tk.Label(window.root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=window.bgcolor)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    window.root.protocol("WM_DELETE_WINDOW", acj_assessment.exit_program)
    
    while acj_assessment.testing:
        window.root.update()
    for widget in window.root.winfo_children():
        widget.destroy()
    if acj_assessment.bad_ending:
        window.root.destroy()
        raise Exception("Assessment not done !")
    
    sort = acj_assessment.sort
    
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
    tup : tuple
        A tuple containing the assessment results ([Max, Average, Min], dist).In the format ([int, int, int], int).
    """
    
    ctj_assessment = AssessmentManager()
    
    window.create_window("CTJ")

    #create text block
    l = tk.Label (padx=10, pady=10, text = "Please sort the item, the best to the worst, then choose the distance betwwen the middle one and the others : \n(To permuting two item, clic the first one then the second)")
    l.config(bg=window.bgcolor)
    l.pack ()

    label_frame = tk.Frame(window.root, bg=window.bgcolor)
    label_frame.pack(padx=10, pady=10)

    for image_name in trio:
        image_path = image_name + ".png"
        
        if not os.path.exists(image_path):
            ctj_assessment.testing = False
            window.root.destroy()
            raise Exception(image_path + " not in directory.")

        ctj_assessment.sort.append(resize_image(image_path, (window.root.winfo_screenwidth() * 0.9)//3,window.root.winfo_screenheight() * 0.6))
    
    ctj_assessment.sort_label = [tk.Label(label_frame, image=image) for image in ctj_assessment.sort]
    
    for i, label in enumerate(ctj_assessment.sort_label):
        label.grid(row=0, column=i, padx=10, pady=10)
        label.bind("<Button-1>", lambda event, idx=i: ctj_assessment.swap_images(event, idx, trio))
    
    slider_frame = tk.Frame(window.root, bg=window.bgcolor)
    slider_frame.pack(padx=10, pady=10)
    
    slider = tk.Scale(slider_frame, from_=0, to=slider_range, orient=tk.HORIZONTAL, length=400)
    slider.grid(row=1, column=0, columnspan=len(trio), pady=10)
    
    window.root.update_idletasks() #For macOs

    close_button = tk.Button(window.root, text="Next", command=lambda: ctj_assessment.ctj_close(trio, slider, slider_range))
    close_button.pack(pady=10)
    
    assessment_label = tk.Label(window.root, text=f"You are making the {nb_assessment} assessment")
    assessment_label.config(bg=window.bgcolor)
    assessment_label.pack(side=tk.BOTTOM, pady=10)

    window.root.protocol("WM_DELETE_WINDOW", ctj_assessment.exit_program)
    
    while ctj_assessment.testing :
        window.root.update()
        
    for widget in window.root.winfo_children():
        widget.destroy()
    if ctj_assessment.bad_ending :
        window.root.destroy()
        raise Exception("Assessment not done !")
    
    tup = (ctj_assessment.sort, ctj_assessment.dist)
    
    return tup

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
