from bs4 import BeautifulSoup
import requests
import urllib.parse
import json



class OlxApi():
    def __init__(self, page_limit, url=None):
        self.headers    = {'user-agent': 'retrobid/0.0.2'}
        self.list_ads = []
        self.tag = 'OlX'
        self.page_limit = page_limit
        self.url = url
        

    def _url(self, product, page=None):
        if self.url:
            return self.url
        if page:
            url = f"https://www.olx.com.br/brasil?o={page}&q={urllib.parse.quote(product.encode('utf-8'))}"
        else:
            url = f"https://www.olx.com.br/brasil?q={urllib.parse.quote(product.encode('utf-8'))}"
        return url


    def _to_html(self, html):
        return BeautifulSoup(html, 'lxml')
    
    def _content_parser(self, content):
        count = 0
        try:
            c = json.loads(content.find('script', attrs={'id': '__NEXT_DATA__'}).text)
            cards = c.get('props').get('pageProps').get('ads')
            print("anuncions para filtrar = ",len(cards))

        except AttributeError as e:
            print("Error na Pagina ", e)
            print(c)
            print(count)
            self.error = True

        for count, c in enumerate(cards):
                # print(f"item {count + 1} de {len(cards)}")
                ad = {}
                ad["thumbnail"]= c.get('thumbnail')
                ad["id"]= c.get('listId')
                ad["title"]= c.get('title')
                ad["price"]= c.get('price')
                ad["permalink"]= c.get('url')
                self.list_ads.append(ad)            

    def request(self, url):
        r = requests.get(url, headers=self.headers)
        return self._to_html(r.text)


    def _get_max_pages(self, product):
        url = self._url(product, page=1)
        print("URL",url)
        r = self.request(url)
        if r:
            try:
                content = r.find("p", {"class":"olx-text olx-text--body-small olx-text--block olx-text--regular olx-color-neutral-110"}).text
                max_ads = int(content.split()[4].replace(".",""))
                max_pag = int(max_ads/49) + (1 if (max_ads % 49) > 0 else 0)
                print("Total Anuncions :",max_ads)
                print("total paginas :",max_pag)
                return max_pag
            except AttributeError as e:
                print(f"erro ao buscar o total de paginas: {e}")
                return 0

    def get_list_product(self, product):
        last_page = self._get_max_pages(product)
        print("======= lista de Anuncios ======== ")
        page = 1
        while (page <= last_page and page <= self.page_limit):
            print("craling page: ",page)
            url = self._url(product, page)
            content = self.request(url)
            self._content_parser(content)
            page += 1
        print("======= FIM Procura ======== ")
        return self.list_ads
    
    @staticmethod
    def run(product, page_limit=1):
        olx_client = OlxApi(page_limit)
        olx_client.get_list_product(product)
        return olx_client.list_ads
    

          

