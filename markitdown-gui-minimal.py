import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MarkItDownConverter:
    def __init__(self):
        self.converters = {}
        self._register_converters()
    
    def _register_converters(self):
        try:
            from markdownify import markdownify as md
            self._html_md = md
            self.converters['.html'] = self._convert_html
            self.converters['.htm'] = self._convert_html
        except:
            pass
        
        self.converters['.txt'] = self._convert_text
        self.converters['.md'] = self._convert_text
        
        try:
            import mammoth
            self._mammoth = mammoth
            self.converters['.docx'] = self._convert_docx
        except:
            pass
        
        try:
            import pdfplumber
            self._pdfplumber = pdfplumber
            self.converters['.pdf'] = self._convert_pdf
        except:
            pass
        
        try:
            from pptx import Presentation
            self._pptx = Presentation
            self.converters['.pptx'] = self._convert_pptx
        except:
            pass
        
        try:
            import json
            self._json = json
            self.converters['.ipynb'] = self._convert_ipynb
        except:
            pass
    
    def _convert_text(self, stream):
        content = stream.read().decode('utf-8', errors='replace')
        return content
    
    def _convert_html(self, stream):
        content = stream.read().decode('utf-8', errors='replace')
        return self._html_md(content)
    
    def _convert_docx(self, stream):
        result = self._mammoth.convert_to_markdown(stream)
        return result.value
    
    def _convert_pdf(self, stream):
        with self._pdfplumber.open(stream) as pdf:
            text = "\n\n".join([page.extract_text() for page in pdf.pages])
        return text
    
    def _convert_pptx(self, stream):
        prs = self._pptx(stream)
        slides_content = []
        for slide in prs.slides:
            slide_text = []
            for shape in slide.shapes:
                if hasattr(shape, 'text'):
                    slide_text.append(shape.text)
            slides_content.append("\n".join(slide_text))
        return "\n\n---\n\n".join(slides_content)
    
    def _convert_ipynb(self, stream):
        nb = self._json.load(stream)
        content = []
        for cell in nb.get('cells', []):
            if cell['cell_type'] == 'markdown':
                content.append(''.join(cell['source']))
            elif cell['cell_type'] == 'code':
                content.append(f"```python\n{''.join(cell['source'])}\n```")
        return '\n\n'.join(content)
    
    def convert(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in self.converters:
            converter = self.converters[file_ext]
            with open(file_path, 'rb') as fh:
                result = converter(fh)
                return result
        else:
            raise Exception(f"不支持的文件格式: {file_ext}")

class MarkItDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown 转换器")
        self.root.geometry("600x450")
        
        self.converter = MarkItDownConverter()
        self.selected_files = []
        
        self.create_widgets()
        
    def create_widgets(self):
        title_label = ttk.Label(self.root, text="MarkItDown 文件转换器", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=10)
        
        self.file_list_frame = ttk.Frame(self.root)
        self.file_list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(self.file_list_frame, selectmode=tk.MULTIPLE, width=70, height=12)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        self.add_btn = ttk.Button(self.button_frame, text="添加文件", command=self.add_files)
        self.add_btn.grid(row=0, column=0, padx=5)
        
        self.remove_btn = ttk.Button(self.button_frame, text="移除选中", command=self.remove_selected)
        self.remove_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(self.button_frame, text="清空列表", command=self.clear_list)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Label(self.output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_path_var = tk.StringVar(value=os.path.expanduser("~\\Desktop"))
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path_var, width=50)
        self.output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.browse_output_btn = ttk.Button(self.output_frame, text="浏览", command=self.browse_output)
        self.browse_output_btn.pack(side=tk.RIGHT, padx=5)
        
        self.convert_btn = ttk.Button(self.root, text="开始转换", command=self.convert_files)
        self.convert_btn.pack(pady=10)
        
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.pack(pady=5)
        
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, foreground="blue")
        self.status_label.pack(pady=5)
        
        supported_formats = "支持格式: TXT, MD, HTML, DOCX, PDF, PPTX, IPYNB"
        ttk.Label(self.root, text=supported_formats, font=('Helvetica', 9), foreground="gray").pack(pady=5)
        
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="选择文件",
            filetypes=[
                ("所有支持的文件", "*.txt;*.md;*.html;*.htm;*.docx;*.pdf;*.pptx;*.ipynb"),
                ("文本文件", "*.txt"),
                ("Markdown文件", "*.md"),
                ("HTML文件", "*.html"),
                ("Word文档", "*.docx"),
                ("PDF文件", "*.pdf"),
                ("PowerPoint", "*.pptx"),
                ("Jupyter笔记本", "*.ipynb"),
                ("所有文件", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status(f"已添加 {len(files)} 个文件")
    
    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()
        for index in reversed(selected_indices):
            del self.selected_files[index]
            self.file_listbox.delete(index)
        
        self.update_status(f"已移除 {len(selected_indices)} 个文件")
    
    def clear_list(self):
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_status("列表已清空")
    
    def browse_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_path_var.set(path)
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def convert_files(self):
        if not self.selected_files:
            messagebox.showwarning("警告", "请先添加要转换的文件")
            return
        
        output_dir = self.output_path_var.get()
        if not os.path.isdir(output_dir):
            messagebox.showwarning("警告", "输出目录无效")
            return
        
        total_files = len(self.selected_files)
        success_count = 0
        fail_count = 0
        failed_files = []
        
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for i, file_path in enumerate(self.selected_files):
            try:
                self.update_status(f"正在转换: {os.path.basename(file_path)}")
                
                result = self.converter.convert(file_path)
                
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}.md")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                success_count += 1
                
            except Exception as e:
                fail_count += 1
                failed_files.append(f"{os.path.basename(file_path)}: {str(e)}")
            
            self.progress['value'] = i + 1
            self.root.update_idletasks()
        
        self.update_status(f"转换完成: 成功 {success_count} 个, 失败 {fail_count} 个")
        
        if failed_files:
            error_message = "\n".join(failed_files)
            messagebox.showerror("转换失败", f"以下文件转换失败:\n{error_message}")
        else:
            messagebox.showinfo("转换完成", f"所有 {success_count} 个文件转换成功！")

def main():
    root = tk.Tk()
    app = MarkItDownGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()