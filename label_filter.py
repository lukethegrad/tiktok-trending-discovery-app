import re

# List of known labels, companies, or phrases indicating a song is likely signed
EXCLUDED_LABEL_KEYWORDS = [
    "Sony", "Universal", "Warner", "UMG", "T-Series", "Virgin", "Som Livre",
    "WM Brazil", "SM", "RCA", "BIGHIT", "Republic", "Epic", "Interscope",
    "under exclusive license", "Taylor Swift", "Netflix", "Coldplay",
    "Think its a game", "broke", "Copar", "Double P Records", "Jonzing World",
    "CDLand", "Geffen records", "Big hit", "BMG", "Spinnin", "Reprise",
    "Believe", "Because", "Empire", "Family Tree", "Native",
    "Hot Girl Productions", "tommy boy", "LaFace", "Capitol", "Zee music",
    "super cassettes", "Manorama", "Five Star Audio", "Plasma records",
    "muzik 247", "times music", "bayshore", "think music", "sun pictures",
    "all ways dance", "artiste first", "mom+pop", "zomba", "saregama",
    "polydor", "domino recordings", "def jam", "island", "3qtr",
    "aditya music", "tips industries", "concord", "10k projects",
    "Mass Appeal", "black 17 media", "oto8", "Atlantic", "WM",
    "Robots & Humans", "TDE", "Columbia"
]

# Precompile regex for performance
EXCLUDED_PATTERNS = [re.compile(re.escape(term), re.IGNORECASE) for term in EXCLUDED_LABEL_KEYWORDS]

def is_signed_label(label_text: str) -> bool:
    """Returns True if the label string contains any excluded terms."""
    if not label_text:
        return False  # Treat empty/None labels as unsigned
    return any(p.search(label_text) for p in EXCLUDED_PATTERNS)
