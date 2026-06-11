import os
import sys

# 直接从文件中提取转换器类
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
            print("已注册: HTML")
        except Exception as e:
            print(f"HTML注册失败: {e}")
        
        self.converters['.txt'] = self._convert_text
        self.converters['.md'] = self._convert_text
        print("已注册: TXT, MD")
        
        try:
            import mammoth
            self._mammoth = mammoth
            self.converters['.docx'] = self._convert_docx
            print("已注册: DOCX")
        except Exception as e:
            print(f"DOCX注册失败: {e}")
        
        try:
            import pdfplumber
            self._pdfplumber = pdfplumber
            self.converters['.pdf'] = self._convert_pdf
            print("已注册: PDF")
        except Exception as e:
            print(f"PDF注册失败: {e}")
        
        try:
            from pptx import Presentation
            self._pptx = Presentation
            self.converters['.pptx'] = self._convert_pptx
            print("已注册: PPTX")
        except Exception as e:
            print(f"PPTX注册失败: {e}")
        
        try:
            import json
            self._json = json
            self.converters['.ipynb'] = self._convert_ipynb
            print("已注册: IPYNB")
        except Exception as e:
            print(f"IPYNB注册失败: {e}")
    
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
        print(f"文件路径: {file_path}")
        print(f"文件扩展名: '{file_ext}'")
        print(f"支持的格式: {list(self.converters.keys())}")
        
        if file_ext in self.converters:
            converter = self.converters[file_ext]
            with open(file_path, 'rb') as fh:
                result = converter(fh)
                return result
        else:
            raise Exception(f"不支持的文件格式: {file_ext}")

# 测试
if __name__ == "__main__":
    converter = MarkItDownConverter()
    print("\n支持的格式:", list(converter.converters.keys()))
    
    # 测试docx
    test_docx = 'packages/markitdown/tests/test_files/test.docx'
    if os.path.exists(test_docx):
        print(f"\n测试文件: {test_docx}")
        try:
            result = converter.convert(test_docx)
            print('DOCX转换成功!')
            print('内容预览:', result[:300] + '...')
        except Exception as e:
            print('DOCX转换失败:', e)
    else:
        print(f"\n测试文件不存在: {test_docx}")
    
    # 测试pdf
    test_pdf = 'packages/markitdown/tests/test_files/test.pdf'
    if os.path.exists(test_pdf):
        print(f"\n测试文件: {test_pdf}")
        try:
            result = converter.convert(test_pdf)
            print('PDF转换成功!')
            print('内容预览:', result[:300] + '...')
        except Exception as e:
            print('PDF转换失败:', e)
    else:
        print(f"\n测试文件不存在: {test_pdf}")