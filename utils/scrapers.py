import datetime
import locale
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from utils.news_vectorizer import *


class NewspaperScraper:

    def __init__(self, url, newspaper):
        """
        Read the URL and create the BeutifulSoup object
        :param url: URL of the news
        """
        self.url = url
        self.newspaper = newspaper
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        req = Request(url, headers=headers)
        page = urlopen(req)
        self.soup = BeautifulSoup(page, 'html.parser')

    def get_title(self):
        """
        :return: String containing the title
        """
        raise Exception("Not Implemented")

    def get_subtitles(self):
        """
        :return: List of strings with all the subtitles
        """
        raise Exception("Not Implemented")

    def get_text(self):
        """
        :return: String with all the text
        """
        raise Exception("Not Implemented")

    def get_authors(self):
        """
        :return: List of strings with all the author
        """
        raise Exception("Not Implemented")

    def get_date(self):
        """
        :return: Datetime of publication date
        """
        raise Exception("Not Implemented")

    def get_picture_url(self):
        """
        :return: String containing the picture url
        """
        raise Exception("Not Implemented")

    def get_elasticsearch_dict(self, model):
        """
        :return: Dictionary containing 'title', 'subtitles', 'text', 'authors' and 'date'
        """
        title = self.get_title()
        title_vector = title_to_vector(title, model)
        d = {
            'newspaper': self.newspaper,
            'title': title,
            'subtitles': self.get_subtitles(),
            'text': self.get_text(),
            'authors': self.get_authors(),
            'date': self.get_date().strftime("%Y-%m-%dT%H:%M:%S"),
            'vector': title_vector,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'picture_url': self.get_picture_url()
        }
        return d


class ElPeriodicoScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "ElPeriodico")

    def get_title(self):
        return self.soup.find("h1", "title").get_text()

    def get_subtitles(self):
        try:
            s = self.soup.find("div", "subtitle").find_all("h2")
            subtitles = [h2.get_text() for h2 in s]
        except:
            subtitles = []
        return subtitles

    def get_text(self):
        all_p = self.soup.find("div", "ep-detail-body").find_all("p")

        filtered_p = []
        for p in all_p:
            # Get all <p> that are text (not titles and subtitles)
            if not (p.has_attr("class") and ("subtitle" in p['class'] or "title" in p['class'])):
                filtered_p.append(p.get_text())

        return "\n".join(filtered_p)

    def get_authors(self):
        try:
            authors = [self.soup.find("span", "author-link").get_text()]
        except:
            try:
                authors = [self.soup.find("a", "author-link").get_text()]
            except:
                authors = []
        return authors

    def get_date(self):
        try:
            str_date = self.soup.find("span", "dateModified").get_text()
            date = datetime.datetime.strptime(str_date, "%d/%m/%Y - %H:%M")
        except:
            str_date = self.soup.find("time", "date")['datetime']
            try:
                date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S%z")
            except:
                date = datetime.datetime.strptime(str_date, "%d/%m/%Y - %H:%M %Z")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url


class LaVanguardiaScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "LaVanguardia")

    def get_title(self):
        return self.soup.find("h1", "d-title__txt").get_text()

    def get_subtitles(self):
        subtitles = self.soup.find("div", "d-subtitle__list").find_all("h2")
        return [h2.get_text() for h2 in subtitles]

    def get_text(self):
        all_p = self.soup.find("div", "story-leaf-txt-p").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        try:
            authors = [self.soup.find("a", "d-signature__name").find("span").get_text()]
        except:
            authors = [self.soup.find("span", "d-signature__name").get_text()]
        return authors

    def get_date(self):
        str_date = self.soup.find("time", "d-signature__time")['datetime']
        date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S%z")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url


class ElPaisScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "ElPais")

    def get_title(self):
        return self.soup.find("h1", "a_t").get_text()

    def get_subtitles(self):
        subtitle = self.soup.find("h2", "a_st").get_text()
        return [subtitle]

    def get_text(self):
        all_p = self.soup.find("div", "a_b").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        all_a = self.soup.find_all("a", "a_aut_n")
        authors = [a.get_text() for a in all_a]
        return authors

    def get_date(self):
        str_date = self.soup.find("a", "a_ti").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        try:
            date = datetime.datetime.strptime(str_date[:6] + "." + str_date[6:], "%d %b %Y - %H:%M %Z")
        except:
            try:
                date = datetime.datetime.strptime(str_date, "%d %b %Y - %H:%M %Z")
            except:
                date = datetime.datetime.now()
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url


class ElMundoScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "ElMundo")

    def get_title(self):
        return self.soup.find("h1", "ue-c-article__headline").get_text()

    def get_subtitles(self):
        subtitle = self.soup.find("p", "ue-c-article__standfirst").get_text()
        return [subtitle]

    def get_text(self):
        all_p = self.soup.find("div", "ue-c-article__body").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        all_a = self.soup.find_all("div", "ue-c-article__byline-name")
        authors = [a.get_text() for a in all_a]
        return authors

    def get_date(self):
        str_date = self.soup.find("div", "ue-c-article__publishdate").find("time")['datetime']
        date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url


class ABCScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "ABC")

    def get_title(self):
        return self.soup.find("span", "titular").get_text()

    def get_subtitles(self):
        subtitle = self.soup.find("h2", "subtitulo").get_text()
        return [subtitle]

    def get_text(self):
        all_p = self.soup.find("span", "cuerpo-texto").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        try:
            all_a = self.soup.find("footer", "autores").find_all("a", "nombre")
            authors = [a.get_text() for a in all_a]
        except:
            authors = []
        return authors

    def get_date(self):
        str_date = self.soup.find("span", "fecha").find("time")['datetime']
        date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url


class ElDiarioScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "ElDiario")

    def get_title(self):
        return self.soup.find("h1", "title").get_text()

    def get_subtitles(self):
        all_li = self.soup.find("div", "news-header").find_all("li")
        return [li.get_text() for li in all_li]

    def get_text(self):
        all_p = self.soup.find_all("p", "article-text")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        try:
            all_a = self.soup.find("p", "authors").find_all("a")
            authors = [a.get_text() for a in all_a]
        except:
            try:
                authors = self.soup.find("div", "author-pill-wrapper").find("div", "featured-data").get_text()
            except:
                authors = []
        return authors

    def get_date(self):
        str_date = self.soup.find("footer", "news-date").find("div", "date").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d de %B de %Y - %H:%M h")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url

    
class LaRazonScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "LaRazon")

    def get_title(self):
        return self.soup.find("h1").find("span").get_text()

    def get_subtitles(self):
        return self.soup.find("h2").find("span").get_text()

    def get_text(self):
        all_p = self.soup.find("section").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        return self.soup.find("div", "byline__credits-container").find("a").get_text()

    def get_date(self):
        str_date = self.soup.find("div", "byline__last-update").find("span", "font--primary byline__date").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d-%m-%Y | %H:%M H")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url

    
class VeinteMinutosScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "20minutos")

    def get_title(self):
        return self.soup.find("h1","notice-title").get_text()

    def get_subtitles(self):
        all_li = self.soup.find("div", "article-intro").find_all("li")
        li_text = [li.get_text() for li in all_li]
        return "\n".join(li_text)

    def get_text(self):
        all_p = self.soup.find("div","article-text").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        return self.soup.find("span", "article-author").get_text()

    def get_date(self):
        str_date = self.soup.find("span", "article-date").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d.%m.%Y - %H:%Mh")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url

    
class OkDiarioScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "OkDiario")

    def get_title(self):
        return self.soup.find("h1","entry-title").get_text()

    def get_subtitles(self):
        try:
            subtitles = self.soup.find("div", "subtitles").find("h2").get_text()
        except:
            subtitles = []
        return subtitles

    def get_text(self):
        all_p = self.soup.find("div","entry-content").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        return self.soup.find("li", "author-name").get_text()

    def get_date(self):
        str_date = self.soup.find("time", "date").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d/%m/%Y %H:%M")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url

    
class PublicoScraper(NewspaperScraper):

    def __init__(self, url):
        super().__init__(url, "Publico")

    def get_title(self):
        return self.soup.find("h1").get_text()

    def get_subtitles(self):
        try:
            return [self.soup.find("div", "article-header-epigraph col-12").find("h2").get_text()]
        except:
            return []

    def get_text(self):
        all_p = self.soup.find("div","article-text").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        try:
            authors = [self.soup.find("li", "author-name").get_text()]
        except:
            try:
                authors = [self.soup.find("footer", "article-info").find("p", "signature").get_text()]
            except:
                authors = []
        return authors

    def get_date(self):
        str_date = self.soup.find("header", "article-published-info").find("span","published").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d/%m/%Y %H:%M")
        return date

    def get_picture_url(self):
        try:
            picture_url = self.soup.find(property="og:image")['content']
        except:
            picture_url = None
        return picture_url
