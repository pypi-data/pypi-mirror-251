## PURPOSE: This script repastes the custom glyphs outside of 
## unicode (those with '.sc' and '.subscript' extentions) to 
## their appropriate positions in unicode.

import fontforge
import psMat

file_version = 4.2
file_name = "Carbon-13EXP, " + str(file_version) + " (Dev).sfd"
PATH = "/home/ironheart/Documents/Creative/Fontstuff/"
full_path = PATH + file_name
current = fontforge.open(full_path)

# Defining constants.
SUPERSCRIPT_OFFSET = 8    # This is how many em-units subscript-references are moved to make superscripts.

all_ascii_superscripts = [
    178,
    179,
    185,
    688,
    690,
    691,
    695,
    696,
    737,
    738,
    739,
    7468,
    7470,
    7472,
    7473,
    7475,
    7476,
    7477,
    7478,
    7479,
    7480,
    7481,
    7482,
    7484,
    7486,
    7487,
    7488,
    7489, 
    7490, 
    7491,
    7495, 
    7496, 
    7497,
    7501,
    7503,
    7504,
    7506,
    7510, 
    7511, 
    7512,
    7515,
    7580,
    7584,
    7611,
    8304,
    8305,
    8308, 
    8309, 
    8310, 
    8311, 
    8312, 
    8313, 
    8314, 
    8315, 
    8316, 
    8317, 
    8318, 
    8319,
    11389,
    42781,
    57344, 
    57347, 
    57349, 
    57351, 
    57353, 
    57355, 
    57357, 
    57359, 
    57361, 
    57363, 
    57365, 
    57367, 
    57369, 
    57371, 
    57373, 
    57375, 
    57377, 
    57381, 
    57385, 
    57397, 
    57400, 
    57406, 
    57408, 
    57410, 
    57412, 
    57414, 
    57416, 
    57418, 
    57420, 
    57422, 
    57429, 
    57434, 
    57436, 
    57438, 
    57440]

## Beginning with small-caps.
current.selection.select('g.sc', 'i.sc', 'n.sc', 'r.sc', 'y.sc')
current.copyReference()
current.selection.select(('unicode', None), 610, 618, 628, 640, 655)
current.paste()

current.selection.select('b.sc', 'h.sc', 'l.sc')
current.copyReference()
current.selection.select(('unicode', None), 665, 668,671)
current.paste()

current.selection.select('a.sc', 'c.sc', 'd.sc', 'e.sc', 'j.sc', 'k.sc', 'm.sc', 'o.sc', 'p.sc', 't.sc', 'u.sc', 'v.sc', 'w.sc', 'z.sc')
current.copyReference()
current.selection.select(('unicode', None), 7424, 7428, 7429, 7431, 7434, 7435, 7437, 7439, 7448, 7451, 7452, 7456, 7457, 7458)
current.paste()

## Trying islenska small-caps.
try:
    current.selection.select('ae.sc', 'eth.sc')
    current.copyReference()
    current.selection.select(('unicode', None), 7425, 7430)
    current.paste()
except:
    print('Icelandic small-caps not supported.')

current.selection.select('f.sc', 's.sc')
current.copyReference()
current.selection.select(('unicode', None), 42800, 42801)
current.paste()

current.selection.select('q.sc')
current.copyReference()
current.selection.select(('unicode', None), 42927)
current.paste()

## BEGINNING SUBSCRIPTS.
## Doing Latin-1 Supplemental.
current.selection.select('two.subscript', 'three.subscript')
current.copyReference()
current.selection.select(('unicode', None), 178, 179)
current.paste()

current.selection.select('one.subscript')
current.copyReference()
current.selection.select(('unicode', None), 185)
current.paste()

# Doing Spacing Modifier Letters.
current.selection.select('h.subscript', 'j.subscript', 'r.subscript', 'w.subscript', 'y.subscript')
current.copyReference()
current.selection.select(('unicode', None), 688, 690, 691, 695, 696)
current.paste()

current.selection.select('l.subscript', 's.subscript', 'x.subscript')
current.copyReference()
current.selection.select(('unicode', None), 737, 738, 739)
current.paste()

## Doing Phonetic Extentions.
phonext_roman_sources_1 = [
    'A.subscript', 
    'B.subscript', 
    'D.subscript', 
    'E.subscript', 
    'G.subscript', 
    'H.subscript',
    'I.subscript',
    'J.subscript',
    'K.subscript',
    'L.subscript',
    'M.subscript',
    'N.subscript',
    'O.subscript',
    'P.subscript',
    'R.subscript',
    'T.subscript',
    'U.subscript',
    'W.subscript',
    'a.subscript',
    'b.subscript',
    'd.subscript',
    'e.subscript',
    'g.subscript',
    'k.subscript',
    'm.subscript',
    'o.subscript',
    'p.subscript',
    't.subscript',
    'u.subscript',
    'v.subscript']
