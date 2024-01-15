# HEADER:
# - Module Name: batch_naming.py
# - Written by: Isaac N. Erb.
# - Created: 2023-Oct-13.
# - Last Edited*: 2023-Oct-14.
#
#       * (Read: "Last time the author bothered to update this.")

import fontforge
from .sets import *

# - Selecting file.

font = "Carbon-13"
file_version = 4.2
suffix = "-Regu"
file_name = f"{font}, {file_version}{suffix}.sfd"

PATH = "/home/ironheart/Documents/Creative/Fontstuff/"
full_path = PATH + file_name
current = fontforge.open(full_path)

# - Defining global variables.
ROMAN = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]

BOLD_START = 119808     # u1D400.
ITAL_START = 119860     # u1D434.
BI_START   = 119912     # u1D468.
MONO_START = 120432     # u1D670.

superscript_prefix = "super_"
inferior_prefix = "inf_"

bold_prefix = "bold_"
italic_prefix = "ital_"
boldItal_prefix = "bi_"
monospace_prefix = "mono_"

def name_contiguous_set(start_position, prefix, character_set=ROMAN):
    current_position = start_position
    prefix = prefix
    characters = character_set

    for letter in characters:
        if prefix + letter != 'ital_h':     # Accounting for the 'h' missing in the middle of the Math Italics.
            unnamed = current.createMappedChar(current_position)
            unnamed.glyphname = prefix + letter
            current_position += 1
        else:
            current_position += 1
    return

# # The below requires user to presort positions and characters
#   to line up properly.
#     @ Maybe write a function to do that for them?
def name_disorderly_set(positions, prefix, character_set=ROMAN):
    positions = positions
    characters = character_set
    if len(positions) != len(characters):
        print("The list-lengths are missmatched; fix before proceeding.")
        exit()

    prefix = prefix
    counter = 0

    while counter < len(positions):
        parent = current.createMappedChar(ord(characters[counter]))
        child = current.createMappedChar(positions[counter])
        child.glyphname = prefix + parent.glyphname
        counter += 1
    return

def name_math_alphas():
    name_contiguous_set(BOLD_START, bold_prefix)
    name_contiguous_set(ITAL_START, italic_prefix)
    name_contiguous_set(BI_START, boldItal_prefix)
    name_contiguous_set(MONO_START, monospace_prefix)


# # Renaming Guidelines:
#     - Use interCaps in general.
#     - When using intercaps would cause the name of a lowercase
#       letter to be capitalized, instead put an underscore
#       before that letter, and leave it lowercase.
#     - Only begin with a capital letter for the names of glyphs
#       which *are* capital letters.
custom_renames = [
    [181, "micro"],     # From 'mu'.
    [439, "Ezh"],
    [658, "ezh"],
    [425, "Esh"],
    [643, "esh"],
    [399, "LatSchwa"]   # 'Latin Schwa'.
    [601, "lat_schwa"]
    [433, "LatUps"],    # For 'Latin Upsilon'.
    [650, "lat_ups"],
    [390, "OpenO"],
    [596, "open_o"],
    [597, "cCurl"],
    [720, "stressmark"],
    [721, "shortmark"],
    [8208, "trueHyphen"],
    [8587, "dek"],
    [8588, "el"],
    [8725, "divslash"],
    [10216, "mathAngleLeft"],
    [10217, "mathAngleRight"],
    [10218, "mathAngleLeftDouble"],
    [10219, "mathAngleRightDouble"]
]

# # The below function takes a list of ordered pairs. The first
#   in each of these pairs is a decimal position in unicode. The
#   second in each pair is what it should be renamed to.
# # The intended use of this function is to just mass-rename
#   glyphs in a new font, or when updating variants of an old
#   font.
def name_custom(pairs):
    pairs = pairs
    for pairing in pairs:
        nameless = current.createMappedChar(pairing[0])
        nameless.glyphname = pairing[1]
        if not nameless.isWorthOutputting():
            nameless.clear()
    return

# - This is the section to call the actual function I want to use.

current.save(full_path)
exit()