import os, math, sys
def resource_path(relative_path):
    """Obtém o caminho absoluto do recurso, seja no .exe ou no script."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from datetime import datetime
from fractions import Fraction
from opencage.geocoder import OpenCageGeocode
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from pathlib import Path

class PhotoCollector:
    def __init__(self):
        self.photo_paths = []

    def select_photos(self):
        root = tk.Tk()
        root.withdraw()

        photo_paths = filedialog.askopenfilenames(title="Selecione as Fotos", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        self.photo_paths = list(photo_paths)


import os
import sys
from PIL import ImageFont


def obter_caminho_pasta_fotos():
    # Caminho padrão da pasta Imagens do usuário
    pasta_imagens = Path(os.path.expandvars(r"%USERPROFILE%\Pictures"))
    pasta_destino = pasta_imagens / "Photo_Info_Manager"

    # Cria a pasta se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)

    return pasta_destino

def obter_info_imagem(caminho_imagem):
    imagem = Image.open(caminho_imagem)
    exif_info = imagem._getexif()

    info = {
        'latitude': None,
        'longitude': None,
        'data_hora': None
    }

    if exif_info is not None:
        for tag, valor in exif_info.items():
            tag_nome = TAGS.get(tag, tag)

            if tag_nome == 'GPSInfo':
                info['latitude'] = valor[2][0] + valor[2][1]/60 + valor[2][2]/3600
                info['longitude'] = valor[4][0] + valor[4][1]/60 + valor[4][2]/3600
            elif tag_nome == 'DateTimeOriginal':
                info['data_hora'] = valor

    return info

def obter_endereco(latitude, longitude):
    # Adiciona a direção diretamente
    if latitude == "Sem dados" or latitude is None or longitude == "Sem dados" or longitude is None:
        cep = "Sem dados"
        estado = "Sem dados"
        return cep, estado
    else:
        latitude = -abs(latitude)  # Considerando "S" como Sul
        longitude = -abs(longitude)  # Considerando "W" como Oeste

        try:
            # Substitua 'SUA_CHAVE_AQUI' pela sua chave da API OpenCageGeocode
            geocoder = OpenCageGeocode('696ab977ed6c46be8ff3ceadac1665b2')

            # Realiza a pesquisa de endereço com as coordenadas
            resultado = geocoder.geocode(f"{latitude}, {longitude}", language='pt-BR')

            if resultado and len(resultado) > 0:
                cep = resultado[0]['components'].get('postcode', 'CEP não encontrado')
                estado = resultado[0]['components'].get('state', 'Estado não encontrado')
                return cep, estado
            else:
                return "Informações não encontradas"
        except Exception as e:
            cep, estado = False, False
            return cep, estado
    
def converter_para_graus(valor):
    if isinstance(valor, Fraction):
        return float(valor)
    graus, minutos, segundos = valor
    return graus + minutos/60 + segundos/3600


def formatar_data_br(data, hora):
    if data and hora:
        data_hora_str = f"{data} {hora}"
        data_hora_obj = datetime.strptime(data_hora_str, "%Y:%m:%d %H:%M:%S")
        data_formatada = data_hora_obj.strftime("%d/%m/%Y")
        hora_formatada = data_hora_obj.strftime("%H:%M:%S")
        return data_formatada, hora_formatada
    else:
        return "Sem dados", "Sem dados"



def adicionar_marca_dagua(caminho_imagem, texto_marca_dagua, compressao=85):
    imagem_original = Image.open(caminho_imagem)
    #print("marca de agua:   ",caminho_imagem)
    
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
    #print(caminho_imagem)
    info_imagem_original = obter_info_imagem(caminho_imagem)

    data_hora = info_imagem_original['data_hora']
    if data_hora is not None:
        data, hora = data_hora.split()
        data, hora = formatar_data_br(data,hora)
    else:
        data, hora = "Sem dados", "Sem dados"
    

    if info_imagem_original['latitude'] is not None and info_imagem_original['longitude'] is not None:
        info_imagem_original['latitude'] = converter_para_graus(info_imagem_original['latitude'])
        info_imagem_original['longitude'] = converter_para_graus(info_imagem_original['longitude'])
        lat = info_imagem_original['latitude']
        long = info_imagem_original['longitude']
        cep, estado = obter_endereco(info_imagem_original['latitude'], info_imagem_original['longitude'])
    else:
        cep, estado, lat, long = "Sem dados", "Sem dados", "Sem dados", "Sem dados"

    if cep == False or estado == False:
         texto_marca_dagua = f"Data: {data}, Hora: {hora}\nLongitude: {long}\nLatitude: {lat}"
    else:
        texto_marca_dagua = f"CEP: {cep} \nEstado: {estado} \nData: {data}, Hora: {hora}\nLongitude: {long}\nLatitude: {lat}"

    adicionar_marca_dagua(caminho_imagem, texto_marca_dagua)

def run():
    #logging.info("entrou no main...")
    collector = PhotoCollector()
    collector.select_photos()

    for caminho_imagem in collector.photo_paths:
        processar_imagem(caminho_imagem)
        #logging.info("Entrou no for...")

        
    #logging.info("Programa concluído, Sr. Jyan.")

if __name__ == "__main__":
   #logging.info("Iniciando programa...")
    run()