phonext_roman_positions_1 = [
    7468,
    7470,
    7472,
    7473,
    7475,
    7476,
    7477,
    7478,
    7479,
    7480,
    7481,
    7482,
    7484,
    7486,
    7487,
    7488,
    7489,
    7490,
    7491,
    7495,
    7496,
    7497,
    7501,
    7503,
    7504,
    7506,
    7510,
    7511,
    7512,
    7515]

current.selection.none()
for glyph in phonext_roman_sources_1:
    current.selection.select(('more', None), glyph)
current.copyReference()
current.selection.none()
for position in phonext_roman_positions_1:
    current.selection.select(('more', 'unicode'), position)
current.paste()

phonext_roman_sources_2 = [
    'i.subscript',
    'r.subscript',
    'u.subscript',
    'v.subscript',]
phonext_roman_positions_2 = range(7522, 7526)

current.selection.none()
for glyph in phonext_roman_sources_2:
    current.selection.select(('more', None), glyph)
current.copyReference()
current.selection.none()
for position in phonext_roman_positions_2:
    current.selection.select(('more','unicode'), position)
current.paste()

phonext_roman_sources_3 = [
    'c.subscript',
    'f.subscript',
    'z.subscript']
phonext_roman_positions_3 = [
    7580,
    7584,
    7611]

current.selection.none()
for glyph in phonext_roman_sources_3:
    current.selection.select(('more', None), glyph)
current.copyReference()
current.selection.none()
for position in phonext_roman_positions_3:
    current.selection.select(('more', 'unicode'), position)
current.paste()

print('Non-ASCII latin supers and subs are not yet supported.')

## Doing Superscripts and Subscripts.
current.selection.select('zero.subscript', 'one.subscript', 'two.subscript', 'three.subscript', 'four.subscript', 'five.subscript', 'six.subscript', 'seven.subscript', 'eight.subscript', 'nine.subscript')
current.copyReference()
current.selection.select(('unicode', 'ranges'), 8320, 8329)
current.paste()

current.selection.select(('less', 'ranges'), ('unicode', None), 8321, 8323)
current.copy()
current.selection.select(('unicode', 'ranges'), 8308, 8313)
current.selection.select(('more', 'unicode'), 8304)
current.paste()

current.selection.select('i.subscript', 'n.subscript')
current.copyReference()
current.selection.select(('unicode', None), 8305, 8319)
current.paste()

current.selection.select('plus.subscript')
current.copyReference()
current.selection.select(('unicode', None), 8330)
current.paste()

current.selection.select('hyphen.subscript')
current.copyReference()
current.selection.select(('unicode', None), 8331)
current.paste()

current.selection.select('equal.subscript')
current.copyReference()
current.selection.select(('unicode', None), 8332)
current.paste()

current.selection.select('parenleft.subscript', 'parenright.subscript')
current.copyReference()
current.selection.select(('unicode', None), 8333, 8334)
current.paste()

current.selection.select(('unicode', 'ranges'), 8330, 8334)
current.copy()
current.selection.select(('unicode', 'ranges'), 8314, 8318)
current.paste()

current.selection.select('a.subscript', 'e.subscript', 'o.subscript', 'x.subscript')
current.copyReference()
current.selection.select(('unicode', 'ranges'), 8336, 8339)
current.paste()

current.selection.select('h.subscript', 'k.subscript', 'l.subscript', 'm.subscript', 'n.subscript', 'p.subscript', 's.subscript', 't.subscript')
current.copyReference()
current.selection.select(('unicode', 'ranges'), 8341, 8348)
current.paste()

## Doing Latin Extended C.
current.selection.select('j.subscript')
current.copyReference()
current.selection.select(('unicode', None), 11388)
current.paste()

current.selection.select('V.subscript')
current.copyReference()
current.selection.select(('unicode', None), 11389)
current.paste()

## Doing Latin Extended D.
current.selection.select('exclam.subscript')
current.copyReference()
current.selection.select(('unicode', None), 42781)
current.paste()

