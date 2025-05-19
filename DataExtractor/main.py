import json
from semanticRetrival import analyze_with_retrieval

INPUT_FILE = "../output/dataScrapy.json"
OUTPUT_FILE = "../output/dataAnalyzed.json"

def clean_llm_response(text):
    """
    Pulisce una risposta da LLM rimuovendo eventuali backtick e blocchi ```json ... ```
    """
    if isinstance(text, dict):
        return text  # è già un JSON
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

import time
from semanticRetrival import analyze_with_retrieval

def timed_analysis(text):
    times = {}

    t0 = time.time()
    risposta = analyze_with_retrieval(text)
    times["Totale"] = round(time.time() - t0, 2)

    for k, v in times.items():
        print(f"[TEMPO] {k}: {v} sec")

    return risposta

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            bandi = json.load(f)

        risultati = []

        for item in bandi:
            titolo = item.get("Titolo", "Senza titolo")
            url = item.get("URL", "Senza URL")
            testo = item.get("Contenuto", "")

            if not testo.strip():
                print(f"[SKIP] Bando vuoto: {titolo}")
                continue

            print(f"[PROCESSING] {titolo}")
            try:
                # raw_response = timed_analysis(testo)
                # risposta_json = clean_llm_response(raw_response)
                risposta_json = timed_analysis(testo)
                risultati.append({
                    "Titolo": titolo,
                    "URL": url,
                    "Risposta": risposta_json
                })
            except Exception as e:
                print(f"[ERRORE] {titolo}: {e}")
                risultati.append({
                    "Titolo": titolo,
                    "Risposta": f"Errore: {e}"
                })

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(risultati, f, ensure_ascii=False, indent=4)

        print(f"[FINE] Output salvato in: {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"File {INPUT_FILE} non trovato.")
    except json.JSONDecodeError:
        print("Errore nel parsing del file JSON.")
    except Exception as e:
        print(f"Errore imprevisto: {e}")

if __name__ == "__main__":
    main()
