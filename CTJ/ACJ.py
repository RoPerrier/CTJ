# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:56:29 2024

@author: Romain Perrier
"""
import random as rd
import numpy as np
import scipy.stats as stats
import time
import choix

from itertools import combinations, permutations

from .util import Rescale, SSR, ready, WindowManager
from .selection import MI, roulette

###############################         FUNCTIONS       ############################################

def make_ACJ_assessment (items, pair, id_judge, sensibility, true_values, assessment_method, nb_assessment, window):
    """
    This function is used to do the assessment on a Pair and return the tuple (Max, Min). In the format (int, int)

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    pair : list of string
        A list of strings representing the pair of items being assessed.
    id_judge : int
        The id of the judge making the assesment.
    sensibility : tuple
         A  tuple cointaining the sensibility treshold, and the probability of making a mystake. In the format (int, double).
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.
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
        A tuple containing the assessment results in the format (int, int).
    assessment_duration : double
        Duration of the assessment in second.
    one_more_bias : int
        One if the judgment is biaised else 0.

    """
    
    one_more_bias = 0
    
    if assessment_method is not None :
        
        ready(window)

        a = time.time()
        
        #We let the judges make the assessment
        pair = assessment_method(id_judge, pair, nb_assessment, window)
        
        b = time.time()
        
        assessment_duration = b-a
        
    elif true_values is not None :
            
        a = time.time()
        
        #We sort the pair        
        Booleen = True
        
        r = rd.random()
        
        if (np.abs(true_values[items.index(pair[0])]-true_values[items.index(pair[1])]) <= sensibility[0]) and (r < sensibility[1]) :
            Booleen = False
            one_more_bias = 1
        pair = sorted(pair, key=lambda x: true_values[items.index(x)], reverse = Booleen)
        
        b = time.time()
        
        assessment_duration = b-a
        
    else :
        
        raise Exception("There are no true value nor assessment_method, both are None")
    
    return (pair[0],pair[1]), assessment_duration, one_more_bias

def estimate_ACJ (items, assessments, true_values):
    """
    The method to estimate the value of each ACJ iteration.

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    assessments : list of tuple
         A list containing all the assessments done in the format (int,int).
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.

    Returns
    -------
    estimated_values : list of int
         A list of int containing the estimated values corresponding to each item in the `items` list.

    """
    
    nb_items = len(items)
    
    estimated_values = []
    
    mean = np.average(true_values)
    std = np.std(true_values)
    
    assessments_ind = [(items.index(x),items.index(y)) for (x,y) in assessments]
    parameters = choix.ilsr_pairwise(nb_items, assessments_ind, alpha=0.1)
    
    Z_parameters = stats.zscore(parameters)
    for x in Z_parameters: 
        val = round( x * std + mean  )
        estimated_values.append(val)

    return estimated_values

def ACJ_new_pair (items, max_item, assessments, estimated_values):
    """
    This function select the best new pair to assess.

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    assessments : list of tuple
        A list containing all the assessments done in the format (int, int).
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.

    Returns
    -------
    pair : list
        A list representing the new pair to assess.
    """
    
    nb_items = len(items)
    
    #Initialize the proximity of items tuples (i,j) to 0
    Prox = np.zeros((nb_items,nb_items))
    
    #Initialize the apparition probabilities
    JointProba = np.zeros((nb_items,nb_items))
    Proba = np.zeros(nb_items)
    
    #let's fill all the probabilities array
    for i, item_1 in enumerate(items):
        nb = sum(1 for tup in assessments if item_1 in tup)
        Proba[i] = nb / (2 * len(assessments))
        
        for j, item_2 in enumerate(items):
            nb_joint = sum(1 for tup in assessments if item_2 in tup and item_1 in tup)
            JointProba[i][j] =  nb_joint / len(assessments)
            
            #Let's calculate the proximity of the ith, jth and kth items
            Prox[i][j]=np.abs(estimated_values[i]-estimated_values[j])

    #Let's calculate the array of Mutual Interaction
    mi=MI(JointProba,Proba)

    #a high proximity must be more important in selection  than  
    Disp = max_item[0]/(Prox+np.finfo(float).eps)

    #Let's create all pairs possible
    pairs = list(combinations(items, 2))
    fit=[]
    
    #For all pair estimate the fitness for the wheel selection
    for pair in pairs:
        i, j = items.index(pair[0]), items.index(pair[1])
        fit.append((mi[i][j])*Disp[i][j])
    
    #Select a pair with a roulette wheel algorithm
    selected_index = roulette(fit)

    p = permutations([pairs[selected_index][0], pairs[selected_index][1]], 2)
    
    #If the intersection of assessment and p is not Null then change the selected pair
    i = 0
    while bool(set(assessments) & set(p)):
        selected_index = roulette(fit)
        p = permutations([pairs[selected_index][0], pairs[selected_index][1]], 2)
        i += 1
        if i>1000:
            break
    
    pair = [pairs[selected_index][0], pairs[selected_index][1]]
    
    return pair

def ACJ_init (items, true_values, nb_judge, sensibility, assessment_method):
    """
    This fonction initialize the ACJ algorithm. Set up the assessments list.

    Parameters
    ----------
    items : list of string
        A list of strings representing the items to be assessed.
    true_values : list of int
        A list of int containing the true values corresponding to each item in the `items` list.
    nb_judge : int, optional
        The number of judge that make the evaluation.
    sensibility :list of tuple
         A list of tuple cointaining the sensibility treshold for each simulated judge, and the probability of making a mystake. In the format (int, double).
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value.

    Returns
    -------
    assessments : list of tuple
         A list containing all the assessments done in the format (int,int).
    assessments_time : int
        The duration of the assessments.
    nb_bias : list of int
        A list containing the number of bias for each judges.
    window : WindowManager
        an object to manage human assessments.

    """
    
    nb_items = len(items)
    
    not_compared = items[:]
    
    #Shuffle items if the items are sort the judgment may be biaised
    rd.shuffle(not_compared)
    
    assessments = []
    assessments_time = np.zeros(nb_judge)
    nb_bias = np.zeros(nb_judge)
    
    window  = None
    
    #if assessment method not None then Show a tutorial
    if assessment_method is not None :
        
        window = WindowManager()
        
        skip_tutorial = ready(window, info = "The ACJ assessment involves comparisons between two items.\n\n On each iteration, you will be asked to click on the best items.\n\n By clicking on the 'Tutorial' button, you can access the tutorial.\n The tutorial consists of an evaluation of the algorithm. After completing the tutorial evaluation, the actual test will begin.\n\n Between each evaluation, a button will appear.\n Ensure you are ready before clicking on it, as once clicked, a countdown will start. At the end of the countdown, you can evaluate the item, so make sure you are prepared.", status =  "Tuto") 
        ###TUTO on pourrait le passer avec un bouton,  reflechir a un break ou un goto
        
        if not skip_tutorial:
            item_1 = rd.choice(items)
            items_copy = items[:]
            items_copy.remove(item_1)
            item_2 = rd.choice(items_copy)
    
            _ = assessment_method(-2,[item_1,item_2], -1, window)
    
    #Assess all items one times
    for i in range(0,nb_items-2,2):
        pair = [not_compared[i], not_compared[i+1]]
        ACJ_assessment = [make_ACJ_assessment(items, pair, id_judge, sensibility[id_judge], true_values, assessment_method, len(assessments)+1, window) for id_judge in range(nb_judge)]
        assessments_done = [assessment[0] for assessment in ACJ_assessment]
        assessments_time += np.array([assessment[1] for assessment in ACJ_assessment])
        nb_bias += np.array([assessment[2] for assessment in ACJ_assessment])
        
        assessments.append(max(set(assessments_done), key=assessments_done.count))

    if nb_items%2 != 0:
        pair = [not_compared[nb_items-1], not_compared[nb_items-2]]
        ACJ_assessment = [make_ACJ_assessment(items, pair, id_judge, sensibility[id_judge], true_values, assessment_method, len(assessments)+1, window) for id_judge in range(nb_judge)]
        assessments_done = [assessment[0] for assessment in ACJ_assessment]
        assessments_time += np.array([assessment[1] for assessment in ACJ_assessment])
        nb_bias += np.array([assessment[2] for assessment in ACJ_assessment])
        
        assessments.append(max(set(assessments_done), key=assessments_done.count))
        
    return assessments, assessments_time, nb_bias, window

def ACJ (min_item, max_item, items, nb_judge = 1, sensibility = [(0,0)], true_values = None, max_iteration = 30, max_accuracy = 0.9, assessment_method = None):
    """
    Adaptive Comparative Judgment (ACJ) is an evaluation method based on the comparison of pairs of items. Rather than scoring each item on a fixed scale, evaluators directly compare two items at a time and judge which is better according to certain criteria.

    Parameters
    ----------
    min_item : tuple
        The min_item we wont to use. In the format (int, string).
    max_item : tuple
        The max_item we wont to use. In the format (int, string).
    items : list of string
        A list of strings representing the items to be assessed.
    nb_judge : int, optional
        The number of judge that make the evaluation. The default is 1.
    sensibility : list of tuple
         A list of tuple cointaining the sensibility treshold for each simulated judge, and the probability of making a mystake. In the format (int, double). The default is [(0,0)]
    true_values : list of int, optional
        A list of int containing the true values corresponding to each item in the `items` list. The default is None.
    max_iteration : int, optional
        Number of maximum iteration of the algorithm. The default is 30.
    max_accuracy : float, optional
        Accuracy of the model. The default is 0.9.
    assessment_method : fun
        The assessment method. If none, the assessment is automatically performed using the true value. The default is None.
    
    Raises
    ------
    Exception
        The len of sensitbility is not equal to the number of judge.
    

    Returns
    -------
    estimated_values : list of int
        A list of int containing the estimated values corresponding to each item in the `items` list.
    int
        Number of iteration.
    cond : float
        Accuracy of estimated value at the end of algorithm.
    nb_bias : list of int
        A list containing the number of bias for each judges.
    assessments_time : int
        The duration of the assessments.

    """
    
    nb_items = len(items)
    
    #If min and max value are not in the items list we add them
    if min_item[1] not in items :
         items.append(min_item[1])
         if true_values is not None :
             true_values.append(min_item[0])
    if max_item[1] not in items :
         items.append(max_item[1])
         if true_values is not None :
             true_values.append(max_item[0])
             
    if sensibility == [(0,0)] :
        sensibility = [(0,0) for i in range(nb_judge)]
        
    if len(sensibility) != nb_judge :
        raise Exception("All the judge need a sensibility tuple ! The len of sensitbility is not equal to the number of judge.")
    
    #We initialize the assessments list
    assessments, assessments_time, nb_bias, window = ACJ_init(items, true_values, nb_judge, sensibility, assessment_method)
    
    iteration = 0
    
    all_estimated_values=[]
    
    #We calculate the estimated value after the initialisation
    if true_values is None :
        val =[ min_item[0] if items[i] == min_item[1] else
               max_item[0] if items[i] == max_item[1] or i > nb_items/2 else
               min_item[0] for i in range(nb_items)]
        
    else :
        val = true_values
        
    estimated_values = estimate_ACJ(items, assessments, val)
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
        
    while ((iteration<max_iteration) and (cond < max_accuracy)):
        
        #We select the best next pair
        pair = ACJ_new_pair(items, max_item, assessments, estimated_values)
        
        #We add the new assessment
        ACJ_assessment = [make_ACJ_assessment(items, pair, id_judge, sensibility[id_judge], true_values, assessment_method, len(assessments)+1, window) for id_judge in range(nb_judge)]
        assessments_done = [assessment[0] for assessment in ACJ_assessment]
        assessments_time += np.array([assessment[1] for assessment in ACJ_assessment])
        nb_bias += np.array([assessment[2] for assessment in ACJ_assessment])
        
        assessments.append(max(set(assessments_done), key=assessments_done.count))

        #We calculate the new estimated values
        if true_values is None :
            val = estimated_values
        else :
            val = true_values
            
        estimated_values = estimate_ACJ(items, assessments, val)
        estimated_values = Rescale(min_item[0], max_item[0], estimated_values)
        
        all_estimated_values.append(estimated_values)
        
        #We calculate the new accuracy
        cond = accuracy(true_values, estimated_values, all_estimated_values)
        
        iteration += 1
    
    if window is not None :
        window.destroy()
        
    print("===============================================================")
    print("| Result of ACJ algorithm")
    print("| Items : ", items)
    if true_values is not None :
        print("| True values : ", true_values)
    print("| Estimated values : ", estimated_values)
    if true_values is not None :
        print("| Accuracy : ", cond)
    if sensibility != [(0,0) for i in range(nb_judge)] :
        print("| Number of bias : ", nb_bias)
    print("| Iteration : ", len(assessments))
    if assessment_method is not None :
        print("| Total duration : ", assessments_time)
    print("===============================================================")
    return estimated_values, len(assessments), cond, nb_bias, assessments_time