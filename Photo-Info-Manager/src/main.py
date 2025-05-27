import sys, os ,subprocess, selecionar, json
def resource_path(relative_path):
    """Obtém o caminho absoluto do recurso, seja no .exe ou no script."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QMessageBox, QGraphicsDropShadowEffect, QLabel, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QBrush, QFont, QPen, QIcon


class animacao_btn(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.hovered = False
        self.offset = 0
        self.direction = 1  # 1 = direita, -1 = esquerda
        self.background_opacity = 0.0  # controla opacidade do gradiente
        self.setFont(QFont("Segoe UI", 10, 900, True))
        self.setStyleSheet(
            """
            QPushButton {
                border-radius: 10px;
                border: 2px solid #000000;
                color: white;
                font: 900 italic 10pt "Segoe UI";
                text-align: center;
            }
            """
        )
        self.setAttribute(Qt.WA_Hover, True)

        # Timer para animar o gradiente e a opacidade
        self.timer = QTimer(self)
        self.timer.setInterval(30)  # ~33 fps
        self.timer.timeout.connect(self.animate)

    def enterEvent(self, event):
        self.hovered = True
        self.timer.start()
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.timer.start()
        self.update()
        super().leaveEvent(event)

    def animate(self):
        step = 5
        if self.hovered:
            self.offset += step * self.direction
            if self.offset > self.width():
                self.offset = self.width()
                self.direction = -1
            elif self.offset < -self.width():
                self.offset = -self.width()
                self.direction = 1

            # Aumentar opacidade gradualmente até 1
            self.background_opacity = min(self.background_opacity + 0.05, 1.0)
        else:
            # Diminuir opacidade gradualmente até 0
            self.background_opacity = max(self.background_opacity - 0.05, 0.0)
            if self.background_opacity == 0.0:
                self.timer.stop()
                self.offset = 0
                self.direction = 1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setFont(self.font())

        rect = self.rect()

        # Cor de fundo baseada no hover
        base_color = QColor(255, 255, 255) if self.hovered else QColor(44, 62, 80)
        painter.setBrush(base_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)  # Usa o mesmo raio de borda do estilo

        # Desenha a borda
        border_color = QColor(0, 0, 0)
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 10, 10)

        # Gradiente animado no texto, se necessário
        if self.hovered or self.background_opacity > 0:
            grad = QLinearGradient(self.offset, 0, self.offset + self.width(), 0)
            grad.setColorAt(0.3, QColor(0, 0, 0, int(255 * self.background_opacity)))
            grad.setColorAt(0.7, QColor(255, 255, 255, int(255 * self.background_opacity)))
            grad.setColorAt(0.8, QColor(0, 0, 0, int(255 * self.background_opacity)))
            grad.setColorAt(1.0, QColor(0, 0, 0, int(255 * self.background_opacity)))
            painter.setPen(QPen(QBrush(grad), 0))
        else:
            painter.setPen(QColor("white"))

        # Desenha o texto centralizado
        painter.drawText(rect, Qt.AlignCenter, self.text())


class animacao_labels(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.texto_exibido = text
        self.hovered = False
        self.offset = 0
        self.direction = 1  # 1 = direita, -1 = esquerda
        self.background_opacity = 0.0  # controla opacidade do fundo e sombra
        self.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.setAttribute(Qt.WA_Hover, True)

        # Timer para animar
        self.timer = QTimer(self)
        self.timer.setInterval(30)  # ~33 fps
        self.timer.timeout.connect(self.animate)

    def setText(self, text):
        self.texto_exibido = text
        super().setText(text)  # Ainda atualiza internamente
        self.update()  # Força o repaint para mostrar o novo texto

    def enterEvent(self, event):
        self.hovered = True
        self.timer.start()
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        # Continua o timer para animar a opacidade até sumir
        self.timer.start()

    def animate(self):
        step = 5
        # Animar o gradiente só se estiver hover
        if self.hovered:
            self.offset += step * self.direction
            if self.offset > self.width():
                self.offset = self.width()
                self.direction = -1
            elif self.offset < -self.width():
                self.offset = -self.width()
                self.direction = 1

            # Aumentar opacidade gradualmente até 1
            self.background_opacity = min(self.background_opacity + 0.05, 1.0)

        else:
            # Diminuir opacidade gradualmente até 0
            self.background_opacity = max(self.background_opacity - 0.05, 0.0)
            if self.background_opacity == 0.0:
                # Para o timer quando opacidade chegar a zero
                self.timer.stop()
                # Resetar o offset e direção para estado inicial, se quiser
                self.offset = 0
                self.direction = 1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setFont(self.font())

        rect = self.rect()
        text = self.texto_exibido

        painter.setPen(QColor(0, 0, 0))

        # Texto base preto
        painter.setPen(QColor(0, 0, 0))
        #painter.drawText(rect, Qt.AlignCenter, text)
        alignment = self.alignment() if self.alignment() else Qt.AlignCenter
        painter.drawText(rect.adjusted(10, 10, -10, -10), alignment, text)



        if self.hovered or self.background_opacity > 0:
            # Gradiente animado com ida e volta
            grad = QLinearGradient(self.offset, -200, self.offset + self.width(), 0)
            grad.setColorAt(0.3, QColor(0, 0, 0))          # Preto (margem esquerda)
            grad.setColorAt(0.7, QColor(255, 255, 255))    # Branco (pico claro)
            grad.setColorAt(0.80, QColor(0, 0, 0))          # Preto (margem direita)
            grad.setColorAt(1.00, QColor(0, 0, 0))          # Reforço do preto

            painter.setPen(QPen(QBrush(grad), 0))
            
            painter.drawText(rect.adjusted(10, 10, -10, -10), alignment, text)

def get_caminho_absoluto_arquivo(nome_arquivo):
    if getattr(sys, 'frozen', False):
        # Executável criado com PyInstaller
        caminho_base = sys._MEIPASS  # Onde estão os arquivos temporários extraídos
        caminho_executavel = os.path.dirname(sys.executable)
    else:
        # Rodando como script .py
        caminho_executavel = os.path.dirname(__file__)
    
    return os.path.join(caminho_executavel, nome_arquivo)


class Temporizador:

    def __init__(self, minutos_limite=10):
        self.inicio = datetime.now()
        self.limite = timedelta(minutes=minutos_limite)

    def tempo_restante(self):
        agora = datetime.now()

        restante = (self.inicio + self.limite) - agora
        if restante.total_seconds() <= 0:
            return timedelta(seconds=0)
        return restante

    def tempo_excedido(self):
        return self.tempo_restante().total_seconds() <= 0

    @staticmethod
    def formatar_tempo(tdelta):
        total_segundos = int(tdelta.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    def salvar_inicio(self, caminho="registro_inicio.json"):
        
        with open(caminho, "w") as f:
            json.dump({"inicio": self.inicio.isoformat()}, f)

    def carregar_inicio(self, caminho="registro_inicio.json"):
        caminho_arquivo = get_caminho_absoluto_arquivo(caminho)
        if os.path.exists(caminho_arquivo):
            with open(caminho, "r") as f:
                data = json.load(f)
                self.inicio = datetime.fromisoformat(data["inicio"])


class MainApp:

    def __init__(self):
        self.app = QApplication(sys.argv)

        # Carrega o arquivo .ui
        loader = QUiLoader()
        ui_file = QFile(resource_path("ui/mainwindow.ui"))  # Caminho relativo

        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Erro ao abrir UI: {ui_file.errorString()}")
            sys.exit(-1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if not self.window:
            print("Erro ao carregar janela principal do UI.")
            sys.exit(-1)

        self.customizar_interface()
        frame_geo = self.window.frameGeometry()
        center_point = self.app.primaryScreen().availableGeometry().center()
        frame_geo.moveCenter(center_point)
        self.window.move(frame_geo.topLeft())

        self.window.show()
        sys.exit(self.app.exec())
        



    def aplicar_sombra(self, widget):
        sombra = QGraphicsDropShadowEffect(widget)
        sombra.setBlurRadius(20)
        sombra.setOffset(0, -2)
        sombra.setColor(QColor(0, 0, 0, 180))
        widget.setGraphicsEffect(sombra)

    def criar_label(self,original_label,objectName=None, texto =""):
            
        isolar = original_label 
        if objectName is None: objectName = isolar.objectName()
        label_animado = animacao_labels(texto, parent=isolar.parent())
        label_animado.setGeometry(isolar.geometry())
        label_animado.setObjectName(objectName)
        label_animado.setAlignment(Qt.AlignCenter)
        label_animado.show()
        isolar.hide()


    def criar_botoes(self,original_button, texto, evento):
        isolar = original_button
        botao_animado = animacao_btn(texto, parent=isolar.parent())
        botao_animado.setGeometry(isolar.geometry())
        botao_animado.setObjectName(isolar.objectName())  
        isolar.hide()
        botao_animado.show()
        botao_animado.clicked.connect(evento)
        self.aplicar_sombra(botao_animado)


    def atualizar_tempo_restante(self):
        restante = self.temporizador.tempo_restante()
        tempo_formatado = self.temporizador.formatar_tempo(restante)

        self.label_temporizador.setText(f"Você tem {tempo_formatado} de tempo disponível.\nAproveite!!\nCriador: JyanDev (GitHub)")

        if restante.total_seconds() <= 0:
            QMessageBox.warning(self.window, "Tempo Esgotado", "O tempo de uso terminou. O programa será encerrado.")
            self.app.quit()


    def customizar_interface(self):


        self.window.setWindowIcon(QIcon(resource_path("imagens/Logo.ico")))  
        self.window.setFixedSize(self.window.size())  # Impede redimensionamento
        self.window.setWindowFlag(Qt.WindowMaximizeButtonHint, False)  # Remove maximizar, mas mantém fechar


        #--------------------------- Labels --------------------------------------
        
        self.criar_label(self.window.label_3, None, "Selecionar  imagens:")
        self.criar_label(self.window.label_4, None, "Imagens prontas :")
        self.criar_label(self.window.label_5, None, "Suporte:")  
        original = self.window.label_6
        self.label_animado_suporte = animacao_labels(    " Passo a passo:\n"
                                                            "1. Clique em \"Selecionar\" e escolha as imagens desejadas.\n"
                                                            "2. Pressione \"OK\" para confirmar.\n"
                                                            "3. Após o carregamento, clique em \"Localizar\" para abrir a pasta das imagens.\n\n"
                                                            " Atenção:\n"
                                                            "Se a mensagem \"Sem dados\" aparecer, a imagem não contém metadados.\n"
                                                            "Nesse caso, a extração de informações não será possível.\n"
                                                            "Em caso de dúvidas ou erros, entre em contato: suporteteste@gmail.com"
                                                            , parent=original.parent())
        self.label_animado_suporte.setGeometry(original.geometry())
        self.label_animado_suporte.setObjectName("label_6")
        self.label_animado_suporte.setWordWrap(True)
        self.label_animado_suporte.setVisible(False)
        original.hide()     
        original = self.window.label_8  # Label texto: "Suporte"
        label_animado = animacao_labels("Photo Info Manager", parent=original.parent())
        label_animado.setGeometry(original.geometry())
        label_animado.setObjectName("label_8")
        label_animado.setAlignment(Qt.AlignCenter)
        sombra = QGraphicsDropShadowEffect(label_animado)
        sombra.setBlurRadius(20)
        sombra.setOffset(3, 3)
        sombra.setColor(QColor(0, 0, 0, 200))  # sombra preta semi-transparente
        fonte = QFont("Consolas", 30)
        fonte.setUnderline(True)
        label_animado.setFont(fonte)
        label_animado.setGraphicsEffect(sombra)
        label_animado.show()
        original.hide()



        #--------------------------- Botões --------------------------------------
        self.criar_botoes(self.window.pushButton, "Localizar", self.acao_botao_localizar)
        self.criar_botoes(self.window.pushButton_2, "Selecionar", self.acao_botao_selecionar)
        self.criar_botoes(self.window.pushButton_3, "Ajuda", self.acao_botao_ajuda)
        
         #--------------------------- Fundo dinâmico --------------------------------------

        self.window.label.setPixmap(QPixmap(resource_path("imagens/fundo.jpeg"))) 
   
        pixmap = QPixmap(resource_path("imagens/icon.png"))
        self.window.label_7.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Efeito de brilho
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setColor(QColor(0, 255, 255))  # Azul claro para testar
        glow.setOffset(0, 0)

        # Aplicar
        self.window.label_7.setGraphicsEffect(glow)
        self.window.label_7.move(350, -30)  


        faixa = self.window.label_2
        faixa.clear()
        faixa.setStyleSheet("""
                            background-color: white; 
                            border-radius: 20px; 
                            border: 1px solid #ccc""")
        self.aplicar_sombra(faixa)
         
        # Temporizador integrado
        self.temporizador = Temporizador(minutos_limite=240)

        if os.path.exists(get_caminho_absoluto_arquivo("registro_inicio.json")):
            self.temporizador.carregar_inicio()
        else:
            self.temporizador.salvar_inicio()
        self.label_temporizador = QLabel("", parent=self.window.label_9.parent())
        self.label_temporizador.setGeometry(self.window.label_9.geometry())
        self.label_temporizador.setObjectName("label_9_temporizador")
        self.label_temporizador.setAlignment(Qt.AlignCenter)
        self.label_temporizador.setStyleSheet("background-color: rgba(255,255,255,200); border-radius: 12px; font: bold 14pt 'Segoe UI'; color: black;")
        self.label_temporizador.show()
        self.window.label_9.hide()

        self.timer_interface = QTimer()
        self.timer_interface.setInterval(1000)
        self.timer_interface.timeout.connect(self.atualizar_tempo_restante)
        self.timer_interface.start()

        # Criar label animado do temporizador uma única vez
        self.label_temporizador = animacao_labels("", parent=self.window.label_9.parent())
        self.label_temporizador.setGeometry(self.window.label_9.geometry())
        self.label_temporizador.setObjectName("label_9_animado")
        self.label_temporizador.setAlignment(Qt.AlignCenter)
        self.label_temporizador.show()
        self.window.label_9.hide()





    def acao_botao_ajuda(self):
        if not self.label_animado_suporte.isVisible():
            # Aplica sombra arredondada com fundo branco opaco personalizado
            sombra = QGraphicsDropShadowEffect(self.label_animado_suporte)
            sombra.setBlurRadius(20)
            sombra.setOffset(3, 3)
            sombra.setColor(QColor(0, 0, 0, 255))  # sombra preta semi-transparente
            self.label_animado_suporte.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.label_animado_suporte.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            self.label_animado_suporte.setGraphicsEffect(sombra)

            # Estilo com fundo branco semi-transparente e cantos arredondados
            self.label_animado_suporte.setStyleSheet("""
            background-color: rgba(255, 255, 255, 200);
            border-radius: 12px;
            padding: 10px;
        """)
        
        visivel = self.label_animado_suporte.isVisible()
        self.label_animado_suporte.setVisible(not visivel)
    
    def acao_botao_selecionar(self):
        selecionar.run()

    def acao_botao_localizar(self):
        caminho = selecionar.obter_caminho_pasta_fotos()

        if os.path.exists(caminho):
            # Abrir no explorador (funciona no Windows)
            if sys.platform == "win32":
                os.startfile(caminho)
            else:
                # Compatível com outros sistemas
                subprocess.Popen(["xdg-open", caminho])
        else:
            self.acao_botao_ajuda()
if __name__ == "__main__":
    MainApp()
