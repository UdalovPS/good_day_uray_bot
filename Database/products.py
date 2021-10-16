from posgre_sql import Product

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

shaurma_1 = [1, 'Шаурма №1', 'Курица', 150]
shaurma_2 = (2, 'Шаурма №2', 'Свинина', 160)
shaurma_3 = (3, 'Шаурма №3', 'Говядина', 170)

if __name__ == '__main__':
    add = Products(*shaurma_3)
    add.insert_products()
