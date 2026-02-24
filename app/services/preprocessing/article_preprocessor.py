
from app.schema.preprocess import Article, Preprocess_object, PreprocessingError

import re



def clean_text_livemint(text: str) -> str:
    """
    Cleans LiveMint articles by removing inline references, author emails,
    image placeholders, promos, city/state prefixes, and agency credits.
    """
    patterns = [
        r'^\(.*?(per IST|Chart \d+).*\)$',       # Full-line chart/date
        r'^Write to .*?@.*$',                    # Author emails
        r'^View Full Image$',                     # Image placeholders
        r'^Photo:.*$',                            # Photo credits
        r'^(Also Read\s*\||Follow updates here\s*:)$',  # Promos
        r'^\(PTI\)$',                             # Agency credits
        r'^[A-Z][a-z]+ \([A-Za-z]+\):$',         # City/state prefixes
        r'Also Read\s*\|',                        # Inline promos
        r'Follow updates here\s*:',               # Inline promos
        r'\(Chart \d+\)',                         # Inline chart
        r'\(.*?per IST.*?\)',                     # Inline IST
        r'\(PTI\)',                               # Inline agency
    ]
    regex = re.compile("|".join(patterns), flags=re.IGNORECASE)

    cleaned = []
    for line in text.splitlines():
        line = line.strip()
        if line and not regex.match(line):
            cleaned.append(line)

    text = " ".join(cleaned)
    text = re.sub(r'[^\x00-\x7F\'"‘’“”]', '', text)  # strip weird chars
    text = re.sub(r'\s+', ' ', text).strip()        # collapse whitespace
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text




def clean_text_india_today(text: str) -> str:
    """
    Cleans India Today articles by removing:
    - Promotional messages
    - Social media references
    - PTI or similar agency inputs
    - Caption blocks
    - Non-ASCII characters
    """
    pattern = re.compile(
        r'To support our brand.*|'
        r'Keep following Inside Northeast.*|'
        r'\s\S*(http|https|\.com|\.in|\.org|\.gov|twitter)\S*|'
        r'Support Inside Northeast.*|'
        r'Readers like you make Inside Northeast\’s work possible\.|'
        r'\s*Download\: The Inside Northeast app HERE.*|'
        r'\s*Do keep following us for news on\-the\-go.*|'
        r'Follow us on Facebook|'
        r'\(With inputs from \w+\)|'
        r'\[caption .*?\]|\[/caption\]',
        re.IGNORECASE | re.DOTALL
    )

    text = pattern.sub('', text)  # Remove matches
    text = re.sub(r'[^\x00-\x7F\'"‘’“”]', '', text)  # Strip weird chars
    text = re.sub(r'\s+', ' ', text).strip()         # Collapse whitespace
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)

    return text



def clean_text_ht(text: str) -> str:
    """
    Cleans Hindustan Times articles by removing:
    - Promotional messages and subscription prompts
    - Photo credits and agency inputs (PTI, AFP, Getty, etc.)
    - Social media links
    - Wire feed disclaimers
    - Non-ASCII characters
    """
    pattern = re.compile(
        r'Subscribe Now\!.*|click here.*?\.|'
        r'To access comprehensive details about weather.*|'
        r'\(([^)]*(source|picture|File|Illustration|photo|pti)[^)]*)\)|'
        r'\(This story has been published from.*?\)|'
        r'\s\S*(http|https|\.com|\.in|\.org|\.gov|twitter)\S*|'
        r'Follow us on Facebook|'
        r'The views expressed are personal.*|'
        r'With inputs from \w+|'
        r'\((?:\w+\s)*inputs(?:\s\w+)*.*?\)',
        re.IGNORECASE | re.DOTALL
    )

    text = pattern.sub('', text)                     # Remove matches
    text = re.sub(r'[^\x00-\x7F\'"‘’“”]', '', text)  # Strip non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()        # Collapse whitespace
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text




