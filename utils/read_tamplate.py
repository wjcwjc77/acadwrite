from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document("tsinghua_template.docx")

with open("template_format.txt", "w", encoding="utf-8") as file:
    for para in doc.paragraphs:
        file.write(f"\n段落: {para.text[:30]}...")  # 写入前30个字符
        
        # 段落对齐方式
        alignment = para.paragraph_format.alignment
        align_name = "未知"
        if alignment == WD_ALIGN_PARAGRAPH.LEFT:
            align_name = "左对齐"
        elif alignment == WD_ALIGN_PARAGRAPH.CENTER:
            align_name = "居中"
        elif alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            align_name = "右对齐"
        file.write(f"对齐方式: {align_name}\n")

        # 遍历段落中的运行（Run）
        for run in para.runs:
            file.write(f"  文本块: {run.text}\n")
            font = run.font
            
            # 字体名称
            font_name = font.name
            if not font_name:  # 如果未显式设置，可能继承样式
                font_name = "默认字体"
            file.write(f"    字体: {font_name}\n")
            
            # 加粗/斜体
            bold = "是" if font.bold else "否"
            italic = "是" if font.italic else "否"
            file.write(f"    加粗: {bold}, 斜体: {italic}\n")
            
            # 字号（转换为磅值）
            if font.size:
                file.write(f"    字号: {font.size.pt} 磅\n")
            else:
                file.write("    字号: 默认\n")