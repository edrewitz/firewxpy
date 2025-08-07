"""
This file hosts the function for CWA Coordinates

(C) Eric J. Drewitz 2025
"""

def get_cwa_coords(cwa):

    """
    This functions returns the coordinate boundaries for a CWA        
    """
    if cwa == None:
        wb, eb, sb, nb = [-170, -128, 50, 75]
    if cwa == 'AER' or cwa == 'aer':
        wb, eb, sb, nb = [-155, -140.75, 55.5, 64.5]
    if cwa == 'ALU' or cwa == 'alu':
        wb, eb, sb, nb = [-170, -151, 52, 62.9]
    if cwa == 'AJK' or cwa == 'ajk':
        wb, eb, sb, nb = [-145, -129.5, 54, 60.75]
    if cwa == 'AFG' or cwa == 'afg':
        wb, eb, sb, nb = [-170, -140.75, 59, 72]

    return wb, eb, sb, nb