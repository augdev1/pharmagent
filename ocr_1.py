import pytesseract
from PIL import Image
import os

# Configure o caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'H:\O_IMG\tesseract.exe'

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
        texto_extraido = pytesseract.image_to_string(imagem, lang='por')
        return texto_extraido
    except pytesseract.TesseractNotFoundError:
        return "Erro: Tesseract não encontrado. Verifique a configuração."
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