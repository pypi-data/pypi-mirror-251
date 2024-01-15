# HEADER:
# - Module Name: reserve_ligatures.py
# - Written by: Isaac N. Erb.
# - Created: 2023-??-??.
# - Last Edited*: 2023-Oct-14.
#
#       * (Read: "Last time the author bothered to update this.")

# PURPOSE:
# - This module uses the fontforge.py module (or package; I
#   don't know which) to create an arbitrarily large batch of
#   ligatures, by a method described later.
# -

import fontforge
from .custom_functions import pasteAfter

file_version = 5.18
suffix = "-Regu"
file_name = f"Carbon-13, {file_version}{suffix}.sfd"
PATH = "/home/ironheart/Documents/Creative/Fontstuff/"
full_path = PATH + file_name
current = fontforge.open(full_path)

## Setting constants.
EM_SIZE = current.em
INCREMENT = EM_SIZE / 48    # EM_SIZE / 48 should be the minimum movement-increment to retain sharpness/fuzziness.

LIGATURE_SUBTABLE = 'Standard Ligatures-1'  # ! Should instead read from font's metadata.

## Below: A list of grouped characters, each item in which is a
## sequence of characters for which a ligature is to be created.
raw_list = ['",', '".', '"/', '"A', '"J', '"_', '"¸', '"À', '"Á', '"Â', '"Ã', '"Ä', '"Å', '"Æ', '"‚', '"„', '"…',
    "',", "'.", "'/", "'A", "'J", "'_", "'¸", "'À", "'Á", "'Â", "'Ã", "'Ä", "'Å", "'Æ", "'‚", "'„", "'…",
    '-,', '-.', '-/', '-A', '-J', '-_', '-¸', '-À', '-Á', '-Â', '-Ã', '-Ä', '-Å', '-Æ', '-‚', '-„', '-…',
    '/,', '/.', '//', '/A', '/J', '/_', '/¸', '/À', '/Á', '/Â', '/Ã', '/Ä', '/Å', '/Æ', '/‚', '/„', '/…',
    'A"', "A'", 'Aª', 'A°', 'A²', 'A³', 'A¹', 'Aº', 'A‘', 'A’', 'A‛', 'A“', 'A”', 'A‟', 'A†', 'A‡', 'A′', 'A″', 'A‴', 'A‵', 'A‶', 'A‷', 'A⁗',
    'C+', 'C-', 'Cf', 'Ct', 'Cv', 'Cw', 'Cy', 'C·', 'C‐', 'C‑', 'C‒', 'C–', 'C—', 'C―', 'C‧', 'C⋯',
    'F+', 'F,', 'F-', 'F.', 'F/', 'FA', 'FJ', 'F_', 'Ff', 'Ft', 'Fv', 'Fw', 'Fy', 'F·', 'F¸', 'FÀ', 'FÁ', 'FÂ', 'FÃ', 'FÄ', 'FÅ', 'FÆ', 'F‐', 'F‑', 'F‒', 'F–', 'F—', 'F―', 'F‚', 'F„', 'F…', 'F‧', 'F⋯',
    'L"', "L'", 'L+', 'L-', 'Lf', 'Lt', 'Lv', 'Lw', 'Ly', 'Lª', 'L°', 'L²', 'L³', 'L·', 'L¹', 'Lº', 'L‐', 'L‑', 'L‒', 'L–', 'L—', 'L―', 'L‘', 'L’', 'L‛', 'L“', 'L”', 'L‟', 'L†', 'L‡', 'L‧', 'L′', 'L″', 'L‴', 'L‵', 'L‶', 'L‷', 'L⁗', 'L⋯',
    'P,', 'P.', 'P/', 'PA', 'PJ', 'P_', 'P¸', 'PÀ', 'PÁ', 'PÂ', 'PÃ', 'PÄ', 'PÅ', 'PÆ', 'P‚', 'P„', 'P…',
    'T+', 'T,', 'T-', 'T.', 'T/', 'TA', 'TJ', 'T_', 'Ta', 'Tc', 'Td', 'Te', 'Tf', 'Tg', 'Tm', 'Tn', 'To', 'Tp', 'Tq', 'Tr', 'Ts', 'Tt', 'Tu', 'Tv', 'Tw', 'Tx', 'Ty', 'Tz', 'T·', 'T¸', 'T»', 'TÀ', 'TÁ', 'TÂ', 'TÃ', 'TÄ', 'TÅ', 'TÆ', 'Tá', 'Tæ', 'Tç', 'Té', 'Tí', 'Tð', 'Tó', 'Tø', 'Tú', 'Tý', 'T‐', 'T‑', 'T‒', 'T–', 'T—', 'T―', 'T‚', 'T„', 'T…', 'T‧', 'T⋯',
    'V,', 'V-', 'V.', 'V/', 'VA', 'VJ', 'V_', 'Va', 'Vc', 'Vd', 'Ve', 'Vf', 'Vg', 'Vm', 'Vn', 'Vo', 'Vp', 'Vq', 'Vr', 'Vs', 'Vt', 'Vu', 'Vv', 'Vw', 'Vx', 'Vy', 'Vz', 'V¸', 'V»', 'VÀ', 'VÁ', 'VÂ', 'VÃ', 'VÄ', 'VÅ', 'VÆ', 'Vá', 'Væ', 'Vç', 'Vé', 'Ví', 'Vð', 'Vó', 'Vø', 'Vú', 'Vý', 'V‚', 'V„', 'V…',
    'W,', 'W-', 'W.', 'W/', 'WA', 'WJ', 'W_', 'Wa', 'Wc', 'Wd', 'We', 'Wf', 'Wg', 'Wm', 'Wn', 'Wo', 'Wp', 'Wq', 'Wr', 'Ws', 'Wt', 'Wu', 'Wv', 'Ww', 'Wx', 'Wy', 'Wz', 'W¸', 'W»', 'WÀ', 'WÁ', 'WÂ', 'WÃ', 'WÄ', 'WÅ', 'WÆ', 'Wá', 'Wæ', 'Wç', 'Wé', 'Wí', 'Wð', 'Wó', 'Wø', 'Wú', 'Wý', 'W‚', 'W„', 'W…',
    'Y,', 'Y-', 'Y.', 'Y/', 'YA', 'YJ', 'Y_', 'Ya', 'Yc', 'Yd', 'Ye', 'Yf', 'Yg', 'Ym', 'Yn', 'Yo', 'Yp', 'Yq', 'Yr', 'Ys', 'Yt', 'Yu', 'Yv', 'Yw', 'Yx', 'Yy', 'Yz', 'Y¸', 'Y»', 'YÀ', 'YÁ', 'YÂ', 'YÃ', 'YÄ', 'YÅ', 'YÆ', 'Yá', 'Yæ', 'Yç', 'Yé', 'Yí', 'Yð', 'Yó', 'Yø', 'Yú', 'Yý', 'Y‚', 'Y„', 'Y…',
    'Z+', 'Z-', 'Zf', 'Zt', 'Zv', 'Zw', 'Zy', 'Z·', 'Z‐', 'Z‑', 'Z‒', 'Z–', 'Z—', 'Z―', 'Z‧', 'Z⋯',
    '\\"', "\\'", '\\ª', '\\°', '\\²', '\\³', '\\¹', '\\º', '\\‘', '\\’', '\\‛', '\\“', '\\”', '\\‟', '\\†', '\\‡', '\\′', '\\″', '\\‴', '\\‵', '\\‶', '\\‷', '\\⁗',
    '`,', '`.', '`/', '`A', '`J', '`_', '`¸', '`À', '`Á', '`Â', '`Ã', '`Ä', '`Å', '`Æ', '`‚', '`„', '`…',
    'aT', 'aV', 'aW', 'aY', 'a\\', 'a`', 'a¨', 'a¯', 'a´', 'a’', 'a‛', 'a”', 'a‟',
    'bT', 'bV', 'bW', 'bY', 'b\\', 'b`', 'b¨', 'b¯', 'b´', 'b’', 'b‛', 'b”', 'b‟',
    'cT', 'cV', 'cW', 'cY', 'c\\', 'c`', 'c¨', 'c¯', 'c´', 'c’', 'c‛', 'c”', 'c‟',
    'eT', 'eV', 'eW', 'eY', 'e\\', 'e`', 'e¨', 'e¯', 'e´', 'e’', 'e‛', 'e”', 'e‟',
    'f,', 'f.', 'f/', 'fA', 'fJ', 'f_', 'f¸', 'fÀ', 'fÁ', 'fÂ', 'fÃ', 'fÄ', 'fÅ', 'fÆ', 'f‚', 'f„', 'f…',
    'gT', 'gV', 'gW', 'gY', 'g\\', 'g`', 'g¨', 'g¯', 'g´', 'g’', 'g‛', 'g”', 'g‟',
    'hT', 'hV', 'hW', 'hY', 'h\\', 'h`', 'h¨', 'h¯', 'h´', 'h’', 'h‛', 'h”', 'h‟',
    'kT', 'kV', 'kW', 'kY', 'k\\', 'k`', 'k¨', 'k¯', 'k´', 'k’', 'k‛', 'k”', 'k‟',
    'lT', 'lV', 'lW', 'lY', 'l\\', 'l`', 'l¨', 'l¯', 'l´', 'l’', 'l‛', 'l”', 'l‟',
    'mT', 'mV', 'mW', 'mY', 'm\\', 'm`', 'm¨', 'm¯', 'm´', 'm’', 'm‛', 'm”', 'm‟',
    'nT', 'nV', 'nW', 'nY', 'n\\', 'n`', 'n¨', 'n¯', 'n´', 'n’', 'n‛', 'n”', 'n‟',
    'oT', 'oV', 'oW', 'oY', 'o\\', 'o`', 'o¨', 'o¯', 'o´', 'o’', 'o‛', 'o”', 'o‟',
    'pT', 'pV', 'pW', 'pY', 'p\\', 'p`', 'p¨', 'p¯', 'p´', 'p’', 'p‛', 'p”', 'p‟',
    'qT', 'qV', 'qW', 'qY', 'q\\', 'q`', 'q¨', 'q¯', 'q´', 'q’', 'q‛', 'q”', 'q‟',
    'r,', 'r-', 'r.', 'r/', 'rA', 'rJ', 'rT', 'rV', 'rW', 'rY', 'r\\', 'r_', 'r`', 'ra', 'r¨', 'r¯', 'r´', 'r¸', 'rÀ', 'rÁ', 'rÂ', 'rÃ', 'rÄ', 'rÅ', 'rÆ', 'rá', 'ræ', 'rð', 'r’', 'r‚', 'r‛', 'r”', 'r„', 'r‟', 'r…'
    'sT', 'sV', 'sW', 'sY', 's\\', 's`', 's¨', 's¯', 's´', 's’', 's‛', 's”', 's‟',
    'tT', 'tV', 'tW', 'tY', 't\\', 't`', 't¨', 't¯', 't´', 't’', 't‛', 't”', 't‟',
    'uT', 'uV', 'uW', 'uY', 'u\\', 'u`', 'u¨', 'u¯', 'u´', 'u’', 'u‛', 'u”', 'u‟',
    'v,', 'v.', 'v/', 'vA', 'vJ', 'vT', 'vV', 'vW', 'vY', 'v\\', 'v_', 'v`', 'v¨', 'v¯', 'v´', 'v¸', 'vÀ', 'vÁ', 'vÂ', 'vÃ', 'vÄ', 'vÅ', 'vÆ', 'v’', 'v‚', 'v‛', 'v”', 'v„', 'v‟', 'v…',
    'w,', 'w.', 'w/', 'wA', 'wJ', 'wT', 'wV', 'wW', 'wY', 'w\\', 'w_', 'w`', 'w¨', 'w¯', 'w´', 'w¸', 'wÀ', 'wÁ', 'wÂ', 'wÃ', 'wÄ', 'wÅ', 'wÆ', 'w’', 'w‚', 'w‛', 'w”', 'w„', 'w‟', 'w…',
    'xT', 'xV', 'xW', 'xY', 'x\\', 'x`', 'x¨', 'x¯', 'x´', 'x’', 'x‛', 'x”', 'x‟',
    'y,', 'y.', 'y/', 'yA', 'yJ', 'yT', 'yV', 'yW', 'yY', 'y\\', 'y_', 'y`', 'y¨', 'y¯', 'y´', 'y¸', 'yÀ', 'yÁ', 'yÂ', 'yÃ', 'yÄ', 'yÅ', 'yÆ', 'y’', 'y‚', 'y‛', 'y”', 'y„', 'y‟', 'y…', 'zT', 'zV', 'zW', 'zY', 'z\\', 'z`', 'z¨', 'z¯', 'z´', 'z’', 'z‛', 'z”', 'z‟', '¡T', '¡V', '¡W', '¡Y', '¡\\', '¡`', '¡¨', '¡¯', '¡´', '¡’', '¡‛', '¡”', '¡‟', '¨,', '¨-', '¨.', '¨/', '¨A', '¨J', '¨_', '¨a', '¨c', '¨d', '¨e', '¨f', '¨g', '¨m', '¨n', '¨o', '¨p', '¨q', '¨r', '¨s', '¨t', '¨u', '¨v', '¨w', '¨x', '¨y', '¨z', '¨¸', '¨»', '¨À', '¨Á', '¨Â', '¨Ã', '¨Ä', '¨Å', '¨Æ', '¨á', '¨æ', '¨ç', '¨é', '¨í', '¨ð', '¨ó', '¨ø', '¨ú', '¨ý', '¨‚', '¨„', '¨…', 'ª,', 'ª.', 'ª/', 'ªA', 'ªJ', 'ª_', 'ª¸', 'ªÀ', 'ªÁ', 'ªÂ', 'ªÃ', 'ªÄ', 'ªÅ', 'ªÆ', 'ª‚', 'ª„', 'ª…', '«,', '«.', '«/', '«A', '«J', '«T', '«V', '«W', '«Y', '«\\', '«_', '«`', '«¨', '«¯', '«´', '«¸', '«À', '«Á', '«Â', '«Ã', '«Ä', '«Å', '«Æ', '«’', '«‚', '«‛', '«”', '«„', '«‟', '«…', '¯,', '¯-', '¯.', '¯/', '¯A', '¯J', '¯_', '¯a', '¯c', '¯d', '¯e', '¯f', '¯g', '¯m', '¯n', '¯o', '¯p', '¯q', '¯r', '¯s', '¯t', '¯u', '¯v', '¯w', '¯x', '¯y', '¯z', '¯¸', '¯»', '¯À', '¯Á', '¯Â', '¯Ã', '¯Ä', '¯Å', '¯Æ', '¯á', '¯æ', '¯ç', '¯é', '¯í', '¯ð', '¯ó', '¯ø', '¯ú', '¯ý', '¯‚', '¯„', '¯…', '°,', '°-', '°.', '°/', '°A', '°J', '°_', '°a', '°c', '°d', '°e', '°f', '°g', '°m', '°n', '°o', '°p', '°q', '°r', '°s', '°t', '°u', '°v', '°w', '°x', '°y', '°z', '°¸', '°»', '°À', '°Á', '°Â', '°Ã', '°Ä', '°Å', '°Æ', '°á', '°æ', '°ç', '°é', '°í', '°ð', '°ó', '°ø', '°ú', '°ý', '°‚', '°„', '°…', '²,', '².', '²/', '²A', '²J', '²_', '²¸', '²À', '²Á', '²Â', '²Ã', '²Ä', '²Å', '²Æ', '²‚', '²„', '²…', '³,', '³.', '³/', '³A', '³J', '³_', '³¸', '³À', '³Á', '³Â', '³Ã', '³Ä', '³Å', '³Æ', '³‚', '³„', '³…', '´,', '´-', '´.', '´/', '´A', '´J', '´_', '´a', '´c', '´d', '´e', '´f', '´g', '´m', '´n', '´o', '´p', '´q', '´r', '´s', '´t', '´u', '´v', '´w', '´x', '´y', '´z', '´¸', '´»', '´À', '´Á', '´Â', '´Ã', '´Ä', '´Å', '´Æ', '´á', '´æ', '´ç', '´é', '´í', '´ð', '´ó', '´ø', '´ú', '´ý', '´‚', '´„', '´…', 'µT', 'µV', 'µW', 'µY', 'µ\\', 'µ`', 'µ¨', 'µ¯', 'µ´', 'µ’', 'µ‛', 'µ”', 'µ‟', '·,', '·.', '·/', '·A', '·J', '·_', '·¸', '·À', '·Á', '·Â', '·Ã', '·Ä', '·Å', '·Æ', '·‚', '·„', '·…', '¹,', '¹.', '¹/', '¹A', '¹J', '¹_', '¹¸', '¹À', '¹Á', '¹Â', '¹Ã', '¹Ä', '¹Å', '¹Æ', '¹‚', '¹„', '¹…', 'º,', 'º.', 'º/', 'ºA', 'ºJ', 'º_', 'º¸', 'ºÀ', 'ºÁ', 'ºÂ', 'ºÃ', 'ºÄ', 'ºÅ', 'ºÆ', 'º‚', 'º„', 'º…', '¿T', '¿V', '¿W', '¿Y', '¿\\', '¿`', '¿¨', '¿¯', '¿´', '¿’', '¿‛', '¿”', '¿‟', 'À"', "À'", 'Àª', 'À°', 'À²', 'À³', 'À¹', 'Àº', 'À‘', 'À’', 'À‛', 'À“', 'À”', 'À‟', 'À†', 'À‡', 'À′', 'À″', 'À‴', 'À‵', 'À‶', 'À‷', 'À⁗', 'Á"', "Á'", 'Áª', 'Á°', 'Á²', 'Á³', 'Á¹', 'Áº', 'Á‘', 'Á’', 'Á‛', 'Á“', 'Á”', 'Á‟', 'Á†', 'Á‡', 'Á′', 'Á″', 'Á‴', 'Á‵', 'Á‶', 'Á‷', 'Á⁗', 'Â"', "Â'", 'Âª', 'Â°', 'Â²', 'Â³', 'Â¹', 'Âº', 'Â‘', 'Â’', 'Â‛', 'Â“', 'Â”', 'Â‟', 'Â†', 'Â‡', 'Â′', 'Â″', 'Â‴', 'Â‵', 'Â‶', 'Â‷', 'Â⁗', 'Ã"', "Ã'", 'Ãª', 'Ã°', 'Ã²', 'Ã³', 'Ã¹', 'Ãº', 'Ã‘', 'Ã’', 'Ã‛', 'Ã“', 'Ã”', 'Ã‟', 'Ã†', 'Ã‡', 'Ã′', 'Ã″', 'Ã‴', 'Ã‵', 'Ã‶', 'Ã‷', 'Ã⁗', 'Ä"', "Ä'", 'Äª', 'Ä°', 'Ä²', 'Ä³', 'Ä¹', 'Äº', 'Ä‘', 'Ä’', 'Ä‛', 'Ä“', 'Ä”', 'Ä‟', 'Ä†', 'Ä‡', 'Ä′', 'Ä″', 'Ä‴', 'Ä‵', 'Ä‶', 'Ä‷', 'Ä⁗', 'Å"', "Å'", 'Åª', 'Å°', 'Å²', 'Å³', 'Å¹', 'Åº', 'Å‘', 'Å’', 'Å‛', 'Å“', 'Å”', 'Å‟', 'Å†', 'Å‡', 'Å′', 'Å″', 'Å‴', 'Å‵', 'Å‶', 'Å‷', 'Å⁗', 'Ç+', 'Ç-', 'Çf', 'Çt', 'Çv', 'Çw', 'Çy', 'Ç·', 'Ç‐', 'Ç‑', 'Ç‒', 'Ç–', 'Ç—', 'Ç―', 'Ç‧', 'Ç⋯', 'æT', 'æV', 'æW', 'æY', 'æ\\', 'æ`', 'æ¨', 'æ¯', 'æ´', 'æ’', 'æ‛', 'æ”', 'æ‟', 'çT', 'çV', 'çW', 'çY', 'ç\\', 'ç`', 'ç¨', 'ç¯', 'ç´', 'ç’', 'ç‛', 'ç”', 'ç‟', 'þT', 'þV', 'þW', 'þY', 'þ\\', 'þ`', 'þ¨', 'þ¯', 'þ´', 'þ’', 'þ‛', 'þ”', 'þ‟', '‘,', '‘-', '‘.', '‘/', '‘A', '‘J', '‘_', '‘a', '‘c', '‘d', '‘e', '‘f', '‘g', '‘m', '‘n', '‘o', '‘p', '‘q', '‘r', '‘s', '‘t', '‘u', '‘v', '‘w', '‘x', '‘y', '‘z', '‘¸', '‘»', '‘À', '‘Á', '‘Â', '‘Ã', '‘Ä', '‘Å', '‘Æ', '‘á', '‘æ', '‘ç', '‘é', '‘í', '‘ð', '‘ó', '‘ø', '‘ú', '‘ý', '‘‚', '‘„', '‘…', '“,', '“-', '“.', '“/', '“A', '“J', '“_', '“a', '“c', '“d', '“e', '“f', '“g', '“m', '“n', '“o', '“p', '“q', '“r', '“s', '“t', '“u', '“v', '“w', '“x', '“y',
    '“z', '“¸', '“»', '“À', '“Á', '“Â', '“Ã', '“Ä', '“Å', '“Æ', '“á', '“æ', '“ç', '“é', '“í', '“ð', '“ó', '“ø', '“ú', '“ý', '“‚', '“„', '“…']

