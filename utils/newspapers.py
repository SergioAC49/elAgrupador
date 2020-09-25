from utils.scrapers import *

newspapers = {
    "elperiodico": {"name": "El Periodico", "scrapper": ElPeriodicoScraper, "baseURL": "elperiodico.com", "twitterID": "198829810"},
    "lavanguardia": {"name": "La Vanguardia", "scrapper": LaVanguardiaScraper, "baseURL": "lavanguardia.com", "twitterID": "74453123"},
    "elpais": {"name": "El Pais", "scrapper": ElPaisScraper, "baseURL": "elpais.com", "twitterID": "7996082"},
    "elmundo": {"name": "El Mundo", "scrapper": ElMundoScraper, "baseURL": "elmundo.es", "twitterID": "14436030"},
    "abc": {"name": "ABC", "scrapper": ABCScraper, "baseURL": "abc.es", "twitterID": "19923515"}, 
    "eldiario": {"name": "eldiario.es", "scrapper": ElDiarioScraper, "baseURL": "eldiario.es", "twitterID": "535707261"},
    "okdiario": {"name": "okdiario", "scrapper": OkDiarioScraper, "baseURL": "okdiario.com", "twitterID": "3439292716"}, 
    "publico": {"name": "Publico", "scrapper": PublicoScraper, "baseURL": "publico.es", "twitterID": "17676713"}, 
    "test": {"name": "Test", "scrapper": ElDiarioScraper, "baseURL": "eldiario.es", "twitterID": "1305141713619619841"}
}


def get_newspaper_by_twitterID(id):
    for n in newspapers:
        if newspapers[n]['twitterID'] == id:
            return n
