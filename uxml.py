import xml.etree.ElementTree as ET  # noqa: N817

DOCTYPE = """<!DOCTYPE root [

<!ENTITY nbsp   "&#160;" ><!-- no-break space = non-breaking space, U+00A0 ISOnum -->
<!ENTITY iexcl  "&#161;" ><!-- inverted exclamation mark, U+00A1 ISOnum -->
<!ENTITY cent   "&#162;" ><!-- cent sign, U+00A2 ISOnum -->
<!ENTITY pound  "&#163;" ><!-- pound sign, U+00A3 ISOnum -->
<!ENTITY curren "&#164;" ><!-- currency sign, U+00A4 ISOnum -->
<!ENTITY yen    "&#165;" ><!-- yen sign = yuan sign, U+00A5 ISOnum -->
<!ENTITY brvbar "&#166;" ><!-- broken bar = broken vertical bar, U+00A6 ISOnum -->
<!ENTITY sect   "&#167;" ><!-- section sign, U+00A7 ISOnum -->
<!ENTITY uml    "&#168;" ><!-- diaeresis = spacing diaeresis, U+00A8 ISOdia -->
<!ENTITY copy   "&#169;" ><!-- copyright sign, U+00A9 ISOnum -->
<!ENTITY ordf   "&#170;" ><!-- feminine ordinal indicator, U+00AA ISOnum -->
<!ENTITY laquo  "&#171;" ><!-- left-pointing double angle quotation mark = left pointing guillemet, U+00AB ISOnum -->
<!ENTITY not    "&#172;" ><!-- not sign, U+00AC ISOnum -->
<!ENTITY shy    "&#173;" ><!-- soft hyphen = discretionary hyphen, U+00AD ISOnum -->
<!ENTITY reg    "&#174;" ><!-- registered sign = registered trade mark sign, U+00AE ISOnum -->
<!ENTITY macr   "&#175;" ><!-- macron = spacing macron = overline = APL overbar, U+00AF ISOdia -->
<!ENTITY deg    "&#176;" ><!-- degree sign, U+00B0 ISOnum -->
<!ENTITY plusmn "&#177;" ><!-- plus-minus sign = plus-or-minus sign, U+00B1 ISOnum -->
<!ENTITY sup2   "&#178;" ><!-- superscript two = superscript digit two = squared, U+00B2 ISOnum -->
<!ENTITY sup3   "&#179;" ><!-- superscript three = superscript digit three = cubed, U+00B3 ISOnum -->
<!ENTITY acute  "&#180;" ><!-- acute accent = spacing acute, U+00B4 ISOdia -->
<!ENTITY micro  "&#181;" ><!-- micro sign, U+00B5 ISOnum -->
<!ENTITY para   "&#182;" ><!-- pilcrow sign = paragraph sign, U+00B6 ISOnum -->
<!ENTITY middot "&#183;" ><!-- middle dot = Georgian comma = Greek middle dot, U+00B7 ISOnum -->
<!ENTITY cedil  "&#184;" ><!-- cedilla = spacing cedilla, U+00B8 ISOdia -->
<!ENTITY sup1   "&#185;" ><!-- superscript one = superscript digit one, U+00B9 ISOnum -->
<!ENTITY ordm   "&#186;" ><!-- masculine ordinal indicator, U+00BA ISOnum -->
<!ENTITY raquo  "&#187;" ><!-- right-pointing double angle quotation mark = right pointing guillemet, U+00BB ISOnum -->
<!ENTITY frac14 "&#188;" ><!-- vulgar fraction one quarter = fraction one quarter, U+00BC ISOnum -->
<!ENTITY frac12 "&#189;" ><!-- vulgar fraction one half = fraction one half, U+00BD ISOnum -->
<!ENTITY frac34 "&#190;" ><!-- vulgar fraction three quarters = fraction three quarters, U+00BE ISOnum -->
<!ENTITY iquest "&#191;" ><!-- inverted question mark = turned question mark, U+00BF ISOnum -->
<!ENTITY Agrave "&#192;" ><!-- latin capital A with grave = latin capital A grave, U+00C0 ISOlat1 -->
<!ENTITY Aacute "&#193;" ><!-- latin capital A with acute, U+00C1 ISOlat1 -->
<!ENTITY Acirc  "&#194;" ><!-- latin capital A with circumflex, U+00C2 ISOlat1 -->
<!ENTITY Atilde "&#195;" ><!-- latin capital A with tilde, U+00C3 ISOlat1 -->
<!ENTITY Auml   "&#196;" ><!-- latin capital A with diaeresis, U+00C4 ISOlat1 -->
<!ENTITY Aring  "&#197;" ><!-- latin capital A with ring above = latin capital A ring, U+00C5 ISOlat1 -->
<!ENTITY AElig  "&#198;" ><!-- latin capital AE = latin capital ligature AE, U+00C6 ISOlat1 -->
<!ENTITY Ccedil "&#199;" ><!-- latin capital C with cedilla, U+00C7 ISOlat1 -->
<!ENTITY Egrave "&#200;" ><!-- latin capital E with grave, U+00C8 ISOlat1 -->
<!ENTITY Eacute "&#201;" ><!-- latin capital E with acute, U+00C9 ISOlat1 -->
<!ENTITY Ecirc  "&#202;" ><!-- latin capital E with circumflex, U+00CA ISOlat1 -->
<!ENTITY Euml   "&#203;" ><!-- latin capital E with diaeresis, U+00CB ISOlat1 -->
<!ENTITY Igrave "&#204;" ><!-- latin capital I with grave, U+00CC ISOlat1 -->
<!ENTITY Iacute "&#205;" ><!-- latin capital I with acute, U+00CD ISOlat1 -->
<!ENTITY Icirc  "&#206;" ><!-- latin capital I with circumflex, U+00CE ISOlat1 -->
<!ENTITY Iuml   "&#207;" ><!-- latin capital I with diaeresis, U+00CF ISOlat1 -->
<!ENTITY ETH    "&#208;" ><!-- latin capital ETH, U+00D0 ISOlat1 -->
<!ENTITY Ntilde "&#209;" ><!-- latin capital N with tilde, U+00D1 ISOlat1 -->
<!ENTITY Ograve "&#210;" ><!-- latin capital O with grave, U+00D2 ISOlat1 -->
<!ENTITY Oacute "&#211;" ><!-- latin capital O with acute, U+00D3 ISOlat1 -->
<!ENTITY Ocirc  "&#212;" ><!-- latin capital O with circumflex, U+00D4 ISOlat1 -->
<!ENTITY Otilde "&#213;" ><!-- latin capital O with tilde, U+00D5 ISOlat1 -->
<!ENTITY Ouml   "&#214;" ><!-- latin capital O with diaeresis, U+00D6 ISOlat1 -->
<!ENTITY times  "&#215;" ><!-- multiplication sign, U+00D7 ISOnum -->
<!ENTITY Oslash "&#216;" ><!-- latin capital O with stroke = latin capital O slash, U+00D8 ISOlat1 -->
<!ENTITY Ugrave "&#217;" ><!-- latin capital U with grave, U+00D9 ISOlat1 -->
<!ENTITY Uacute "&#218;" ><!-- latin capital U with acute, U+00DA ISOlat1 -->
<!ENTITY Ucirc  "&#219;" ><!-- latin capital U with circumflex, U+00DB ISOlat1 -->
<!ENTITY Uuml   "&#220;" ><!-- latin capital U with diaeresis, U+00DC ISOlat1 -->
<!ENTITY Yacute "&#221;" ><!-- latin capital Y with acute, U+00DD ISOlat1 -->
<!ENTITY THORN  "&#222;" ><!-- latin capital THORN, U+00DE ISOlat1 -->
<!ENTITY szlig  "&#223;" ><!-- latin small sharp s = ess-zed, U+00DF ISOlat1 -->
<!ENTITY agrave "&#224;" ><!-- latin small a with grave = latin small a grave, U+00E0 ISOlat1 -->
<!ENTITY aacute "&#225;" ><!-- latin small a with acute, U+00E1 ISOlat1 -->
<!ENTITY acirc  "&#226;" ><!-- latin small a with circumflex, U+00E2 ISOlat1 -->
<!ENTITY atilde "&#227;" ><!-- latin small a with tilde, U+00E3 ISOlat1 -->
<!ENTITY auml   "&#228;" ><!-- latin small a with diaeresis, U+00E4 ISOlat1 -->
<!ENTITY aring  "&#229;" ><!-- latin small a with ring above = latin small a ring, U+00E5 ISOlat1 -->
<!ENTITY aelig  "&#230;" ><!-- latin small ae = latin small ligature ae, U+00E6 ISOlat1 -->
<!ENTITY ccedil "&#231;" ><!-- latin small c with cedilla, U+00E7 ISOlat1 -->
<!ENTITY egrave "&#232;" ><!-- latin small e with grave, U+00E8 ISOlat1 -->
<!ENTITY eacute "&#233;" ><!-- latin small e with acute, U+00E9 ISOlat1 -->
<!ENTITY ecirc  "&#234;" ><!-- latin small e with circumflex, U+00EA ISOlat1 -->
<!ENTITY euml   "&#235;" ><!-- latin small e with diaeresis, U+00EB ISOlat1 -->
<!ENTITY igrave "&#236;" ><!-- latin small i with grave, U+00EC ISOlat1 -->
<!ENTITY iacute "&#237;" ><!-- latin small i with acute, U+00ED ISOlat1 -->
<!ENTITY icirc  "&#238;" ><!-- latin small i with circumflex, U+00EE ISOlat1 -->
<!ENTITY iuml   "&#239;" ><!-- latin small i with diaeresis, U+00EF ISOlat1 -->
<!ENTITY eth    "&#240;" ><!-- latin small eth, U+00F0 ISOlat1 -->
<!ENTITY ntilde "&#241;" ><!-- latin small n with tilde, U+00F1 ISOlat1 -->
<!ENTITY ograve "&#242;" ><!-- latin small o with grave, U+00F2 ISOlat1 -->
<!ENTITY oacute "&#243;" ><!-- latin small o with acute, U+00F3 ISOlat1 -->
<!ENTITY ocirc  "&#244;" ><!-- latin small o with circumflex, U+00F4 ISOlat1 -->
<!ENTITY otilde "&#245;" ><!-- latin small o with tilde, U+00F5 ISOlat1 -->
<!ENTITY ouml   "&#246;" ><!-- latin small o with diaeresis, U+00F6 ISOlat1 -->
<!ENTITY divide "&#247;" ><!-- division sign, U+00F7 ISOnum -->
<!ENTITY oslash "&#248;" ><!-- latin small o with stroke, = latin small o slash, U+00F8 ISOlat1 -->
<!ENTITY ugrave "&#249;" ><!-- latin small u with grave, U+00F9 ISOlat1 -->
<!ENTITY uacute "&#250;" ><!-- latin small u with acute, U+00FA ISOlat1 -->
<!ENTITY ucirc  "&#251;" ><!-- latin small u with circumflex, U+00FB ISOlat1 -->
<!ENTITY uuml   "&#252;" ><!-- latin small u with diaeresis, U+00FC ISOlat1 -->
<!ENTITY yacute "&#253;" ><!-- latin small y with acute, U+00FD ISOlat1 -->
<!ENTITY thorn  "&#254;" ><!-- latin small thorn with, U+00FE ISOlat1 -->
<!ENTITY yuml   "&#255;" ><!-- latin small y with diaeresis, U+00FF ISOlat1 -->

]>
"""


def parse(xml: str) -> ET.Element:
    return ET.fromstring(DOCTYPE + "<root>" + xml + "</root>")