privUse_position = 57936    # Starting-position in Private Use for custom ligatures. (U+E250.)

erase = input("Erase existing positions? (True/False)\n")
erase = bool(erase.lower() == "true")

if erase:
    for position in range(privUse_position, privUse_position + len(raw_list)):
        current.selection.select(['more', 'unicode'], position)
    current.clear()

for pair in raw_list:   #@ I want the ability to handle trios, as well. Should this be more modular?
    component = list(pair)  # Separating pair into its constituent characters.
    first = current.createMappedChar(ord(component[0]))
    second = current.createMappedChar(ord(component[1]))

    if not first.isWorthOutputting():       # Checking whether font supports ligature-component 0.
        first.clear()
        privUse_position += 1

        if not second.isWorthOutputting():  # This should account for neither component being supported. I think.
            second.clear()


    elif not second.isWorthOutputting():    # Checking whether font supports ligature-component 1.
        second.clear()
        privUse_position += 1

    else:
        ## Defining new ligature as part of class glyph.
        new_lig = current.createChar(privUse_position)

        ## Doing paste-after, to position the characters roughly as they would be with default kerning.
        pasteAfter(first, second, new_lig)

        ## Naming the new ligature.
        new_lig.glyphname = first.glyphname + '_' + second.glyphname

        ## Ideally, properly configuring the ligature-subtable for the new ligature.
        new_lig.addPosSub(LIGATURE_SUBTABLE, [first.glyphname, second.glyphname])

        ## Setting default ligature-caret-position to just past the end of the first component. Needs manual adjustment after.
        c_positon = int(first.width - first.right_side_bearing + round(INCREMENT))
        new_lig.lcarets = [c_positon]

        ## Looping.
        privUse_position += 1

# - The below three lines are for if I want to save to a new
#   file after the script finishes. I don't currently deem that
#   necessary.
# file_version += 0.01
# file_name = "IronNew, " +str(file_version) + "-Regu (Dev).sfd"
# full_path = PATH + file_name
current.save(full_path)
