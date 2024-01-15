# PURPOSE:
# - This module contains custom functions I have made for use
#   along-side those in fontforge.py. It is intended for use by
#   a module which has imported the cli_functions' round*()
#   functions and psMat.

def pasteAfter(glyph_0, glyph_1, new_glyph):    # Takes: First component (on left); second component, to be pasted thereafter; final glyph, made of two references. All are predefined objects of class 'glyph'.
    current = current
    glyph_0 = glyph_0
    glyph_1 = glyph_1
    new_glyph = new_glyph

    current.selection.select(glyph_1.glyphname)     # Copying second component.
    current.copyReference()
    current.selection.select(new_glyph.glyphname)   # Pasting second component into position of new_glyph.
    current.paste()
    new_glyph.transform(psMat.translate(round_iron(glyph_0.width), 0))    # Moving second component over, as if it was appended to the first.

    current.selection.select(glyph_0.glyphname)
    current.copyReference()
    current.selection.select(new_glyph.glyphname)   # Pasting the first component into its proper place.
    current.pasteInto()