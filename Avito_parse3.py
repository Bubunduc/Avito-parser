from bs4 import BeautifulSoup
import requests
from sys import exit

class parse():
    def __init__(self, url): # we take url outside class
        super().__init__()

        self.new_url(url)

    def new_url(self, url):# this funtion parse this url and take HTML

        self.Html = requests.get(url)
        self.Html = self.Html.text
        self.Html = BeautifulSoup(self.Html, "html.parser")#We need use "html.parser" if we need use bs4

        self.Url = self.Html.find_all(
            'a', rel='noopener', target='_blank',
            class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes')

    def get_price_and_name(self, html_doc, index):#main function, we process all lots on page

        self.information = str(html_doc[index])#We transform bs4 format to str() and work with HTML fragment as usuall string.
        self.information = self.information.split('<')
        self.all_info = []
        self.name = self.information[12]
        self.name = self.name.split('itemprop="name">')
        self.name = self.name[-1]
        self.all_info.append(self.name)

        self.price = self.information[20]
        self.price = self.price.split('"')
        self.price = self.price[1]
        if self.price == '...':
            self.price = 'Цена не указана'
        else:
            self.price = self.price
            self.all_info.append(self.price)

            self.url = self.information[11]
            self.url = self.url.split('"')
            self.url = 'https://www.avito.ru' + self.url[5]
            self.all_info.append(self.url)

        return self.all_info

    def price_list(self, url=None):
        if url:
            self.new_url(url)
        self.Row_list = self.Html.find_all('div', class_='iva-item-body-R_Q9c')
        self.Row_list = list(self.Row_list)# we find out quantity of lost
        self.list_with_all_lots = []
        for index in range(0, len(self.Row_list)):
            try:
                self.sorted_list = self.get_price_and_name(self.Row_list, 0)

                del self.Row_list[0]

                #self.lot = f'Имя: {self.sorted_list[0]}   Цена: {self.sorted_list[1]}, Ссылка:  {self.sorted_list[2]}'#We list from format Title Price Link
                self.lot = self.sorted_list

                self.list_with_all_lots.append(self.lot)

            except IndexError:
                continue
        return self.list_with_all_lots

    def max_pages(self):#This function needs only for parse ALL pages on site
        try:
            max_page = self.Html.find_all('span', class_='pagination-item-JJq_j')
            max_page = list(max_page)
            max_page = max_page[-2]
            max_page = str(max_page)
            max_page = max_page.split('"')
            max_page = max_page[-1]
            max_page = max_page.replace('</span>', '')
            max_page = max_page[1:]
            return int(max_page)
        except:
            print('Not correct link,you must have pages to do this, try again')
            exit()
