from aqt import Collection, fields, mw
from aqt.gui_hooks import profile_did_open
from anki.consts import MODEL_STD
from functools import cache
from typing import Any

mcnt_model_name = "Multiple Choice Note Type"
mcnt_card_name = "Multiple Choice Card"

front_template_path = "card-templates/front_template.html"
back_template_path = "card-templates/back_template.html"
styling_template_path = "card-templates/styling.css"

# Get the folder path
def get_addon_path() -> str:
    return mw.addonManager.addonsFolder() + "/" + mw.addonManager.addonFromModule(__name__) + "/"

# Load the template file to text
@cache
def load_template(path: str) -> str:
    with open(get_addon_path() + path, encoding="utf-8") as f:
        return f.read()

def create_note_type(col: Collection) -> dict[str, Any]:
    
    print(f"Creating {mcnt_model_name} note type")

    model = col.models.new(mcnt_model_name)
    model["type"] = MODEL_STD
    model["sortf"] = 0

    # Add Fields
    col.models.add_field(model, col.models.new_field("number"))
    col.models.add_field(model, col.models.new_field("question"))
    col.models.add_field(model, col.models.new_field("a"))
    col.models.add_field(model, col.models.new_field("b"))
    col.models.add_field(model, col.models.new_field("c"))
    col.models.add_field(model, col.models.new_field("d"))
    col.models.add_field(model, col.models.new_field("e"))
    col.models.add_field(model, col.models.new_field("f"))
    col.models.add_field(model, col.models.new_field("g"))
    col.models.add_field(model, col.models.new_field("h"))
    col.models.add_field(model, col.models.new_field("i"))
    col.models.add_field(model, col.models.new_field("j"))
    col.models.add_field(model, col.models.new_field("answers"))
    col.models.add_field(model, col.models.new_field("ref"))
    col.models.add_field(model, col.models.new_field("explanation"))

    # Create Card Template
    template = col.models.new_template(mcnt_card_name)
    col.models.add_template(model, template)

    front_template = load_template(front_template_path)
    if config["isShuffle"] is True and config["isDisplayAnswerLetters"] is True:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","true").replace("isDisplayAnswerLetters","true")
    elif config["isShuffle"] is True and config["isDisplayAnswerLetters"] is False:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","true").replace("isDisplayAnswerLetters","false")
    elif config["isShuffle"] is False and config["isDisplayAnswerLetters"] is True:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","false").replace("isDisplayAnswerLetters","true")
    else:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","false").replace("isDisplayAnswerLetters","false")
    back_template = load_template(back_template_path)
    if config["isDisplayAnswerLetters"] is True:
        model["tmpls"][0]["afmt"] = back_template.replace("isDisplayAnswerLetters","true")
    else:
        model["tmpls"][0]["afmt"] = back_template.replace("isDisplayAnswerLetters","false")
    styling = load_template(styling_template_path)
    model["css"] = styling

    col.models.add(model)
   
    return model

def update_note_type(col: Collection) -> dict[str, Any]:
    
    model = mw.col.models.by_name(mcnt_model_name)

    print(f"Updating {mcnt_model_name} note type")

    # Update Card Template
    front_template = load_template(front_template_path)
    if config["isShuffle"] is True and config["isDisplayAnswerLetters"] is True:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","true").replace("isDisplayAnswerLetters","true")
    elif config["isShuffle"] is True and config["isDisplayAnswerLetters"] is False:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","true").replace("isDisplayAnswerLetters","false")
    elif config["isShuffle"] is False and config["isDisplayAnswerLetters"] is True:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","false").replace("isDisplayAnswerLetters","true")
    else:
        model["tmpls"][0]["qfmt"] = front_template.replace("isShuffle","false").replace("isDisplayAnswerLetters","false")
    back_template = load_template(back_template_path)
    if config["isDisplayAnswerLetters"] is True:
        model["tmpls"][0]["afmt"] = back_template.replace("isDisplayAnswerLetters","true")
    else:
        model["tmpls"][0]["afmt"] = back_template.replace("isDisplayAnswerLetters","false")
    styling = load_template(styling_template_path)
    model["css"] = styling

    col.models.save(model)

    return model

def create_update_note_type():
    model = mw.col.models.by_name(mcnt_model_name)

    if not model:
        create_note_type(mw.col)
    else:
        update_note_type(mw.col)

config = mw.addonManager.getConfig(__name__)

profile_did_open.append(create_update_note_type)
