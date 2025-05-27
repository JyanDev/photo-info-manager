# 📸 Photo Info Manager

**Photo Info Manager** é um software demonstrativo criado em Python que permite extrair metadados de imagens (como localização, data, hora, latitude e longitude) e inseri-los visualmente na imagem. Conta com uma interface gráfica moderna e recursos como timer de uso, geolocalização via API e instalador independente para Windows.

> ⚠️ **Atenção:** Este software é **apenas demonstrativo**. Atualmente, a chave de API utilizada para obter dados de geolocalização **está expirada**, portanto, ao utilizá-lo, será exibida a mensagem **"Sem dados"** nos campos que dependem da API externa. Prints com exemplos reais de funcionamento estão incluídos neste repositório.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.12**
- **PySide6** – Interface gráfica com animações e sombreamento
- **Pillow** – Manipulação de imagens e sobreposição de texto
- **OpenCage Geocode** – API de localização geográfica via coordenadas GPS
- **ExifTags** – Extração de metadados embutidos em imagens
- **Tkinter** – Seleção de arquivos e diretórios
- **JSON / QTimer** – Armazenamento e controle de tempo de uso por sessão

---

## 💡 Funcionalidades

- Extração automática de metadados (data, hora, localização) de imagens
- Inserção dos dados extraídos diretamente sobre a imagem
- Interface customizada com efeitos visuais e limitação de redimensionamento
- Temporizador embutido com aviso de tempo restante (simulado via `.json`)
- Criação de instalador funcional para Windows
- Prevenção de uso contínuo após tempo limite

---

## 📦 Instalação

> Este projeto é compatível com sistemas **Windows** (via instalador incluído).

1. Baixe o instalador na pasta `/installer`
2. Execute como administrador
3. Siga as instruções para instalar o Photo Info Manager

Ou, se desejar executar o projeto diretamente:

### 🔧 Execução via código-fonte

```bash
git clone https://github.com/JyanDev/photo-info-manager.git
cd photo-info-manager
pip install -r requirements.txt
python main.py
