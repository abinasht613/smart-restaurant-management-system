import spacy
from word2number import w2n
from backend.models.Item import Item
from backend.models.Size import Size
from backend.models.Modifier import Modifier
from backend.models.Type import Type
from backend.extensions import db

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
    print("spaCy model loaded successfully!")
except Exception as e:
    print(f"Error loading spaCy model: {e}")

def fetch_menu_data():
    """Fetch menu items, sizes, types, and modifiers from the database."""
    items = {i.iname.lower(): {"id": i.id, "iname": i.iname} for i in db.session.query(Item).all()}
    sizes = {s.sname.lower(): {"id": s.id,"sname":s.sname} for s in db.session.query(Size).all()}
    modifiers = {m.mname.lower(): {"id": m.id,"mname":m.mname, "price": m.price} for m in db.session.query(Modifier).all()}
    types = {t.tname.lower(): {"id": t.id,"tname":t.tname} for t in db.session.query(Type).all()}
    return items, sizes, modifiers, types

def extract_order(order_text):
    """
    Extracts items, sizes, quantities, types, and modifiers from an order text.

    Example:
        Input:  "Two large chicken pepperoni pizzas extra cheese, one caesar salad, and two diet cokes"
        Output: [
            {"item_id": 1, "size_id": 3, "type_id": 2, "quantity": 2, "modifiers": [{"id": 5, "price": 1.0}]},
            {"item_id": 2, "size_id": None, "type_id": None, "quantity": 1, "modifiers": []},
            {"item_id": 3, "size_id": None, "type_id": None, "quantity": 2, "modifiers": []}
        ]
    """
    items, sizes, modifiers, types = fetch_menu_data()

    doc = nlp(order_text.lower())  # Process text with spaCy
    # words = [token.text for token in doc]
    items_found = []

    current_quantity = 1  # Default quantity
    current_size     = None
    current_type        = None
    #current_modifiers = []
    current_item = None  # To store the latest detected item

    for i, token in enumerate(doc):
        word = token.text

        # Ignore commas and conjunctions
        if word in [",", "and"]:
            continue

        # Detect quantity before an item
        if word.isdigit():
            current_quantity = int(word)
            continue
        else:
            try:
                current_quantity = w2n.word_to_num(word)  # Convert words like "two" to 2
                continue
            except ValueError:
                pass

        # Detect size (must come before an item)
        if word in sizes:
            current_size = sizes[word]["id"]
            continue

        # Detect type (must come before an item)
        if word in types:
            current_type = types[word]["id"]
            continue

        # If the word is an item, create a new entry
        if word in items:
            current_item = {
                "item_id": items[word]["id"],
                "type_id": current_type,
                "size_id": current_size,
                "quantity": current_quantity,
                "modifiers": []
            }
            items_found.append(current_item)

            # Reset tracking variables for the next item
            current_quantity = 1
            current_size = None
            current_type = None

            continue  # Move to the next word

        # Detect modifiers **only if an item was detected before**
        if word in modifiers and current_item:
            modifier_data = {"id": modifiers[word]["id"], "price": modifiers[word]["price"]}
            current_item["modifiers"].append(modifier_data)

    # print(items_found)
    return items_found
