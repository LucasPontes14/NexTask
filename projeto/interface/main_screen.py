import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime

PRETO      = "#0a0a0a"
VERDE_NEON = "#00ff41"
VERDE_ESC  = "#00cc33"
CINZA_CARD = "#141414"
CINZA_BRD  = "#2a2a2a"
CINZA_LADO = "#0f0f0f"
BRANCO     = "#f0f0f0"
CINZA_TEXT = "#888888"
ERRO       = "#ff4444"
AZUL_TAG   = "#1a3a2a"


def _parse_data(texto: str):

    texto = (texto or "").strip()
    if not texto:
        return None
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError('Data inválida. Use o formato dd/mm/aaaa.')


def _formatar_data(valor) -> str:

    if not valor:
        return ""
    if isinstance(valor, str):

        try:
            valor = datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError:
            return valor
    return valor.strftime("%d/%m/%Y")


class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, pai, usuario, lista_service, tarefa_service):
        super().__init__(pai, fg_color=PRETO)

        self.usuario        = usuario
        self.lista_service  = lista_service
        self.tarefa_service = tarefa_service
        self.lista_selecionada = None
        self.sidebar_visivel = True

        self.pack(fill="both", expand=True)

        self._construir_ui()
        self._carregar_listas()
        self._carregar_tarefas()

    def _construir_ui(self):
        self.barra_top = ctk.CTkFrame(self, fg_color=CINZA_CARD,
                                      border_width=1, border_color=CINZA_BRD,
                                      height=52, corner_radius=0)
        self.barra_top.pack(fill="x", side="top")
        self.barra_top.pack_propagate(False)

        frame_esq = ctk.CTkFrame(self.barra_top, fg_color="transparent")
        frame_esq.pack(side="left", padx=(12, 0))

        ctk.CTkButton(frame_esq, text="☰",
                      font=("JetBrains Mono", 16, "bold"),
                      fg_color="transparent", text_color=BRANCO,
                      hover_color=CINZA_BRD, width=32, height=32,
                      corner_radius=6,
                      command=self._alternar_sidebar).pack(side="left")

        ctk.CTkLabel(frame_esq, text="▶ NexTask",
                     font=("JetBrains Mono", 15, "bold"),
                     text_color=VERDE_NEON).pack(side="left", padx=(8, 0))

        frame_dir = ctk.CTkFrame(self.barra_top, fg_color="transparent")
        frame_dir.pack(side="right", padx=16)

        ctk.CTkLabel(frame_dir,
                     text=self.usuario.nome.split()[0].lower(),
                     font=("JetBrains Mono", 12),
                     text_color=CINZA_TEXT).pack(side="left", padx=(0, 12))

        ctk.CTkButton(frame_dir, text="Config",
                      font=("JetBrains Mono", 12),
                      fg_color="transparent", border_width=1,
                      border_color=CINZA_BRD, text_color=BRANCO,
                      hover_color=CINZA_CARD, width=80, height=30,
                      corner_radius=6).pack(side="left", padx=(0, 8))

        ctk.CTkButton(frame_dir, text="Sair",
                      font=("JetBrains Mono", 12),
                      fg_color="transparent", border_width=1,
                      border_color=CINZA_BRD, text_color=BRANCO,
                      hover_color="#2a0a0a", width=60, height=30,
                      corner_radius=6,
                      command=self._sair).pack(side="left")

        self.frame_corpo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_corpo.pack(fill="both", expand=True)

        self._construir_sidebar()
        self._construir_area_principal()

    def _alternar_sidebar(self):
        if self.sidebar_visivel:
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side="left", fill="y", before=self.area_principal)
        self.sidebar_visivel = not self.sidebar_visivel

    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.frame_corpo, fg_color=CINZA_LADO,
                                    width=270, corner_radius=0,
                                    border_width=1, border_color=CINZA_BRD)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        frame_contadores = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_contadores.pack(fill="x", padx=12, pady=(12, 8))

        self.card_pendentes = self._criar_card_contador(
            frame_contadores, "0", "PENDENTES", VERDE_NEON, "#0a1f0a")
        self.card_pendentes.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.card_concluidas = self._criar_card_contador(
            frame_contadores, "0", "CONCLUÍDAS", "#00aaff", "#0a0f1f")
        self.card_concluidas.pack(side="left", expand=True, fill="x")

        frame_listas_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_listas_header.pack(fill="x", padx=16, pady=(12, 4))

        ctk.CTkLabel(frame_listas_header, text="LISTAS",
                     font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(side="left")

        ctk.CTkButton(frame_listas_header, text="+",
                      font=("JetBrains Mono", 14, "bold"),
                      fg_color="transparent", text_color=VERDE_NEON,
                      hover_color=CINZA_CARD, width=24, height=24,
                      command=self._nova_lista).pack(side="right")

        self.botao_todas = ctk.CTkButton(
            self.sidebar, text="◆  Todas",
            font=("JetBrains Mono", 13, "bold"),
            fg_color=AZUL_TAG, text_color=VERDE_NEON,
            hover_color=AZUL_TAG, anchor="w",
            corner_radius=6, height=36,
            command=lambda: self._selecionar_lista(None))
        self.botao_todas.pack(fill="x", padx=12, pady=(0, 2))

        self.frame_listas = ctk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent", corner_radius=0)
        self.frame_listas.pack(fill="both", expand=True, padx=12)

        self.label_sem_listas = ctk.CTkLabel(
            self.sidebar, text="Nenhuma lista. Crie uma!",
            font=("JetBrains Mono", 11), text_color=CINZA_TEXT)
        self.label_sem_listas.pack(pady=8)

    def _criar_card_contador(self, pai, valor, rotulo, cor_valor, cor_fundo):
        card = ctk.CTkFrame(pai, fg_color=cor_fundo,
                            corner_radius=8, border_width=1,
                            border_color=CINZA_BRD)
        ctk.CTkLabel(card, text=valor,
                     font=("JetBrains Mono", 22, "bold"),
                     text_color=cor_valor).pack(pady=(8, 0))
        ctk.CTkLabel(card, text=rotulo,
                     font=("JetBrains Mono", 9),
                     text_color=CINZA_TEXT).pack(pady=(0, 8))
        return card

    def _construir_area_principal(self):
        self.area_principal = ctk.CTkFrame(
            self.frame_corpo, fg_color="transparent")
        self.area_principal.pack(side="left", fill="both", expand=True)

        header = ctk.CTkFrame(self.area_principal, fg_color="transparent",
                              height=52)
        header.pack(fill="x", padx=24, pady=(16, 8))
        header.pack_propagate(False)

        self.label_titulo_area = ctk.CTkLabel(
            header, text="Todas as tarefas (0)",
            font=("JetBrains Mono", 18, "bold"), text_color=BRANCO)
        self.label_titulo_area.pack(side="left")

        frame_acoes = ctk.CTkFrame(header, fg_color="transparent")
        frame_acoes.pack(side="right")

        self.filtro_prioridade = ctk.CTkOptionMenu(
            frame_acoes,
            values=["Prioridade", "alta", "media", "baixa"],
            font=("JetBrains Mono", 12),
            fg_color=CINZA_CARD, button_color=CINZA_BRD,
            button_hover_color=CINZA_BRD, text_color=BRANCO,
            dropdown_fg_color=CINZA_CARD,
            width=140, height=34, corner_radius=6,
            command=self._aplicar_filtro)
        self.filtro_prioridade.pack(side="left", padx=(0, 8))

        self.filtro_status = ctk.CTkOptionMenu(
            frame_acoes,
            values=["Status", "pendente", "em_andamento", "concluida"],
            font=("JetBrains Mono", 12),
            fg_color=CINZA_CARD, button_color=CINZA_BRD,
            button_hover_color=CINZA_BRD, text_color=BRANCO,
            dropdown_fg_color=CINZA_CARD,
            width=140, height=34, corner_radius=6,
            command=self._aplicar_filtro)
        self.filtro_status.pack(side="left", padx=(0, 8))

        ctk.CTkButton(frame_acoes, text="+ Criar tarefa",
                      font=("JetBrains Mono", 13, "bold"),
                      fg_color=VERDE_NEON, hover_color=VERDE_ESC,
                      text_color=PRETO, height=34, corner_radius=6,
                      command=self._nova_tarefa).pack(side="left")

        self.frame_tarefas = ctk.CTkScrollableFrame(
            self.area_principal, fg_color="transparent", corner_radius=0)
        self.frame_tarefas.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.frame_vazio = ctk.CTkFrame(
            self.area_principal, fg_color="transparent")

        ctk.CTkLabel(self.frame_vazio, text="◆",
                     font=("JetBrains Mono", 32),
                     text_color=VERDE_NEON).pack(pady=(80, 8))
        ctk.CTkLabel(self.frame_vazio, text="Crie uma lista para começar",
                     font=("JetBrains Mono", 14),
                     text_color=CINZA_TEXT).pack()
        ctk.CTkButton(self.frame_vazio, text="+ Nova lista",
                      font=("JetBrains Mono", 13),
                      fg_color="transparent", border_width=1,
                      border_color=VERDE_NEON, text_color=VERDE_NEON,
                      hover_color=AZUL_TAG, height=36, corner_radius=6,
                      command=self._nova_lista).pack(pady=16)

        self.frame_sem_tarefas = ctk.CTkFrame(
            self.area_principal, fg_color="transparent")

        ctk.CTkLabel(self.frame_sem_tarefas, text="◇",
                     font=("JetBrains Mono", 32),
                     text_color=CINZA_TEXT).pack(pady=(80, 8))
        ctk.CTkLabel(self.frame_sem_tarefas, text="Nenhuma tarefa por aqui",
                     font=("JetBrains Mono", 14),
                     text_color=CINZA_TEXT).pack()

    def _carregar_listas(self):
        for w in self.frame_listas.winfo_children():
            w.destroy()

        listas = self.lista_service.listar_por_usuario(
            self.usuario.id_usuario)

        if not listas:
            self.label_sem_listas.pack(pady=8)
        else:
            self.label_sem_listas.pack_forget()
            for lista in listas:
                self._criar_botao_lista(lista)

    def _criar_botao_lista(self, lista):
        linha = ctk.CTkFrame(self.frame_listas, fg_color="transparent")
        linha.pack(fill="x", pady=1)

        btn = ctk.CTkButton(
            linha,
            text=f"◇  {lista.nome}",
            font=("JetBrains Mono", 12),
            fg_color="transparent", text_color=CINZA_TEXT,
            hover_color=CINZA_CARD, anchor="w",
            corner_radius=6, height=32,
            command=lambda l=lista: self._selecionar_lista(l))
        btn.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            linha, text="✎", width=28, height=28,
            font=("JetBrains Mono", 12),
            fg_color="transparent", text_color=CINZA_TEXT,
            hover_color=CINZA_CARD, corner_radius=6,
            command=lambda l=lista: self._editar_lista(l)
        ).pack(side="left", padx=(2, 0))

        ctk.CTkButton(
            linha, text="✕", width=28, height=28,
            font=("JetBrains Mono", 12),
            fg_color="transparent", text_color=CINZA_TEXT,
            hover_color="#2a0a0a", corner_radius=6,
            command=lambda l=lista: self._excluir_lista(l)
        ).pack(side="left", padx=(2, 0))

    def _tarefa_atrasada(self, tarefa) -> bool:
        if not tarefa.data_venc or tarefa.status == "concluida":
            return False
        venc = tarefa.data_venc
        if isinstance(venc, str):
            try:
                venc = datetime.strptime(venc, "%Y-%m-%d").date()
            except ValueError:
                return False
        elif isinstance(venc, datetime):
            venc = venc.date()
        return venc < date.today()

    def _carregar_tarefas(self):
        for w in self.frame_tarefas.winfo_children():
            w.destroy()

        if self.lista_selecionada is None:
            tarefas = self.tarefa_service.listar_todas()
            titulo  = "Todas as tarefas"
        else:
            tarefas = self.tarefa_service.listar_tarefas(
                self.lista_selecionada.id_lista)
            titulo  = self.lista_selecionada.nome

        prioridade = self.filtro_prioridade.get()
        status     = self.filtro_status.get()

        if prioridade != "Prioridade":
            tarefas = [t for t in tarefas if t.prioridade == prioridade]
        if status != "Status":
            tarefas = [t for t in tarefas if t.status == status]

        pendentes  = sum(1 for t in tarefas if t.status != "concluida")
        concluidas = sum(1 for t in tarefas if t.status == "concluida")

        self.label_titulo_area.configure(text=f"{titulo} ({len(tarefas)})")
        self.card_pendentes.winfo_children()[0].configure(text=str(pendentes))
        self.card_concluidas.winfo_children()[0].configure(text=str(concluidas))

        if not tarefas:
            self.frame_sem_tarefas.place_forget()
            self.frame_vazio.place_forget()

            existem_listas = bool(
                self.lista_service.listar_por_usuario(self.usuario.id_usuario))

            if self.lista_selecionada is None and not existem_listas:
                self.frame_vazio.place(relx=0.5, rely=0.5, anchor="center")
            else:
                self.frame_sem_tarefas.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.frame_vazio.place_forget()
            self.frame_sem_tarefas.place_forget()
            for tarefa in tarefas:
                self._criar_card_tarefa(tarefa)

    def _criar_card_tarefa(self, tarefa):
        cor_prioridade = {
            "alta":  "#ff4444",
            "media": "#ffaa00",
            "baixa": "#00aaff",
        }.get(tarefa.prioridade, CINZA_TEXT)

        cor_status = {
            "pendente":     "#ffaa00",
            "em_andamento": "#00aaff",
            "concluida":    VERDE_NEON,
        }.get(tarefa.status, CINZA_TEXT)

        atrasada = self._tarefa_atrasada(tarefa)

        card = ctk.CTkFrame(self.frame_tarefas, fg_color=CINZA_CARD,
                            corner_radius=8, border_width=1,
                            border_color=CINZA_BRD)
        card.pack(fill="x", pady=4)

        ctk.CTkFrame(card, fg_color=cor_prioridade,
                     width=4, corner_radius=0).pack(side="left", fill="y")

        checkbox_var = ctk.BooleanVar(value=(tarefa.status == "concluida"))
        ctk.CTkCheckBox(
            card, text="", variable=checkbox_var,
            width=20, height=20, corner_radius=4,
            fg_color=VERDE_NEON, hover_color=VERDE_ESC,
            border_color=CINZA_BRD, checkmark_color=PRETO,
            command=lambda t=tarefa: self._toggle_status(t)
        ).pack(side="left", padx=(10, 4))

        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        linha_top = ctk.CTkFrame(corpo, fg_color="transparent")
        linha_top.pack(fill="x")

        ctk.CTkLabel(linha_top, text=tarefa.titulo,
                     font=("JetBrains Mono", 13, "bold"),
                     text_color=CINZA_TEXT if tarefa.status == "concluida"
                     else BRANCO).pack(side="left")

        ctk.CTkLabel(linha_top, text=tarefa.prioridade,
                     font=("JetBrains Mono", 10, "bold"),
                     text_color=cor_prioridade,
                     fg_color=AZUL_TAG, corner_radius=4,
                     width=60).pack(side="right")

        linha_meio = ctk.CTkFrame(corpo, fg_color="transparent")
        linha_meio.pack(fill="x", pady=(4, 0))

        if tarefa.descricao:
            ctk.CTkLabel(linha_meio,
                         text=tarefa.descricao[:60] + ("…" if len(tarefa.descricao) > 60 else ""),
                         font=("JetBrains Mono", 11),
                         text_color=CINZA_TEXT).pack(side="left")

        ctk.CTkLabel(linha_meio,
                     text=tarefa.status.replace("_", " "),
                     font=("JetBrains Mono", 10),
                     text_color=cor_status,
                     fg_color=AZUL_TAG, corner_radius=4).pack(side="right", padx=4)

        linha_bot = ctk.CTkFrame(corpo, fg_color="transparent")
        linha_bot.pack(fill="x", pady=(4, 0))

        if tarefa.data_venc:
            cor_prazo = ERRO if atrasada else CINZA_TEXT
            ctk.CTkLabel(linha_bot,
                         text=f"📅 prazo: {_formatar_data(tarefa.data_venc)}",
                         font=("JetBrains Mono", 10),
                         text_color=cor_prazo).pack(side="left")

        ctk.CTkButton(linha_bot, text="✎",
                      font=("JetBrains Mono", 11),
                      fg_color="transparent", text_color=VERDE_NEON,
                      hover_color=AZUL_TAG, width=28, height=24,
                      command=lambda t=tarefa: self._editar_tarefa(t)
                      ).pack(side="right", padx=(4, 0))

        ctk.CTkButton(linha_bot, text="✕",
                      font=("JetBrains Mono", 11),
                      fg_color="transparent", text_color=CINZA_TEXT,
                      hover_color="#2a0a0a", width=28, height=24,
                      command=lambda t=tarefa: self._excluir_tarefa(t)
                      ).pack(side="right")

    def _selecionar_lista(self, lista):
        self.lista_selecionada = lista
        self._carregar_tarefas()

    def _aplicar_filtro(self, _=None):
        self._carregar_tarefas()

    def _nova_lista(self):
        dialogo = ctk.CTkInputDialog(
            text="Nome da nova lista:", title="Nova lista")
        nome = dialogo.get_input()
        if nome and nome.strip():
            try:
                self.lista_service.cadastrar_lista(
                    self.usuario.id_usuario, nome.strip())
                self._carregar_listas()
                self._carregar_tarefas()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _editar_lista(self, lista):
        dialogo = ctk.CTkInputDialog(
            text=f'Novo nome para "{lista.nome}":', title="Editar lista")
        novo_nome = dialogo.get_input()
        if novo_nome and novo_nome.strip():
            try:
                self.lista_service.atualizar_lista(
                    lista.id_lista, self.usuario.id_usuario, novo_nome.strip())
                self._carregar_listas()
                self._carregar_tarefas()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _excluir_lista(self, lista):
        ok = messagebox.askyesno(
            "Excluir lista",
            f'Tem certeza que deseja excluir a lista "{lista.nome}"?\n'
            f"Todas as tarefas dessa lista também serão excluídas.")
        if not ok:
            return
        self.lista_service.excluir_lista(lista.id_lista, self.usuario.id_usuario)
        if self.lista_selecionada and self.lista_selecionada.id_lista == lista.id_lista:
            self.lista_selecionada = None
        self._carregar_listas()
        self._carregar_tarefas()

    def _nova_tarefa(self):
        if self.lista_selecionada is None:
            messagebox.showwarning(
                "Selecione uma lista",
                "Selecione uma lista antes de criar uma tarefa.")
            return
        JanelaNovaTarefa(self, self.lista_selecionada,
                         self.tarefa_service, self._carregar_tarefas)

    def _editar_tarefa(self, tarefa):
        JanelaEditarTarefa(self, tarefa, self.tarefa_service, self._carregar_tarefas)

    def _toggle_status(self, tarefa):
        novo_status = "pendente" if tarefa.status == "concluida" else "concluida"
        self.tarefa_service.atualizar_tarefa(
            id_tarefa=tarefa.id_tarefa,
            titulo=tarefa.titulo,
            descricao=tarefa.descricao or "",
            prioridade=tarefa.prioridade,
            status=novo_status,
            data_inicio=tarefa.data_inicio,
            data_venc=tarefa.data_venc,
            hora_venc=tarefa.hora_venc,
        )
        self._carregar_tarefas()

    def _excluir_tarefa(self, tarefa):
        ok = messagebox.askyesno(
            "Excluir tarefa",
            f'Excluir "{tarefa.titulo}"?')
        if ok:
            self.tarefa_service.excluir_tarefa(tarefa.id_tarefa)
            self._carregar_tarefas()

    def _sair(self):
        self.winfo_toplevel().destroy()


