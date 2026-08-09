import re
import unicodedata


# =====================================================
# Nepali Stopwords
# =====================================================

NEPALI_STOPWORDS = {
    "छ", "छन्", "थियो", "थिए", "हो", "हुन्", "भएको",
    "गरेको", "गर्ने", "गर्नु", "र", "पनि", "तर",
    "यो", "त्यो", "यी", "ती", "जुन", "कि", "भने",
    "जस्तो", "लागि", "बारे", "साथ", "देखि", "सम्म",
    "मा", "को", "का", "की", "ले", "लाई", "बाट",
    "हुँदा", "गर्दै", "भन्ने", "उनी", "उनले",
    "उनको", "हामी", "तिमी", "म", "मेरो", "हाम्रो",
    "उक्त", "एक", "दुई", "थप", "यस", "यसको"
}


# =====================================================
# Regular Expressions
# =====================================================

# URL removal
URL_RE = re.compile(
    r"https?://\S+|www\.\S+",
    re.UNICODE
)


# Email removal
EMAIL_RE = re.compile(
    r"\S+@\S+"
)


# HTML tag removal
HTML_RE = re.compile(
    r"<.*?>"
)


# Keep:
# - Nepali Unicode characters
# - Nepali combining marks
# - English letters
# - Numbers
# - Spaces
# - Common punctuation

INVALID_CHAR_RE = re.compile(
    r"[^\u0900-\u097F\u200C\u200D"
    r"a-zA-Z0-9\s"
    r"।,!?()%:/\-]"
)


# Multiple spaces
MULTISPACE_RE = re.compile(
    r"\s+"
)



# =====================================================
# Text Cleaning Function
# =====================================================

def clean_text(text, remove_stopwords=True):

    if text is None:
        return ""


    text = str(text)


    # Unicode normalization
    text = unicodedata.normalize(
        "NFC",
        text
    )


    # Lowercase English
    text = text.lower()


    # Remove URLs
    text = URL_RE.sub(
        " ",
        text
    )


    # Remove emails
    text = EMAIL_RE.sub(
        " ",
        text
    )


    # Remove HTML
    text = HTML_RE.sub(
        " ",
        text
    )


    # Remove unwanted characters
    text = INVALID_CHAR_RE.sub(
        " ",
        text
    )


    # Normalize spaces
    text = MULTISPACE_RE.sub(
        " ",
        text
    ).strip()



    # Remove stopwords
    if remove_stopwords:

        words = []

        for word in text.split():

            if word not in NEPALI_STOPWORDS:
                words.append(word)


        text = " ".join(words)



    return text