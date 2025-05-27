<p align="center">
  <img src="assets/icon.png" alt="Ícone" width="100" />
</p>

<h1 align="center">Photo Info Manager</h1>

**Photo Info Manager** é um software com interface gráfica desenvolvido em Python que permite visualizar metadados de imagens (como data, resolução, câmera, localização GPS etc.). A ferramenta foi pensada para quem deseja explorar informações embutidas em fotos de forma prática, sem necessidade de comandos no terminal.

⚠️ **Aviso importante:**  
Este projeto é demonstrativo. A chave de API utilizada para obtenção de dados geográficos a partir de coordenadas expirou e, por isso, atualmente o software exibe a mensagem **"Sem dados"** nessa parte.  
Apesar disso, deixei **prints com exemplos práticos** do funcionamento original, para fins de compreensão e visualização do projeto.

---

## 🔧 Funcionalidades

- Leitura de metadados de imagens JPEG
- Interface amigável feita com PySide6 e Qt Designer
- Efeitos visuais e animações suaves
- Suporte à abertura de pastas e leitura em lote
- Compatível com Windows e Linux

---

<h2>🖼️ Exemplos visuais</h2>

<p>Prints do funcionamento completo antes da expiração da API:</p>

<img src="assets/prints_exemplo/TorreEiffel_Photo_Info_Manager.jpg" alt="Torre Eiffel" width="600"/>
<img src="assets/prints_exemplo/EstatuaDaLiberdade_Photo_Info_Manager.jpg" alt="Estátua da Liberdade" width="600"/>

---

## 🧠 Sobre o desenvolvimento

Este projeto foi desenvolvido como uma forma de aprendizado prático em Python e construção de interfaces gráficas com PySide6.

Durante o processo, utilizei o **ChatGPT** como ferramenta de apoio técnico. A IA foi usada para:
- Ajudar a estruturar trechos de código
- Sugerir formas de organizar funções
- Resolver erros pontuais
- Criar métodos de integração entre a lógica e a interface `.ui`

Todas as implementações passaram por **curadoria e adaptação pessoal**. O objetivo foi aprender ativamente, entender o funcionamento das ferramentas, e estruturar um projeto funcional de forma progressiva.  

Essa abordagem me permitiu focar em entender conceitos e resolver problemas, algo que acredito ser essencial no desenvolvimento moderno.

---

## 🚀 Como executar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/photo-info-manager.git
   cd photo-info-manager
