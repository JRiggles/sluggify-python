"""Sluggifier for Python based on https://github.com/Skeddles/sluggify

MIT LICENSE
Copyright © 2024 John Riggles

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from re import sub


_LETTERS: dict[str, str] = {
    "áàâǎăãảȧạäåḁāąⱥȁấầẫẩậắằẵẳặǻǡǟȁȃａ": "a",
    "ÁÀÂǍĂÃẢȦẠÄÅḀĀĄȺȀẤẦẪẨẬẮẰẴẲẶǺǠǞȀȂＡ": "A",
    "ḃḅḇƀᵬᶀｂ": "b",
    "ḂḄḆɃƁʙＢ": "B",
    "ćĉčċçḉȼɕｃƇ": "c",
    "ĆĈČĊÇḈȻＣƈ": "C",
    "ďḋḑḍḓḏđɗƌｄᵭᶁᶑȡ": "d",
    "ĎḊḐḌḒḎĐƉƊƋＤᴅᶑȡ": "D",
    "éèêḙěĕẽḛẻėëēȩęɇȅếềễểḝḗḕȇẹệｅᶒⱸ": "e",
    "ÉÈÊḘĚĔẼḚẺĖËĒȨĘɆȄẾỀỄỂḜḖḔȆẸỆＥᴇ": "E",
    "ḟƒｆᵮᶂ": "f",
    "ḞƑＦ": "F",
    "ǵğĝǧġģḡǥɠｇᶃ": "g",
    "ǴĞĜǦĠĢḠǤƓＧɢ": "G",
    "ĥȟḧḣḩḥḫ̱ẖħⱨｈ": "h",
    "ĤȞḦḢḨḤḪĦⱧＨʜ": "H",
    "íìĭîǐïḯĩįīỉȉȋịḭɨiıｉ": "i",
    "ÍÌĬÎǏÏḮĨĮĪỈȈȊỊḬƗİIＩ": "I",
    "ĵɉｊʝɟʄǰ": "j",
    "ĴɈＪᴊ": "J",
    "ḱǩķḳḵƙⱪꝁｋᶄ": "k",
    "ḰǨĶḲḴƘⱩꝀＫᴋ": "K",
    "ĺľļḷḹḽḻłŀƚⱡɫｌɬᶅɭȴ": "l",
    "ĹĽĻḶḸḼḺŁĿȽⱠⱢＬʟ": "L",
    "ḿṁṃɱｍᵯᶆ": "m",
    "ḾṀṂⱮＭᴍ": "M",
    "ńǹňñṅņṇṋṉɲƞｎŋᵰᶇɳȵ": "n",
    "ŃǸŇÑṄŅṆṊṈṉƝȠＮŊɴ": "N",
    "óòŏôốồỗổǒöȫőõṍṏȭȯȱøǿǫǭōṓṑỏȍȏơớờỡởợọộɵｏⱺᴏ": "o",
    "ÓÒŎÔỐỒỖỔǑÖȪŐÕṌṎȬȮȰØǾǪǬŌṒṐỎȌȎƠỚỜỠỞỢỌỘƟＯ": "O",
    "ṕṗᵽ": "p",
    "ṔṖⱣƤＰ": "P",
    "ɋʠｑ": "q",
    "ɊＱ": "Q",
    "ŕřṙŗȑȓṛṝṟɍɽｒᵲᶉɼɾᵳ": "r",
    "ŔŘṘŖȐȒṚṜṞɌⱤＲʀ": "R",
    "śṥŝšṧṡşṣṩșｓßẛᵴᶊʂȿſ": "s",
    "ŚṤŜŠṦṠŞṢṨȘＳẞ": "S",
    "ťṫţṭțṱṯŧⱦƭʈｔẗᵵƫȶ": "t",
    "ŤṪŢṬȚṰṮŦȾƬƮＴᴛ": "T",
    "úùŭûǔůüǘǜǚǖűũṹųūṻủȕȗưứừữửựụṳṷṵʉᶙ": "u",
    "ÚÙŬÛǓŮÜǗǛǙǕŰŨṸŲŪṺỦȔȖƯỨỪỮỬỰỤṲṶṴɄＵ": "U",
    "ṽṿʋｖⱱⱴᴠᶌ": "v",
    "ṼṾƲＶ": "V",
    "ẃẁŵẅẇẉⱳｗẘ": "w",
    "ẂẀŴẄẆẈⱲＷ": "W",
    "ẍẋｘᶍ": "x",
    "ẌẊＸ": "X",
    "ýỳŷÿỹẏȳỷỵɏƴｙẙ": "y",
    "ÝỲŶŸỸẎȲỶỴɎƳＹʏ": "Y",
    "źẑžżẓẕƶȥⱬｚᵶᶎʐʑɀᴢ": "z",
    "ŹẐŽŻẒẔƵȤⱫＺ": "Z",
}


def _replace_accents(text: str) -> str:
    """
    Replace any accented characters in the input `text` with their closest
    "normalized" unaccented English variant, e.g.: `'á'` becomes `'a'`
    """
    normalized_string = ''
    for char in text:
        replaced = False
        for accent_chars, replacement_char in _LETTERS.items():
            if char in accent_chars:
                normalized_string += replacement_char
                replaced = True
                break
        if not replaced:
            normalized_string += char
    return normalized_string


def sluggify(text: str) -> str:
    """
    Take an input string and return a "sluggified" version

    Example:

    >>> slug = sluggify('Pokémon Yellow!')
    >>> print(slug)
    >>> pokemon-yellow

    Args:
        text (str): the string to sluggify

    Returns:
        str: the sluggified string
    """
    # replace slashes and spaces with dashes '-'
    slug = sub('[\\/ ]+', '-', text)
    # replace all accent characters with their 'normal' equivalent
    slug = _replace_accents(slug)
    # remove all non-alphanumeric characters
    slug = sub('[^A-Za-z0-9-]+', '', slug)
    # replace multiple consecutive dashes with single dash
    slug = sub('-+', '-', slug)
    # remove leading dashes
    slug = sub('^-+', '', slug)
    # remove trailing dashes
    slug = sub('-+$', '', slug)
    slug = slug.lower()
    return slug


if __name__ == '__main__':
    assert sluggify('Pokémon Yellow!') == 'pokemon-yellow'
