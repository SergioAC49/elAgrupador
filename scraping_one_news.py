import argparse
from utils.scrapers import *
from utils.elasticsearch_connector import save_news, print_all_news


def get_scraper(newspaper, url):
    scraper_switcher = {
        "elperiodico": ElPeriodicoScraper,
        "lavanguardia": LaVanguardiaScraper,
        "elpais": ElPaisScraper,
        "elmundo": ElMundoScraper,
        "abc": ABCScraper,
        "eldiario": ElDiarioScraper, 
        "okdiario": OkDiarioScraper, 
        "publico": PublicoScraper
    }
    Scraper = scraper_switcher.get(newspaper)
    return Scraper(url)


if __name__ == '__main__':
    """
    Call the script as: 
    python3 scraping_one_news.py --url {url} --newspaper {newspaper}
    
    Example URLs:
    'elperiodico': https://www.elperiodico.com/es/sanidad/20200706/la-incidencia-del-virus-en-segria-es-20-veces-mayor-que-en-catalunya-8028249
    'lavanguardia': https://www.lavanguardia.com/politica/20200707/482180289185/reyes-catalunya-figueres-barcelona-murcia.html
    'elpais': https://elpais.com/espana/madrid/2020-07-07/madrid-recurre-la-resolucion-del-ministerio-de-sanidad-sobre-los-controles-en-barajas-hay-que-exigir-test-en-origen-48-horas-antes-de-viajar.html
    'elmundo': https://www.elmundo.es/espana/2020/07/07/5f0452b9fc6c83977f8b462a.html
    'abc': https://www.abc.es/tecnologia/moviles/aplicaciones/abci-estados-unidos-extiende-lucha-contra-china-estudia-resringir-tiktok-y-otras-aplicaciones-chinas-202007071235_noticia.html#vca=rrss&vmc=abc-es&vso=tw&vli=cm-general&_tcode=ZTN2MnUx
    'eldiario': https://www.eldiario.es/politica/iglesias-asegura-comparte-sanchez-estrategia-negociadora-presupuestos_1_6087609.html
    'okdiario': https://okdiario.com/espana/podemos-admite-primera-vez-perdidas-debacles-electorales-2-648-097-2019-5968444
    'publico': https://www.publico.es/espana/prevision-meteorologica-temperaturas-bajan-gran-parte-espana-15-provincias-estaran-aviso-calor-8-tormentas-consulta-prevision-comunidad.html
    """
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="url of the news")
    parser.add_argument("--newspaper", required=True, help="name of the newspaper")

    args = parser.parse_args()
    newspaper = args.newspaper.lower()
    url = args.url

    # Get scraper and save data
    scraper = get_scraper(newspaper, url)
    res = save_news(scraper)
    # print(res)

    # Print all the news saved in elasticsearch (to check if we have saved them)
    print_all_news()
