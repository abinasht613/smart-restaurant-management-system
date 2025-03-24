import spacy
from word2number import w2n
from backend.models.Item import Item
from backend.models.Size import Size
from backend.models.ItemDetails import ItemDetails
from backend.models.Modifier import Modifier
from backend.models.Type import Type
from backend.extensions import db
import inflect
from fuzzywuzzy import process

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
    p = inflect.engine()  # Inflect engine for singularization
except Exception as e:
    print(f"Error loading spaCy model: {e}")

def fuzzy_match(word, choices, threshold=80):
    # print(f"word: {word} choices: {choices}")
    """Find the closest match from choices using fuzzy matching."""
    match, confidence = process.extractOne(word, choices) if word else (None, 0)
    return match if confidence > threshold else None

def fetch_menu_data():
    """Fetch menu items, sizes, types, and modifiers from the database."""
    items = {i.iname.lower(): {"id": i.id, "iname": i.iname} for i in db.session.query(Item).all()}
    sizes = {s.sname.lower(): {"id": s.id,"sname":s.sname} for s in db.session.query(Size).all()}
    modifiers = {m.mname.lower(): {"id": m.id,"mname":m.mname, "price": m.price} for m in db.session.query(Modifier).all()}
    types = {t.tname.lower(): {"id": t.id,"tname":t.tname} for t in db.session.query(Type).all()}

    # Plural-to-Singular Dictionary (for exceptions not handled by `inflect`)
    plural_to_singular = {
        "fries": "fries"  # No singular change needed
    }

    return items, sizes, modifiers, types, plural_to_singular

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
    items, sizes, modifiers, types, plural_to_singular = fetch_menu_data()

    doc = nlp(order_text.lower())  # Process text with spaCy
    # print(f"doc: {doc}")

    words = [token.text for token in doc]
    print(f"words: {words}")
    
    processed_order = []
    invalid_words = [];
    size_missing = []
    i = 0

    while i < len(words):
        word = words[i]
        next_word = words[i+1] if i < len(words) - 1 else None
        # print(f"word: {word} next_word: {next_word}")

        # Convert plural to singular (priority: dictionary → inflect → original)
        if word and word.strip():  # Ensure word is not empty or just whitespace
            singular_word = plural_to_singular.get(word, p.singular_noun(word) or word)
        else:
            singular_word = word  # Keep the word unchanged if empty
        if next_word and next_word.strip():
            singular_next_word = plural_to_singular.get(next_word, p.singular_noun(next_word) or next_word)
        else:
            singular_next_word = None
        # print(f"singular_word:-{singular_word} singular_next_word:-{singular_next_word}")

        # Check for multi-word food items
        if singular_next_word:
            if singular_word not in {",", "and"} and singular_next_word not in {",", "and"}:
                combined = f"{singular_word} {singular_next_word}"
            elif singular_word not in {",", "and"}:
                combined = singular_word
            elif singular_next_word not in {",", "and"}:
                combined = singular_next_word
            else:
                pass
                combined = ""  # Default case if both are ',' or 'and'
            print(f"combined: {combined}")

            # Apply fuzzy matching to correct words
            if (singular_word in sizes.keys()):
                print(f"size found in singular_word: {singular_word}")
                pass
            elif (singular_word in modifiers.keys()):
                print(f"modifier found in singular_word: {singular_word}")
                pass
            else:
                corrected_word = fuzzy_match(combined, items.keys()) or combined
                if corrected_word != combined:
                    invalid_words.append({combined:corrected_word})  # Store invalid words for error reporting
                else:
                    pass

                print(f"corrected_word: {corrected_word}")

                if combined in items:
                    processed_order.append(combined)
                    i += 2  # Skip next word since it's merged
                    continue

        processed_order.append(singular_word)
        i += 1

    # print(f"processed_order: {processed_order}")

    # processed_order = nlp(processed_order.lower())


    items_found = []

    current_quantity = 1  # Default quantity
    current_size     = None
    current_type        = None
    #current_modifiers = []
    current_item = None  # To store the latest detected item

    # print(list(enumerate(doc)))
    # print(list(enumerate(processed_order)))

    for i, token in (enumerate(processed_order)):
        word = token
        # print(f"word: {word}")

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
            if current_size is None:
                results = ItemDetails.query.filter(ItemDetails.item_id == items[word]["id"]).all()    
                item_sizes  =[item.size.sname for item in results]

                size_missing.append({word:item_sizes})
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
    # print(f"order text {order_text}")
    # print(f"items found: {items_found}")
    print(f"invalid words: {invalid_words}")
    print(f"size missing: {size_missing}")

    
    
    return items_found, invalid_words, size_missing
