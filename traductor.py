from lingua import Language, LanguageDetectorBuilder
from transformers import MarianMTModel, MarianTokenizer
import time

# --- cargar traductor EU->ES ---
MODEL_NAME = "Helsinki-NLP/opus-mt-eu-es"
tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
model = MarianMTModel.from_pretrained(MODEL_NAME)


def detect_lang_lingua(text: str) -> str:
    """Detecta el idioma usando lingua y devuelve 'es', 'eu' o 'unk'."""
    start_time = time.time()
    try:
        # Crear detector con idiomas específicos
        detector = LanguageDetectorBuilder.from_languages(Language.SPANISH, Language.BASQUE).build()
        
        # Detectar idioma
        detected_language = detector.detect_language_of(text.replace("\n", " "))
        
        # Obtener scores para todos los idiomas configurados
        confidence_values = detector.compute_language_confidence_values(text.replace("\n", " "))
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de detección (lingua): {execution_time:.4f} segundos")
        
        # Imprimir scores
        print("Scores de confianza:")
        for result in confidence_values:
            language = result.language
            confidence = result.value
            lang_name = "español" if language == Language.SPANISH else "euskera" if language == Language.BASQUE else str(language)
            print(f"  {lang_name}: {confidence:.4f}")
        
        if detected_language == Language.SPANISH:
            return "es"
        elif detected_language == Language.BASQUE:
            return "eu"
        else:
            return "unk"
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de detección (lingua): {execution_time:.4f} segundos")
        print(f"Error: {e}")
        return "unk"

def translate_eu_to_es(text: str) -> str:
    """Traduce texto del euskera al castellano usando Helsinki NLP MarianMT."""
    start_time = time.time()
    try:
        # Si no está cargado, return mismo texto
        if tokenizer is None or model is None:
            print("Modelo de traducción no disponible.")
            return text
        
        # Tokenizar el texto
        batch = tokenizer([text], return_tensors="pt", padding=True)
        
        # Generar traducción
        gen = model.generate(**batch, max_length=128)
        
        # Decodificar resultado
        translated = tokenizer.decode(gen[0], skip_special_tokens=True)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de traducción: {execution_time:.4f} segundos")     
        
        print(translated)
        return translated
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de traducción: {execution_time:.4f} segundos")
        print(f"Error en traducción: {e}")
        return text  # Devolver texto original si hay error

def process_query(query: str) -> str:
    """Devuelve la query en castellano, traduciendo si es EU."""
    lang = detect_lang_lingua(query)
    if lang == "eu":
        return translate_eu_to_es(query)
    return query  # si ya está en castellano, no se toca

# --- ejemplo ---
q1 = "¿Dónde está el archivo de configuración?"
q2 = "inteligencia"
q3 = "Nola konfiguratu dezaket zerbitzaria?"
q4 = "Kaixo, zer moduz zaude?"

process_query(q3)