from flask import request, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.extensions import socketio
from backend.models.Item import Item
from backend.models.Size import Size
from backend.models.Modifier import Modifier 
from backend.models.ItemDetails import ItemDetails
from backend.models.Order import Order
from backend.models.OrderDetails import OrderDetails
from backend.models.OrderDetailModifier import  OrderDetailModifier
from backend.utils.OrderExtraction import extract_order  # NLP Order Parsing
# from flask_socketio import emit

class OrderResource(Resource):
    @jwt_required()
    def post(self):
        # socketio = current_app.extensions.get("socketio")  # ✅ Get socketio from extensions
        # if not socketio:
        #     return {"error": "SocketIO not initialized"}, 500

        """Place a new order based on extracted NLP data."""
        data = request.json
        order_text = data.get("order_text")
        customer_name = data.get("customer_name","N/A")
        customer_mobile = data.get("customer_mobile","N/A")

        if not order_text:
            return {"error": "Order text is required"}, 400

        # Step 1: Extract items, sizes, and modifiers using NLP
        extracted_order, invalid_words, size_missing = extract_order(order_text)
        print(f"Extracted Order: {extracted_order}")
        if not extracted_order:
            return {"error": "Could not process order"}, 400
        


        if len(invalid_words) > 0 or len(size_missing) > 0:
            return {"invalid_words":invalid_words, "size_missing":size_missing,"error": "Missing Size or Invalid Items"}, 400


        total_amount = 0
        order_items = []

        try:
            # Step 2: Validate order items, fetch prices & stock
            for item_data in extracted_order:
                item_id = item_data["item_id"]
                size_id = item_data.get("size_id")
                type_id = item_data.get("type_id")
                quantity = item_data["quantity"]
                modifiers = item_data.get("modifiers", [])

                # Fetch item details from DB
                item = Item.query.get(item_id)
                if not item:
                    return {"error": f"Invalid item: {item_id}"}, 400

                # If size_id is None, retrieve the smallest available size
                if not size_id:
                    size = Size.query.filter_by(sname="small").first()
                else:
                    size = Size.query.get(size_id)

                # if not type_id: 
                #     type_id =   Null

                item_detail = ItemDetails.query.filter_by(item_id=item.id, size_id=size.id, type_id=type_id).first()
                print(f"Item Detail: {item.id} - {size.id} - {type_id} - {item_detail}")
                if not item_detail:
                    return {"error": f"Item {item_id} (Size: {size.id}) (Type: {type_id}) not found in Item Details"}, 400

                if item_detail.qty < quantity:
                    return {"error": f"Not enough stock for Item {item_id} (Size: {size_id})  (Type: {type_id})"}, 400

                # Calculate price with modifiers
                item_price = item_detail.price
                modifier_cost = sum(mod["price"] for mod in modifiers)
                subtotal = (item_price + modifier_cost) * quantity
                total_amount += subtotal

                # Save item details for order
                order_items.append({
                    "item_detail_id": item_detail.id,
                    "quantity": quantity,
                    "price": item_price,
                    "subtotal": subtotal,
                    "modifiers": modifiers
                })

                # Reduce stock
                item_detail.qty -= quantity
                # db.session.commit()

            # Step 3: Create Order in DB
            new_order = Order(user_id=get_jwt_identity().get("id"), cus_name=customer_name, cus_mobile=customer_mobile, tot_amt=total_amount)
            db.session.add(new_order)
            db.session.flush()

            # Step 4: Add Order Details
            for item in order_items:
                order_detail = OrderDetails(order_id=new_order.id, item_detail_id=item["item_detail_id"], qty=item["quantity"], price=item["price"], sub_tot=item["subtotal"])
                db.session.add(order_detail)
                db.session.flush()  # Get order ID before committing

                # Add modifiers for this item
                for mod in item["modifiers"]:
                    order_mod = OrderDetailModifier(order_detail_id=order_detail.id, modifier_id=mod["id"], qty=1, price=mod["price"])
                    db.session.add(order_mod)

            db.session.commit() # Commit all changes
            # print("aa")
            # print(new_order.id,customer_name,customer_mobile,total_amount,order_items)
            # print("bb")

            # Emit order to chefs

            order = Order.query.filter_by(id=new_order.id).first()
            order_data = {
                "id": order.id,
                "customer": order.cus_name,
                "mobile": order.cus_mobile,
                "total_amount": order.tot_amt,
                "order_time": order.order_time.strftime("%Y-%m-%d %H:%M:%S"),
                "items": []
            }

            # Fetch order details using relationships
            for detail in order.order_details:
                item_data = {
                    #"item_detail_id": detail.item_detail_id,
                    "item_detail": {
                            "item_id": detail.item_detail.item.id,
                            "item": detail.item_detail.item.iname,
                            "size_id": detail.item_detail.size.id,
                            "size": detail.item_detail.size.sname,
                            "type_id": detail.item_detail.type.id if detail.item_detail.type else None,
                            "type": detail.item_detail.type.tname if detail.item_detail.type else None
                    },
                    "quantity": detail.qty,
                    "price": detail.price,
                    "subtotal": detail.sub_tot,
                    "modifiers": [
                        {
                            "modifier_id": mod.modifier.id,
                            "name": mod.modifier.mname,
                            "price": mod.modifier.price
                        }
                        for mod in detail.modifiers
                    ]
                }

                order_data["items"].append(item_data)

            

            socketio.emit("new_order", order_data)

            return {"message": "Order placed successfully", "order_id": new_order.id, "total_amount": total_amount}, 201
        
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error placing order: {str(e)}"}, 500
        

    @jwt_required()
    def get(self):
        """Retrieve all orders with details and modifiers using Foreign Keys."""
        orders = Order.query.all()

        response = []
        for order in orders:
            order_data = {
                "id": order.id,
                "customer": order.cus_name,
                "mobile": order.cus_mobile,
                "total_amount": order.tot_amt,
                "order_time": order.order_time.strftime("%Y-%m-%d %H:%M:%S"),
                "items": []
            }

            # Fetch order details using relationships
            for detail in order.order_details:
                item_data = {
                    #"item_detail_id": detail.item_detail_id,
                    "item_detail": {
                            "item_id": detail.item_detail.item.id,
                            "item": detail.item_detail.item.iname,
                            "size_id": detail.item_detail.size.id,
                            "size": detail.item_detail.size.sname,
                            "type_id": detail.item_detail.type.id if detail.item_detail.type else None,
                            "type": detail.item_detail.type.tname if detail.item_detail.type else None
                    },
                    "quantity": detail.qty,
                    "price": detail.price,
                    "subtotal": detail.sub_tot,
                    "modifiers": [
                        {
                            "modifier_id": mod.modifier.id,
                            "name": mod.modifier.mname,
                            "price": mod.modifier.price
                        }
                        for mod in detail.modifiers
                    ]
                }

                order_data["items"].append(item_data)

            response.append(order_data)

        return (response), 200
    