class _JanelaTarefaBase(ctk.CTkToplevel):

    def __init__(self, pai, titulo_janela: str, texto_botao: str):
        super().__init__(pai)
        self.title(titulo_janela)
        self.geometry("480x580")
        self.resizable(False, False)
        self.configure(fg_color=PRETO)
        self.grab_set()
        self._construir_ui(titulo_janela, texto_botao)

    def _construir_ui(self, titulo_janela, texto_botao):
        card = ctk.CTkFrame(self, fg_color=CINZA_CARD,
                            corner_radius=12, border_width=1,
                            border_color=CINZA_BRD)
        card.pack(padx=24, pady=24, fill="both", expand=True)

        ctk.CTkLabel(card, text=titulo_janela,
                     font=("JetBrains Mono", 18, "bold"),
                     text_color=BRANCO).pack(anchor="w", padx=20, pady=(20, 16))

        ctk.CTkLabel(card, text="TÍTULO", font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(anchor="w", padx=20)
        self.campo_titulo = ctk.CTkEntry(
            card, placeholder_text="Ex: Revisar relatório",
            font=("JetBrains Mono", 13), height=40,
            fg_color="#1a1a1a", border_color=CINZA_BRD,
            border_width=1, text_color=BRANCO, corner_radius=6)
        self.campo_titulo.pack(fill="x", padx=20, pady=(4, 12))

        ctk.CTkLabel(card, text="DESCRIÇÃO", font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(anchor="w", padx=20)
        self.campo_descricao = ctk.CTkEntry(
            card, placeholder_text="Detalhes da tarefa...",
            font=("JetBrains Mono", 13), height=40,
            fg_color="#1a1a1a", border_color=CINZA_BRD,
            border_width=1, text_color=BRANCO, corner_radius=6)
        self.campo_descricao.pack(fill="x", padx=20, pady=(4, 12))

        frame_dupla = ctk.CTkFrame(card, fg_color="transparent")
        frame_dupla.pack(fill="x", padx=20, pady=(0, 12))

        col_prioridade = ctk.CTkFrame(frame_dupla, fg_color="transparent")
        col_prioridade.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkLabel(col_prioridade, text="PRIORIDADE",
                     font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(anchor="w")
        self.campo_prioridade = ctk.CTkOptionMenu(
            col_prioridade, values=["media", "alta", "baixa"],
            font=("JetBrains Mono", 12),
            fg_color="#1a1a1a", button_color=CINZA_BRD,
            button_hover_color=CINZA_BRD, text_color=BRANCO,
            dropdown_fg_color=CINZA_CARD, height=40, corner_radius=6)
        self.campo_prioridade.pack(fill="x", pady=(4, 0))

        col_status = ctk.CTkFrame(frame_dupla, fg_color="transparent")
        col_status.pack(side="left", fill="x", expand=True, padx=(6, 0))
        ctk.CTkLabel(col_status, text="STATUS",
                     font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(anchor="w")
        self.campo_status = ctk.CTkOptionMenu(
            col_status, values=["pendente", "em_andamento", "concluida"],
            font=("JetBrains Mono", 12),
            fg_color="#1a1a1a", button_color=CINZA_BRD,
            button_hover_color=CINZA_BRD, text_color=BRANCO,
            dropdown_fg_color=CINZA_CARD, height=40, corner_radius=6)
        self.campo_status.pack(fill="x", pady=(4, 0))

        frame_datas = ctk.CTkFrame(card, fg_color="transparent")
        frame_datas.pack(fill="x", padx=20, pady=(0, 12))

        col_inicio = ctk.CTkFrame(frame_datas, fg_color="transparent")
        col_inicio.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkLabel(col_inicio, text="DATA DE INÍCIO",
                     font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(anchor="w")
        self.campo_data_inicio = ctk.CTkEntry(
            col_inicio, placeholder_text="dd/mm/aaaa",
            font=("JetBrains Mono", 13), height=40,
            fg_color="#1a1a1a", border_color=CINZA_BRD,
            border_width=1, text_color=BRANCO, corner_radius=6)
        self.campo_data_inicio.pack(fill="x", pady=(4, 0))

        col_prazo = ctk.CTkFrame(frame_datas, fg_color="transparent")
        col_prazo.pack(side="left", fill="x", expand=True, padx=(6, 0))
        ctk.CTkLabel(col_prazo, text="PRAZO (VENCIMENTO)",
                     font=("JetBrains Mono", 10),
                     text_color=CINZA_TEXT).pack(anchor="w")
        self.campo_data_venc = ctk.CTkEntry(
            col_prazo, placeholder_text="dd/mm/aaaa",
            font=("JetBrains Mono", 13), height=40,
            fg_color="#1a1a1a", border_color=CINZA_BRD,
            border_width=1, text_color=BRANCO, corner_radius=6)
        self.campo_data_venc.pack(fill="x", pady=(4, 0))

        self.label_erro = ctk.CTkLabel(card, text="",
                                       font=("JetBrains Mono", 11),
                                       text_color=ERRO, wraplength=400)
        self.label_erro.pack(padx=20, anchor="w")

        ctk.CTkButton(card, text=texto_botao,
                      font=("JetBrains Mono", 13, "bold"),
                      fg_color=VERDE_NEON, hover_color=VERDE_ESC,
                      text_color=PRETO, height=44, corner_radius=6,
                      command=self._salvar).pack(fill="x", padx=20, pady=(8, 20))

    def _ler_campos(self) -> dict:
        data_inicio = _parse_data(self.campo_data_inicio.get())
        data_venc   = _parse_data(self.campo_data_venc.get())
        return dict(
            titulo=self.campo_titulo.get().strip(),
            descricao=self.campo_descricao.get().strip(),
            prioridade=self.campo_prioridade.get(),
            status=self.campo_status.get(),
            data_inicio=data_inicio,
            data_venc=data_venc,
        )

    def _salvar(self):
        raise NotImplementedError


class JanelaNovaTarefa(_JanelaTarefaBase):
    def __init__(self, pai, lista, tarefa_service, callback_atualizar):
        self.lista          = lista
        self.tarefa_service = tarefa_service
        self.callback       = callback_atualizar
        super().__init__(pai, "Nova tarefa", "Criar tarefa →")

    def _salvar(self):
        try:
            dados = self._ler_campos()
            self.tarefa_service.cadastrar_tarefa(
                id_lista=self.lista.id_lista, **dados)
            self.callback()
            self.destroy()
        except ValueError as e:
            self.label_erro.configure(text=str(e))


class JanelaEditarTarefa(_JanelaTarefaBase):
    def __init__(self, pai, tarefa, tarefa_service, callback_atualizar):
        self.tarefa          = tarefa
        self.tarefa_service  = tarefa_service
        self.callback        = callback_atualizar
        super().__init__(pai, "Editar tarefa", "Salvar alterações →")
        self._preencher_campos()

    def _preencher_campos(self):
        self.campo_titulo.insert(0, self.tarefa.titulo)
        self.campo_descricao.insert(0, self.tarefa.descricao or "")
        self.campo_prioridade.set(self.tarefa.prioridade)
        self.campo_status.set(self.tarefa.status)
        self.campo_data_inicio.insert(0, _formatar_data(self.tarefa.data_inicio))
        self.campo_data_venc.insert(0, _formatar_data(self.tarefa.data_venc))

    def _salvar(self):
        try:
            dados = self._ler_campos()
            self.tarefa_service.atualizar_tarefa(
                id_tarefa=self.tarefa.id_tarefa, **dados)
            self.callback()
            self.destroy()
        except ValueError as e:
            self.label_erro.configure(text=str(e))