"""
内容映射模块，负责将Markdown内容映射到模板结构中
"""

import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class ContentMapper:
    """
    内容映射器，将Markdown内容结构映射到模板结构
    """
    
    def __init__(self):
        self.structure_issues = []
    
    def map(self, content_structure: Dict[str, Any], template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        将内容结构映射到模板结构
        
        Args:
            content_structure: Markdown内容的结构化表示
            template_structure: 模板的结构化表示
            
        Returns:
            映射后的内容结构
        """
        logger.info("开始内容映射")
        
        # 重置问题列表
        self.structure_issues = []
        
        # 获取模板类型
        template_type = template_structure.get('type', '')
        
        # 根据模板类型选择不同的映射策略
        if template_type == 'docx':
            mapped_content = self._map_to_docx(content_structure, template_structure)
        elif template_type == 'tex':
            mapped_content = self._map_to_tex(content_structure, template_structure)
        else:
            logger.warning(f"未知的模板类型: {template_type}，使用通用映射")
            mapped_content = self._map_generic(content_structure, template_structure)
        
        logger.info(f"内容映射完成，发现 {len(self.structure_issues)} 个结构问题")
        return mapped_content
    
    def has_structure_issues(self) -> bool:
        """
        检查是否存在结构匹配问题
        
        Returns:
            是否存在问题
        """
        return len(self.structure_issues) > 0
    
    def get_structure_issues(self) -> List[Dict[str, Any]]:
        """
        获取结构匹配问题列表
        
        Returns:
            问题列表
        """
        return self.structure_issues
    
    def _map_to_docx(self, content_structure: Dict[str, Any], template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        将内容映射到docx模板
        
        Args:
            content_structure: Markdown内容结构
            template_structure: docx模板结构
            
        Returns:
            映射后的内容结构
        """
        # 创建映射结果
        mapped_content = {
            'type': 'mapped_content',
            'template_type': 'docx',
            'elements': []
        }
        
        # 获取模板中的样式
        template_styles = template_structure.get('styles', {})
        template_elements = template_structure.get('structure', [])
        
        # 分析模板结构，找出标题层级和段落样式
        heading_styles = self._extract_heading_styles(template_elements)
        paragraph_style = self._extract_default_paragraph_style(template_elements)
        
        # 处理内容元素
        content_elements = content_structure.get('elements', [])
        
        for element in content_elements:
            element_type = element.get('type', '')
            
            if element_type == 'heading':
                # 映射标题
                level = element.get('level', 1)
                style_name = self._get_heading_style_for_level(level, heading_styles)
                
                if not style_name:
                    # 记录问题：模板中没有对应级别的标题样式
                    self.structure_issues.append({
                        'type': 'missing_heading_style',
                        'level': level,
                        'text': element.get('text', '')
                    })
                    style_name = f"Heading {level}"  # 使用默认样式
                
                mapped_element = {
                    'type': 'heading',
                    'level': level,
                    'text': element.get('text', ''),
                    'style': style_name
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'paragraph':
                # 映射段落
                mapped_element = {
                    'type': 'paragraph',
                    'text': element.get('text', ''),
                    'style': paragraph_style
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'list' or element_type == 'list_item':
                # 映射列表
                list_type = element.get('list_type', 'unordered')
                mapped_element = {
                    'type': 'list_item',
                    'text': element.get('text', ''),
                    'list_type': list_type,
                    'style': 'List Paragraph'
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'code_block':
                # 映射代码块
                mapped_element = {
                    'type': 'code_block',
                    'text': element.get('text', ''),
                    'style': 'Code'
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'block_quote':
                # 映射引用块
                mapped_element = {
                    'type': 'block_quote',
                    'text': element.get('text', ''),
                    'style': 'Quote'
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'table':
                # 映射表格
                mapped_element = {
                    'type': 'table',
                    'rows': element.get('rows', []),
                    'style': 'Table Normal'
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'image':
                # 映射图片
                mapped_element = {
                    'type': 'image',
                    'src': element.get('src', ''),
                    'alt': element.get('alt', ''),
                    'caption_style': 'Caption'
                }
                mapped_content['elements'].append(mapped_element)
        
        return mapped_content
    
    def _map_to_tex(self, content_structure: Dict[str, Any], template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        将内容映射到tex模板
        
        Args:
            content_structure: Markdown内容结构
            template_structure: tex模板结构
            
        Returns:
            映射后的内容结构
        """
        # 创建映射结果
        mapped_content = {
            'type': 'mapped_content',
            'template_type': 'tex',
            'elements': []
        }
        
        # 获取模板中的样式
        template_styles = template_structure.get('styles', {})
        document_class = template_structure.get('document_class', {})
        packages = template_structure.get('packages', [])
        
        # 保存文档类和包信息
        mapped_content['document_class'] = document_class
        mapped_content['packages'] = packages
        
        # 处理内容元素
        content_elements = content_structure.get('elements', [])
        
        for element in content_elements:
            element_type = element.get('type', '')
            
            if element_type == 'heading':
                # 映射标题
                level = element.get('level', 1)
                command = self._get_tex_heading_command(level, template_styles)
                
                if not command:
                    # 记录问题：模板中没有对应级别的标题命令
                    self.structure_issues.append({
                        'type': 'missing_heading_command',
                        'level': level,
                        'text': element.get('text', '')
                    })
                    command = self._get_default_tex_heading_command(level)
                
                mapped_element = {
                    'type': 'heading',
                    'level': level,
                    'text': element.get('text', ''),
                    'command': command
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'paragraph':
                # 映射段落
                mapped_element = {
                    'type': 'paragraph',
                    'text': element.get('text', '')
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'list' or element_type == 'list_item':
                # 映射列表
                list_type = element.get('list_type', 'unordered')
                env_type = 'itemize' if list_type == 'unordered' else 'enumerate'
                
                mapped_element = {
                    'type': 'environment',
                    'env_type': env_type,
                    'items': [element.get('text', '')]
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'code_block':
                # 映射代码块
                mapped_element = {
                    'type': 'environment',
                    'env_type': 'verbatim',
                    'content': element.get('text', '')
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'block_quote':
                # 映射引用块
                mapped_element = {
                    'type': 'environment',
                    'env_type': 'quote',
                    'content': element.get('text', '')
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'table':
                # 映射表格
                mapped_element = {
                    'type': 'environment',
                    'env_type': 'tabular',
                    'content': element.get('content', '')
                }
                mapped_content['elements'].append(mapped_element)
                
            elif element_type == 'image':
                # 映射图片
                mapped_element = {
                    'type': 'command',
                    'name': 'includegraphics',
                    'options': [],
                    'arguments': [element.get('src', '')],
                    'caption': element.get('alt', '')
                }
                mapped_content['elements'].append(mapped_element)
        
        return mapped_content
    
    def _map_generic(self, content_structure: Dict[str, Any], template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        通用映射策略
        
        Args:
            content_structure: Markdown内容结构
            template_structure: 模板结构
            
        Returns:
            映射后的内容结构
        """
        # 简单地复制内容结构，添加映射标记
        mapped_content = content_structure.copy()
        mapped_content['type'] = 'mapped_content'
        mapped_content['template_type'] = 'generic'
        
        return mapped_content
    
    def _extract_heading_styles(self, template_elements: List[Dict[str, Any]]) -> Dict[int, str]:
        """
        从模板元素中提取标题样式
        
        Args:
            template_elements: 模板元素列表
            
        Returns:
            标题级别到样式名称的映射
        """
        heading_styles = {}
        
        for element in template_elements:
            if element.get('type') == 'heading':
                level = element.get('level', 1)
                style = element.get('style', f"Heading {level}")
                heading_styles[level] = style
        
        return heading_styles
    
    def _extract_default_paragraph_style(self, template_elements: List[Dict[str, Any]]) -> str:
        """
        从模板元素中提取默认段落样式
        
        Args:
            template_elements: 模板元素列表
            
        Returns:
            默认段落样式名称
        """
        for element in template_elements:
            if element.get('type') == 'paragraph':
                return element.get('style', 'Normal')
        
        return 'Normal'  # 默认样式
    
    def _get_heading_style_for_level(self, level: int, heading_styles: Dict[int, str]) -> Optional[str]:
        """
        获取指定级别标题的样式
        
        Args:
            level: 标题级别
            heading_styles: 标题样式映射
            
        Returns:
            样式名称，如果没有找到则返回None
        """
        return heading_styles.get(level)
    
    def _get_tex_heading_command(self, level: int, template_styles: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """
        获取指定级别标题的LaTeX命令
        
        Args:
            level: 标题级别
            template_styles: 模板样式定义
            
        Returns:
            LaTeX命令，如果没有找到则返回None
        """
        level_to_command = {
            1: 'section',
            2: 'subsection',
            3: 'subsubsection',
            4: 'paragraph',
            5: 'subparagraph'
        }
        
        command_name = level_to_command.get(level)
        if not command_name:
            return None
        
        style = template_styles.get(command_name)
        if style:
            return style.get('definition', f'\\{command_name}')
        
        return f'\\{command_name}'
    
    def _get_default_tex_heading_command(self, level: int) -> str:
        """
        获取默认的LaTeX标题命令
        
        Args:
            level: 标题级别
            
        Returns:
            默认的LaTeX命令
        """
        level_to_command = {
            1: '\\section',
            2: '\\subsection',
            3: '\\subsubsection',
            4: '\\paragraph',
            5: '\\subparagraph',
            6: '\\subparagraph'
        }
        
        return level_to_command.get(level, '\\section')
