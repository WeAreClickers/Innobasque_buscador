import fasttext
from transformers import MarianMTModel, MarianTokenizer

# --- cargar detector de idioma ---
lid_model = fasttext.load_model("lid.176.bin")

# --- cargar traductor EU->ES ---
MODEL_NAME = "Helsinki-NLP/opus-mt-eu-es"
tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
model = MarianMTModel.from_pretrained(MODEL_NAME)

def detect_lang(text: str) -> str:
    """Detecta el idioma y devuelve 'es', 'eu' o 'unk'."""
    prediction = lid_model.predict(text.replace("\n", " "))
    lang_code = prediction[0][0].replace("__label__", "")
    if lang_code.startswith("es"):
        return "es"
    elif lang_code.startswith("eu"):
        return "eu"
    else:
        return "unk"

def translate_eu_to_es(text: str) -> str:
    """Traduce texto del euskera al castellano usando MarianMT."""
    batch = tokenizer([text], return_tensors="pt", padding=True)
    gen = model.generate(**batch, max_length=128)
    translated = tokenizer.decode(gen[0], skip_special_tokens=True)
    return translated

def process_query(query: str) -> str:
    """Devuelve la query en castellano, traduciendo si es EU."""
    lang = detect_lang(query)
    if lang == "eu":
        return translate_eu_to_es(query)
    return query  # si ya está en castellano, no se toca

# --- ejemplo ---
q1 = "¿Dónde está el archivo de configuración?"
q2 = "Nola konfiguratu dezaket zerbitzaria?"

print("q1 procesada:", process_query(q1))
print("q2 procesada:", process_query(q2))
