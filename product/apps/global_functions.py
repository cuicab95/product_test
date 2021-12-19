from ..apps.store.models import ProductProvider, OrderDetail, Order
from django.shortcuts import get_object_or_404


def validate_additional_data(type, data={}):
    is_correct = True
    message = ""
    if type == "CD":
        stock = data.get('stock', None)
        if not stock or stock == "":
            is_correct = False
            message = "Es requerido la propiedad 'stock' en additional_data cuando el tipo de pedido es por centro de distribución"
    if type == "SU":
        reference = data.get('reference', None)
        num_branch_office = data.get('num_branch_office', None)
        if not reference or reference == "":
            is_correct = False
            message = "Es requerido la propiedad 'reference' en additional_data cuando el tipo de pedido es por sucursal"
        if not num_branch_office or num_branch_office == "":
            is_correct = False
            message = "Es requerido la propiedad 'num_branch_office' en additional_data cuando el tipo de pedido es por sucursal"
    if type == "EA":
        reference = data.get('reference', None)
        code_partner = data.get('code_partner', None)
        if not reference or reference == "":
            is_correct = False
            message = "Es requerido la propiedad 'reference' en additional_data cuando el tipo de pedido es por empresa asociada"
        if not code_partner or code_partner == "":
            is_correct = False
            message = "Es requerido la propiedad 'code_partner' en additional_data cuando el tipo de pedido es por empresa asociada"
    return is_correct, message


def validate_structure_order_detail(items=[]):
    is_correct = True
    message = ""
    if len(items) <=0:
        is_correct = False
        message = "Items no puede ser una lista vacía"
    try:
        for item in items:
            product_id = item.get('product_id', None)
            quantity = item.get('quantity', None)
            if not product_id:
                is_correct = False
                message = "Es requerido la propiedad 'product_id' en items"
                break
            if not quantity:
                is_correct = False
                message = "Es requerido la propiedad 'quantity' en items"
                break
    except Exception as e:
        is_correct = False
        message = str(e)
    return is_correct, message


def save_order_detail(order_id, items=[]):
    is_correct = True
    message = ""
    try:
        order_total = 0
        order = get_object_or_404(Order, id=order_id)
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            product = get_object_or_404(ProductProvider, id=product_id)
            order_total += (product.price * int(quantity))
            order_detail = OrderDetail()
            order_detail.order = order
            order_detail.product_provider = product
            order_detail.quantity = int(quantity)
            order_detail.sale_price = product.price
            order_detail.save()

        order.total = order_total
        order.save()
    except Exception as e:
        is_correct = False
        message = str(e)
    return is_correct, message
