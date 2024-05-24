# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:56:30 2024

@author: Romain Perrier
"""

import numpy as np
import random as rd

###############################         FUNCTIONS       ############################################

def shannon_entropy(p):
    """
    Calculate the Shannon entropy for a given probability p.
    
    Parameters
    ----------
    p : float
        Probability of an event occurring, ranging from 0 to 1.
    
    Returns
    -------
    float
        Shannon entropy value for the given probability.
    
    """
    return - p * np.log2((p + np.finfo(float).eps)) - (1-p) * np.log2(((1-p) + np.finfo(float).eps))
 
def MI(JointProba,Proba):
    """
    Calculate the Mutual information array representing the mutual information between each pair of random variables.
    
    Parameters
    ----------
    JointProba : float array
        Joint probability distribution of the two random variables.
    Proba : float array
        Marginal probability distribution of each random variable.

    Returns
    -------
    mi : float array
        Mutual information array representing the mutual information between each pair of random variables.

    """
    n = len(JointProba)
    mi = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i!=j:
                mi[i][j] = shannon_entropy(Proba[i]) + shannon_entropy(Proba[j]) - shannon_entropy(JointProba[i][j])
    return mi
     
def II(TriProba,JointProba,Proba):
    """
    Calculate the triple-wise interaction information between three random variables.

    Parameters
    ----------
    TriProba : float array
        Conditional probability distribution of three random variables.
    JointProba : float array
        Joint probability distribution of the two random variables.
    Proba : float array
        Marginal probability distribution of each random variable.

    Returns
    -------
    ii : float array
        Triple-wise interaction information matrix representing the interaction information between each triple of random variables.

    """
    n = len(JointProba)
    ii = np.zeros((n, n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i!=j or j!=k or k!=i:
                    #calculation of mutual information
                    ii[i][j][k] = shannon_entropy(Proba[i]) + shannon_entropy(Proba[j]) - shannon_entropy(JointProba[i][j])
                    #calculation of Conditional mutual information
                    ii[i][j][k] -= shannon_entropy(JointProba[i][k])+shannon_entropy(JointProba[j][k])-shannon_entropy(TriProba[i][j][k])-shannon_entropy(Proba[k])
    return ii
     
def roulette(population):
    """
    Perform roulette wheel selection to select an index from the population.

    Parameters
    ----------
    population : float array
        List or array containing the fitness values of individuals in the population.

    Returns
    -------
    selected_index : int
        Index of the selected individual in the population.

    """
    total_fitness = sum(individual for individual in population)
    selection_probabilities = [(individual + np.finfo(float).eps) / (total_fitness + np.finfo(float).eps) for individual in population]
    selected_index = rd.choices(range(len(population)), weights=selection_probabilities)[0]
    return selected_index
