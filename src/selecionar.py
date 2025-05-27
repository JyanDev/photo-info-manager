import os, math, sys
def resource_path(relative_path):
    """Obtém o caminho absoluto do recurso, seja no .exe ou no script."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
from opencage.geocoder import OpenCageGeocode
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

class PhotoCollector:
    def __init__(self):
        self.photo_paths = []

    def select_photos(self):
        root = tk.Tk()
        root.withdraw()

        photo_paths = filedialog.askopenfilenames(title="Selecione as Fotos", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        self.photo_paths = list(photo_paths)

def obter_caminho_pasta_fotos():
    # Caminho padrão da pasta Imagens do usuário
    pasta_imagens = Path(os.path.expandvars(r"%USERPROFILE%\Pictures"))
    pasta_destino = pasta_imagens / "Photo_Info_Manager"

    # Cria a pasta se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)

    return pasta_destino

def obter_info_imagem(caminho):
    img = Image.open(caminho)
    exif_data = img._getexif()
    info = {
        'data_hora': None,
        'latitude': None,
        'latitude_ref': None,
        'longitude': None,
        'longitude_ref': None
    }

    if not exif_data:
        return info

    # Extrai data/hora padrão
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'DateTimeOriginal':
            info['data_hora'] = value

        # GPS Info fica numa tag separada
        if tag == 'GPSInfo':
            gps_info = {}
            for key in value.keys():
                decode = GPSTAGS.get(key, key)
                gps_info[decode] = value[key]

            info['latitude'] = gps_info.get('GPSLatitude')
            info['latitude_ref'] = gps_info.get('GPSLatitudeRef')
            info['longitude'] = gps_info.get('GPSLongitude')
            info['longitude_ref'] = gps_info.get('GPSLongitudeRef')

    return info


def obter_endereco(latitude, longitude, chaveAPI = None):
    # Adiciona a direção diretamente
    if latitude == "Sem dados" or latitude is None or longitude == "Sem dados" or longitude is None:
        cep = "Sem dados"
        estado = "Sem dados"
        return cep, estado
    else:
        try:
            # Substitua 'ChaveAPI' pela sua chave da API OpenCageGeocode
            geocoder = OpenCageGeocode(chaveAPI)

            # Realiza a pesquisa de endereço com as coordenadas
            resultado = geocoder.geocode(f"{latitude}, {longitude}", language='pt-BR')

            if resultado and len(resultado) > 0:
                cep = resultado[0]['components'].get('postcode')
                if not cep:
                    cep = resultado[0]['components'].get('city', 'CEP não encontrado')

                estado = resultado[0]['components'].get('state')
                if not estado:
                    estado = resultado[0]['components'].get('county', 'Estado não encontrado')

                return cep, estado
            else:
                return "Informações não encontradas"
        except Exception as e:
            cep, estado = False, False
            return cep, estado
    
def converter_para_graus(valor, ref=None):
    """
    Converte valor GPS em (graus, minutos, segundos) para decimal
    e aplica sinal negativo se a referência indicar Sul ou Oeste.

    Args:
        valor: tupla ou lista com (graus, minutos, segundos), cada um pode ser Fraction ou float
        ref: str, opcional, deve ser 'N', 'S', 'E' ou 'W'

    Returns:
        float: valor em graus decimais, com sinal aplicado se ref for S ou W.
    """
    def to_float(v):
        # Caso venha como Fraction, converte para float
        if hasattr(v, 'numerator'):
            return float(v)
        return v

    graus, minutos, segundos = map(to_float, valor)
    decimal = graus + minutos/60 + segundos/3600

    if ref in ['S', 'W']:
        decimal = -decimal

    return decimal


def formatar_data_br(data, hora):
    if data and hora:
        data_hora_str = f"{data} {hora}"
        data_hora_obj = datetime.strptime(data_hora_str, "%Y:%m:%d %H:%M:%S")
        data_formatada = data_hora_obj.strftime("%d/%m/%Y (BR)")
        hora_formatada = data_hora_obj.strftime("%H:%M:%S (BR)")
        return data_formatada, hora_formatada
    else:
        return "Sem dados", "Sem dados"

def obter_chaveAPI (nome_var='API_KEY_OPENCAGE'):
    if getattr(sys, 'frozen', False):
        # Se estiver rodando empacotado (PyInstaller, etc)
        base_path = os.path.dirname(sys.executable)
    else:
        # Rodando script normal
        base_path = os.path.dirname(os.path.abspath(__file__))

    env_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path=env_path)

    chave = os.getenv(nome_var)
    return chave

def adicionar_marca_dagua(caminho_imagem, texto_marca_dagua, compressao=85):
    imagem_original = Image.open(caminho_imagem)
    
    # Converte a imagem para o modo RGB (sem canal alfa)
    imagem_rgb = imagem_original.convert('RGB')
    
    largura, altura = imagem_original.size
    tamanho_fonte = (altura + largura) * 0.011
    try:
        caminho_fonte = resource_path("CourierBold.ttf")
        fonte = ImageFont.truetype(caminho_fonte, tamanho_fonte)
    except IOError:
        # Se não conseguir carregar a fonte desejada, carrega a fonte padrão do sistema (Arial)
        fonte = ImageFont.load_default()
    
    desenho = ImageDraw.Draw(imagem_rgb)

    posicao = (largura*0.011, int(altura * 0.756))
    texto_quebrado = "\n".join(texto_marca_dagua.split(', '))
    
    # Adiciona contorno preto à fonte para torná-la mais visível
    desenho.text(posicao, texto_quebrado, font=fonte, fill=(255, 255, 255), stroke_width=math.floor(tamanho_fonte * 0.2), stroke_fill=(0, 0, 0))

    nome_arquivo, extensao = os.path.splitext(os.path.basename(caminho_imagem))
    pasta_destino = obter_caminho_pasta_fotos()
    caminho_saida = pasta_destino / f"{nome_arquivo}_Photo_Info_Manager.jpg"

    imagem_rgb.save(str(caminho_saida), format="JPEG", quality=compressao)

def processar_imagem(caminho_imagem):
    chaveAPI = obter_chaveAPI()
    info_imagem_original = obter_info_imagem(caminho_imagem)

    data_hora = info_imagem_original.get('data_hora')
    if data_hora is not None:
        data, hora = data_hora.split()
        data, hora = formatar_data_br(data, hora)
    else:
        data, hora = "Sem dados", "Sem dados"

    lat_val = info_imagem_original.get('latitude')
    lat_ref = info_imagem_original.get('latitude_ref')
    long_val = info_imagem_original.get('longitude')
    long_ref = info_imagem_original.get('longitude_ref')

    if lat_val is not None and long_val is not None and lat_ref is not None and long_ref is not None:
        lat = converter_para_graus(lat_val, lat_ref)
        long = converter_para_graus(long_val, long_ref)

        cep, estado = obter_endereco(lat, long, chaveAPI)
    else:
        cep, estado, lat, long = "Sem dados", "Sem dados", "Sem dados", "Sem dados"

    if cep is False or estado is False:
        texto_marca_dagua = f"Data: {data}, Hora: {hora}\nLongitude: {long}\nLatitude: {lat}"
    else:
        texto_marca_dagua = f"CEP: {cep} \nEstado: {estado} \nData: {data}, Hora: {hora}\nLongitude: {long}\nLatitude: {lat}"

    adicionar_marca_dagua(caminho_imagem, texto_marca_dagua)


def run():
    collector = PhotoCollector()
    collector.select_photos()

    for caminho_imagem in collector.photo_paths:
        processar_imagem(caminho_imagem)

if __name__ == "__main__":
    load_dotenv()
    run()