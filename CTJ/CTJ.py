# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:35:28 2024

@author: Romain Perrier
"""
import random as rd
import numpy as np
import time

from itertools import chain, combinations, permutations

from .util import Rescale, SSR, ready, WindowManager
from .selection import II, roulette


###############################         FUNCTIONS       ############################################

def make_CTJ_assessment (items, trio, sensibility, true_values, scale, assessment_method, nb_assessment, window):
    """
    This function is used to do the assessment on a Trio and return the tuple (Max,(dist,Average),Min)

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    trio : list of string
        A list of strings representing the trio of items being assessed.
    sensibility : tuple
         A  tuple cointaining the sensibility treshold, the absolute value of the error on the scaler, and the probability of making a mystake. In the format (int, int, double).
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.
    scale : int
        The value of the scale for the CTJ model. Default is 10.
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value.
    nb_assessment : int
        The number of assessment done.
    window : WindowManager
        an object to manage human assessments.
        
    Raises
    ------
    Exception
        There are no true value nor assessment_method, both are None.

    Returns
    -------
    tuple
        A tuple containing the assessment results (Max,(dist,Average),Min).In the format (int, (int, int), ini).
    assessment_duration : double
        Duration of the assessment in second.
    assessments_time : int
        The duration of the assessments.
    error : list of int
        The first element is the number of inversion done in automated assessment, the second is the number of scale error. Default is [0,0].
        

    """
    
    nb_inversion = 0
    nb_scale_error = 0
            
    if assessment_method is not None :
        
        ready(window)

        a = time.time()
        
        #We let the judge make the assessment
        trio, dist = assessment_method(scale, trio, nb_assessment, window)
        
        b = time.time()
        
        assessment_duration = b-a
        
    elif true_values is not None :
        
        a = time.time()
        
        #We sort the trio
        trio = sorted(trio, key=lambda x: true_values[items.index(x)], reverse = True)
        
        b = time.time()
        
        #We calculate the distance between the Average and the Max value
        dmin = true_values[items.index(trio[1])] - true_values[items.index(trio[0])]
        
        #We calculate the distance between the Min and the Max value
        dmax = true_values[items.index(trio[2])] - true_values[items.index(trio[0])]
        
        ###################
        
        k = -np.log(1/9)/(sensibility[0] + np.finfo(float).eps)
        
        val = np.abs(true_values[items.index(trio[0])]-true_values[items.index(trio[1])])
        
        if rd.random() >= 1/(1+np.exp(- k * val)) :
            
            trio[0], trio[1] = trio[1], trio[0]
            
            nb_inversion += 1
        
        val = np.abs(true_values[items.index(trio[1])]-true_values[items.index(trio[2])])
            
        if rd.random() >= 1/(1+np.exp(- k * val)) :
                
            trio[1], trio[2] = trio[2], trio[1]
                
            val = np.abs(true_values[items.index(trio[0])]-true_values[items.index(trio[1])])
            
            nb_inversion += 1
                    
            if rd.random() >= 1/(1+np.exp(- k * val)) :
                        
                trio[0], trio[1] = trio[1], trio[0]
                
                nb_inversion += 1
        
        ###################
        
        if rd.random() <= sensibility[2] :
            
            bias = sensibility[1]
            
            r = rd.random()
            
            if r < 0.5 :
                bias = bias * -1
                
            nb_scale_error = 1
        
        if dmax == 0:
            dist = scale//2 + bias
        else :
            dist = round(scale*dmin/dmax + bias)
            
        if dist >= scale:
            dist = scale-1
        elif dist <= -1:
            dist = 0  
                
        assessment_duration = b-a
                
    else :
        
        raise Exception("There are no true value nor assessment_method, both are None")
    
    error = [nb_inversion, nb_scale_error]
        
    return (trio[0], (dist, trio[1]), trio[2]), assessment_duration, error

def CTJ_assessments (items, A, b, assessment,scale):
    """
    This function calculates the new line to add in the A array for the CTJ model based on given assessments.

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    A : array of double
        An array used to calculate the estimated value.
    b : array of double
        Array of zeros execept for two value, the fixed point of the model.
    assessment : tuple
        A tuple containing the assessment results (Max,(dist,Average),Min).In the format (int, (int, int), int).
    scale : int
        The value of the scale for the CTJ model. Default is 10.

    Returns
    -------
    line : list
        A list representing the new line to add in the A array.
    """
    
    nb_items = len(items)
    
    d1 = assessment[1][0]
    d2 = scale - d1
    alpha = d1/d2
    Max = items.index(assessment[0])
    Average = items.index(assessment[1][1])
    Min = items.index(assessment[2])

    #Create a new line for A array
    line = list(np.zeros(nb_items))
    line[Max] = 1
    line[Average] = -(alpha + 1)
    line[Min] = alpha
    
    return line

def CTJ_new_trio (items, assessments, estimated_values):
    """
    This function select the best new trio to assess.

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    assessments : list of tuple
        A list containing all the assessments done in the format (int,(int,int),int).
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.

    Returns
    -------
    trio : list
        A list representing the new trio to assess.
    """
    
    nb_items = len(items)
    
    #Let's set the assessment from (Max, (dist, Average), Min) to (Max, Average, Min)
    assessment = [(tup[0],tup[1][1],tup[2]) for tup in assessments]
    
    #Initialize the proximity of items tuples (i,j,k) to 0
    Prox = np.zeros((nb_items,nb_items,nb_items))
    
    #Initialize the apparition probabilities
    TriProba = np.zeros((nb_items,nb_items,nb_items))
    JointProba = np.zeros((nb_items,nb_items))
    Proba = np.zeros(nb_items)
    
    #let's fill all the probabilities array
    for i, item_1 in enumerate(items):
        nb = sum(1 for tup in assessment if item_1 in tup)
        Proba[i] = nb / (3 * len(assessment))
        
        for j, item_2 in enumerate(items):
            nb_joint = sum(1 for tup in assessment if item_2 in tup and item_1 in tup)
            JointProba[i][j] = 2 * nb_joint / (3 * len(assessment))
    
            if i == j:
                JointProba[i][j] = 0
    
            for k, item_3 in enumerate(items):
                 nb_tri = sum(1 for tup in assessment if item_3 in tup and item_2 in tup and item_1 in tup)
                 TriProba[i][j][k] = nb_tri / len(assessment)
                 
                 #Let's calculate the proximity of the ith, jth and kth items
                 Prox[i][j][k] = np.sqrt((estimated_values[i] - estimated_values[j]) ** 2 +
                                         (estimated_values[j] - estimated_values[k]) ** 2 +
                                         (estimated_values[i] - estimated_values[k]) ** 2)        
                 
                 if i == j and j == k:
                     TriProba[i][j][k] = 0

    #Let's calculate the array of Information Interaction
    ii=II(TriProba,JointProba,Proba)

    #Let's create all trios possible
    trios = list(combinations(items, 3))
    fit=[]
    
    #For all trio estimate the fitness for the wheel selection
    for trio in trios:
        i, j, k = items.index(trio[0]), items.index(trio[1]), items.index(trio[2])
        fit.append(((ii[i][j][k])**2)*Prox[i][j][k])
    
    #Select a trio with a roulette wheel algorithm
    selected_index = roulette(fit)
    
    p = permutations([trios[selected_index][0], trios[selected_index][1], trios[selected_index][2]], 3)
    
    #If the intersection of assessment and p is not Null then change the selected trio
    i = 0
    while bool(set(assessment) & set(p)):
        selected_index = roulette(fit)
        p=permutations([trios[selected_index][0], trios[selected_index][1], trios[selected_index][2]], 3)
        i+=1
        if i>1000:
            break
        
    trio = [trios[selected_index][0], trios[selected_index][1], trios[selected_index][2]]

    return trio

def CTJ_init (items, max_id, min_id, max_val, min_val, sensibility, true_values, scale, assessment_method ):
    """
    This fonction initialize the CTJ algorithm. Set up the array of the model and the assessments list.

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    max_id : int
        The position of the max value in the items list.
    min_id : int
        The position of the min value in the items list.
    max_val : int
        The max value of items list.
    min_val : int
        The min value of items list.
    sensibility : tuple
        A  tuple cointaining the sensibility treshold, the absolute value of the error on the scaler, and the probability of making a mystake. In the format (int, int, double).
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.
    scale : int
        The value of the scale for the CTJ model.
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value.

    Returns
    -------
    A : array of double
        An array used to calculate the estimated value.
    b : array of double
        Array of zeros execept for two value, the fixed point of the model.
    assessments : list of tuple
         A list containing all the assessments done in the format (int,(int,int),int).
    error : list of int
        The first element is the number of inversion done in automated assessment, the second is the number of scale error. Default is [0,0].
    window : WindowManager
        an object to manage human assessments.

    """
    
    nb_items = len(items)
    
    window = None
    
    #Create the matrices
    A = np.zeros((2, nb_items), dtype=np.double)
    b = np.zeros((2, 1), dtype=np.double)
    A[0][min_id] = 1
    b[0] = min_val
    A[1][max_id] = 1
    b[1] = max_val

    not_compared = items[:]
    
    #Shuffle items if the items are sort the judgment may be biaised
    rd.shuffle(not_compared)
    
    assessments = []
    
    assessments_time = 0
    
    error = [0,0]
    
    #if assessment method not None then Show a tutorial
    if assessment_method is not None :
        
        window = WindowManager()
        
        skip_tutorial = ready(window, info = "The CTJ assessment involves comparisons between three items.\n\n On each iteration, you will be asked to sort the item, the best (at the left) to the worst (at the right).\n Then you must use the slider bellow to indicate the distance betwwen the extremums items and the average one.\n To swap item, you must click on both of them.\n\n By clicking on the 'Tutorial' button, you can access the tutorial.\n The tutorial consists of an evaluation of the algorithm. After completing the tutorial evaluation, the actual test will begin.\n\n Between each evaluation, a button will appear.\n Ensure you are ready before clicking on it, as once clicked, a countdown will start. At the end of the countdown, you can evaluate the item, so make sure you are prepared.", status =  "Tuto") 
        
        if not skip_tutorial:
            item_1 = rd.choice(items)
            items_copy = items[:]
            items_copy.remove(item_1)
            item_2 = rd.choice(items_copy)
            items_copy.remove(item_2)
            item_3 = rd.choice(items_copy)
    
            _ = assessment_method(scale,[item_1, item_2, item_3] , -1, window) 

    #Assess all items one times
    for i in range(0,nb_items-3,3):
        trio = [not_compared[i], not_compared[i+1], not_compared[i+2]]
        assessment = make_CTJ_assessment(items, trio, sensibility, true_values, scale, assessment_method, len(assessments)+1, window)
        assessments.append(assessment[0])
        assessments_time += assessment[1]
        error[0] += assessment[2][0]
        error[1] += assessment[2][1]
        line = CTJ_assessments(items, A, b, assessments[-1], scale)
        A = np.vstack([A, line])
        b = np.vstack([b, [0]])

    if nb_items%3 != 0:
        trio = [not_compared[nb_items-1], not_compared[nb_items-2], not_compared[nb_items-3]]
        assessment = make_CTJ_assessment(items, trio, sensibility, true_values, scale, assessment_method, len(assessments)+1, window)
        assessments.append(assessment[0])
        assessments_time += assessment[1]
        error[0] += assessment[2][0]
        error[1] += assessment[2][1]
        A = np.vstack([A, line])
        b = np.vstack([b, [0]])
        
    return A, b, assessments, assessments_time, error, window

def CTJ (min_item, max_item, items, sensibility = (0,0,0), true_values = None, max_iteration = 30, max_accuracy = 0.9, scale = 10, assessment_method = None):
    """
    Comparative Triple judgement (CTJ) is an evaluation method based on the comparison of a trio of elements. Rather than scoring each item on a fixed scale, evaluators directly compare three items at once, ranking them from best to worst, and then position the central item on a scale by moving it closer to the end that best matches it.  CTJ was devised by Dr Kevin Kelly.

    Parameters
    ----------
    min_item : tuple
        The min_item we wont to use.  In the format (int, string).
    max_item : tuple
        The max_item we wont to use. In the format (int, string).
    items : list of string
        A list of strings representing the items to be assessed.
    sensibility : tuple
        A  tuple cointaining the sensibility treshold, the absolute value of the error on the scaler, and the probability of making a mystake. (int, int, double)
    true_values : list of int, optional
        A list of int containing the true values corresponding to each item in the `items` list. The default is None.
    sensibility : tuple
        A  tuple cointaining the sensibility treshold, the absolute value of the error on the scaler, and the probability of making a mystake. (int, int, double)
    max_iteration : int, optional
        Number of maximum iteration of the algorithm. The default is 30.
    max_accuracy : float, optional
        Accuracy of the model. The default is 0.9.
    scale : int, optional
        The value of the scale for the CTJ model. Default is 10.
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value. Default is None.
        
    Returns
    -------
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.
    int
        Number of iteration.
    cond : float
        Accuracy of estimated value at the end of algorithm.
    error : list of int
        The first element is the number of inversion done in automated assessment, the second is the number of scale error. Default is [0,0].
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
    
    #We initialize the A array, b array and assessments list
    A, b, assessments, assessments_time, error, window = CTJ_init(items, items.index(max_item[1]), items.index(min_item[1]), max_item[0], min_item[0], sensibility, true_values, scale, assessment_method )
    
    iteration = 0
    
    all_estimated_values=[]
    
    #We calculate the estimated value after the initialisation
    estimated_values = np.linalg.lstsq(A,b,rcond=1e-17)[0]
    estimated_values = list(chain.from_iterable(estimated_values)) 
    estimated_values = Rescale(min_item[0], max_item[0], estimated_values)
    
    #We add it to the list containing all the estimated values
    all_estimated_values.append(estimated_values)
        
    #We select the accuracy method depending the existence of true_values list
    if true_values is None:
        accuracy = lambda true_values, estimated_values, all_estimated_values: SSR(all_estimated_values[-2], all_estimated_values[-1])
        cond = 0
    else :
        accuracy = lambda true_values, estimated_values, all_estimated_values: SSR(true_values, estimated_values)
        cond = accuracy(true_values, estimated_values, all_estimated_values)

    
    while ((iteration<max_iteration) and (cond<max_accuracy)):
        
        #We select the best next trio
        trio = CTJ_new_trio(items, assessments, estimated_values)
        
        #We add the new assessment
        assessment = make_CTJ_assessment(items, trio, sensibility, true_values, scale, assessment_method, len(assessments)+1, window)
        assessments.append(assessment[0])
        assessments_time += assessment[1]
        error[0] += assessment[2][0]
        error[1] += assessment[2][1]
        
        #We upgrade the A and b array
        line = CTJ_assessments(items, A, b, assessments[-1], scale)
        A = np.vstack([A, line])
        b = np.vstack([b, [0]])
        
        #We calculate the new estimated values
        estimated_values = np.linalg.lstsq(A,b,rcond=1e-17)[0]
        estimated_values = list(chain.from_iterable(estimated_values)) 
        
        #We rescale them
        estimated_values = Rescale(min_item[0], max_item[0], estimated_values)
        
        all_estimated_values.append(estimated_values)
        
        #We calculate the new accuracy
        cond = accuracy(true_values, estimated_values, all_estimated_values)
        
        iteration += 1
    
    if window is not None :
        window.root.destroy()
        
    print("===============================================================")
    print("| Result of CTJ algorithm")
    print("| Items : ", items)
    if true_values is not None :
        print("| True values : ", true_values)
    print("| Estimated values : ", estimated_values)
    if true_values is not None :
        print("| Accuracy : ", cond)
    if sensibility != (0,0,0) :
        print("| Number of inversion : ", error[0])
        print("| Number of scale error : ", error[1])
    print("| Iteration : ", len(assessments))
    if assessment_method is not None :
        print("| Total duration : ", assessments_time)
    print("===============================================================")
    return estimated_values, len(assessments), cond, error, assessments_time