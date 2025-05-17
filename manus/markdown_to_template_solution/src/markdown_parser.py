"""
Markdown解析模块，负责解析Markdown文件并转换为内部结构表示
"""

import re
import logging
from typing import Dict, List, Any, Union, Optional
import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class MarkdownStructureExtractor(Treeprocessor):
    """
    Markdown处理器，用于提取文档结构
    """
    def __init__(self, md):
        super().__init__(md)
        self.structure = []
        
    def run(self, root):
        """处理解析树，提取结构信息"""
        self._process_element(root)
        return root
    
    def _process_element(self, element, parent_path=None):
        """递归处理元素，构建结构树"""
        if parent_path is None:
            parent_path = []
        
        # 处理当前元素
        element_info = self._extract_element_info(element)
        if element_info:
            current_path = parent_path + [len(self.structure)]
            element_info['path'] = current_path
            self.structure.append(element_info)
        
        # 递归处理子元素
        for child in element:
            self._process_element(child, parent_path)
    
    def _extract_element_info(self, element) -> Optional[Dict[str, Any]]:
        """提取元素信息"""
        tag = element.tag
        text = element.text or ""
        tail = element.tail or ""
        attrib = element.attrib
        
        # 根据标签类型提取不同信息
        if tag.startswith('h') and len(tag) == 2 and tag[1].isdigit():
            # 标题
            level = int(tag[1])
            return {
                'type': 'heading',
                'level': level,
                'text': text.strip(),
                'attributes': attrib
            }
        elif tag == 'p':
            # 段落
            return {
                'type': 'paragraph',
                'text': text.strip(),
                'attributes': attrib
            }
        elif tag == 'ul' or tag == 'ol':
            # 列表
            list_type = 'unordered' if tag == 'ul' else 'ordered'
            return {
                'type': 'list',
                'list_type': list_type,
                'attributes': attrib
            }
        elif tag == 'li':
            # 列表项
            return {
                'type': 'list_item',
                'text': text.strip(),
                'attributes': attrib
            }
        elif tag == 'pre' or tag == 'code':
            # 代码块
            return {
                'type': 'code_block',
                'text': text,
                'attributes': attrib
            }
        elif tag == 'blockquote':
            # 引用块
            return {
                'type': 'block_quote',
                'text': text.strip(),
                'attributes': attrib
            }
        elif tag == 'table':
            # 表格
            return {
                'type': 'table',
                'attributes': attrib
            }
        elif tag == 'tr':
            # 表格行
            return {
                'type': 'table_row',
                'attributes': attrib
            }
        elif tag == 'td' or tag == 'th':
            # 表格单元格
            cell_type = 'header' if tag == 'th' else 'cell'
            return {
                'type': 'table_cell',
                'cell_type': cell_type,
                'text': text.strip(),
                'attributes': attrib
            }
        elif tag == 'img':
            # 图片
            return {
                'type': 'image',
                'src': attrib.get('src', ''),
                'alt': attrib.get('alt', ''),
                'attributes': attrib
            }
        
        return None


class StructureExtractorExtension(Extension):
    """
    Markdown扩展，用于注册结构提取处理器
    """
    def __init__(self, **kwargs):
        self.extractor = None
        super().__init__(**kwargs)
    
    def extendMarkdown(self, md):
        self.extractor = MarkdownStructureExtractor(md)
        md.treeprocessors.register(self.extractor, 'structure_extractor', 175)


class MarkdownParser:
    """
    Markdown解析器，将Markdown文本解析为内部结构表示
    """
    def __init__(self):
        self.extension = StructureExtractorExtension()
        self.md = markdown.Markdown(extensions=[self.extension, 'tables', 'fenced_code'])
    
    def parse(self, markdown_text: str) -> Dict[str, Any]:
        """
        解析Markdown文本，返回结构化表示
        
        Args:
            markdown_text: Markdown格式的文本
            
        Returns:
            结构化的文档表示
        """
        # 转换Markdown为HTML
        self.md.convert(markdown_text)
        
        # 获取提取的结构
        structure = self.extension.extractor.structure
        
        # 构建文档结构
        document = {
            'type': 'document',
            'elements': structure,
            'metadata': self._extract_metadata(markdown_text)
        }
        
        logger.info(f"解析完成，文档包含 {len(structure)} 个元素")
        return document
    
    def _extract_metadata(self, markdown_text: str) -> Dict[str, str]:
        """
        从Markdown文本中提取元数据
        
        Args:
            markdown_text: Markdown格式的文本
            
        Returns:
            元数据字典
        """
        metadata = {}
        
        # 尝试提取YAML前置元数据
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        yaml_match = re.search(yaml_pattern, markdown_text, re.DOTALL)
        if yaml_match:
            yaml_text = yaml_match.group(1)
            for line in yaml_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        return metadata
