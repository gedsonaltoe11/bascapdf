from fastapi import FastAPI, HTTPException
import requests
import io
import PyPDF2

app = FastAPI()

# Mude esta lista para os URLs dos seus PDFs
URLS_DOS_PDFS = [
    "https://www.w3.org/WAI/ER/pdf/accessibility-guidelines-draft.pdf",
    "https://www.epa.gov/sites/default/files/2016-09/documents/intro-to-pdf.pdf",
    # Adicione mais URLs aqui
]

def buscar_texto_em_pdf(url: str, query: str):
    """
    Baixa um PDF da internet e busca por uma palavra-chave.
    Retorna True se a palavra for encontrada, False caso contrário.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Lança um erro para status 4xx/5xx

        # Ler o PDF a partir do conteúdo binário na memória
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text and query.lower() in text.lower():
                return True # Encontrou a palavra-chave
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o PDF de {url}: {e}")
    except Exception as e:
        print(f"Erro ao processar o PDF de {url}: {e}")

    return False

@app.get("/buscar")
def buscar_pdfs(query: str):
    """
    Endpoint para buscar uma palavra-chave em uma lista de PDFs online.
    """
    if not query:
        raise HTTPException(status_code=400, detail="O parâmetro 'query' é obrigatório.")
    
    resultados = []
    
    for url in URLS_DOS_PDFS:
        if buscar_texto_em_pdf(url, query):
            resultados.append({"url": url, "encontrado": True})
            
    if not resultados:
        return {"mensagem": f"Nenhum resultado encontrado para a pesquisa: '{query}'."}
    
    return {"resultados": resultados}

@app.get("/")
def home():
    return {"status": "Serviço de busca de PDFs online está rodando!"}
