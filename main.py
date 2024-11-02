from parser_products import get_products_from_category
import openpyxl


def remove_all_sheets(path: str) -> None:
    wb = openpyxl.load_workbook(filename=path,)
    print(wb.sheetnames)
    for sheet_name in wb.sheetnames:
        wb.remove(wb[sheet_name])
    wb.create_sheet(str(1))
    wb.save(path)


def write_cat(path: str, num: int) -> None:
    prods = get_products_from_category(num)
    wb = openpyxl.load_workbook(filename=path,)
    ws = wb.create_sheet(str(prods["category"]))

    ws.cell(row=1, column=1).value = "Категория"
    ws.cell(row=1, column=2).value = "Артикул"
    ws.cell(row=1, column=3).value = "Бренд"
    ws.cell(row=1, column=4).value = "Наименование товара"
    ws.cell(row=1, column=5).value = "Цена"
    ws.cell(row=1, column=6).value = "Описание"
    ws.cell(row=1, column=7).value = "Ссылки на изображения через запятую"

    row = 2
    for product in prods["prods"]:
        ws.cell(row=row, column=1).value = prods["category"]
        ws.cell(row=row, column=2).value = product["art"]
        ws.cell(row=row, column=3).value = product["brand"]
        ws.cell(row=row, column=4).value = product["name_product"]
        ws.cell(row=row, column=5).value = product["price"]
        ws.cell(row=row, column=6).value = product["preview"]
        ws.cell(row=row, column=7).value = product["images"]
        row += 1

    wb.save(path)


def main():
    # prods = get_products()

    path = 'product_catalog.xlsx'

    remove_all_sheets(path)

    # write_cat(path,123)
    # write_cat(path,456)

    # get_style()

    # wb = xlwt.Workbook()
    # ws = wb.add_sheet('Каталог товаров')

    # ws.write(0, 0, "Категория")
    # ws.write(0, 1, "Артикул")
    # ws.write(0, 2, "Бренд")
    # ws.write(0, 3, "Наименование товара")
    # ws.write(0, 4, "Цена")
    # ws.write(0, 5, "Описание")
    # ws.write(0, 6, "Ссылки на изображения через запятую")

    # row = 1
    # for cat in prods:
    #     for product in cat["prods"]:
    #         ws.write(row, 0, cat["category"])
    #         ws.write(row, 1, product["art"])
    #         ws.write(row, 2, product["brand"])
    #         ws.write(row, 3, product["name_product"])
    #         ws.write(row, 4, product["price"])
    #         ws.write(row, 5, product["preview"])
    #         ws.write(row, 6, product["images"])
    #         row += 1

    # wb.save('product_catalog.xls')


main()
