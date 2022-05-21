from mms.orders import Order
from mms.product import Product
from mms.business import Business
from mms.users import User


Product.all_products.load()
Business.all_businesses.load()
User.all_users.load()

Order.all_orders.load()