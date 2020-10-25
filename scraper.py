import requests
import lxml.html as html

HOME_URL='https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//h2/a[contains(@href, "larepublica.co") and @href!="https://www.larepublica.co/"][not(contains(@href, "/inside/video/"))]/@href'
XPATH_TITLE = '//div[contains(@class,continer)]/div[@class="mb-auto"]/h2/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/descendant-or-self::*/text()'


def parse_home():
    try:
        response= requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8') # devuelve el html de la respuesta decode ayuda a convertir algo legible para el lenguaje
            parsed = html.fromstring(home) #toma el html y lo tranfoma en un documeto para hacer xphat
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notice)
        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()


