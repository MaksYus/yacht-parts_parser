import requests
from bs4 import BeautifulSoup

def get_categories(soup: BeautifulSoup,products: list) -> None:
    categories_ = soup.findAll('ul', class_='clearfix')
    for category in categories_:
        category_name = ""
        for cat in category.contents:
            if cat.text != "\n":
                if "name" in cat.attrs["class"]:
                    category_name = cat.text[1:len(cat.text)-2]
                else:
                    for item in cat.contents:
                        if item.text != "\n":
                            category_text = category_name+" - " + item.text  # category name
                            products.append({"category" : category_text, "href" : item.contents[0].attrs['href']})

def get_products_hrefs(path:str, product:dict) -> None:
    i = 1
    new_req = requests.get(path+product["href"],{"PAGEN_1":i})
    new_soup = BeautifulSoup(new_req.text, 'lxml')
    items = new_soup.findAll(class_="item-title")
    another_pages_hrefs_raw = new_soup.find(class_ = "nums")
    last_page_num = int(another_pages_hrefs_raw.contents[len(another_pages_hrefs_raw.contents)-2].text)
    product["prods"] = []

    for i in range(2,last_page_num+2):
        for item in items:
            product["prods"].append({"name_product":item.text, "href":item.contents[1].attrs["href"]})
        new_req = requests.get(path+product["href"],{"PAGEN_1":i})
        new_soup = BeautifulSoup(new_req.text, 'lxml')
        items = new_soup.findAll(class_="item-title")

def main():
    path = "https://yacht-parts.ru"
    req = requests.get(path+"/catalog/")
    src = req.text
    products = []
    soup = BeautifulSoup(src, 'lxml')

    get_categories(soup,products)
    
    for item in products:
        get_products_hrefs(path,item)
    
main()
