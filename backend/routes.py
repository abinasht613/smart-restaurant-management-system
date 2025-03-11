from flask_restful import Api
from backend.resources.UserResource import RegisterAPI, LoginAPI, RefreshTokenAPI, ProtectedResource, NotProtectedResource
from backend.resources.ItemResource import ItemResourceCR,ItemResourceUD
from backend.resources.SizeResource import SizeListResource, SizeResource
from backend.resources.TypeResource import TypeListResource, TypeResource
from backend.resources.ModifierResource import ModifierListResource, ModifierResource
from backend.resources.ItemDetailsResource import ItemDetailsResource
from backend.resources.OrderResource import OrderResource, OrderDetailResource
from backend.resources.MenuResource import MenuResource


def register_routes(app):
    api = Api(app)

    # Authentication Routes
    api.add_resource(RegisterAPI, "/register")
    api.add_resource(LoginAPI, "/login")
    api.add_resource(RefreshTokenAPI, "/refresh")

    # Protected Routes
    api.add_resource(ProtectedResource, "/protected")
    api.add_resource(NotProtectedResource, "/not-protected")


    # Item Routes
    api.add_resource(ItemResourceCR, "/items")  # POST, GET
    api.add_resource(ItemResourceUD, "/items/<int:item_id>")  # PUT, DELETE

    #item details
    api.add_resource(ItemDetailsResource, "/itemdetails", "/itemdetails/<int:item_detail_id>")

    # Size Routes
    api.add_resource(SizeListResource, "/sizes")  # Handles GET (all sizes) & POST (create size)
    api.add_resource(SizeResource, "/sizes/<int:size_id>")  # Handles PUT & DELETE for a specific size

    # Type Routes
    api.add_resource(TypeListResource, "/types")  # Handles GET (all types) & POST (create type)
    api.add_resource(TypeResource, "/types/<int:type_id>")  # Handles PUT & DELETE for a specific type

    # Modifier Routes
    api.add_resource(ModifierListResource, "/modifiers")  # GET (all) & POST (add)
    api.add_resource(ModifierResource, "/modifiers/<int:modifier_id>")  # PUT & DELETE

    # Order Routes
    api.add_resource(OrderResource, "/order")

    #OrderDetails Routes
    api.add_resource(OrderDetailResource, "/order-details/<int:order_id>")

    # Menu Route
    api.add_resource(MenuResource, "/menu")

    return api
