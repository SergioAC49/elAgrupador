import datetime
import locale
import requests

from bs4 import BeautifulSoup


class NewspaperScraper:

    def __init__(self, url):
        """
        Read the URL and create the BeutifulSoup object
        :param url: URL of the news
        """
        self.url = url
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        req = requests.get(url, headers)
        self.soup = BeautifulSoup(req.content, 'html.parser')

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

    def get_elasticsearch_dict(self):
        """
        :return: Dictionary containing 'title', 'subtitles', 'text', 'authors' and 'date'
        """
        d = {
            'title': self.get_title(),
            'subtitles': self.get_subtitles(),
            'text': self.get_text(),
            'authors': self.get_authors(),
            'date': self.get_date().strftime("%Y-%m-%dT%H:%M:%S")
        }
        return d


class ElPeriodicoScraper(NewspaperScraper):

    def get_title(self):
        return self.soup.find("h1", "title").get_text()

    def get_subtitles(self):
        subtitles = self.soup.find("div", "subtitle").find_all("h2")
        return [h2.get_text() for h2 in subtitles]

    def get_text(self):
        all_p = self.soup.find("div", "ep-detail-body").find_all("p")

        filtered_p = []
        for p in all_p:
            # Get all <p> that are text (not titles and subtitles)
            if not (p.has_attr("class") and ("subtitle" in p['class'] or "title" in p['class'])):
                filtered_p.append(p.get_text())

        return "\n".join(filtered_p)

    def get_authors(self):
        return [self.soup.find("span", "author-link").get_text()]

    def get_date(self):
        str_date = self.soup.find("span", "dateModified").get_text()
        date = datetime.datetime.strptime(str_date, "%d/%m/%Y - %H:%M")
        return date


class LaVanguardiaScraper(NewspaperScraper):

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
        return [self.soup.find("a", "d-signature__name").find("span").get_text()]

    def get_date(self):
        str_date = self.soup.find("time", "d-signature__time")['datetime']
        date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S%z")
        return date


class ElPaisScraper(NewspaperScraper):

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
        date = datetime.datetime.strptime(str_date[:6] + "." + str_date[6:], "%d %b %Y - %H:%M %Z")
        return date


class ElMundoScraper(NewspaperScraper):

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


class ABCScraper(NewspaperScraper):

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
        all_a = self.soup.find("footer", "autores").find_all("a", "nombre")
        authors = [a.get_text() for a in all_a]
        return authors

    def get_date(self):
        str_date = self.soup.find("span", "fecha").find("time")['datetime']
        date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ")
        return date


class ElDiarioScraper(NewspaperScraper):

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
        all_a = self.soup.find("p", "authors").find_all("a")
        authors = [a.get_text() for a in all_a]
        return authors

    def get_date(self):
        str_date = self.soup.find("footer", "news-date").find("div", "date").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d de %B de %Y - %H:%M h")
        return date
    
class LaRazonScraper(NewspaperScraper):

    def get_title(self):
        return self.soup.find("h1").find("span").get_text()

    def get_subtitles(self):
        return = self.soup.find("h2").find("span").get_text()

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
    
class VeinteminutosScraper(NewspaperScraper):

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
    
class OkdiarioScraper(NewspaperScraper):

    def get_title(self):
        return self.soup.find("h1","entry-title").get_text()

    def get_subtitles(self):
        return self.soup.find("div", "subtitles").find("h2").get_text()

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
    
class PublicoScraper(NewspaperScraper):

    def get_title(self):
        return self.soup.find("div","title").find("a").get_text()

    def get_subtitles(self):
        return self.soup.find("div", "article-header-epigraph col-12").find("h2").get_text()

    def get_text(self):
        all_p = self.soup.find("div","article-text").find_all("p")
        p_text = [p.get_text() for p in all_p]
        return "\n".join(p_text)

    def get_authors(self):
        return self.soup.find("li", "author-name").get_text()

    def get_date(self):
        str_date = self.soup.find("header", "article-published-info").find("span","published").get_text()
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        date = datetime.datetime.strptime(str_date, "%d/%m/%Y %H:%M")
        return date
