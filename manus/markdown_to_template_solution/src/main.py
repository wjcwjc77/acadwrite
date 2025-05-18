"""
主模块，提供程序入口和主要流程控制
"""

import os
import logging
import argparse
from typing import Dict, Any

from .config import LOG_CONFIG, SUPPORTED_TEMPLATE_FORMATS, SUPPORTED_OUTPUT_FORMATS
from .markdown_parser import MarkdownParser
from .template_parser import TemplateParserFactory
from .content_mapper import ContentMapper
from .style_mapper import StyleMapper
from .output_generator import OutputGeneratorFactory
from .ai_helper import AIHelper

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['level']),
    format=LOG_CONFIG['format'],
    filename=LOG_CONFIG['file']
)
logger = logging.getLogger(__name__)


class TemplateMapper:
    """
    主类，负责协调各模块完成从Markdown到模板的映射过程
    """
    
    def __init__(self):
        self.markdown_parser = MarkdownParser()
        self.ai_helper = AIHelper()
        
    def process(self, markdown_file: str, template_file: str, output_file: str = None) -> str:
        """
        处理Markdown文件和模板文件，生成最终输出
        
        Args:
            markdown_file: Markdown文件路径
            template_file: 模板文件路径
            output_file: 输出文件路径，如果为None则自动生成
            
        Returns:
            输出文件路径
        """
        logger.info(f"开始处理: {markdown_file} -> {template_file}")
        
        # 确定模板格式和输出格式
        template_format = self._get_file_extension(template_file)
        if template_format not in SUPPORTED_TEMPLATE_FORMATS:
            raise ValueError(f"不支持的模板格式: {template_format}")
        
        # 如果未指定输出文件，则自动生成
        if output_file is None:
            output_file = self._generate_output_filename(markdown_file, template_format)
        
        # 解析Markdown文件
        logger.info(f"解析Markdown文件: {markdown_file}")
        markdown_content = self._read_file(markdown_file)
        content_structure = self.markdown_parser.parse(markdown_content)
        
        # 解析模板文件
        logger.info(f"解析模板文件: {template_file}")
        template_parser = TemplateParserFactory.create_parser(template_format)
        template_structure = template_parser.parse(template_file)
        
        # 内容映射
        logger.info("执行内容映射")
        content_mapper = ContentMapper()
        mapped_content = content_mapper.map(content_structure, template_structure)
        
        # 样式映射
        logger.info("执行样式映射")
        style_mapper = StyleMapper(template_format)
        styled_content = style_mapper.apply_styles(mapped_content, template_structure)
        
        # 检查结构匹配问题
        if content_mapper.has_structure_issues():
            logger.info("检测到结构匹配问题，尝试使用AI辅助调整")
            issues = content_mapper.get_structure_issues()
            adjusted_content = self.ai_helper.adjust_structure(styled_content, issues)
            if adjusted_content:
                styled_content = adjusted_content
        
        # 生成输出文件
        logger.info(f"生成输出文件: {output_file}")
        output_generator = OutputGeneratorFactory.create_generator(template_format)
        output_generator.generate(styled_content, template_structure, output_file)
        
        logger.info(f"处理完成: {output_file}")
        return output_file
    
    def _read_file(self, file_path: str) -> str:
        """读取文件内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _get_file_extension(self, file_path: str) -> str:
        """获取文件扩展名"""
        return os.path.splitext(file_path)[1].lstrip('.').lower()
    
    def _generate_output_filename(self, input_file: str, output_format: str) -> str:
        """生成输出文件名"""
        base_name = os.path.splitext(input_file)[0]
        return f"{base_name}_output.{output_format}"


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='将Markdown文件映射到模板中')
    parser.add_argument('markdown_file', help='输入的Markdown文件路径')
    parser.add_argument('template_file', help='模板文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        mapper = TemplateMapper()
        output_file = mapper.process(args.markdown_file, args.template_file, args.output)
        print(f"处理完成，输出文件: {output_file}")
    except Exception as e:
        logger.error(f"处理过程中出错: {str(e)}", exc_info=True)
        print(f"错误: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
