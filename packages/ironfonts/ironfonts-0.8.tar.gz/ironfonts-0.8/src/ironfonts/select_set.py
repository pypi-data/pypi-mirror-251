# HEADER:
# - Module Name: select_set.py
# - Written by: Isaac N. Erb.
# - Created: 2023-??-??.
# - Last Edited*: 2023-Oct-14.
#
#       * (Read: "Last time the author bothered to update this.") 

# PURPOSE: 
# - This module contains a function (selector()) which selects a
#   set of related characters in the font-editor FontForge for
#   the purpose of mass-operations thereupon.
# - This module's core function may be called by other modules
#   in the package, or accessed thru the CLI function also found
#   in select_set.py.


# Doing imports.
import fontforge
import psMat
from .sets import *

# Selecting font-file to operate upon. Must be set manually, 
# for now.
file_version = 4.2
suffix = "-Ital"
file_name = f"Carbon-13, {file_version}{suffix}.sfd"
PATH = "/home/ironheart/Documents/Creative/Fontstuff/"
full_path = PATH + file_name
current = fontforge.open(full_path)


# Below: Core function; selects all positions in the list passed in.
def selector(requested_set):
    current = current
    requested_set = requested_set

    current.selection.none()
    for position in requested_set:
        current.selection.select(('more', 'unicode'), position)     # This will select unicode-positions by decimal value.
    return


def transformation(trans_type, magnitudes):
    trans_type = trans_type
    magnitudes = magnitudes
    if magnitudes.type() == list and len(magnitudes) == 1:
        magnitudes = float(magnitudes)

    if trans_type == "move":
        current.translate(psMat.translate(magnitudes))
    elif trans_type == "turn":
        current.rotate(psMat.rotate(magnitudes))
    elif trans_type == "scale":
        current.scale(psMat.scale(magnitudes))
    return


def request():
    requested_set = input(
"""What set do you want to select?
\t- Inferiors, Unicode.
\t- Inferiors, All.
\t- Superscripts, Unicode.
\t- Superscripts, All.
\t- Zero-Widths.
""")
    requested_set = requested_set.lower()

    if "inf" in requested_set and "uni" in requested_set:
        selector(unicode_ascii_inferiors)
    elif "inf" in requested_set:
        selector(all_ascii_inferiors)
    elif "sup" in requested_set and "uni" in requested_set:
        selector(unicode_ascii_superscripts)
    elif "sup" in requested_set:
        selector(all_ascii_superscripts)
    elif any(["z", "0"]) in requested_set:
        selector(all_known_zeroWidths)
    else:
        print("That is not a valid operation.")
        return False    #@ If I want this function to run from the command-line, I should instead call a file-save function here.
    

    trans_request = input(
"""Please choose from the following transformations to perform on the selected glyphs:
\t- None.
\t- Movement.
\t- Rotation.
\t- Scaling.
""")
    trans_request = trans_request.lower()

    if "no" in trans_request:
        return
    elif "mov" in trans_request:
        trans_type = "move"
    elif "rot" in trans_request:
        trans_type = "turn"
    elif "sca" in trans_request:
        trans_type = "scale"
    else:
        print("That is not a valid operation.")
        return False
    
    magnitudes = input("Now, please input the magnitudes of that transformation.\n([x,y] for Move and Scale, degrees counterclockwise for rotation.)\n")
    magnitudes = eval(magnitudes)

    transformation(trans_type, magnitudes)

    return True

# Saving changes and outputting message before ending a manual 
# run of the module.
success = request()
if success:
    current.save(full_path)
    print("Success.")
else:
    print("Execution unsuccessful.")

exit()