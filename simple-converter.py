import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SimpleConverter:
    def __init__(self):
        self.converters = {}
        self._register_basic_converters()
    
    def _register_basic_converters(self):
        # 基础文本格式
        self.converters['.txt'] = self._convert_text
        self.converters['.md'] = self._convert_text
        
        # DOCX支持
        try:
            import mammoth
            self._mammoth = mammoth
            self.converters['.docx'] = self._convert_docx
            self.converters['.doc'] = self._convert_docx
            print("[INFO] 已加载 DOCX 支持")
        except Exception as e:
            print(f"[WARN] 无法加载 DOCX 支持: {e}")
        
        # PDF支持
        try:
            import pdfplumber
            self._pdfplumber = pdfplumber
            self.converters['.pdf'] = self._convert_pdf
            print("[INFO] 已加载 PDF 支持")
        except Exception as e:
            print(f"[WARN] 无法加载 PDF 支持: {e}")
    
    def _convert_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    
    def _convert_docx(self, file_path):
        with open(file_path, 'rb') as f:
            result = self._mammoth.convert_to_markdown(f)
            return result.value
    
    def _convert_pdf(self, file_path):
        with self._pdfplumber.open(file_path) as pdf:
            text = "\n\n".join([page.extract_text() for page in pdf.pages])
        return text
    
    def convert(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in self.converters:
            return self.converters[file_ext](file_path)
        else:
            raise Exception(f"不支持的格式: {file_ext}\n\n支持的格式: {', '.join(self.converters.keys())}")

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文件转MD转换器")
        self.root.geometry("600x400")
        
        self.converter = SimpleConverter()
        self.selected_files = []
        
        self.create_ui()
    
    def create_ui(self):
        # 标题
        ttk.Label(self.root, text="文件转Markdown转换器", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # 文件列表
        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=70, height=10)
        self.listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # 按钮区
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="添加文件", command=self.add_files).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="移除选中", command=self.remove_files).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="清空列表", command=self.clear_list).grid(row=0, column=2, padx=5)
        
        # 输出目录
        output_frame = ttk.Frame(self.root)
        output_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value=self.get_default_output())
        ttk.Entry(output_frame, textvariable=self.output_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览", command=self.browse_output).pack(side=tk.RIGHT)
        
        # 转换按钮
        ttk.Button(self.root, text="开始转换", command=self.convert_files).pack(pady=10)
        
        # 状态
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.root, textvariable=self.status_var, foreground="blue").pack()
        
        # 支持格式提示
        formats = f"支持格式: {', '.join(sorted(self.converter.converters.keys()))}"
        ttk.Label(self.root, text=formats, font=('Arial', 9), foreground="gray").pack(pady=5)
    
    def get_default_output(self):
        default = os.path.join(os.path.expanduser("~"), "MarkItDown输出")
        if not os.path.exists(default):
            try:
                os.makedirs(default)
            except:
                default = os.path.expanduser("~")
        return default
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="选择文件",
            filetypes=[
                ("支持的文件", "*.txt;*.md;*.docx;*.doc;*.pdf"),
                ("所有文件", "*.*")
            ]
        )
        
        for f in files:
            if f not in self.selected_files:
                self.selected_files.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
        
        self.status_var.set(f"已添加 {len(files)} 个文件")
    
    def remove_files(self):
        selected = self.listbox.curselection()
        for idx in reversed(selected):
            del self.selected_files[idx]
            self.listbox.delete(idx)
        self.status_var.set(f"已移除 {len(selected)} 个文件")
    
    def clear_list(self):
        self.selected_files.clear()
        self.listbox.delete(0, tk.END)
        self.status_var.set("列表已清空")
    
    def browse_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_var.set(path)
    
    def convert_files(self):
        if not self.selected_files:
            messagebox.showwarning("警告", "请先添加文件")
            return
        
        output_dir = self.output_var.get()
        
        # 检查输出目录
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        except Exception as e:
            messagebox.showerror("错误", f"无法创建目录: {e}")
            return
        
        # 检查写入权限
        test_file = os.path.join(output_dir, "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except PermissionError:
            messagebox.showerror("权限错误", f"无法写入目录: {output_dir}\n\n请尝试：\n1. 选择其他目录\n2. 以管理员身份运行程序")
            return
        except Exception as e:
            messagebox.showerror("错误", f"目录检查失败: {e}")
            return
        
        # 执行转换
        success = 0
        failed = []
        
        for i, file_path in enumerate(self.selected_files):
            try:
                self.status_var.set(f"转换中 ({i+1}/{len(self.selected_files)})...")
                self.root.update_idletasks()
                
                content = self.converter.convert(file_path)
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}.md")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success += 1
            except Exception as e:
                failed.append(f"{os.path.basename(file_path)}: {e}")
        
        # 显示结果
        self.status_var.set(f"转换完成: 成功 {success} 个")
        
        if failed:
            error_msg = "\n".join(failed)
            messagebox.showerror("转换失败", f"以下文件转换失败:\n{error_msg}")
        else:
            messagebox.showinfo("成功", f"所有 {success} 个文件转换完成!\n\n输出目录: {output_dir}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()