# MarkItDown 文件转换器

原仓库：https://github.com/microsoft/markitdown

一个基于 Python 的文件转 Markdown 工具，支持多种常见文档格式的批量转换。

本仓库在原仓库的基础上，设计了界面以及部署方式，不用通过命令行进行转换，更适合用户操作。

## 🎯 功能特点

- **批量处理**：支持一次选择多个文件进行转换
- **多格式支持**：TXT、MD、DOCX、PDF 等常见文档格式
- **可视化界面**：基于 Tkinter 的图形界面，操作简单直观
- **自定义输出**：可自由选择转换后的文件保存目录
- **进度显示**：实时显示转换进度，让您随时了解处理状态
- **错误提示**：详细的错误信息提示，方便排查问题

## 🚀 快速开始

### 方式一：直接运行（推荐）

**💡 重要说明**：仓库中不包含虚拟环境和依赖包，用户克隆后需要自己创建环境并安装依赖。

如果您的系统已安装 Python 环境，可以直接运行脚本：

```bash
# 克隆仓库到本地
git clone https://github.com/dzh-gitcode/markitdown
cd markitdown-0.1.6

# 创建虚拟环境（首次运行必须执行）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖包（首次运行必须执行）
pip install mammoth pdfplumber python-docx python-pptx markdownify

# 启动程序
python simple-converter.py
```

**为什么需要安装依赖？**
- `.venv` 目录是本地创建的虚拟环境，不会上传到 GitHub
- 每次克隆新仓库或在新机器上运行，都需要安装依赖包
- 安装一次后，后续运行只需激活环境并启动程序

### 方式二：使用打包好的程序

对于 Windows 用户，可以直接运行已打包的可执行文件，无需安装 Python：

```
dist/MarkItDown-Converter/MarkItDown-Converter.exe
```

注：打包后文件较大，未上传到 GitHub 仓库。如果需要可联系作者获取。

```### 方式三：使用现有 Conda 环境

如果您已经有 Conda 环境（如 base 环境），可以直接在该环境中安装依赖运行：

```bash
# 激活您的 Conda 环境
conda activate base

# 安装依赖
pip install mammoth pdfplumber python-docx python-pptx markdownify

# 运行程序
python simple-converter.py
```

### 🤔 为什么有多种环境选择？

**推荐选择：方式一（使用 .venv 虚拟环境）**

- 这是 Python 官方推荐的标准虚拟环境方案
- 轻量级，隔离性好，适合单个项目
- 不会与系统 Python 或其他项目产生依赖冲突

**使用 Conda 的情况：**

- 如果您已经安装了 Anaconda/Miniconda，并且希望复用现有的环境
- 如果您的系统中已经有其他项目使用 Conda 管理依赖
- 注意：使用 Conda 环境时，确保先激活环境再安装依赖

**总结：**

对于这个项目，**推荐使用方式一（.venv 虚拟环境）**，因为它更轻量、更简洁，也更适合作为独立项目管理。

## 📦 打包成可执行文件

如需将程序打包成独立的 EXE 文件：

```bash
# 安装打包工具
pip install pyinstaller

# 清理旧的构建文件
rmdir /s /q dist build 2>nul  # Windows
# rm -rf dist build  # macOS/Linux

# 执行打包命令
pyinstaller --windowed --name MarkItDown-Converter ^
  --exclude-module matplotlib ^
  --exclude-module scipy ^
  --exclude-module PyQt5 ^
  --exclude-module tensorflow ^
  --exclude-module torch ^
  --exclude-module sklearn ^
  --exclude-module IPython ^
  --exclude-module notebook ^
  --exclude-module pandas ^
  simple-converter.py
```

打包完成后，可执行文件位于：
```
dist/MarkItDown-Converter/MarkItDown-Converter.exe
```

## 💡 使用说明

1. **添加文件**：点击「添加文件」按钮，选择要转换的文档
2. **选择输出目录**：默认输出到「文档/MarkItDown输出」目录，可点击「浏览」自定义
3. **开始转换**：点击「开始转换」按钮，等待转换完成
4. **查看结果**：转换成功后会提示输出目录位置

## ❓ 常见问题

### 问题：转换失败，提示「权限拒绝」

**原因**：程序无法将文件写入指定目录（通常是系统目录权限限制）

**解决方案**：
- 选择其他输出目录（如 D 盘下的文件夹）
- 右键点击程序，选择「以管理员身份运行」
- 使用默认输出目录（位于用户文档文件夹下）

### 问题：提示「不支持的文件格式」

**当前支持格式**：TXT、MD、DOCX、PDF

如果需要支持更多格式，可以安装完整的 MarkItDown 库：
```bash
pip install 'markitdown[all]'
```

### 问题：打包时出现 cryptography 错误

**解决方案**：更新 cryptography 库或使用更新版本的 Python

## 🛠️ 技术栈

- **Python 3.7+**：核心开发语言
- **Tkinter**：图形用户界面框架
- **Mammoth**：DOCX 文档解析
- **pdfplumber**：PDF 文档解析
- **python-docx**：Word 文档处理
- **python-pptx**：PowerPoint 文档处理
- **PyInstaller**：打包工具

## 📄 许可证

本项目基于 MIT 许可证开源。