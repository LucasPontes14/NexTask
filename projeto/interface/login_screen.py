import customtkinter as ctk
from tkinter import messagebox
from interface.main_screen import TelaPrincipal

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

PRETO      = "#0a0a0a"
VERDE_NEON = "#00ff41"
VERDE_ESC  = "#00cc33"
CINZA_CARD = "#141414"
CINZA_BRD  = "#2a2a2a"
BRANCO     = "#f0f0f0"
CINZA_TEXT = "#888888"
ERRO       = "#ff4444"


class TelaLogin(ctk.CTk):
    def __init__(self, usuario_service, lista_service, tarefa_service): 
        super().__init__()

        self.usuario_service = usuario_service
        self.lista_service   = lista_service   
        self.tarefa_service  = tarefa_service  
        self.title("NexTask - Gerenciador de Tarefas")
        self.geometry("1920x1080")
        self.configure(fg_color=PRETO)
        self._construir_ui()

    def _construir_ui(self):
        frame_logo = ctk.CTkFrame(self, fg_color="transparent")
        frame_logo.pack(pady=(48, 0))

        ctk.CTkLabel(
            frame_logo,
            text="▶ NexTask",
            font=("JetBrains Mono", 28, "bold"),
            text_color=BRANCO,
        ).pack()

        ctk.CTkLabel(
            frame_logo,
            text="Gerenciador de Tarefas",
            font=("JetBrains Mono", 11),
            text_color=CINZA_TEXT,
        ).pack(pady=(4, 0))

        card = ctk.CTkFrame(
            self,
            fg_color=CINZA_CARD,
            corner_radius=12,
            border_width=1,
            border_color=CINZA_BRD,
        )
        card.pack(padx=36, pady=32, fill="x")

        ctk.CTkLabel(
            card,
            text="Entrar",
            font=("JetBrains Mono", 22, "bold"),
            text_color=BRANCO,
        ).pack(anchor="w", padx=28, pady=(28, 20))

        ctk.CTkLabel(
            card,
            text="E-MAIL",
            font=("JetBrains Mono", 10),
            text_color=CINZA_TEXT,
        ).pack(anchor="w", padx=28)

        self.campo_email = ctk.CTkEntry(
            card,
            placeholder_text="seu@email.com",
            font=("JetBrains Mono", 13),
            height=44,
            corner_radius=8,
            fg_color="#1a1a1a",
            border_color=CINZA_BRD,
            border_width=1,
            text_color=BRANCO,
        )
        self.campo_email.pack(padx=28, pady=(4, 16), fill="x")

        ctk.CTkLabel(
            card,
            text="SENHA",
            font=("JetBrains Mono", 10),
            text_color=CINZA_TEXT,
        ).pack(anchor="w", padx=28)

        self.campo_senha = ctk.CTkEntry(
            card,
            placeholder_text="••••••••",
            font=("JetBrains Mono", 13),
            height=44,
            corner_radius=8,
            fg_color="#1a1a1a",
            border_color=CINZA_BRD,
            border_width=1,
            text_color=BRANCO,
            show="•",
        )
        self.campo_senha.pack(padx=28, pady=(4, 8), fill="x")
        self.campo_senha.bind("<Return>", lambda e: self._entrar())

        self.label_erro = ctk.CTkLabel(
            card,
            text="",
            font=("JetBrains Mono", 11),
            text_color=ERRO,
        )
        self.label_erro.pack(padx=28, anchor="w")

        self.botao_entrar = ctk.CTkButton(
            card,
            text="Entrar →",
            font=("JetBrains Mono", 14, "bold"),
            height=48,
            corner_radius=8,
            fg_color=VERDE_NEON,
            hover_color=VERDE_ESC,
            text_color=PRETO,
            command=self._entrar,
        )
        self.botao_entrar.pack(padx=28, pady=(12, 20), fill="x")

        ctk.CTkFrame(card, height=1, fg_color=CINZA_BRD).pack(padx=28, fill="x")

        frame_rodape = ctk.CTkFrame(card, fg_color="transparent")
        frame_rodape.pack(pady=16)

        ctk.CTkLabel(
            frame_rodape,
            text="Sem conta?",
            font=("JetBrains Mono", 12),
            text_color=CINZA_TEXT,
        ).pack(side="left")

        ctk.CTkButton(
            frame_rodape,
            text=" Cadastrar-se",
            font=("JetBrains Mono", 12, "bold"),
            text_color=VERDE_NEON,
            fg_color="transparent",
            hover_color="#1a1a1a",
            width=0,
            command=self._abrir_cadastro,
        ).pack(side="left")

    def _entrar(self):
        email = self.campo_email.get().strip()
        senha = self.campo_senha.get()

        if not email or not senha:
            self._mostrar_erro("Preencha e-mail e senha.")
            return

        try:
            usuario = self.usuario_service.buscar_usuario_por_email(email)

            if usuario is None or usuario.senha != senha:
                self._mostrar_erro("E-mail ou senha incorretos.")
                return

            self._mostrar_erro("")
            self._abrir_tela_principal(usuario)

        except Exception as e:
            self._mostrar_erro(f"Erro: {e}")

    def _mostrar_erro(self, mensagem: str):
        self.label_erro.configure(text=mensagem)

    def _abrir_cadastro(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._construir_ui_cadastro()

    def _construir_ui_cadastro(self):
        frame_logo = ctk.CTkFrame(self, fg_color="transparent")
        frame_logo.pack(pady=(48, 0))

        ctk.CTkLabel(
            frame_logo,
            text="▶ NexTask",
            font=("JetBrains Mono", 28, "bold"),
            text_color=BRANCO,
        ).pack()

        ctk.CTkLabel(
            frame_logo,
            text="Gerenciador de Tarefas",
            font=("JetBrains Mono", 11),
            text_color=CINZA_TEXT,
        ).pack(pady=(4, 0))

        card = ctk.CTkFrame(self, fg_color=CINZA_CARD, corner_radius=12,
                            border_width=1, border_color=CINZA_BRD)
        card.pack(padx=600, pady=10, fill="x")

        ctk.CTkLabel(card, text="Cadastrar-se",
                     font=("JetBrains Mono", 22, "bold"),
                     text_color=BRANCO).pack(anchor="w", padx=28, pady=(16, 10))

        campos = [
            ("NOME",   "Seu nome",      False),
            ("E-MAIL", "seu@email.com", False),
            ("SENHA",  "••••••••",      True),
        ]

        self.entradas = {}
        for label, placeholder, oculto in campos:
            ctk.CTkLabel(card, text=label, font=("JetBrains Mono", 10),
                         text_color=CINZA_TEXT).pack(anchor="w", padx=28)
            entrada = ctk.CTkEntry(card, placeholder_text=placeholder,
                                   font=("JetBrains Mono", 13), height=44,
                                   corner_radius=8, fg_color="#1a1a1a",
                                   border_color=CINZA_BRD, border_width=1,
                                   text_color=BRANCO,
                                   show="•" if oculto else "")
            entrada.pack(padx=28, pady=(4, 6), fill="x")
            self.entradas[label] = entrada

        self.label_erro = ctk.CTkLabel(card, text="",
                                       font=("JetBrains Mono", 11),
                                       text_color=ERRO)
        self.label_erro.pack(padx=28, anchor="w")

        ctk.CTkButton(card, text="Criar conta →",
                      font=("JetBrains Mono", 14, "bold"), height=48,
                      corner_radius=8, fg_color=VERDE_NEON,
                      hover_color=VERDE_ESC, text_color=PRETO,
                      command=self._cadastrar).pack(padx=28, pady=(8, 10), fill="x")

        ctk.CTkFrame(card, height=1, fg_color=CINZA_BRD).pack(padx=28, fill="x")

        frame_rodape = ctk.CTkFrame(card, fg_color="transparent")
        frame_rodape.pack(pady=12)
        ctk.CTkLabel(frame_rodape, text="Já tem conta?",
                     font=("JetBrains Mono", 12),
                     text_color=CINZA_TEXT).pack(side="left")
        ctk.CTkButton(frame_rodape, text=" Entrar",
                      font=("JetBrains Mono", 12, "bold"),
                      text_color=VERDE_NEON, fg_color="transparent",
                      hover_color="#1a1a1a", width=0,
                      command=self._voltar_login).pack(side="left")

    def _cadastrar(self):
        nome  = self.entradas["NOME"].get().strip()
        email = self.entradas["E-MAIL"].get().strip()
        senha = self.entradas["SENHA"].get()

        try:
            usuario = self.usuario_service.cadastrar_usuario(nome, email, senha)
            self._abrir_tela_principal(usuario)
        except ValueError as e:
            self.label_erro.configure(text=str(e))

    def _abrir_tela_principal(self, usuario):
        for widget in self.winfo_children():
            widget.destroy()
        from interface.main_screen import TelaPrincipal
        TelaPrincipal(self, usuario, self.usuario_service, self.lista_service, self.tarefa_service)

    def _voltar_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._construir_ui()