from bs4 import BeautifulSoup
import requests
import json
import os
import PyPDF2

def process_pdf(url):
    """Scarica e legge il contenuto di un PDF."""
    try:
        pdf_response = requests.get(url)
        if 'application/pdf' in pdf_response.headers.get('Content-Type', ''):
            pdf_filename = "temp.pdf"
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            """Leggi il contenuto del PDF"""
            with open(pdf_filename, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
            
            """Rimuovi il file temporaneo dopo averlo letto"""
            os.remove(pdf_filename)  # Rimuovi il file temporaneo
            return content
        else:
            return "Il file scaricato non è un PDF valido."
    except Exception as e:
        return f"Errore durante l'accesso al PDF: {e}"

def process_page(url):
    """Analizza una pagina per trovare link a PDF."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_links = []

        """Trova tutti i link ai PDF nella pagina"""
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.pdf'):
                pdf_links.append(href if href.startswith('http') else f"{url.rsplit('/', 1)[0]}/{href}")

        return pdf_links
    except Exception as e:
        return []

site_url = "https://noi.bz.it/it/chi-siamo/societa-trasparente/bandi-di-gara-e-contratti/avvisi-e-indagini-di-mercato"

response = requests.get(site_url)
soup = BeautifulSoup(response.content, 'html.parser')

data_section = soup.find('div', class_='content')

if data_section:
    links = data_section.find_all('a')
    extracted_data = []

    for link in links:
        title = link.get_text(strip=True)
        url = link.get('href')

        if url:
            if url.endswith('.pdf'):  # Se è un PDF diretto
                content = process_pdf(url)
            else:  # Se è una pagina intermedia
                pdf_links = process_page(url)
                if pdf_links:
                    content = ""
                    for pdf_url in pdf_links:
                        content += process_pdf(pdf_url) + "\n---\n"
                else:
                    content = "Nessun PDF trovato nella pagina."

            # Aggiungi i dati alla lista
            extracted_data.append({'Titolo': title, 'URL': url, 'Contenuto': content})

            # Stampa i dati (opzionale)
            print(f"Titolo: {title}")
            print(f"URL: {url}")
            print(f"Contenuto: {content[:100]}...")  # Mostra solo i primi 100 caratteri del contenuto
            print("-" * 40)

    # Salva i dati in un file JSON
    with open('dataBeautifulSoup.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(extracted_data, jsonfile, ensure_ascii=False, indent=4)

    print("Dati salvati in 'dataBeautifulSoup.json'.")
else:
    print("Sezione dati non trovata.")