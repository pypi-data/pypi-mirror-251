"""
--------------------------------
The abstract_collector module
--------------------------------
This module defines the main_paragraph function.

"""


from urllib import request

import bs4
    


def main_paragraph(url: str):
    """From a web page, return the paragraph with the biggest length.

    Args:
        url (str): the url of the web page to treat.
    """
    html = request.urlopen(url)
    soup = bs4.BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    res=''
    for paragraph in paragraphs:
        text=paragraph.text
        text=" ".join(text.split())
        if len(text)>len(res):
            res=text
    return res


