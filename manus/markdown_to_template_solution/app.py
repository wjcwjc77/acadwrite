import os
import sys
from src.main import TemplateMapper

# 添加根目录路径
sys.path.append(os.path.dirname(__file__))
sys_path = os.path.dirname(__file__)
mapper = TemplateMapper()

output_file = mapper.process(os.path.join(sys_path, "asserts", "comprehensive_document.md"), os.path.join(sys_path, "asserts", "template.docx"), os.path.join(sys_path, "asserts", "output.docx"))