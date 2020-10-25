import requests
import lxml.html as html
import os
import datetime

HOME_URL='https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//h2/a[contains(@href, "larepublica.co") and @href!="https://www.larepublica.co/"][not(contains(@href, "/inside/video/"))]/@href'
XPATH_TITLE = '//div[contains(@class,continer)]/div[@class="mb-auto"]/text-fill/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/descendant-or-self::*/text()'


def parse_notice(link,today):
    """
    docstring
    """
    try:
        response= requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8') # devuelve el html de la respuesta decode ayuda a convertir algo legible para el lenguaje
            parsed = html.fromstring(notice) #toma el html y lo tranfoma en un documeto para hacer xphat
            
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace("\'","")
                summary= parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt','w', encoding='utf-8') as f: #with manejador contextual de Python
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n\n')

        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response= requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8') # devuelve el html de la respuesta decode ayuda a convertir algo legible para el lenguaje
            parsed = html.fromstring(home) #toma el html y lo tranfoma en un documeto para hacer xphat
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notice)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notice:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()


