from peewee import *

db = SqliteDatabase('sneakershop11.db')


class Base(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class User(Base):
    name = CharField()
    surname = CharField()
    city = CharField()
    telephone = CharField(unique=True)
    email = CharField(unique=True)

    class Meta:
        db_table = 'users'


class Customer(Base):
    user_id = ForeignKeyField(User)

    class Meta:
        db_table = 'customers'


class Order(Base):
    customer_id = ForeignKeyField(Customer)

    class Meta:
        db_table = 'order'


class Product(Base):
    model = CharField(unique=True)
    price = FloatField()
    description = TextField(unique=True)

    class Meta:
        db_table = 'products'


class Size(Base):
    us_size = CharField(unique=True)

    class Meta:
        db_table = 'sizes'


class OrderItem(Base):
    order_id = ForeignKeyField(Order)
    product_id = ForeignKeyField(Product)
    size_id = ForeignKeyField(Size)
    quantity = IntegerField()
    price = FloatField()

    class Meta:
        db_table = 'order_items'


class ProductSize(Model):
    product_id = ForeignKeyField(Product)
    size_id = ForeignKeyField(Size)

    class Meta:
        database = db
        db_table = 'product_sizes'