## Doing Private Use.
privuse_sub_sources = [
    'space.subscript',
    'exclam.subscript',
    'quotedbl.subscript',
    'numbersign.subscript',
    'dollar.subscript',
    'percent.subscript',
    'ampersand.subscript',
    'quotesingle.subscript',
    'asterisk.subscript',
    'comma.subscript',
    'period.subscript',
    'slash.subscript',
    'colon.subscript',
    'semicolon.subscript',
    'less.subscript',
    'greater.subscript',
    'question.subscript',
    'at.subscript',
    'A.subscript',
    'B.subscript',
    'C.subscript',
    'D.subscript',
    'E.subscript',
    'F.subscript',
    'G.subscript',
    'H.subscript',
    'I.subscript',
    'J.subscript',
    'K.subscript',
    'L.subscript',
    'M.subscript',
    'N.subscript',
    'O.subscript',
    'P.subscript',
    'Q.subscript',
    'R.subscript',
    'S.subscript',
    'T.subscript',
    'U.subscript',
    'V.subscript',
    'W.subscript',
    'X.subscript',
    'Y.subscript',
    'Z.subscript',
    'bracketleft.subscript',
    'backslash.subscript',
    'bracketright.subscript',
    'asciicircum.subscript',
    'underscore.subscript',
    'grave.subscript',
    'b.subscript',
    'c.subscript',
    'd.subscript',
    'f.subscript',
    'g.subscript',
    'q.subscript',
    'w.subscript',
    'y.subscript',
    'z.subscript',
    'braceleft.subscript',
    'bar.subscript',
    'braceright.subscript',
    'asciitilde.subscript']

privuse_sub_positions = [
    57345,
    57346,
    57348,
    57350,
    57352,
    57354,
    57356,
    57358,
    57360,
    57362,
    57364,
    57366,
    57368,
    57370,
    57372,
    57374,
    57376,
    57378,
    57379,
    57380,
    57382,
    57383,
    57384,
    57386,
    57387,
    57388,
    57389,
    57390,
    57391,
    57392,
    57393,
    57394,
    57395,
    57396,
    57398,
    57399,
    57401,
    57402,
    57403,
    57404,
    57405,
    57407,
    57409,
    57411,
    57413,
    57415,
    57417,
    57419,
    57421,
    57423,
    57424,
    57425,
    57426,
    57427,
    57428,
    57430,
    57431,
    57432,
    57433,
    57435,
    57437,
    57439,
    57441]

privuse_super_sources = [
    'space.subscript',
    'quotedbl.subscript',
    'numbersign.subscript',
    'dollar.subscript',
    'percent.subscript',
    'ampersand.subscript',
    'quotesingle.subscript',
    'asterisk.subscript',
    'comma.subscript',
    'period.subscript',
    'slash.subscript',
    'colon.subscript',
    'semicolon.subscript',
    'less.subscript',
    'greater.subscript',
    'question.subscript',
    'at.subscript',
    'C.subscript',
    'F.subscript',
    'Q.subscript',
    'S.subscript',
    'X.subscript',
    'Y.subscript',
    'Z.subscript',
    'bracketleft.subscript',
    'backslash.subscript',
    'bracketright.subscript',
    'asciicircum.subscript',
    'underscore.subscript',
    'grave.subscript',
    'q.subscript',
    'braceleft.subscript',
    'bar.subscript',
    'braceright.subscript',
    'asciitilde.subscript']

privuse_super_positions = [
    57344, 
    57347, 
    57349, 
    57351, 
    57353, 
    57355, 
    57357, 
    57359, 
    57361, 
    57363, 
    57365, 
    57367, 
    57369, 
    57371, 
    57373, 
    57375, 
    57377, 
    57381, 
    57385, 
    57397, 
    57400, 
    57406, 
    57408, 
    57410, 
    57412, 
    57414, 
    57416, 
    57418, 
    57420, 
    57422, 
    57429, 
    57434, 
    57436, 
    57438, 
    57440]

current.selection.none()
for glyph in privuse_sub_sources:
    current.selection.select(('more', None), glyph)
current.copyReference()
current.selection.none()
for position in privuse_sub_positions:
    current.selection.select(('unicode', 'more'), position)
current.paste()

current.selection.none()
for glyph in privuse_super_sources:
    current.selection.select(('more', None), glyph)
current.copyReference()
current.selection.none()
for position in privuse_super_positions:
    current.selection.select(('unicode', 'more'), position)
current.paste()

## Repositioning appropriate references to subscripts, to make 
## them into superscripts.
current.selection.none()
for position in all_ascii_superscripts:
    current.selection.select(('unicode', None), position)
    present_super = current.createMappedChar(position)
    present_super.transform(psMat.translate(0, SUPERSCRIPT_OFFSET))

## Below is commented out because this script seems pretty stable;
## it *shouldn't* corrupt if I save over the same file.
# file_version += 0.01
# file_name = "Carbon13EXP, " + str(file_version) +".sfd"
# full_path = PATH + file_name
current.save(full_path)
