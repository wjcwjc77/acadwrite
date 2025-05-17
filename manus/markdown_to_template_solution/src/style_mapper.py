"""
样式映射模块，负责将内容元素应用模板样式
"""

import logging
from typing import Dict, List, Any, Optional

from .config import DEFAULT_STYLE_MAPPING, STYLE_CONFLICT_RESOLUTION

logger = logging.getLogger(__name__)


class StyleMapper:
    """
    样式映射器，将内容元素应用模板样式
    """
    
    def __init__(self, template_format: str):
        """
        初始化样式映射器
        
        Args:
            template_format: 模板格式，如'docx'或'tex'
        """
        self.template_format = template_format
        self.default_mapping = DEFAULT_STYLE_MAPPING.get(template_format, {})
        self.conflict_resolution = STYLE_CONFLICT_RESOLUTION
    
    def apply_styles(self, mapped_content: Dict[str, Any], template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用样式到映射后的内容
        
        Args:
            mapped_content: 映射后的内容结构
            template_structure: 模板结构
            
        Returns:
            应用样式后的内容结构
        """
        logger.info(f"开始应用{self.template_format}格式的样式")
        
        # 获取模板样式
        template_styles = template_structure.get('styles', {})
        
        # 创建样式应用结果
        styled_content = mapped_content.copy()
        
        # 处理每个元素
        elements = styled_content.get('elements', [])
        for i, element in enumerate(elements):
            element_type = element.get('type', '')
            
            if self.template_format == 'docx':
                elements[i] = self._apply_docx_style(element, template_styles)
            elif self.template_format == 'tex':
                elements[i] = self._apply_tex_style(element, template_styles)
            else:
                logger.warning(f"未知的模板格式: {self.template_format}，跳过样式应用")
        
        styled_content['elements'] = elements
        logger.info("样式应用完成")
        return styled_content
    
    def _apply_docx_style(self, element: Dict[str, Any], template_styles: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        应用docx样式到元素
        
        Args:
            element: 内容元素
            template_styles: 模板样式定义
            
        Returns:
            应用样式后的元素
        """
        element_type = element.get('type', '')
        
        # 根据元素类型获取默认样式名称
        default_style_name = self._get_default_docx_style(element_type)
        
        # 获取元素当前样式
        current_style_name = element.get('style', default_style_name)
        
        # 检查模板中是否有对应样式
        if current_style_name in template_styles:
            # 使用模板中的样式
            template_style = template_styles[current_style_name]
            
            # 应用样式属性
            styled_element = element.copy()
            styled_element['style'] = current_style_name
            styled_element['style_properties'] = template_style
            
            return styled_element
        else:
            # 模板中没有对应样式，使用默认样式
            logger.warning(f"模板中未找到样式: {current_style_name}，使用默认样式: {default_style_name}")
            
            styled_element = element.copy()
            styled_element['style'] = default_style_name
            
            return styled_element
    
    def _apply_tex_style(self, element: Dict[str, Any], template_styles: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        应用tex样式到元素
        
        Args:
            element: 内容元素
            template_styles: 模板样式定义
            
        Returns:
            应用样式后的元素
        """
        element_type = element.get('type', '')
        
        styled_element = element.copy()
        
        if element_type == 'heading':
            # 处理标题
            level = element.get('level', 1)
            command = element.get('command', self._get_default_tex_heading_command(level))
            
            # 检查模板中是否有对应命令的样式
            command_name = command.lstrip('\\').split('{')[0]
            if command_name in template_styles:
                # 使用模板中的样式
                template_style = template_styles[command_name]
                styled_element['command'] = template_style.get('definition', command)
            
        elif element_type == 'environment':
            # 处理环境
            env_type = element.get('env_type', '')
            
            # 检查模板中是否有对应环境的样式
            if env_type in template_styles:
                # 使用模板中的样式
                template_style = template_styles[env_type]
                styled_element['begin_def'] = template_style.get('begin_def', f'\\begin{{{env_type}}}')
                styled_element['end_def'] = template_style.get('end_def', f'\\end{{{env_type}}}')
        
        return styled_element
    
    def _get_default_docx_style(self, element_type: str) -> str:
        """
        获取元素类型的默认docx样式名称
        
        Args:
            element_type: 元素类型
            
        Returns:
            默认样式名称
        """
        # 将元素类型映射到样式名称
        type_to_style = {
            'heading': 'Heading',  # 会根据级别进一步处理
            'paragraph': 'Normal',
            'list_item': 'List Paragraph',
            'code_block': 'Code',
            'block_quote': 'Quote',
            'table': 'Table Normal',
            'image': 'Normal'
        }
        
        if element_type == 'heading':
            # 标题需要特殊处理，因为有级别
            return 'Heading 1'  # 默认一级标题
        
        return type_to_style.get(element_type, 'Normal')
    
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
