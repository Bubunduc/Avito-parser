# I split into 2 files because I mean this is do my code more readable
from Avito_parse3 import parse
import xlsxwriter
from time import sleep
import sys
from os.path import exists


class Xls_writer(parse):  # we inherit the class from Avito_parse3

    def __init__(self, url):
        super(Xls_writer, self).__init__(url)  # we take url
        self.parsed = parse(url)
        self.max_page = parse.max_pages(self)
        self.all_pages = []
        self.url = self.check_url(url)

    def check_url(self, url):  # url must have a flag that denotes the page, in this function we check for its presence
        if '?p' in url:
            return url
        else:
            if '&p' not in url:
                url += '&p=1'
                return url
            else:
                return url

    def find_cd(self, url):
        if 'cd' in url:
            return url
        else:
            return url + '?cd=1'

    def find_p(self, url):  # with this function, we extract the digit after p
        self.url = str(url)
        self.url = self.url.split('p=')
        self.url = self.url[1]
        try:
            self.url = int(self.url)
            return self.url
        except:
            self.url = self.url.split('&')
            self.url = self.url[0]
            self.url = int(self.url)
            return self.url

    def find_s(self, url):  # with this function, we extract the digit after s
        self.url = str(url)
        self.url = self.url.split('s=')
        self.url = self.url[1]
        try:
            self.url = int(self.url)
            return self.url
        except:
            self.url = self.url.split('&')
            self.url = self.url[0]
            self.url = int(self.url)
            return self.url

    def check_s(self, url, index):
        self.url = url
        if '&s=' not in self.url:
            return self.url + f'&s={index}'
        else:
            self.s = self.find_s(url)
            self.s = str(self.s)
            self.url = self.url.replace(f'&s{self.s}', f'&s{index}')
            return self.url

    def page(self):
        print(f'Максимальное количество страниц {self.parsed.max_pages()}')
        self.pages = int(
            input('Напишите, сколько страниц спарсить, или напишите 0, тогда по умолчанию спарсятся все страницы : '))
        print()
        while self.pages > self.parsed.max_pages():
            print('Нельзя спарсить страниц больше, чем на сайте')
            print()
            self.page()

        if self.pages == 0:
            self.pages = self.parsed.max_pages()
        else:
            self.pages = self.pages
        return self.pages

    def parser_1(self):
        self.url = self.find_cd(self.url)
        self.url = self.check_url(self.url)
        if exists('parsed.xlsx') == False:
            self.workbook = xlsxwriter.Workbook('parsed.xlsx')
        else:
            self.name = 'parsed'
            self.count = 0
            namer ='0'
            while exists(namer) == True:
                self.count += 1
                namer = f'{self.name}_{self.count}.xlsx'
            self.workbook = xlsxwriter.Workbook(f'{namer}')

        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write('A1', "Название")
        self.worksheet.write('B1', "Цена")
        self.worksheet.write('C1', 'Ссылка')
        self.begin = 2
        self.pages = self.page()
        for i in range(1, self.pages + 1):

            self.url = self.url.replace(f'p={self.find_p(self.url)}', f'p={i}')
            print(f'Загрузка, страниц записано : {i}')
            self.parsed = parse(self.url)
            self.parsed = self.parsed.price_list()
            del self.parsed[7:10]
            del self.parsed[7:10]

            try:
                for j, (item, cost, link) in enumerate(self.parsed, start=self.begin):
                    self.worksheet.write(f'A{j}', item)
                    self.worksheet.write(f'B{j}', cost)
                    self.worksheet.write(f'C{j}', link)
            except:
                continue
            self.begin += len(self.parsed)

            sleep(5)
        self.workbook.close()
        print('Загрузка успешно завершена')


class Call_Menager(Xls_writer):
    def page(self):
        super().page()

    def sorter(self):

        print('Введите Ссылку:')
        self.url = input()
        print()
        self.parser = Xls_writer(self.url)
        print('Напишите вид сортировки, можно написать вид буквами или цифрами')
        print()
        self.categories = ['никак', 'дешевле', 'дороже', "самые новые"]
        print("Напишите /help, чтобы узнать возможные виды сортировки")
        print()
        print('Напишите /exit, для того, для того чтобы закрыть программу')
        print()
        self.text = input('Что делаем ?: ')
        if self.text == '/help':
            self.count = 0
            for i in self.categories:
                print()
                self.count += 1
                print(f'{self.count} - {i}')

            self.text = input('Что делаем ?: ')
        if self.text.lower() == self.categories[0] or self.text.lower() == '1':
            Xls_writer.parser_1(self)

        if self.text.lower() == self.categories[1] or self.text.lower() == '2':
            self.url = self.check_s(self.url, 1)
            self.parser = Xls_writer(self.url)
            self.parser.parser_1()

        if self.text.lower() == self.categories[2] or self.text.lower() == '3':
            self.url = self.check_s(self.url, 2)
            self.parser = Xls_writer(self.url)
            self.parser.parser_1()

        if self.text.lower() == self.categories[3] or self.text.lower() == '4':
            self.url = self.check_s(self.url, 104)
            self.parser = Xls_writer(self.url)
            self.parser.parser_1()

        if self.text.lower() == '/exit':
            sys.exit()
        print()
        input('Введите что угодно, чтобы закрыть программу: ')


url = 'https://www.avito.ru/voronezhskaya_oblast/avtomobili/audi-ASgBAgICAUTgtg3elyg?cd=1'
pp = Call_Menager(url)
pp.sorter()
