# AI生成的Markdown格式综述报告映射到模板的使用说明

## 1. 项目概述

本项目实现了一个将AI生成的markdown格式综述报告自动映射到用户提供的.docx或.tex格式模板的工具。该工具能够解析markdown内容和模板文件，智能匹配内容结构与模板样式，并生成符合模板格式要求的最终文档。

## 2. 功能特点

- 支持解析AI生成的markdown格式综述报告
- 支持解析.docx和.tex格式的模板文件
- 智能匹配内容结构与模板样式
- 自动应用模板中定义的样式到内容元素
- 处理标题、段落、列表、表格、图片等多种内容元素
- 当内容结构与模板结构不匹配时，可调用大模型API进行智能调整
- 生成符合模板格式要求的.docx或.tex输出文档

## 3. 安装依赖

在使用本工具前，请确保已安装以下依赖：

```bash
pip install python-docx markdown
```

对于.tex格式的支持，建议安装以下额外依赖：

```bash
pip install jinja2
```

## 4. 使用方法

### 4.1 命令行使用

```bash
python -m src.main <markdown_file> <template_file> [-o <output_file>]
```

参数说明：
- `<markdown_file>`: AI生成的markdown格式综述报告文件路径
- `<template_file>`: 模板文件路径，支持.docx或.tex格式
- `-o, --output`: 可选，输出文件路径，如不指定则自动生成

示例：

```bash
# 使用.docx模板
python -m src.main report.md template.docx -o output.docx

# 使用.tex模板
python -m src.main report.md template.tex -o output.tex
```

### 4.2 作为模块导入

您也可以在Python代码中导入本工具作为模块使用：

```python
from src.main import TemplateMapper

# 创建映射器
mapper = TemplateMapper()

# 处理文件
output_file = mapper.process('report.md', 'template.docx', 'output.docx')

print(f"输出文件: {output_file}")
```

## 5. 工作原理

本工具的工作流程如下：

1. **输入处理**：读取markdown文件和模板文件
2. **Markdown解析**：解析markdown内容，识别标题、段落、列表等元素
3. **模板解析**：根据文件格式选择相应方法解析模板，提取样式和结构信息
4. **内容映射**：将markdown内容结构映射到模板结构
5. **样式应用**：应用模板中定义的样式到内容元素
6. **结构调整**：当发现内容结构与模板结构不匹配时，调用大模型API进行智能调整
7. **输出生成**：根据映射结果和目标格式生成最终文档

## 6. 自定义配置

您可以通过修改`src/config.py`文件来自定义工具的行为：

- 修改默认样式映射规则
- 配置大模型API参数
- 调整样式冲突解决策略
- 设置日志级别和格式

## 7. 注意事项

- 确保模板文件格式正确，且包含必要的样式定义
- 对于复杂的表格和图片，可能需要手动调整最终输出
- 大模型API调用功能需要配置相应的API密钥
- .tex格式的输出可能需要额外的LaTeX环境来编译生成PDF

## 8. 故障排除

如果遇到问题，请检查：

- 依赖库是否正确安装
- 输入文件路径是否正确
- 模板文件格式是否支持
- 日志文件中是否有详细错误信息

## 9. 联系与支持

如有任何问题或建议，请联系项目维护者。
