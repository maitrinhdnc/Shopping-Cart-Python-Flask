from app.main.model.cart import Cart
from app.main.model.cart_item import CartItem
from app.main.model.order import Order
from app.main.model.order_item import OrderItem
from app.main.model.product import Product
from app.main.service.auth_helper import Auth

from typing import Dict
from app.main import db
from flask import request
import uuid

def add_cart(data: Dict[str, str]):
    user_id = Auth.get_userId_from_token(request)
    product = Product.query.filter_by(product_id=data.get("product_id")).first()

    if user_id:
        cart_data = Cart.query.filter_by(userId = user_id).first()
        if cart_data:
            if not product:
                return {"message":"Product not found"}, 400
            else:
                cart_item=CartItem.query.filter_by(cart_id=cart_data.cart_id,
                product_id=data.get("product_id")).first()
                if cart_item:
                    if data.get("quantity") > 0:
                        cart_item.quantity += data.get("quantity")
                        subtotal_ex_tax = cart_item.quantity * product.price
                        cart_item.subtotal_ex_tax = subtotal_ex_tax
                        tax_total = subtotal_ex_tax * 0.1
                        cart_item.tax_total = tax_total
                        cart_item.total = subtotal_ex_tax + tax_total
                        db.session.commit()
                        cal_cart(user_id)
                        save_changes(cart_data)
                    else:
                        return {"message":"Quantity must be greater than 0"}, 403
                else:
                    add_cart_item(data, cart_data, product)
                    cal_cart(user_id)
                    save_changes(cart_data)
        else:
            new_cart = Cart()
            new_cart.userId = user_id
            new_cart.cart_id = str(uuid.uuid4())
            save_changes(new_cart)     
            add_cart_item(data, new_cart, product)
            cal_cart(user_id)
            save_changes(new_cart)     
        return resp_data(user_id)
    else:   
        return {"message":"Bad request!!!"}, 403

def add_cart_item(data: Dict[str, str], cart, product):
    new_cart_item=CartItem()
    new_cart_item.cart_id = cart.cart_id
    new_cart_item.product_id=data.get("product_id")
    new_cart_item.quantity=data.get("quantity")
    new_cart_item.subtotal_ex_tax=int(data.get("quantity"))*product.price
    new_cart_item.tax_total= int(data.get("quantity"))*product.price * 0.1   
    new_cart_item.total = new_cart_item.tax_total + new_cart_item.subtotal_ex_tax
    return save_changes(new_cart_item)

def change_quantity_cart_item(cart_item_id, data: Dict[str, str]):
    user_id = Auth.get_userId_from_token(request)
    if user_id:
        cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id).first()
        if cart_item:
            product = Product.query.filter_by(product_id=cart_item.product_id).first()
            if not product:
                return {"message":"Product not found"}, 403
            else:
                # calculate values for cart-item
                cart_item.quantity = int(data.get("quantity"))
                if cart_item.quantity > 0:
                    sub_total = cart_item.quantity * product.price
                    cart_item.subtotal_ex_tax = sub_total
                    tax_total = (sub_total*10)/100
                    cart_item.tax_total = tax_total
                    cart_item.total = sub_total + tax_total
                    db.session.commit()
                    cal_cart(user_id)
                    return resp_data(user_id)
                else:
                    return {"message":"Quantity must be greater than 0"}, 403
        else:
            return {"message":"Cart item not found"}, 403
    else:
        return {"message":"Bad request!!!"}, 403


def delete_cart_item(cart_item_id):
    user_id = Auth.get_userId_from_token(request)
    if user_id:
        cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id).first()
        if cart_item:
            product = Product.query.filter_by(product_id=cart_item.product_id).first()
            if not product:
                return {"message":"Product not found"}, 403
            else:
                db.session.delete(cart_item)
                db.session.commit()
                cal_cart(user_id)
                return resp_data(user_id)
        else:
            return {"message":"Cart item not found"}, 403
    else:
        return {"message":"Bad request!!!"}, 403

