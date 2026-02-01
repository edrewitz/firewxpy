"""
This file manages the FireWxPy graphics directory. 

(C) Eric J. Drewitz 2024-2026

"""

import os

def build_directory_branch(path):
    
    """
    This function builds a new directory branch if it does not exist already
    
    Required Arguments:
    
    1) path (String) - The path that is the branch of the directory. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    A directory path.     
    """
    
    try:
        os.makedirs(f"{path}")
    except Exception as e:
        pass