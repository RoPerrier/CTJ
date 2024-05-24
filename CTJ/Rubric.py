# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:45:35 2024

@author: Romain Perrier
"""
import random as rd
import numpy as np
import time

from .util import SSR, Rescale, ready

def make_Rubric_assessment(items, item, sensibility, true_values, estimated_values, assessment_method, nb_assessment, width, height):
    """
    This function is used to do the assessment on an item and return the value of it

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    item :  string
        A string representing the item being assessed.
    sensibility :tuple
         A tuple cointaining the marge of error, and the probability of making a mystake. In the format (int, double).
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.
    true_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.    
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value.
    nb_assessment: int
        The number of assessment done.
    width : int
        The maximum width of images displayed. Proportion are preserved.
    height : int
        The maximum height of images displayed. Proportion are preserved.

    Raises
    ------
    Exception
        There are no true value nor assessment_method, both are None.
    
    Returns
    -------
    estimated_values : list of int
        The list containing the estimated values for all items.
    assessment_duration : double
        Duration of the assessment in second.
    one_more_bias : int
        One if the judgment is biaised else 0.

    """
    
    one_more_bias = 0
    
    if assessment_method is not None :
        
        ready()

        a = time.time()
        
        #We let the judges make the assessment
        estimated_values[items.index(item)] = assessment_method(item, width, height, nb_assessment)
        
        b = time.time()
        
        assessment_duration = b-a
        
    elif true_values is not None :
            
        a = time.time()
        
        bias = 0
        
        r = rd.random()
        
        if r < sensibility[1] :
        
            bias = sensibility[0]
            
            r = rd.random()
            
            if r < 0.5 :
                bias = bias * -1
                
            one_more_bias = 1
            
        
        estimated_values[items.index(item)]  =  true_values[items.index(item)] + bias
        
        b = time.time()
        
        assessment_duration = b-a
        
    else :
        
        raise Exception("There are no true value nor assessment_method, both are None")
    
    return estimated_values , assessment_duration, one_more_bias

def Rubric(min_item, max_item, items, sensibility = (0,0), true_values = None, assessment_method = None, width = 500, height = 500):
    """
    Rubric Judgment is an evaluation method based on the direct notation of an item. An item is shown and we must evaluate it and give a value to it.

    Parameters
    ----------
    min_item : tuple
        The min_item we wont to use. In the format (int, string).
    max_item : tuple
        The max_item we wont to use. In the format (int, string).
    items : list of string
        A list of strings representing the items to be assessed.
    sensibility : tuple
        A tuple cointaining the marge of error, and the probability of making a mystake. In the format (int, double). The default is (0,0).
    true_values : list of int, optional
        A list of int containing the true values corresponding to each item in the `items` list. The default is None.
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value. The default is None.
    width : int
        The maximum width of images displayed. Proportion are preserved. The default is 500.
    height : int
        The maximum height of images displayed. Proportion are preserved. The default is 500.
    

    Returns
    -------
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.
    int
        Number of iteration.
    cond : float
        Accuracy of estimated value at the end of algorithm.
    nb_bias : int
        Number of biases.
    assessments_time : int
        The duration of the assessments.
        
    """
    
    #If min and max value are not in the items list we add them
    if min_item[1] not in items :
         items.append(min_item[1])
         if true_values is not None :
             true_values.append(min_item[0])
    if max_item[1] not in items :
         items.append(max_item[1])
         if true_values is not None :
             true_values.append(max_item[0])
    
    items_copy = items[:]
    
    rd.shuffle(items_copy)
    
    assessments_time = 0
    
    nb_bias = 0
    
    estimated_values = np.zeros(len(items))
    
    if assessment_method is not None :
        
        skip_tutorial = ready(info="The Rubric assessment involves individually grading each item.\n\n On each iteration, you will be asked to enter the value of the item shown, in a box below.\n\n By clicking on the 'Tutorial' button, you can access the tutorial.\nThe tutorial consists of an evaluation of the algorithm. After completing the tutorial evaluation, the actual test will begin.\n\n Between each evaluation, a button will appear.\n Ensure you are ready before clicking on it, as once clicked, a countdown will start. At the end of the countdown, you can evaluate the item, so make sure you are prepared.", status="Tuto")
    
        if not skip_tutorial:
            item = rd.choice(items)
            _ = assessment_method(item, width, height, -1)    

    while len(items_copy) != 0 :
        
        item = items_copy.pop()
        estimated_values, time, one_more_bias = make_Rubric_assessment(items, item, sensibility, true_values, estimated_values, assessment_method, len(items)-len(items_copy), width, height)
        assessments_time += time
        nb_bias += one_more_bias
    
    estimated_values = Rescale(min_item[0], max_item[0], estimated_values)
    
    acc = None
    
    print("===============================================================")
    print("| Result of Rubric algorithm")
    print("| Items : ", items)
    if true_values is not None :
        print("| True values : ", true_values)
    print("| Estimated values : ", estimated_values)
    if true_values is not None :
        acc = SSR(true_values, estimated_values)
        print("| Accuracy : ", acc)
    if sensibility != (0,0) :
        print("| Number of bias : ", nb_bias)
    print("| Iteration : ", len(items))
    if assessment_method is not None :
        print("| Total duration : ", assessments_time)
    print("===============================================================")
    return estimated_values, len(items), acc, nb_bias, assessments_time
########################################BASIC EXAMPLE##############################################

# colors = [('black', 0), ('g1', 160), ('g2', 106), ('g3', 209),
#            ('g4', 80), ('g5', 135), ('white', 255)]

# _,s,j,_ = Rubric([0,'black'],[255,'white'],[color[0] for color in colors], true_values = [color[1] for color in colors], sensibility = (10,1))