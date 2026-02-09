import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

class AutomacoesEPC:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizar RPCMs por lote - EPC")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Tentar carregar ícone
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'app_icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Variáveis
        self.pasta_origem = tk.StringVar()
        self.pasta_destino = tk.StringVar()
        self.lista_numeros_texto = tk.StringVar()
        
        self.criar_interface()
    
    def criar_interface(self):
        """Cria a interface gráfica"""
        
        # Frame com scroll para o conteúdo principal
        canvas = tk.Canvas(self.root, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Mostrar scrollbar apenas se necessário
            if canvas.bbox("all") and canvas.bbox("all")[3] > self.root.winfo_height():
                scrollbar.pack(side="right", fill="y")
            else:
                scrollbar.pack_forget()
        
        scrollable_frame.bind("<Configure>", on_frame_configure)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Permitir scroll APENAS dentro do canvas
        def _on_mousewheel(event):
            if canvas.winfo_containing(event.x_root, event.y_root) == canvas:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        self.root.bind("<Configure>", on_frame_configure)
        
        # Agora o conteúdo vai dentro de scrollable_frame
        main_frame = scrollable_frame
        main_frame.configure(padx=20, pady=20)
        
        # Título
        titulo = tk.Label(main_frame, text="Organizar RPCMs por lote - EPC", 
                         font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        titulo.pack(pady=(0, 20))
        
        # ===== PASTA DE ORIGEM =====
        frame_origem = tk.LabelFrame(main_frame, text="📁 Pasta de Origem (Banco)", 
                                     font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame_origem.pack(fill=tk.X, pady=(0, 15))
        
        tk.Entry(frame_origem, textvariable=self.pasta_origem, width=70, font=("Arial", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(frame_origem, text="📂 Selecionar", command=self.selecionar_pasta_origem, 
                 bg="#4CAF50", fg="white", padx=15, font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
        
        # ===== PASTA DE DESTINO =====
        frame_destino = tk.LabelFrame(main_frame, text="📁 Pasta de Destino (Lote)", 
                                      font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame_destino.pack(fill=tk.X, pady=(0, 15))
        
        tk.Entry(frame_destino, textvariable=self.pasta_destino, width=70, font=("Arial", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(frame_destino, text="📂 Selecionar", command=self.selecionar_pasta_destino, 
                 bg="#4CAF50", fg="white", padx=15, font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
        
        # ===== LISTA DE NÚMEROS =====
        frame_numeros = tk.LabelFrame(main_frame, text="📝 Lista de Números das RPCMs", 
                                      font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame_numeros.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        info_label = tk.Label(frame_numeros, 
                             text="Insira os números separados por vírgula, espaço ou quebra de linha\nExemplo: 400006, 400009, 400010 ou cada um em uma linha", 
                             font=("Arial", 9), bg="#f0f0f0", fg="#666")
        info_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.texto_numeros = scrolledtext.ScrolledText(frame_numeros, height=6, width=80, font=("Courier", 10))
        self.texto_numeros.pack(fill=tk.BOTH, expand=True)
        
        # ===== BOTÕES DE AÇÃO =====
        frame_botoes = tk.Frame(main_frame, bg="#f0f0f0")
        frame_botoes.pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(frame_botoes, text="❌ Sair", command=self.root.quit, 
                 bg="#f44336", fg="white", padx=15, pady=10, font=("Arial", 11),
                 cursor="hand2").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(frame_botoes, text="🧹 Limpar Histórico", command=self.limpar_terminal, 
                 bg="#757575", fg="white", padx=15, pady=10, font=("Arial", 11),
                 cursor="hand2").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(frame_botoes, text="🧹 Limpar Tudo", command=self.limpar_campos, 
                 bg="#757575", fg="white", padx=15, pady=10, font=("Arial", 11),
                 cursor="hand2").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(frame_botoes, text="✓ Verificar Destino", command=self.verificar_numeros, 
                 bg="#FF9800", fg="white", padx=15, pady=10, font=("Arial", 11, "bold"),
                 cursor="hand2").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(frame_botoes, text="🚀 Organizar Lote", command=self.executar_copia, 
                 bg="#2196F3", fg="white", padx=15, pady=10, font=("Arial", 11, "bold"),
                 cursor="hand2").pack(side=tk.LEFT)
        
        # ===== ÁREA DE LOG =====
        frame_log = tk.LabelFrame(main_frame, text="📊 Histórico", 
                                 font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        frame_log.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.log_texto = scrolledtext.ScrolledText(frame_log, height=15, width=80, 
                                                   font=("Courier", 9), bg="#333", fg="#00FF00")
        self.log_texto.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags de cor para o log
        self.log_texto.tag_configure("sucesso", foreground="#00FF00")
        self.log_texto.tag_configure("erro", foreground="#FF4444")
        self.log_texto.tag_configure("info", foreground="#00AAFF")
        self.log_texto.tag_configure("aviso", foreground="#FFAA00")
    
    def selecionar_pasta_origem(self):
        """Abre diálogo para selecionar pasta de origem"""
        pasta = filedialog.askdirectory(title="Selecione a pasta do banco")
        if pasta:
            self.pasta_origem.set(pasta)
    
    def selecionar_pasta_destino(self):
        """Abre diálogo para selecionar pasta de destino"""
        pasta = filedialog.askdirectory(title="Selecione a pasta do lote")
        if pasta:
            self.pasta_destino.set(pasta)
    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.pasta_origem.set("")
        self.pasta_destino.set("")
        self.texto_numeros.delete(1.0, tk.END)
        self.log_texto.delete(1.0, tk.END)
        self.adicionar_log("✨ Campos e histórico limpos!", "info")
    
    def limpar_terminal(self):
        """Limpa apenas o terminal/log"""
        self.log_texto.delete(1.0, tk.END)
        self.adicionar_log("✨ Histórico limpo!", "info")
    
    def adicionar_log(self, mensagem, tipo="info"):
        """Adiciona mensagem ao log"""
        self.log_texto.insert(tk.END, mensagem + "\n", tipo)
        self.log_texto.see(tk.END)
        self.root.update()
    
    def obter_lista_numeros(self):
        """Obtém e processa a lista de números"""
        texto_numeros = self.texto_numeros.get(1.0, tk.END).strip()
        if not texto_numeros:
            return None
        
        lista_numeros = []
        for item in texto_numeros.replace(',', '\n').split('\n'):
            item = item.strip()
            if item:
                lista_numeros.append(item)
        
        return lista_numeros if lista_numeros else None
    
    def extrair_numero_arquivo(self, nome_arquivo):
        """Extrai os primeiros dígitos do nome do arquivo"""
        numero = ""
        for char in nome_arquivo:
            if char.isdigit():
                numero += char
            else:
                break
        return numero
    
    def verificar_numeros(self):
        """Verifica se todos os números existem na pasta de DESTINO"""
        
        if not self.pasta_destino.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta do lote!")
            return
        
        lista_numeros = self.obter_lista_numeros()
        if not lista_numeros:
            messagebox.showerror("Erro", "Por favor, insira números para verificar!")
            return
        
        # Limpar log
        self.log_texto.delete(1.0, tk.END)
        
        # Executar em thread
        thread = threading.Thread(target=self.thread_verificar, 
                                 args=(self.pasta_destino.get(), lista_numeros))
        thread.start()
    
    def thread_verificar(self, pasta_destino, lista_numeros):
        """Thread para verificar números na pasta de destino"""
        
        try:
            self.adicionar_log("🔍 Iniciando Verificação...\n", "info")
            self.adicionar_log(f"📂 Pasta de Destino (Lote): {pasta_destino}\n", "info")
            self.adicionar_log("-" * 80 + "\n", "info")
            
            pasta_destino = Path(pasta_destino)
            
            if not pasta_destino.exists():
                self.adicionar_log("❌ Pasta de destino (lote) não existe!\n", "erro")
                return
            
            # Obter todos os PDFs
            arquivos_encontrados = list(pasta_destino.glob("*.[pP][dD][fF]"))
            numeros_encontrados = set()  # Números ÚNICOS encontrados
            mapa_numeros_arquivos = {}   # Mapear números para seus arquivos
            
            # Contar arquivos por número
            for arquivo in arquivos_encontrados:
                numero = self.extrair_numero_arquivo(arquivo.stem)
                if numero:
                    numeros_encontrados.add(numero)
                    if numero not in mapa_numeros_arquivos:
                        mapa_numeros_arquivos[numero] = []
                    mapa_numeros_arquivos[numero].append(arquivo.name)
            
            # Converter lista para conjunto
            lista_numeros_str = {str(num).strip() for num in lista_numeros}
            
            # Calcular categorias
            conformes = sorted(lista_numeros_str & numeros_encontrados)  # Tudo certo
            ausentes = sorted(lista_numeros_str - numeros_encontrados)   # Faltando
            excedentes = sorted(numeros_encontrados - lista_numeros_str) # Sobrando
            
            # Exibir resultado no log
            self.adicionar_log(f"📊 RESULTADO DA VERIFICAÇÃO:\n", "info")
            self.adicionar_log(f"\n1️⃣  Total de arquivos na pasta de Destino (Lote): {len(arquivos_encontrados)}", "sucesso")
            self.adicionar_log(f"2️⃣  Números ÚNICOS encontrados no Destino (Lote): {len(numeros_encontrados)}", "sucesso")
            self.adicionar_log(f"3️⃣  Total de números solicitados: {len(lista_numeros_str)}", "info")
            self.adicionar_log(f"4️⃣  Conformes (solicitados encontrados): {len(conformes)}", "sucesso")
            
            if ausentes:
                self.adicionar_log(f"\n5️⃣  ❌ Ausentes (não encontrados): {len(ausentes)}", "erro")
                self.adicionar_log(f"   {', '.join(ausentes)}", "erro")
            else:
                self.adicionar_log(f"\n5️⃣  ✅ Ausentes (não encontrados): 0", "sucesso")
            
            if excedentes:
                self.adicionar_log(f"\n6️⃣  ⚠️ Excedentes (não solicitados): {len(excedentes)}", "aviso")
                self.adicionar_log(f"   {', '.join(excedentes)}", "aviso")
            else:
                self.adicionar_log(f"\n6️⃣  ✅ Excedentes (não solicitados): 0", "sucesso")
            
            # Verificar números repetidos
            numeros_repetidos = {num: arquivos for num, arquivos in mapa_numeros_arquivos.items() if len(arquivos) > 1}
            
            if numeros_repetidos:
                self.adicionar_log(f"\n7️⃣  🔄 NÚMEROS REPETIDOS DETECTADOS: {len(numeros_repetidos)}", "aviso")
                for numero, arquivos in sorted(numeros_repetidos.items()):
                    self.adicionar_log(f"   Número {numero}: {len(arquivos)} arquivos", "aviso")
                    for arquivo in arquivos:
                        self.adicionar_log(f"      • {arquivo}", "aviso")
            else:
                self.adicionar_log(f"\n7️⃣  ✅ Números repetidos: 0", "sucesso")
            
            self.adicionar_log("\n" + "-" * 80, "info")
            
            # Mensagem de conclusão
            resumo = f"VERIFICAÇÃO CONCLUÍDA\n\n"
            resumo += f"1️⃣  Total de arquivos na pasta de Destino (Lote): {len(arquivos_encontrados)}\n"
            resumo += f"2️⃣  Números ÚNICOS encontrados no Destino (Lote): {len(numeros_encontrados)}\n"
            resumo += f"3️⃣  Total de números solicitados: {len(lista_numeros_str)}\n"
            resumo += f"4️⃣  Conformes: {len(conformes)}\n"
            
            if ausentes:
                resumo += f"\n5️⃣  ❌ Ausentes ({len(ausentes)}):\n{', '.join(ausentes)}\n"
            else:
                resumo += f"\n5️⃣  ✅ Ausentes: 0\n"
            
            if excedentes:
                resumo += f"\n6️⃣  ⚠️ Excedentes ({len(excedentes)}):\n{', '.join(excedentes)}\n"
            else:
                resumo += f"\n6️⃣  ✅ Excedentes: 0\n"
            
            # Adicionar informações de números repetidos
            numeros_repetidos = {num: arquivos for num, arquivos in mapa_numeros_arquivos.items() if len(arquivos) > 1}
            
            if numeros_repetidos:
                resumo += f"\n7️⃣  🔄 NÚMEROS REPETIDOS ({len(numeros_repetidos)}):\n"
                for numero, arquivos in sorted(numeros_repetidos.items()):
                    resumo += f"   • Número {numero}: {len(arquivos)} arquivos\n"
                    for arquivo in arquivos:
                        resumo += f"      - {arquivo}\n"
            else:
                resumo += f"\n7️⃣  ✅ Números repetidos: 0\n"
            
            if not ausentes and not excedentes:
                resumo += "\n✅ Tudo está em conformidade!"
            
            messagebox.showinfo("Verificação Concluída", resumo)
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante verificação: {str(e)}")
    
    def executar_copia(self):
        """Executa a cópia de arquivos"""
        
        if not self.pasta_origem.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta do banco!")
            return
        
        if not self.pasta_destino.get():
            messagebox.showerror("Erro", "Por favor, selecione a pasta do lote!")
            return
        
        lista_numeros = self.obter_lista_numeros()
        if not lista_numeros:
            messagebox.showerror("Erro", "Por favor, insira números para copiar!")
            return
        
        # Limpar log
        self.log_texto.delete(1.0, tk.END)
        
        # Executar em thread
        thread = threading.Thread(target=self.thread_copia, 
                                 args=(self.pasta_origem.get(), 
                                       self.pasta_destino.get(), 
                                       lista_numeros))
        thread.start()
    
    def thread_copia(self, pasta_origem, pasta_destino, lista_numeros):
        """Thread para executar a cópia de arquivos"""
        
        try:
            self.adicionar_log("🔍 Iniciando organização do lote...\n", "info")
            self.adicionar_log(f"📂 Pasta de Origem (Banco): {pasta_origem}", "info")
            self.adicionar_log(f"📂 Pasta de Destino (Lote): {pasta_destino}", "info")
            self.adicionar_log(f"📝 Números a copiar: {len(lista_numeros)}\n", "info")
            self.adicionar_log("-" * 80 + "\n", "info")
            
            # Converter para Path
            pasta_origem = Path(pasta_origem)
            pasta_destino = Path(pasta_destino)
            
            # Verificar pasta de origem
            if not pasta_origem.exists():
                self.adicionar_log(f"❌ Erro: Pasta de origem (banco) não existe!\n", "erro")
                messagebox.showerror("Erro", "A pasta de origem (banco) não existe!")
                return
            
            # Criar pasta de destino
            if not pasta_destino.exists():
                pasta_destino.mkdir(parents=True, exist_ok=True)
                self.adicionar_log(f"✅ Pasta de destino (lote) criada\n", "sucesso")
            
            # Converter lista para conjunto
            lista_numeros_str = {str(num).strip() for num in lista_numeros}
            
            # Contadores
            arquivos_copiados = 0
            numeros_copiados = set()
            erros = 0
            
            # Processar PDFs
            arquivos_encontrados = list(pasta_origem.glob("*.[pP][dD][fF]"))
            
            self.adicionar_log(f"Total de arquivos na pasta de Origem (Banco): {len(arquivos_encontrados)}\n", "info")
            
            for arquivo in arquivos_encontrados:
                # Extrair número dos primeiros dígitos
                numero = self.extrair_numero_arquivo(arquivo.stem)
                
                # Verificar se está na lista
                if numero in lista_numeros_str:
                    try:
                        caminho_destino = pasta_destino / arquivo.name
                        shutil.copy2(str(arquivo), str(caminho_destino))
                        self.adicionar_log(f"✅ Copiado: {arquivo.name}", "sucesso")
                        arquivos_copiados += 1
                        numeros_copiados.add(numero)
                    except Exception as e:
                        self.adicionar_log(f"❌ Erro ao copiar {arquivo.name}: {str(e)}", "erro")
                        erros += 1
            
            # Números faltando
            numeros_nao_encontrados = sorted(lista_numeros_str - numeros_copiados)
            
            # Resumo
            self.adicionar_log("\n" + "-" * 80, "info")
            self.adicionar_log("\n📊 RESUMO DA OPERAÇÃO:\n", "info")
            self.adicionar_log(f"1️⃣  Arquivos copiados: {arquivos_copiados}", "sucesso")
            self.adicionar_log(f"2️⃣  Números únicos copiados: {len(numeros_copiados)}", "sucesso")
            
            if numeros_nao_encontrados:
                self.adicionar_log(f"3️⃣  ❌ Números não encontrados: {len(numeros_nao_encontrados)}", "erro")
                self.adicionar_log(f"   {', '.join(numeros_nao_encontrados)}", "erro")
            else:
                self.adicionar_log(f"3️⃣  ✅ Números não encontrados: 0", "sucesso")
            
            if erros > 0:
                self.adicionar_log(f"\n⚠️ Erros durante cópia: {erros}", "erro")
            
            self.adicionar_log("\n✨ Operação concluída!", "sucesso")
            
            # Criar mensagem resumida
            resumo = f"Operação concluída!\n\n"
            resumo += f"1️⃣  Arquivos copiados: {arquivos_copiados}\n"
            resumo += f"2️⃣  Números únicos copiados: {len(numeros_copiados)}\n"
            
            if numeros_nao_encontrados:
                resumo += f"\n3️⃣  ❌ Números não encontrados ({len(numeros_nao_encontrados)}):\n"
                resumo += f"{', '.join(numeros_nao_encontrados)}\n"
            else:
                resumo += f"\n3️⃣  ✅ Números não encontrados: 0\n"
            
            if erros > 0:
                resumo += f"\n⚠️ Erros: {erros}\n"
            
            messagebox.showinfo("Sucesso", resumo)
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro geral: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante operação: {str(e)}")


def main():
    root = tk.Tk()
    app = AutomacoesEPC(root)
    root.mainloop()


if __name__ == "__main__":
    main()
