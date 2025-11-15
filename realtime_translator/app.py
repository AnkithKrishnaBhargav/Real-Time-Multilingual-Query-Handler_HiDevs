from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langdetect import detect, DetectorFactory
import time, logging, os

DetectorFactory.seed = 0
logging.basicConfig(level=logging.INFO)

HF_MODEL_MAP = {
    "es": ("Helsinki-NLP/opus-mt-es-en","Helsinki-NLP/opus-mt-en-es"),
    "fr": ("Helsinki-NLP/opus-mt-fr-en","Helsinki-NLP/opus-mt-en-fr"),
    "de": ("Helsinki-NLP/opus-mt-de-en","Helsinki-NLP/opus-mt-en-de"),
    "hi": ("Helsinki-NLP/opus-mt-hi-en","Helsinki-NLP/opus-mt-en-hi"),
    "pt": ("Helsinki-NLP/opus-mt-pt-en","Helsinki-NLP/opus-mt-en-pt"),
    "it": ("Helsinki-NLP/opus-mt-it-en","Helsinki-NLP/opus-mt-en-it")
}

_hf_cache = {}

def load_hf_pipeline(model_id):
    from transformers import pipeline
    if model_id not in _hf_cache:
        _hf_cache[model_id] = pipeline("translation", model=model_id, tokenizer=model_id)
    return _hf_cache[model_id]

app = FastAPI(title="Real-Time Translator")

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class QueryIn(BaseModel):
    text: str
    translate_back: bool = False

class QueryOut(BaseModel):
    original_text: str
    detected_lang: str
    translated_text: str
    response_english: str
    response_translated: str | None = None
    timings_ms: dict


def detect_lang_safe(txt):
    try: return detect(txt)
    except: return "und"

def translate_to_english(text, lang):
    if lang in ("en","und"): return text
    m = HF_MODEL_MAP.get(lang)
    if m:
        pipe = load_hf_pipeline(m[0])
        return pipe(text)[0]["translation_text"]
    return text

def translate_from_english(text, lang):
    if lang in ("en","und"): return text
    m = HF_MODEL_MAP.get(lang)
    if m:
        pipe = load_hf_pipeline(m[1])
        return pipe(text)[0]["translation_text"]
    return text

def canned_reply(txt):
    t = txt.lower()
    if "price" in t or "cost" in t:
        return "Thanks for asking about pricing! How can I help further?"
    if "refund" in t or "return" in t:
        return "Sorry to hear that. Please share your order number."
    return f"We received your message: '{txt[:150]}'. Thanks for contacting us!"

@app.post("/api/query", response_model=QueryOut)
async def handle_query(payload: QueryIn):
    t0 = time.time()

    lang = detect_lang_safe(payload.text)
    t_en = translate_to_english(payload.text, lang)
    reply_en = canned_reply(t_en)
    reply_back = translate_from_english(reply_en, lang) if payload.translate_back else None

    return QueryOut(
        original_text=payload.text,
        detected_lang=lang,
        translated_text=t_en,
        response_english=reply_en,
        response_translated=reply_back,
        timings_ms={"total_ms": int((time.time()-t0)*1000)}
    )

@app.get("/")
def home():
    return HTMLResponse(open(os.path.join(static_dir,"index.html"),"r").read())

@app.get("/health")
def health():
    return {"status":"ok"}