def clean_text_et(text: str) -> str:
    """
    Cleans Economic Times articles by removing:
    - Non-ASCII characters
    - Photo/data/disclaimer/PTI credits
    - URLs and social media links
    - Promotional messages and subscription prompts
    """
    pattern = re.compile(
        r"[^\x00-\x7F'‘’“”]|"
        r'\(([^)]*(source|picture|File|Illustration|photo|data|disclaimer|pti)[^)]*)\)|'
        r'\s\S*(http|https|\.com|\.in|\.org|\.gov|twitter)\S*|'
        r'Live Events|You can now subscribe to our.*?|You Might Also Like|Economic Times WhatsApp channel|ETMarkets WhatsApp channel',
        flags=re.IGNORECASE | re.DOTALL
    )

    text = pattern.sub(' ', text)                  # Remove matches
    text = re.sub(r'\s+', ' ', text).strip()      # Collapse whitespace
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text





def clean_text_moneycontrol(text: str) -> str:
    """
    Cleans Moneycontrol articles by removing:
    - Image/photo/illustration credits
    - Agency signatures (PTI, ANI, RSN, ANU, Reuters)
    - Ads, disclaimers, 'Also Read', 'Read More'
    - Election promos and junk fragments
    - Non-ASCII characters
    """
    # Combined full-line and inline patterns
    patterns = [
        r'^\s*\(.*?(Image credit|Image:|Illustration|Photo credit|File image|With PTI inputs|With Reuters inputs|Image source).*?\)\s*$',
        r'^For all commodities report, click here Disclaimer:.*',
        r'^Disclaimer:.*Moneycontrol\.com advises.*',
        r'^Story continues below Advertisement Remove Ad$',
        r'^(Also Read\s*\||ALSO READ:)$',
        r'^\s*Read More\s*$',
        r'^Catch the latest news, views and analysis.*$',
        r'^(Photo credit:.*|File image:.*)$',
        r'\(Image (credit|source).*?\)',
        r'\(Illustration.*?\)',
        r'\(File image.*?\)',
        r'\(Photo credit.*?\)',
        r'Story continues below Advertisement Remove Ad',
        r'Also Read\s*\|',
        r'ALSO READ:',
        r'Read More\s*$',
        r'\b(PTI|ANI|RSN|ANU|Reuters)\b',
    ]
    regex = re.compile("|".join(patterns), flags=re.IGNORECASE | re.DOTALL)

    text = regex.sub('', text)                       # Remove matches
    text = re.sub(r'[^\x00-\x7F\'"‘’“”]', '', text)  # Strip non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()        # Collapse whitespace
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text






