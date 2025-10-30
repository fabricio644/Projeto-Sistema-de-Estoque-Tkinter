import tkinter as tk
from tkinter import messagebox, simpledialog
from sistema_estoque import SistemaEstoque
from modelo.classe_produto import Produto
from modelo.classe_endereco import Endereco
from modelo.classe_usuario import Usuario

# Arquivo único de interface simples em Tkinter
# Requisitos:
# - Tela de login
# - Menu principal que muda conforme cargo (gerente/analista/assistente)
# - Janelas simples para listar/cadastrar/remover produtos, endereços e usuários
# - Movimentação (entrada/saída/transferência) simplificada


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("LOG WMS")
        self.root.geometry("640x360")
        self.sistema = SistemaEstoque()

        # Se não há usuários, criar admin padrão (senha: admin)
        if not self.sistema.usuarios:
            admin = Usuario("admin", "admin", "gerente")
            self.sistema.usuarios.append(admin)
            self.sistema.exportar_usuarios_para_csv()

        self.build_login()

    def build_login(self):
        # limpa
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, bg="#111", padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="LOG WMS", bg="#111", fg="white", font=(None, 14)).pack(pady=(0,10))

        lbl_user = tk.Label(frame, text="Usuário:", bg="#111", fg="white")
        lbl_user.pack(anchor="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(fill=tk.X, pady=(0,10))

        lbl_pass = tk.Label(frame, text="Senha:", bg="#111", fg="white")
        lbl_pass.pack(anchor="w")
        self.entry_pass = tk.Entry(frame, show="*")
        self.entry_pass.pack(fill=tk.X, pady=(0,10))

        btn = tk.Button(frame, text="Confirmar", command=self.try_login)
        btn.pack(pady=(10,0))

    def try_login(self):
        nome = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()

        for u in self.sistema.usuarios:
            if u.nome_usuario == nome and u.senha_usuario == senha:
                messagebox.showinfo("Sucesso", f"Bem-vindo {u.nome_usuario} ({u.cargo})")
                self.user = u
                self.build_menu()
                return

        messagebox.showerror("Erro", "Credenciais inválidas")

    def build_menu(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, bg="#111", padx=10, pady=10)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="LOG WMS", bg="#111", fg="white", font=(None, 14)).grid(row=0, column=0, columnspan=4, pady=(0,10))

        cargo = self.user.cargo.lower()

        # Buttons: position grid similar to images simple
        btn_cons_prod = tk.Button(frame, text="Consultar Produtos", width=20, height=4, command=self.win_produtos)
        btn_cons_end = tk.Button(frame, text="Consultar Endereços", width=20, height=4, command=self.win_enderecos)
        btn_mov = tk.Button(frame, text="Movimentação de Estoque", width=20, height=4, command=self.win_movimentacao)

        btn_cons_prod.grid(row=1, column=0, padx=10, pady=10)
        btn_cons_end.grid(row=1, column=1, padx=10, pady=10)
        btn_mov.grid(row=2, column=0, padx=10, pady=10)

        if cargo == "gerente":
            btn_cons_user = tk.Button(frame, text="Consultar Usuários", width=20, height=4, command=self.win_usuarios)
            btn_cons_user.grid(row=2, column=1, padx=10, pady=10)

        btn_logout = tk.Button(frame, text="Logout", command=self.build_login)
        btn_logout.grid(row=3, column=0, columnspan=2, pady=(20,0))

    # ---------- janelas de apoio --------------
    def win_produtos(self):
        cargo = self.user.cargo.lower()
        w = tk.Toplevel(self.root)
        w.title("Produtos")
        w.geometry("520x320")

        listbox = tk.Listbox(w, width=80, height=10)
        listbox.pack(padx=10, pady=10)

        def refresh():
            listbox.delete(0, tk.END)
            if not self.sistema.produtos:
                listbox.insert(tk.END, "Nenhum produto cadastrado")
                return
            for i, p in enumerate(self.sistema.produtos, start=1):
                listbox.insert(tk.END, f"[{i}] {p.nome} | R$ {p.valor:.2f} | Qt: {p.quantidade} | Tipo: {p.tipo}")

        refresh()

        frame_btn = tk.Frame(w)
        frame_btn.pack(pady=5)

        if cargo in ["gerente", "analista"]:
            def add_prod():
                nome = simpledialog.askstring("Nome", "Nome do produto:", parent=w)
                if not nome:
                    return
                try:
                    valor = float(simpledialog.askstring("Valor", "Valor unitário:", parent=w))
                except Exception:
                    messagebox.showerror("Erro", "Valor inválido")
                    return
                tipo = simpledialog.askstring("Tipo", "Tipo do produto:", parent=w) or ""
                produto = Produto(nome, valor, 0, 0, tipo)
                self.sistema.produtos.append(produto)
                self.sistema.exportar_produtos_para_csv()
                refresh()

            def remover():
                sel = listbox.curselection()
                if not sel:
                    messagebox.showwarning("Aviso", "Selecione um produto")
                    return
                idx = sel[0]
                if idx >= len(self.sistema.produtos):
                    messagebox.showerror("Erro", "Seleção inválida")
                    return
                prod = self.sistema.produtos.pop(idx)
                self.sistema.exportar_produtos_para_csv()
                messagebox.showinfo("Removido", f"{prod.nome} removido")
                refresh()

            tk.Button(frame_btn, text="Cadastrar Produto", command=add_prod).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_btn, text="Remover Produto", command=remover).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_btn, text="Atualizar", command=refresh).pack(side=tk.LEFT, padx=5)

    def win_enderecos(self):
        cargo = self.user.cargo.lower()
        w = tk.Toplevel(self.root)
        w.title("Endereços")
        w.geometry("520x320")

        listbox = tk.Listbox(w, width=80, height=10)
        listbox.pack(padx=10, pady=10)

        def refresh():
            listbox.delete(0, tk.END)
            if not self.sistema.enderecos:
                listbox.insert(tk.END, "Nenhum endereço cadastrado")
                return
            for i, e in enumerate(self.sistema.enderecos, start=1):
                produto_no_endereco = None
                for p in self.sistema.produtos:
                    if p.endereco == e:
                        produto_no_endereco = p
                        break
                prod_str = produto_no_endereco.nome if produto_no_endereco else "Nenhum"
                listbox.insert(tk.END, f"[{i}] Rua:{e.rua} | Pr:{e.predio} | And:{e.andar} | Pos:{e.posicao} | Status:{e.status_endereco} | Produto:{prod_str}")

        refresh()

        frame_btn = tk.Frame(w)
        frame_btn.pack(pady=5)

        if cargo in ["gerente", "analista"]:
            def add_end():
                try:
                    rua = simpledialog.askinteger("Rua", "Número da rua:", parent=w)
                    predio = simpledialog.askinteger("Prédio", "Número do prédio:", parent=w)
                    andar = simpledialog.askinteger("Andar", "Número do andar:", parent=w)
                    pos = simpledialog.askinteger("Posição", "Número da posição:", parent=w)
                except Exception:
                    messagebox.showerror("Erro", "Valores inválidos")
                    return
                endereco = Endereco(rua, predio, andar, pos, "L")
                self.sistema.enderecos.append(endereco)
                self.sistema.exportar_enderecos_para_csv()
                refresh()

            def remover():
                sel = listbox.curselection()
                if not sel:
                    messagebox.showwarning("Aviso", "Selecione um endereço")
                    return
                idx = sel[0]
                end = self.sistema.enderecos[idx]
                if end.status_endereco != "L":
                    messagebox.showerror("Erro", "Não é permitido excluir endereço com saldo")
                    return
                del self.sistema.enderecos[idx]
                self.sistema.exportar_enderecos_para_csv()
                refresh()

            tk.Button(frame_btn, text="Cadastrar Endereço", command=add_end).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_btn, text="Remover Endereço", command=remover).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_btn, text="Atualizar", command=refresh).pack(side=tk.LEFT, padx=5)

    def win_usuarios(self):
        # apenas para gerente
        if self.user.cargo.lower() != "gerente":
            messagebox.showerror("Erro", "Acesso negado")
            return

        w = tk.Toplevel(self.root)
        w.title("Usuários")
        w.geometry("520x320")

        listbox = tk.Listbox(w, width=80, height=10)
        listbox.pack(padx=10, pady=10)

        def refresh():
            listbox.delete(0, tk.END)
            if not self.sistema.usuarios:
                listbox.insert(tk.END, "Nenhum usuário cadastrado")
                return
            for i, u in enumerate(self.sistema.usuarios, start=1):
                listbox.insert(tk.END, f"[{i}] {u.nome_usuario} | Cargo: {u.cargo}")

        refresh()

        frame_btn = tk.Frame(w)
        frame_btn.pack(pady=5)

        def add_user():
            nome = simpledialog.askstring("Nome", "Nome do usuário:", parent=w)
            if not nome:
                return
            senha = simpledialog.askstring("Senha", "Senha:", parent=w)
            cargo = simpledialog.askstring("Cargo", "Cargo (gerente/analista/assistente):", parent=w)
            usuario = Usuario(nome, senha, cargo)
            self.sistema.usuarios.append(usuario)
            self.sistema.exportar_usuarios_para_csv()
            refresh()

        def remover():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um usuário")
                return
            idx = sel[0]
            u = self.sistema.usuarios.pop(idx)
            self.sistema.exportar_usuarios_para_csv()
            messagebox.showinfo("Removido", f"{u.nome_usuario} removido")
            refresh()

        def promover_rebaixar(promote=True):
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um usuário")
                return
            idx = sel[0]
            novo = simpledialog.askstring("Novo cargo", "Digite o novo cargo:", parent=w)
            if novo not in ["gerente", "analista", "assistente"]:
                messagebox.showerror("Erro", "Cargo inválido")
                return
            self.sistema.usuarios[idx].cargo = novo
            self.sistema.exportar_usuarios_para_csv()
            refresh()

        tk.Button(frame_btn, text="Cadastrar Usuário", command=add_user).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Remover Usuário", command=remover).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Promover/Rebaixar", command=lambda: promover_rebaixar(True)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Atualizar", command=refresh).pack(side=tk.LEFT, padx=5)

    def win_movimentacao(self):
        w = tk.Toplevel(self.root)
        w.title("Movimentação")
        w.geometry("520x320")

        tk.Label(w, text="Escolha operação:").pack(pady=5)
        frame = tk.Frame(w)
        frame.pack(pady=10)

        tk.Button(frame, text="Entrada", width=12, command=lambda: self.mov_entrada(w)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Saída", width=12, command=lambda: self.mov_saida(w)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Transferência", width=12, command=lambda: self.mov_transferencia(w)).pack(side=tk.LEFT, padx=5)

    def mov_entrada(self, parent):
        if not self.sistema.produtos or not self.sistema.enderecos:
            messagebox.showerror("Erro", "É necessário ter produtos e endereços cadastrados")
            return

        w = tk.Toplevel(parent)
        w.title("Entrada")

        tk.Label(w, text="Produto:").pack()
        prod_var = tk.StringVar(w)
        prod_var.set(self.sistema.produtos[0].nome)
        prod_menu = tk.OptionMenu(w, prod_var, *[p.nome for p in self.sistema.produtos])
        prod_menu.pack()

        tk.Label(w, text="Endereço:").pack()
        end_var = tk.StringVar(w)
        end_var.set(0)
        end_menu = tk.OptionMenu(w, end_var, *[f"[{i+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}" for i,e in enumerate(self.sistema.enderecos)])
        end_menu.pack()

        tk.Label(w, text="Quantidade:").pack()
        qtd_entry = tk.Entry(w)
        qtd_entry.pack()

        def confirmar():
            nome = prod_var.get()
            endereco_idx = end_menu.children['menu'].index('active') if 'menu' in end_menu.children else None
            # safer approach: match by label
            end_label = end_var.get()
            try:
                qtd = int(qtd_entry.get())
            except Exception:
                messagebox.showerror("Erro", "Quantidade inválida")
                return

            # localizar produto e endereco
            produto = next((p for p in self.sistema.produtos if p.nome == nome), None)
            endereco = None
            for e in self.sistema.enderecos:
                label = f"[{self.sistema.enderecos.index(e)+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}"
                if label == end_label:
                    endereco = e
                    break

            if produto is None or endereco is None:
                messagebox.showerror("Erro", "Produto ou endereço inválido")
                return

            # lógica semelhante à do sistema
            if endereco.status_endereco == "L" or (endereco.status_endereco == "O" and produto.endereco == endereco):
                if qtd > 0:
                    produto.quantidade += qtd
                    produto.valortotal = produto.atualizar_valor_total()
                    endereco.status_endereco = "O"
                    produto.endereco = endereco
                    self.sistema.exportar_produtos_para_csv()
                    self.sistema.exportar_enderecos_para_csv()
                    messagebox.showinfo("Sucesso", "Entrada realizada")
                    w.destroy()
                else:
                    messagebox.showerror("Erro", "Quantidade deve ser > 0")
            else:
                messagebox.showerror("Erro", "Endereço ocupado por outro produto")

        tk.Button(w, text="Confirmar", command=confirmar).pack(pady=8)

    def mov_saida(self, parent):
        if not self.sistema.enderecos:
            messagebox.showerror("Erro", "Não há endereços")
            return
        w = tk.Toplevel(parent)
        w.title("Saída")

        tk.Label(w, text="Endereço:").pack()
        end_var = tk.StringVar(w)
        occupied = [e for e in self.sistema.enderecos if e.status_endereco == 'O']
        if not occupied:
            messagebox.showerror("Erro", "Nenhum endereço ocupado")
            w.destroy()
            return
        end_var.set(f"[{self.sistema.enderecos.index(occupied[0])+1}] {occupied[0].rua}-{occupied[0].predio}-{occupied[0].andar}-{occupied[0].posicao}")
        end_menu = tk.OptionMenu(w, end_var, *[f"[{self.sistema.enderecos.index(e)+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}" for e in occupied])
        end_menu.pack()

        tk.Label(w, text="Quantidade:").pack()
        qtd_entry = tk.Entry(w)
        qtd_entry.pack()

        def confirmar():
            label = end_var.get()
            qtd = 0
            try:
                qtd = int(qtd_entry.get())
            except Exception:
                messagebox.showerror("Erro", "Quantidade inválida")
                return

            endereco = None
            for e in self.sistema.enderecos:
                lab = f"[{self.sistema.enderecos.index(e)+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}"
                if lab == label:
                    endereco = e
                    break
            if endereco is None:
                messagebox.showerror("Erro", "Endereço inválido")
                return

            produto = next((p for p in self.sistema.produtos if p.endereco == endereco), None)
            if produto is None:
                messagebox.showerror("Erro", "Nenhum produto neste endereço")
                return

            if qtd <= produto.quantidade:
                produto.quantidade -= qtd
                produto.valortotal = produto.atualizar_valor_total()
                if produto.quantidade == 0:
                    endereco.status_endereco = 'L'
                    produto.endereco = None
                else:
                    endereco.status_endereco = 'O'
                self.sistema.exportar_produtos_para_csv()
                self.sistema.exportar_enderecos_para_csv()
                messagebox.showinfo("Sucesso", "Saída realizada")
                w.destroy()
            else:
                messagebox.showerror("Erro", "Quantidade maior que o disponível")

        tk.Button(w, text="Confirmar", command=confirmar).pack(pady=8)

    def mov_transferencia(self, parent):
        if not self.sistema.enderecos:
            messagebox.showerror("Erro", "Não há endereços")
            return
        w = tk.Toplevel(parent)
        w.title("Transferência")

        ocupados = [e for e in self.sistema.enderecos if e.status_endereco == 'O']
        livres = [e for e in self.sistema.enderecos if e.status_endereco == 'L']
        if not ocupados or not livres:
            messagebox.showerror("Erro", "É necessário um endereço ocupado e outro livre")
            w.destroy()
            return

        tk.Label(w, text="Origem (ocupado):").pack()
        orig_var = tk.StringVar(w)
        orig_var.set(f"[{self.sistema.enderecos.index(ocupados[0])+1}] {ocupados[0].rua}-{ocupados[0].predio}-{ocupados[0].andar}-{ocupados[0].posicao}")
        orig_menu = tk.OptionMenu(w, orig_var, *[f"[{self.sistema.enderecos.index(e)+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}" for e in ocupados])
        orig_menu.pack()

        tk.Label(w, text="Destino (livre):").pack()
        dest_var = tk.StringVar(w)
        dest_var.set(f"[{self.sistema.enderecos.index(livres[0])+1}] {livres[0].rua}-{livres[0].predio}-{livres[0].andar}-{livres[0].posicao}")
        dest_menu = tk.OptionMenu(w, dest_var, *[f"[{self.sistema.enderecos.index(e)+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}" for e in livres])
        dest_menu.pack()

        def confirmar():
            orig_label = orig_var.get()
            dest_label = dest_var.get()
            origem = None
            destino = None
            for e in self.sistema.enderecos:
                lab = f"[{self.sistema.enderecos.index(e)+1}] {e.rua}-{e.predio}-{e.andar}-{e.posicao}"
                if lab == orig_label:
                    origem = e
                if lab == dest_label:
                    destino = e
            if origem is None or destino is None:
                messagebox.showerror("Erro", "Endereço inválido")
                return

            produto = next((p for p in self.sistema.produtos if p.endereco == origem), None)
            if not produto:
                messagebox.showerror("Erro", "Nenhum produto no endereço de origem")
                return

            produto.endereco = destino
            origem.status_endereco = 'L'
            destino.status_endereco = 'O'
            self.sistema.exportar_produtos_para_csv()
            self.sistema.exportar_enderecos_para_csv()
            messagebox.showinfo("Sucesso", "Transferência realizada")
            w.destroy()

        tk.Button(w, text="Confirmar", command=confirmar).pack(pady=8)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
