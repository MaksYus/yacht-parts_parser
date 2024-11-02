import requests
from bs4 import BeautifulSoup


def get_index_digit_in_str(string: str) -> int:
    """
    Индекс первого вхождения цифры в строку
    """
    index = 0
    for i in string:
        if i.isdigit():
            return index
        index += 1
    return -1


def get_categories(path: str, products: list) -> None:
    """
    Получаем список всех категорий на сайте и ссылки на страницы этих категорий
    """
    req = requests.get(path+"/catalog/")
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    categories_ = soup.findAll('ul', class_='clearfix')
    for category in categories_:
        category_name = ""
        for cat in category.contents:
            if cat.text != "\n":
                if "name" in cat.attrs["class"]:
                    category_name = cat.text[1:len(cat.text)-1]
                else:
                    for item in cat.contents:
                        if item.text != "\n":
                            if item.text == "Оборудование Osculati": continue
                            category_text = category_name+" - " + item.text  # category name
                            products.append(
                                {"category": category_text, "href": item.contents[0].attrs['href']})


def get_products_hrefs(path: str, product: dict) -> None:
    """
    получаем наименования товаров и ссылки на их страницы
    """
    new_req = requests.get(path+product["href"], {"PAGEN_1": 1})
    new_soup = BeautifulSoup(new_req.text, 'lxml')
    items = new_soup.findAll(class_="item-title")
    another_pages_hrefs_raw = new_soup.find(class_="nums")
    last_page_num = 1
    if another_pages_hrefs_raw is not None: last_page_num = int(another_pages_hrefs_raw.contents[len(
        another_pages_hrefs_raw.contents)-2].text)
    product["prods"] = []

    for i in range(2, last_page_num+2):
        for item in items:
            product["prods"].append(
                {"name_product": item.text.replace('\n', ''), "href": item.contents[1].attrs["href"]})
        new_req = requests.get(path+product["href"], {"PAGEN_1": i})
        new_soup = BeautifulSoup(new_req.text, 'lxml')
        items = new_soup.findAll(class_="item-title")


def get_products_info(path: str, product: dict) -> None:
    """
    Получаем всю остальную нужную информацию о продукте
    """
    req = requests.get(path+product["href"])
    soup = BeautifulSoup(req.text, 'lxml')

    product["art"]= ""
    product["art"] = soup.find(
        class_="article iblock").find(class_="value").text
    
    # есть другие кнопки, влияющие на цену
    product["price"] = ""
    price_raw_1 = soup.find(class_="middle_info wrap_md").find(
        class_="price")
    if price_raw_1 is not None: # может быть пустым
        price_raw = price_raw_1.text
        product["price"] = price_raw[get_index_digit_in_str(
            price_raw):price_raw.find(".")+1:]

    product["preview"] = ""
    preview_rav = soup.find(class_="preview_text")
    if preview_rav is not None: product["preview"] = preview_rav.text

    images_text = ""
    main_image_src = soup.findAll('img')[1].attrs["src"]
    all_imgs = soup.findAll('img')  # тут нет следующих изображений
    images_text += main_image_src
    product["images"] = images_text
    # остальные изображения подгружаются позже, пока нет идей как можно их получить

    product["brand"] = ""
    brand_href_block = soup.find(class_="brand iblock")
    if brand_href_block is not None:
        brand_href = brand_href_block.find(class_="brand_picture").attrs["href"]
        if brand_href is not None:
            beand_req = requests.get(path+brand_href)
            brand_soup = BeautifulSoup(beand_req.text, 'lxml')
            product["brand"] = brand_soup.find('h1', {"id": "pagetitle"}).text


def get_products() -> list:
    """
    Парсим сайт https://yacht-parts.ru и получаем товары с информацией о них
    """
    path = "https://yacht-parts.ru"
    products = []

    get_categories(path, products)

    for item in products:
        get_products_hrefs(path, item)

    for cat in products:
        for product in cat["prods"]:
            get_products_info(path, product)

    return products

def get_products_from_category(bum) -> dict:
    path = "https://yacht-parts.ru"
    products = []
    # get_categories(path, products)
    test_prods_1 = {
        "category":bum,
        "prods":[
            {
                "art":"sdf art",
                "brand":"v brand",
                "name_product":"sdf name_product",
                "price":" zxcv price",
                "preview":"v preview",
                "images":"vs images"
            }
        ]
    }
    return test_prods_1