def clean_text_ie(text: str, patterns=None) -> str:
    """
    Cleans Indian Express articles by removing:
    - Parentheses containing keywords (source, photo, picture, pti, etc.)
    - URLs, newsletter fragments, story continuation phrases
    - PTI inputs, watch patterns with dates
    - Non-ASCII characters (except standard quotes)
    - Repetitive subscription/join channel messages
    """
    if patterns is None:
        patterns = [
            r'\(([^)]*(source|picture|File|click here|Illustration|photo|pti)[^)]*)\)',
            r'\s\S*(http|\.com|\.in|\.org|\.gov|twitter)\S*',
            r'Story continues below this ad|Click here to read this article in \w+|Get Express Premium.*|Subscribe Now|CLICK HERE FOR MORE \w+ NEWS|Limited Time Offer|Click here to join our channel|Click here to subscribe|Express Premium with ad|lite for just Rs 2|Follow Express Pune.*|Stay updated with the latest Pune news|You can also join our Express Pune Telegram channel here|Also Read|Newsletter|Click to get the day\x19s best explainers in your inbox',
            r'\(?(With\s+(inputs\s+from\s+)?PTI\s+inputs|PTI)\)?',
            r'#watch.*?\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}',
            r'= Limited Time Offer \| Express Premium with ad-lite for just Rs 2/ day =I< Click here to subscribe =',
            r'[^\x00-\x7F\'"‘’“”]'
        ]

    combined_pattern = '|'.join(f'(?:{p})' for p in patterns)
    text = re.sub(combined_pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text




def clean_text_ndtv(text: str) -> str:
    """
    Cleans NDTV articles by removing:
    - Syndication/legal disclaimers
    - ANI/PTI/Reuters credits
    - Twitter/WhatsApp promo links
    - Hindi greetings/non-article lines
    - Ad placeholders and stray artifacts
    - Non-ASCII characters (except quotes)
    """
    patterns = [
        r'^\s*pic\.twitter\.com/\S+\s*$',
        r'^\(This story has not been edited by NDTV staff.*\)$',
        r'^\(Except for the headline.*syndicated feed.*\)$',
        r'^\(With inputs? from (ANI|PTI|Reuters).*\)$',
        r'^\s*With input from agencies.*$',
        r'^Disclaimer: NDTV has been sued.*$',
        r'^NDTV is now available on WhatsApp channels.*$',
        r'Click on the link to get all the latest updates.*$',
        r'^(PTI|COR|HDA|ANI)\b.*$',
        r'^[\u0900-\u097F\s।]+$',
        r'^Story continues below Advertisement Remove Ad$',
        r'pic\.twitter\.com/\S+',  # inline
        r'Story continues below Advertisement Remove Ad',
        r'\(With inputs? from (ANI|PTI|Reuters).*?\)',
        r'[^\x00-\x7F\'"‘’“”]',   # non-ASCII
        r'\s—\s',                  # isolated em dash
    ]
    combined_regex = re.compile("|".join(patterns), flags=re.IGNORECASE | re.DOTALL)
    text = combined_regex.sub(' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text






def clean_text_op(text: str) -> str:
    """
    Cleans OpIndia articles by removing:
    - Emoticons and non-ASCII junk
    - Syndicated feed disclaimers
    - Photo, illustration, and PTI credits
    - URLs and social media links
    - Newsletter/promotional fragments
    - Date-specific #watch patterns
    """
    patterns = [
        r"[^\x00-\x7F'‘’“”]",
        r'Subscribe Now! Get features like|click here.*?\.|To access comprehensive details about weather.*',
        r'This news report is published from .*?',
        r'The complete press statement can be read below',
        r'\(([^)]*(source|picture|File|click here|Illustration|photo|pti)[^)]*)\)',
        r'#watch.*?\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}',
        r'\(This story has been published from.*?\)',
        r'\s\S*(http|https|\.com|\.in|\.org|\.gov|twitter)\S*',
        r'Follow us on Facebook',
        r'The views expressed are personal.*',
        r'With inputs from \w+',
        r'\((?:\w+\s)*inputs(?:\s\w+)*.*?\)',
    ]

    combined_regex = re.compile("|".join(patterns), flags=re.IGNORECASE | re.DOTALL)
    text = combined_regex.sub(' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text






def _normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces and remove leading bullets/dashes."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[•\-\–\—]\s*", "", text)
    text = re.sub(r'(?<=[a-z])([.!?])([A-Z])', r'\1 \2', text)
    return text

# ---------- Scroll.in cleaner ----------
def clean_text_scroll(text: str) -> str:
    """
    Clean Scroll.in article text by removing:
    - Membership/donation prompts
    - In-article CTAs
    - Agency credits (PTI, ANI, Reuters, AFP, AP)
    - Parenthetical references to Scroll.in
    """
    patterns = [
        r"\(.*?Scroll\.in.*?\)",
        r"(?:Support\s+Scroll|Contribute\s+now)[^.?!]*",
        r"(?:Also\s+Read|Read\s+more|Read|Watch|WATCH|Subscribe|Sign\s+up|Join\s+our\s+Telegram|Follow\s+us\s+on|Download\s+the\s+app)[:\s][^.?!]*",
        r"\(?(?:with\s+inputs\s+from\s+)?(?:PTI|ANI|Reuters|AFP|AP)\)?|—\s*(?:PTI|ANI|Reuters|AFP|AP)\b"
    ]
    combined = re.compile("|".join(f"(?:{p})" for p in patterns), flags=re.IGNORECASE | re.DOTALL)
    text = combined.sub(' ', text)
    text = re.sub(r"(?:\s*[–—-]\s*){2,}", " — ", text)
    text = re.sub(r"\(\s*\)|\[\s*\]", "", text)
    return _normalize_whitespace(text)

# ---------- The Quint cleaner ----------
def clean_text_quint(text: str) -> str:
    """
    Clean The Quint article text by removing:
    - App download prompts
    - Follow/subscribe CTAs
    - Hashtag blocks
    - Agency credits
    """
    patterns = [
        r"(?:Subscribe\s+to|Follow\s+The\s+Quint|Download\s+The\s+Quint\s+app)[^.?!]*",
        r"#[A-Za-z0-9_]+(?:\s#[A-Za-z0-9_]+)*",
        r"(?:Also\s+Read|Read\s+more|Read|Watch|WATCH|Subscribe|Sign\s+up|Join\s+our\s+Telegram|Follow\s+us\s+on|Download\s+the\s+app)[:\s][^.?!]*",
        r"\(?(?:with\s+inputs\s+from\s+)?(?:PTI|ANI|Reuters|AFP|AP)\)?|—\s*(?:PTI|ANI|Reuters|AFP|AP)\b"
    ]
    combined = re.compile("|".join(f"(?:{p})" for p in patterns), flags=re.IGNORECASE | re.DOTALL)
    text = combined.sub(' ', text)
    text = re.sub(r"(?:\s*[–—-]\s*){2,}", " — ", text)
    text = re.sub(r"\(\s*\)|\[\s*\]", "", text)
    return _normalize_whitespace(text)

# ---------- NDLI cleaner ----------
def clean_text_ndli(text: str) -> str:
    """
    Clean NDLI (ndl.iitkgp.ac.in) article text by removing:
    - Library metadata (Source, Publisher, Collection, Handle, Identifier, ISSN, DOI)
    - “Read full story” / visit original / more details prompts
    - NDLI brackets and parenthetical notes
    - URLs
    """
    patterns = [
        r"(?:Source|Publisher|Collection|Handle|Identifier|ISSN|DOI)\s*:\s*[^.\n]*",
        r"(?:Read\s+full\s+story|Visit\s+original|For\s+more\s+details)\s*[:\-]?\s*[^.\n]*",
        r"\[[^\]]*NDLI[^\]]*\]",
        r"\(NDLI.*?\)",
        r"\s\S*(?:https?://|www\.|\.com|\.in|\.org|\.net|\.gov|twitter|facebook|instagram|youtube|t\.co|bit\.ly)\S*"
    ]
    combined = re.compile("|".join(f"(?:{p})" for p in patterns), flags=re.IGNORECASE | re.DOTALL)
    text = combined.sub(' ', text)
    text = re.sub(r"(?:\s*[–—-]\s*){2,}", " — ", text)
    text = re.sub(r"\(\s*\)|\[\s*\]", "", text)
    return _normalize_whitespace(text)



#  change these values by trial of scraper api

preprocessors={
    'mint': clean_text_livemint, 
    'India Today': clean_text_india_today, 
    'India Today NE': clean_text_india_today,
    'Hindustan Times': clean_text_ht,
    'The Economic Times': clean_text_et, 
    'Moneycontrol': clean_text_moneycontrol,
    'The Indian Express': clean_text_ie, 
    'ndtv.com': clean_text_ndtv, 
    'OpIndia': clean_text_op,
    'Scroll.in':clean_text_scroll,
    'TheQuint':clean_text_quint,
    'ndl.iitkgp.ac.in': clean_text_ndli
}


ERROR_CODES = {
    "UNKNOWN_SOURCE": 1001,
    "PREPROCESSING_FAILED": 1002,
    "EMPTY_CONTENT": 1003,
}

def apply_preprocessing(data: Preprocess_object) -> Article:
    try:
        content = data.content
        source = data.source

        if not content or not content.strip():
            raise PreprocessingError(
                ERROR_CODES["EMPTY_CONTENT"],
                "Content is empty or invalid"
            )

        if source not in preprocessors:
            raise PreprocessingError(
                ERROR_CODES["UNKNOWN_SOURCE"],
                f"No preprocessor registered for source '{source}'"
            )

        processed_content = preprocessors[source](content)

        return Article(
            title=data.title,
            content=processed_content,
            url=data.url,
            source=source,
            error_code=200,
            error_message=f"preprocessed successfully using {source} preprocessor"
        )

    except PreprocessingError as e:
        return Article(
            title=data.title,
            content=data.content or "",
            url=data.url,
            source=data.source,
            error_code=e.error_code,
            error_message=e.message
        )

    except Exception as e:
        return Article(
            title=data.title,
            content=data.content or "",
            url=data.url,
            source=data.source,
            error_code=ERROR_CODES["INTERNAL_ERROR"],
            error_message=str(e)
        )
