def split_into_sentences(content_list):
    """
    
    GRABBED THIS FUNCTION FROM HERE: https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
    I MODIFIED IT SOMEWHAT.
    
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    all_sentences = []
    # -*- coding: utf-8 -*-
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    
    for text in content_list:
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
        text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences]
        if sentences and not sentences[-1]: sentences = sentences[:-1]
        for sentence in sentences:
            all_sentences.append(sentence)
    return all_sentences


def beaut_soup_grab(url,find_all='div',div_class=""):
    r = requests.get(url, headers={'accept': 'application/json'})
    if r.status_code == 200:
        # Process the response content here
        print(f"Success for {url}")
    else:
        # Log an error for non-success status codes
        print(f"Error: {url} returned status code {r.status_code}")
    output = r.text
    soup = BeautifulSoup(output, 'html.parser')
    if div_class == "":
        divs = soup.find_all(find_all) 
    else:
        divs = soup.find_all(find_all,class_=div_class) 
    return divs

def run_url_scrape(url_list):
    now = datetime.now()
    search_date = now.strftime("%m/%d/%y")

    content_list = []
    for url in url_list:
        try:
            divs = beaut_soup_grab(url)
            # rid the list of divs without user postings by filtering for div's with anonymous 2 or more times
            for div in divs:
                content = div.text
                if content.count("Anonymous") >= 2:
                    if search_date in content:
                        if content in content_list:
                            pass
                        else:
                            content_list.append(content)
        except requests.exceptions.RequestException as e:
            # Handle exceptions raised by requests, e.g., connection error, timeout, etc.
            print(f"Request Exception for {url}: {e}")
        except Exception as e:
            # Handle other unexpected exceptions
            print(f"An unexpected error occurred for {url}: {e}")
            
    return content_list