class OrderDetailResource(Resource):
    @jwt_required()
    def get(self,order_id):
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            return {"error": "Order not found"}, 404
        
        order_data = {
            "id": order.id,
            "customer": order.cus_name,
            "mobile": order.cus_mobile,
            "total_amount": order.tot_amt,
            "order_time": order.order_time.strftime("%Y-%m-%d %H:%M:%S"),
            "items": []
        }

        # Fetch order details using relationships
        for detail in order.order_details:
            item_data = {
                #"item_detail_id": detail.item_detail_id,
                "item_detail": {
                        "item_id": detail.item_detail.item.id,
                        "item": detail.item_detail.item.iname,
                        "size_id": detail.item_detail.size.id,
                        "size": detail.item_detail.size.sname,
                        "type_id": detail.item_detail.type.id if detail.item_detail.type else None,
                        "type": detail.item_detail.type.tname if detail.item_detail.type else None
                },
                "quantity": detail.qty,
                "price": detail.price,
                "subtotal": detail.sub_tot,
                "modifiers": [
                    {
                        "modifier_id": mod.modifier.id,
                        "name": mod.modifier.mname,
                        "price": mod.modifier.price
                    }
                    for mod in detail.modifiers
                ]
            }

            order_data["items"].append(item_data)

        return (order_data), 200