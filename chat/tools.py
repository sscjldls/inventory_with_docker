from .models import Item
from decimal import Decimal


def check_stock(name):
    """Look up how many of an item we have."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    return {"name": item.name, "quantity": item.quantity}


def list_items():
    """Return every item in the inventory."""
    items = Item.objects.all()
    return {"items": [{"name": i.name, "quantity": i.quantity, "price": float(i.price)} for i in items]}


def add_item(name, quantity, price=0.0):
    """Create a new item, or add to an existing one's stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is not None:
        item.quantity += quantity
        if price > 0:
            item.price = price
        item.save()
        return {"name": item.name, "quantity": item.quantity, "price": float(item.price), "created": False}
    item = Item.objects.create(name=name, quantity=quantity, price=price)
    return {"name": item.name, "quantity": item.quantity, "price": float(item.price), "created": True}


def remove_stock(name, quantity):
    """Take a quantity out of stock."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    if quantity > item.quantity:
        return {
            "error": f"Cannot remove {quantity}. Only {item.quantity} in stock.",
            "name": item.name,
            "quantity": item.quantity,
        }
    item.quantity -= quantity
    item.save()
    return {"name": item.name, "quantity": item.quantity}


def delete_item(name):
    """Remove an item from the inventory entirely."""
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    item.delete()
    return {"deleted": name}


def get_item_price(name):
    """Get the price of an item."""
    try:
        item = Item.objects.get(name__iexact=name)
        return {"name": item.name, "quantity": item.quantity, "price": float(item.price)}
    except Item.DoesNotExist:
        return {"error": f"Item '{name}' not found."}

def set_price(name, price):
    """Change the unit price of an existing item."""
    if price < 0:
        return {"error": "Price cannot be negative."}
    item = Item.objects.filter(name__iexact=name).first()
    if item is None:
        return {"error": f"No item named '{name}' exists in the inventory."}
    old_price = float(item.price)
    item.price = Decimal(str(price)).quantize(Decimal("0.01"))
    item.save()
    return {"name": item.name, "old_price": old_price, "new_price": float(item.price)}


TOOL_DECLARATIONS = [
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Look up the current quantity of a single item in the inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item, e.g. 'Hammer'.",
                    },
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_items",
            "description": "Return every item in the inventory with its quantity and price.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_item",
            "description": "Add stock to the inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item.",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "How many units to add.",
                    },
                    "price": {
                        "type": "number",
                        "description": "Optional price per unit.",
                    },
                },
                "required": ["name", "quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_stock",
            "description": "Reduce the quantity of an existing item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item.",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "How many units to remove.",
                    },
                },
                "required": ["name", "quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_item",
            "description": "Permanently remove an item from the inventory entirely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item to delete.",
                    },
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_item_price",
            "description": "Get the unit price and details of a specific item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item, e.g. 'Chocolate bar'.",
                    },
                },
                "required": ["name"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "set_price",
            "description": "Set a new unit price for an existing item. Use this to raise or lower a price. For percentage changes, look up the current price first, calculate the new price, then call this.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the item.",
                    },
                    "price": {
                        "type": "number",
                        "description": "The new price per unit.",
                    },
                },
                "required": ["name", "price"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "check_stock": check_stock,
    "list_items": list_items,
    "add_item": add_item,
    "remove_stock": remove_stock,
    "delete_item": delete_item,
    "get_item_price": get_item_price,
    "set_price": set_price,
}   