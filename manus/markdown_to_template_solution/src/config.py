"""
配置文件，包含全局配置和常量
"""

# 支持的模板格式
SUPPORTED_TEMPLATE_FORMATS = ['docx', 'tex']

# 支持的输出格式
SUPPORTED_OUTPUT_FORMATS = ['docx', 'tex']

# 大模型API配置
AI_MODEL_CONFIG = {
    'api_type': 'openai',  # 可选: openai, azure, etc.
    'model_name': 'gpt-4',  # 使用的模型名称
    'temperature': 0.3,     # 生成文本的随机性
    'max_tokens': 1000,     # 最大生成token数
}

# Markdown元素到模板样式的默认映射
DEFAULT_STYLE_MAPPING = {
    'docx': {
        'heading_1': 'Heading 1',
        'heading_2': 'Heading 2',
        'heading_3': 'Heading 3',
        'heading_4': 'Heading 4',
        'heading_5': 'Heading 5',
        'heading_6': 'Heading 6',
        'paragraph': 'Normal',
        'code_block': 'Code',
        'block_quote': 'Quote',
        'list_item': 'List Paragraph',
        'table': 'Table Normal',
        'image_caption': 'Caption',
    },
    'tex': {
        'heading_1': '\\section',
        'heading_2': '\\subsection',
        'heading_3': '\\subsubsection',
        'heading_4': '\\paragraph',
        'heading_5': '\\subparagraph',
        'heading_6': '\\subparagraph',
        'paragraph': '',  # 默认段落不需要特殊命令
        'code_block': 'verbatim',
        'block_quote': 'quote',
        'list_item': 'itemize',
        'table': 'tabular',
        'image_caption': 'caption',
    }
}

# 样式冲突解决策略
STYLE_CONFLICT_RESOLUTION = {
    'priority': 'template',  # 'template' 或 'content'，决定冲突时优先使用哪方的样式
    'merge_strategy': 'override',  # 'override' 或 'blend'，决定是完全覆盖还是混合样式
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',  # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'template_mapper.log',
}
