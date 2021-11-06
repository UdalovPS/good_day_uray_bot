from posgre_sql import Product, Additional

class Products(Product):
    def __init__(self, product_id, name, description, price):
        super(Products, self).__init__()
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price

    def insert_products(self):
        values = f'{self.product_id, self.name, self.description, self.price}'
        self.insert_data_in_table(self.table_name, self.fields, values)


class AdditionalForProduct(Additional):
    def __init__(self, add_id, name):
        super(AdditionalForProduct, self).__init__()
        self.add_id = add_id
        self.name = name

    def insert_additional_for_product(self):
        values = f"({self.add_id}, '{self.name}')"
        self.insert_data_in_table(self.table_name, self.fields, values)

shaurma_1 = [1, 'Шаурма №1', 'Лаваш, куриное филе, огурцы, '
                             'помидоры, капуска пекинская, перец болгакрский', 150]
shaurma_2 = (2, 'Шаурма №2', 'Лаваш, куриное филе, огурцы, '
                             'помидоры, морковь по-корейски, сыр Моцарелла', 160)
shaurma_3 = (3, 'Шаурма №3', 'Лаваш, свинина, огурцы, '
                             'помидоры, морковь по-корейски, капуска пекинская', 170)
shaurma_4 = (4, 'Шаурма №4', 'Лаваш, свинина, огурцы, '
                             'помидоры, морковь по-корейски, капуска пекинскаяб '
                             'перец боглаский, шампиньоны', 180)
shaurma_5_1 = (51, 'Шаурма №5/1', 'Лаваш, курица, огурцы маринованные, '
                                  'сыр, помидор, капуста, морковь', 160)
shaurma_5_2 = (52, 'Шаурма №5/2', 'Лаваш, свинина, огурцы маринованные, '
                                  'сыр, помидор, капуста, морковь', 170)
shaurma_6 = (6, 'Шаурма №6 вегетерианская', 'Лаваш, шампиньоны жаренные, '
                                            'помидоры, капуста,''морковь, '
                                            'перец болгаский', 160)
shaurma_7 = (7, 'Шаурма №7 с говядиной', 'Лаваш, говядина, огурец,'
                                         'морковь, сыр, помидоры, капуста', 250)
shaurma_8 = (8, 'Шаурма №8', 'йогурт, фрукты', 170)
shaurma_9 = (9, 'Шаурма №9 три мяса', 'Лаваш, свинина/говядина/курица, '
                                      'огурец, морковь, сыр, помидоры, капуста', 220)

sauses = ((1, 'Соус чесночный'), (2, 'Соус томатный'), (3, 'Соус турецкий (острый)'), (4, 'Кетчуп-майонез'))


if __name__ == '__main__':
    # add = Products(*shaurma_9)
    # add.insert_products()
    for sause in sauses:
        list_add = AdditionalForProduct(*sause)
        list_add.insert_additional_for_product()
