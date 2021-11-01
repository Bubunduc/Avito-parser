# I split into 2 files because I mean this is do my code more readable
from Avito_parse3 import parse
import xlsxwriter
from time import sleep
import random
url = 'https://www.avito.ru/voronezhskaya_oblast/avtomobili?cd=1'
class Xls_writer(parse):#we inherit the class from Avito_parse3

    def __init__(self,url):
        super(Xls_writer, self).__init__(url)# we take url
        self.parsed = parse(url)
        self.max_page = parse.max_pages(self)
        self.all_pages = []
        self.url = self.check_url(url)
        
    def check_url(self,url):#url must have a flag that denotes the page, in this function we check for its presence
        if '&p' not in url:
            url +='&p=1'
            return url
        else:
            return url
    def find_p(self,url):#with this function, we extract the digit after p
        self.url = str(url)
        self.url = self.url.split('p=')
        self.url = self.url[1]
        try:
            self.url = int(self.url)
            return self.url
        except:
            self.url = self.url.split('&')
            self.url = self.url[0]
            self.url = int(url)
            return self.url
    def parser_1(self):
        self.url = self.check_url(url)
        self.workbook = xlsxwriter.Workbook('Parsed.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write('A1', "Название")
        self.worksheet.write('B1', "Цена")
        self.worksheet.write('C1', 'Ссылка')
        self.begin = 2
        for i in range(1,self.max_page+1):

            self.url = self.url.replace(f'p={self.find_p(self.url)}',f'p={i}')
            print(f'page {i}')
            self.parsed = parse(self.url)
            self.parsed = self.parsed.price_list()
            for j,(item,cost,link) in enumerate(self.parsed,start=self.begin):
                self.worksheet.write(f'A{j}',item )
                self.worksheet.write(f'B{j}',cost )
                self.worksheet.write(f'C{j}', link)
            self.begin +=len(self.parsed)



            sleep(random.randint(1, 4))
        self.workbook.close()



write =Xls_writer(url)
write.parser_1()

    #all_pages.append(parsed.price_list())

#pprint(all_pages)

