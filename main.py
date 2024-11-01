from parser_products import get_products
import xlwt


def main():
    prods = get_products()

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = False

    style0 = xlwt.XFStyle()
    style0.font = font0

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Каталог товаров')

    ws.write(0, 0, "Категория")
    ws.write(0, 1, "Артикул")
    ws.write(0, 2, "Бренд")
    ws.write(0, 3, "Наименование товара")
    ws.write(0, 4, "Цена")
    ws.write(0, 5, "Описание")
    ws.write(0, 6, "Ссылки на изображения через запятую")

    row = 1
    for cat in prods:
        for product in cat["prods"]:
            ws.write(row, 0, cat["category"])
            ws.write(row, 1, product["art"])
            ws.write(row, 2, product["brand"])
            ws.write(row, 3, product["name_product"])
            ws.write(row, 4, product["price"])
            ws.write(row, 5, product["preview"])
            ws.write(row, 6, product["images"])
            row += 1

    wb.save('product_catalog.xls')


main()
