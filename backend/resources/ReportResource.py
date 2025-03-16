from flask_restful import Resource
from flask import jsonify, request
from sqlalchemy import func
from flask_jwt_extended import jwt_required
from backend.extensions import db
from backend.models.Order import Order
from backend.models.OrderDetails import OrderDetails
from backend.models.ItemDetails import ItemDetails
from backend.models.Item import Item

class ReportResource(Resource):
    @jwt_required()
    def get(self):
        return jsonify({
            "popular_items": self.get_popular_items(),
            "peak_hours": self.get_peak_hours(),
            "sales_trends": self.get_sales_trends()
        })

    def get_popular_items(self):
        popular_items = (
            db.session.query(Item.iname, func.sum(OrderDetails.qty).label("total_qty"))
            .join(ItemDetails, ItemDetails.id == OrderDetails.item_detail_id)
            .join(Item, Item.id == ItemDetails.item_id)
            # .join(ItemDetails)  # Use relationship between Item and ItemDetails
            # .join(OrderDetails)  # Use relationship between ItemDetails and OrderDetails
            .group_by(Item.iname)
            .order_by(func.sum(OrderDetails.qty).desc())
            .limit(10)
            .all()
            
        )
        return [{"item": item[0], "quantity": item[1]} for item in popular_items]

    def get_peak_hours(self):
        peak_hours = (
            db.session.query(
                func.to_char(func.date_trunc('hour', Order.order_time), 'FMHH AM').label("hour"),  # Formats as 12-hour AM/PM
                func.count(Order.id).label("total_orders")
            )
            .group_by("hour")
            .order_by("hour")
            # .order_by(func.count(Order.id).desc())
            .all()
        )
        return [{"hour": str(row[0]), "total_orders": row[1]} for row in peak_hours]

    def get_sales_trends(self):
        sales_trends = (
            db.session.query(
                func.to_char(func.date_trunc('day', Order.order_time), 'DD-Mon').label("date"),
                func.sum(Order.tot_amt).label("total_sales")
            )
            .group_by("date")
            .order_by("date")
            .all()
        )
        return [{"date": str(row[0]), "total_sales": row[1]} for row in sales_trends]
