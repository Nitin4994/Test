
from scoopn.Ecom_app.models import *
from scoopn.Ecom_app.login_controller import *
from scoopn.Ecom_app.registrationcontroller import *
from scoopn.Ecom_app.registrationcontroller_admin import *
from scoopn.Ecom_app.product_controller import *
from scoopn.Ecom_app.inventory_controller import *
from scoopn.Ecom_app.user_dashbord_controller import *
from scoopn.Ecom_app.user_products_controller import *
from scoopn.Ecom_app.user_order_controller import *
from scoopn.Ecom_app.user_purchase_controller import *
from scoopn.Ecom_app.vendor_account_controller import *
from scoopn.Ecom_app.user_transactions_controller import *
from scoopn.Ecom_app.vend_transactions_controller import *

if __name__ == '__main__':
    app.run(debug=True)