def checkout_cart():
    user_id = Auth.get_userId_from_token(request)
    if user_id:
        cart = Cart.query.filter_by(userId = user_id).first()
        if cart:
            cart_items = CartItem.query.filter_by(cart_id = cart.cart_id).all()
            if len(cart_items) == 0:
                return {"message":"No cart item in cart. Cannot check out"}, 200 
            else:
                order = Order()
                order.order_id = str(uuid.uuid4())
                order.user_id = user_id
                order.payment_status = 'INIT'
                order.subtotal_ex_tax = cart.subtotal_ex_tax
                order.tax_total = cart.tax_total
                order.total = cart.total 
                save_changes(order)

                for item in cart_items:
                    order_item = OrderItem()
                    order_item.order_item_id = str(uuid.uuid4())
                    order_item.order_id = order.order_id
                    order_item.product_id = item.product_id
                    order_item.quantity = item.quantity
                    order_item.subtotal_ex_tax = item.subtotal_ex_tax
                    order_item.tax_total = item.tax_total
                    order_item.total = item.total
                    save_changes(order_item)
                db.session.delete(cart)
                db.session.commit()
                return resp_checkout(user_id)
        else:
            return {"message":"Cart not found"}, 403 
    else:
        return {"message":"Bad request!!!"}, 403

def resp_data(user_id):
    cart = Cart.query.filter_by(userId = user_id).first()
    cart_items = CartItem.query.filter_by(cart_id = cart.cart_id).all()
    
    obj = {
        'cart_id' : cart.cart_id,
        'userId' : cart.userId,
        'cart_items': None,
        'subtotal_ex_tax': 0,
        'tax_total': 0,
        'total': 0
        }
    lst_cart_items = []
    for data in cart_items:
        obj_item = {
            'cart_item_id': data.cart_item_id,
            'product_id': data.product_id,
            'quantity': data.quantity,
            'subtotal_ex_tax': data.subtotal_ex_tax,
            'tax_total': data.tax_total,
            'total': data.total
        }
        lst_cart_items.append(obj_item)
    obj['cart_items'] = lst_cart_items
    obj['subtotal_ex_tax'] = sum (data.subtotal_ex_tax for data in cart.cart_items)
    obj['tax_total'] = sum (data.tax_total for data in cart.cart_items)
    obj['total'] = sum (data.total for data in cart.cart_items)
    return obj

def resp_checkout(user_id):
    order = Order.query.filter_by(user_id = user_id).all()
    if len(order) > 1:
        order = order[-1]
        order_items = OrderItem.query.filter_by(order_id = order.order_id).all()

    else:
        order = order[0]
        order_items = OrderItem.query.filter_by(order_id = order.order_id).all()

    obj = {
        'order_id' : order.order_id,
        'userId' : order.user_id,
        'order_items': None,
        'subtotal_ex_tax': 0,
        'tax_total': 0,
        'total': 0
        }
    lst_order_items = []
    for data in order_items:
        obj_item = {
            'order_item_id': data.order_item_id,
            'product_id': data.product_id,
            'quantity': data.quantity,
            'subtotal_ex_tax': data.subtotal_ex_tax,
            'tax_total': data.tax_total,
            'total': data.total
        }
        lst_order_items.append(obj_item)
    obj['order_items'] = lst_order_items
    obj['subtotal_ex_tax'] = sum (data.subtotal_ex_tax for data in order.order_items)
    obj['tax_total'] = sum (data.tax_total for data in order.order_items)
    obj['total'] = sum (data.total for data in order.order_items)
    return obj

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def cal_cart(user_id):
    cart = Cart.query.filter_by(userId=user_id).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    cart.subtotal_ex_tax = sum(row.subtotal_ex_tax for row in cart_items)
    cart.tax_total = sum(row.tax_total for row in cart_items)
    cart.total = sum(row.total for row in cart_items)
    db.session.commit()