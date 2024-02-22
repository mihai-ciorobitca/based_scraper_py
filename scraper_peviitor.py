from bs4 import BeautifulSoup
import requests
from lxml import etree
import json
import os
import time

class Scraper:
    """
    O clasă utilizată pentru a realiza scraping web.

    Atribute
    ----------
    url : str
        URL-ul website-ului de pe care se va face scraping-ul.
    soup : obiect BeautifulSoup
        Un obiect care reprezintă codul HTML parsat al website-ului.

    Metode
    -------
    __init__(url: str)
        Inițializează un nou obiect Scraper cu URL-ul dat.
    getSoup()
        Descarcă codul HTML de la URL și creează un obiect BeautifulSoup.
    """

    def __init__(self, url: str = None):
        """
        Inițializează un nou obiect Scraper cu URL-ul dat.

        Parametri
        ----------
        url : str, opțional
            URL-ul website-ului de pe care se va face scraping-ul.
        """
        self.session = self.getSession()
        self._url = url
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        self._soup = None  
        self.status_code = None

        if url is not None:
            self.getSoup()  

    def getSession(self):
        """
        Creează o sesiune nouă HTTP pentru a face request-uri.

        Returnează
        ----------
        session : obiect requests.Session
            Sesiunea HTTP.
        """

        session = requests.Session()
        return session
    
    def post(self, *args, **kwargs):
        """
        Creează o sesiune nouă HTTP pentru a face request-uri.
        Parametri
        ----------
        url : str
            URL-ul website-ului de pe care se va face scraping-ul.
        data : dict
            Dicționarul cu datele de trimis.
        json : dict
            Dicționarul cu datele de trimis.

        Returnează
        ----------
        session : obiect requests.Session
            Sesiunea HTTP.
        """

        response = self.session.post(*args ,**kwargs, timeout=10)

        return response
    
    def getSoup(self, **kwargs):
        """
        Descarcă codul HTML de la URL și creează un obiect BeautifulSoup.

        Returnează
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup creat.
        """

        try:
            document = self.session.get(self.url,headers=self.user_agent , **kwargs)
            self.status_code = document.status_code
            self._soup = BeautifulSoup(document.text, "html.parser")
        except Exception as e:
            print(e)  
            return [] 
    
    def getJson(self):
        """
        Descarcă codul HTML de la URL și creează un obiect BeautifulSoup.

        Returnează
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup creat.
        """


        document = self.session.get(self.url,headers=self.user_agent ,timeout=10)
        return document.json()
    

    def getContent(self, **kwargs):
        """
        Descarcă codul HTML de la URL și creează un obiect BeautifulSoup.

        Returnează
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup creat.
        """

        try:
            document = self.session.get(self.url,headers=self.user_agent , **kwargs)
            self.status_code = document.status_code
            self._soup = BeautifulSoup(document.content, "html.parser")
        except Exception as e:
            print(e)  
            return []


    @property
    def url(self):
        """
        Proprietate ce permite obținerea URL-ului obiectului Scraper.

        Returnează
        ----------
        url : str
            URL-ul obiectului Scraper.
        """

        return self._url

    @url.setter
    def url(self, url):
        """
        Proprietate ce permite setarea URL-ului obiectului Scraper.

        Parametri
        ----------
        url : str
            URL-ul de setat.
        """

        self._url = url
        self.getSoup()

    @property
    def soup(self):
        """
        Proprietate ce permite obținerea obiectului BeautifulSoup al obiectului Scraper.

        Returnează
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup al obiectului Scraper.
        """

        return self._soup
    
    @soup.setter
    def soup(self, soup):
        """
        Proprietate ce permite setarea obiectului BeautifulSoup al obiectului Scraper.

        Parametri
        ----------
        soup : obiect BeautifulSoup
            Obiectul BeautifulSoup de setat.
        """

        self._soup = BeautifulSoup(soup, "html.parser")

class Rules:
    def __init__(self, scraper : Scraper):
        """
        Constructorul clasei.
        :param scraper: instanța Scraper utilizată pentru a extrage informații de pe o pagină web
        """
        self.scraper = scraper
    
    def getTags(self,tag : str , attrs : dict = None):
        """
        Returnează toate tagurile care corespund cu criteriile specificate.
        :param tag: tagul pe care se face căutarea
        :param attrs: un dicționar cu atributele tagului căutat (ex. {'class': 'foo', 'id': 'bar'})
        :return: un set de taguri găsite după criteriile de căutare specificate
        """
        self.anchors = self.scraper.soup.find_all(tag, attrs=attrs)
        return set(self.anchors)
    
    def getTag(self,tag : str , attrs : dict = None):
        """
        Returnează primul tag care corespunde cu criteriile specificate.
        :param tag: tagul pe care se face căutarea
        :param attrs: un dicționar cu atributele tagului căutat (ex. {'class': 'foo', 'id': 'bar'})
        :return: primul tag găsit după criteriile de căutare specificate
        """

        self.anchor = self.scraper.soup.find(tag, attrs=attrs)
        return self.anchor
    
    def getXpath(self, xpath : str):
        """
        Returnează elementele care corespund cu expresia XPath specificată.
        :param xpath: expresia XPath utilizată pentru căutare
        :return: o listă de elemente găsite folosind expresia XPath specificată
        """
        dom = etree.HTML(str(self.scraper.soup))
        self.xpath = dom.xpath(xpath)
        return BeautifulSoup(etree.tostring(self.xpath[0]), "html.parser")
    

def loadingData(data : dict, company : str):
    """
    Încarcă datele din fișierul de intrare.
    :return: un dicționar cu datele din fișierul de intrare
    """

    apikey = os.environ.get("APIKEY")
    url_encoded = "application/x-www-form-urlencoded"
    application_json = "application/json"

    for version in [1,4]:
        clean_url = f"https://api.peviitor.ro/v{version}/clean/"
        requests.post(clean_url, headers={"apikey": apikey, "Content-Type": url_encoded}, data={"company": company})

        time.sleep(0.5)
        update_url = f"https://api.peviitor.ro/v{version}/update/"
        requests.post(update_url, headers={"apikey": apikey, "Content-Type": application_json}, data = json.dumps(data))

    data_set_url = f"https://dev.laurentiumarian.ro/dataset/based_scraper_py/{company.lower()}.py/"
    requests.post(data_set_url, headers={"Content-Type": application_json}, data = json.dumps({"data":len(data)}))
