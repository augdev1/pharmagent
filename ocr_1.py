import pytesseract
from PIL import Image
import os

# Configura o caminho para o executável do Tesseract OCR.
# Prioriza a variável de ambiente TESSERACT_CMD; em seguida tenta caminhos comuns no Windows.
_tesseract_cmd = os.getenv("TESSERACT_CMD")
if _tesseract_cmd and os.path.exists(_tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = _tesseract_cmd
else:
    common_windows_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in common_windows_paths:
        if os.path.exists(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            break

def extract_text_from_image(image_path):
    """
    Extrai texto de uma imagem usando Tesseract OCR.

    Args:
        image_path (str): O caminho para o arquivo de imagem.

    Returns:
        str: O texto extraído da imagem, ou uma mensagem de erro se a imagem não for encontrada.
    """
    try:
        if not os.path.exists(image_path):
            return f"Erro: Arquivo de imagem não encontrado em '{image_path}'"
        
        imagem = Image.open(image_path)
        primary_lang = os.getenv("OCR_LANG", "por")
        fallback_lang = os.getenv("OCR_FALLBACK_LANG", "eng")

        try:
            texto_extraido = pytesseract.image_to_string(imagem, lang=primary_lang)
            return texto_extraido
        except pytesseract.TesseractError as e:
            erro = str(e)
            if "Failed loading language" in erro and primary_lang != fallback_lang:
                texto_extraido = pytesseract.image_to_string(imagem, lang=fallback_lang)
                return texto_extraido
            raise
    except pytesseract.TesseractNotFoundError:
        return (
            "Erro: Tesseract não encontrado. Instale o Tesseract OCR no Windows "
            "e configure a variável de ambiente TESSERACT_CMD, se necessário."
        )
    except pytesseract.TesseractError as e:
        return (
            "Erro do Tesseract ao processar OCR: "
            f"{e}. Se estiver usando português, instale o arquivo por.traineddata "
            "na pasta tessdata do Tesseract."
        )
    except Exception as e:
        return f"Ocorreu um erro inesperado durante o OCR: {e}"

if __name__ == '__main__':
    # Exemplo de uso
    caminho_imagem_exemplo = r'X:\Downloads\receita_fake.jpg'  # Coloque um caminho de imagem válido para testar
    if os.path.exists(caminho_imagem_exemplo):
        texto = extract_text_from_image(caminho_imagem_exemplo)
        print("--- Texto extraído ---")
        print(texto)
        print("----------------------")
    else:
        print(f"Arquivo de exemplo não encontrado em: {caminho_imagem_exemplo}")
        print("Por favor, atualize a variável 'caminho_imagem_exemplo' em ocr_1.py com um caminho de imagem válido para testar o script.")