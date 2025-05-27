# Photo Info Manager

**Photo Info Manager** é um aplicativo desktop feito em Python (PySide6) para leitura, visualização e inserção de metadados em imagens, incluindo localização GPS, data e hora.

O programa permite adicionar essas informações diretamente nas fotos de forma visual, com interface animada, limite de tempo de uso e instalador compatível com Windows.

## 🧰 Tecnologias Utilizadas

- Python 3.x
- PySide6
- PIL (Pillow)
- ExifTool (ou biblioteca equivalente para metadados)
- JSON
- QTimer (temporizador de uso)

## 🎯 Funcionalidades

- Leitura automática de metadados (EXIF) de imagens.
- Exibição de localização (latitude/longitude), data e hora.
- Inserção ou modificação de metadados diretamente no arquivo.
- Interface gráfica com animações.
- Bloqueio de redimensionamento para manter layout estável.
- Timer interno que registra data/hora de uso (gera `.json`).
- Informações sobre o tempo restante exibidas na inicialização.
- Instalador `.exe` para Windows incluso.

## 🖼️ Interface

*Adicione aqui uma ou mais imagens do seu software em funcionamento (prints da janela aberta são ideais).*

## 📦 Instalação

### Opção 1: Usando o Instalador
1. Baixe o instalador [aqui](link-para-o-arquivo).
2. Execute e siga as instruções.

### Opção 2: Rodar com Python (para desenvolvedores)
```bash
git clone https://github.com/seu-usuario/photo-info-manager.git
cd photo-info-manager
pip install -r requirements.txt
python main.py
