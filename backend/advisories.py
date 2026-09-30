from .engine import metrics


def generate(level: str, audience: str, language: str):
    values = metrics(level)
    text = (
        f"PreLandfall {level.upper()} scenario: screening-level surge estimate is {values['surge_m']} m. "
        f"{values['critical_assets']} critical assets are flagged and {values['isolated_wards']} wards may lose road access. "
    )
    actions = {
        "commissioner": "Activate ward evacuation checks and pre-position shelter teams.",
        "power": "Stage isolation crews and protect substations before landfall.",
        "health": "Confirm ambulance routes and move supplies to reachable facilities.",
    }
    if language == "Hindi":
        text += "कृपया स्थानीय नियंत्रण कक्ष के माध्यम से सत्यापन कर कार्रवाई करें।"
    elif language == "Odia":
        text += "ଦୟାକରି ସ୍ଥାନୀୟ ନିୟନ୍ତ୍ରଣ କକ୍ଷ ମାଧ୍ୟମରେ ଯାଞ୍ଚ କରି କାର୍ଯ୍ୟ କରନ୍ତୁ।"
    else:
        text += actions[audience]
    return text


def validate(text: str, level: str):
    allowed = {str(value) for value in metrics(level).values()}
    import re
    numbers = re.findall(r"\b\d+(?:\.\d+)?\b", text)
    invalid = [number for number in numbers if number not in allowed]
    return {"valid": not invalid, "unmatched_numbers": invalid}
