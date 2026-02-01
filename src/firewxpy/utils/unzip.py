"""
This file hosts the function that unzips the shapefiles

(C) Eric J. Drewitz 2024-2026
"""

from zipfile import ZipFile

def extract_zipped_files(file_path, 
                         extraction_folder):

    """
    This function unzips a file in a folder. 

    Required Arguments:

    1) file_path (String) - The path to the file that needs unzipping.

    2) extraction_folder (String) - The folder that the zipped files are located in.
    
    Optional Arguments: None
    
    Returns
    -------
    
    Shapefiles are extracted to {extraction_folder}
    """

    # Load the zipfile
    with ZipFile(file_path, 'r') as zObject:
        # extract a specific file in the zipped folder
        zObject.extractall(extraction_folder)
    zObject.close()