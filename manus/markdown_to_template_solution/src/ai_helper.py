"""
AI辅助模块，负责调用大模型API进行结构调整
"""

import logging
import json
from typing import Dict, List, Any, Optional

from .config import AI_MODEL_CONFIG

logger = logging.getLogger(__name__)


class AIHelper:
    """
    AI辅助类，用于调用大模型API进行内容结构调整
    """
    
    def __init__(self):
        """
        初始化AI辅助类
        """
        self.config = AI_MODEL_CONFIG
        logger.info(f"初始化AI辅助模块，使用模型: {self.config.get('model_name', 'unknown')}")
    
    def adjust_structure(self, content: Dict[str, Any], issues: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        调用大模型API调整内容结构
        
        Args:
            content: 需要调整的内容结构
            issues: 结构问题列表
            
        Returns:
            调整后的内容结构，如果调整失败则返回None
        """
        if not issues:
            logger.info("没有需要调整的结构问题")
            return None
        
        logger.info(f"开始调用大模型API调整结构，共有 {len(issues)} 个问题")
        
        try:
            # 在实际应用中，这里应该调用真实的大模型API
            # 本demo中使用模拟调用
            adjusted_content = self._simulate_ai_adjustment(content, issues)
            
            logger.info("结构调整完成")
            return adjusted_content
            
        except Exception as e:
            logger.error(f"调用大模型API时出错: {str(e)}", exc_info=True)
            return None
    
    def _simulate_ai_adjustment(self, content: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        模拟大模型API调用进行结构调整
        
        Args:
            content: 需要调整的内容结构
            issues: 结构问题列表
            
        Returns:
            调整后的内容结构
        """
        # 创建调整后的内容副本
        adjusted_content = content.copy()
        elements = adjusted_content.get('elements', []).copy()
        
        # 处理每个问题
        for issue in issues:
            issue_type = issue.get('type', '')
            
            if issue_type == 'missing_heading_style':
                # 处理缺失标题样式问题
                level = issue.get('level', 1)
                text = issue.get('text', '')
                
                # 查找对应的元素
                for i, element in enumerate(elements):
                    if (element.get('type') == 'heading' and 
                        element.get('level') == level and 
                        element.get('text') == text):
                        # 调整样式
                        elements[i]['style'] = f"Heading {level}"
                        logger.info(f"调整了标题样式: {text} -> Heading {level}")
                        break
            
            elif issue_type == 'missing_heading_command':
                # 处理缺失标题命令问题
                level = issue.get('level', 1)
                text = issue.get('text', '')
                
                # 查找对应的元素
                for i, element in enumerate(elements):
                    if (element.get('type') == 'heading' and 
                        element.get('level') == level and 
                        element.get('text') == text):
                        # 调整命令
                        level_to_command = {
                            1: '\\section',
                            2: '\\subsection',
                            3: '\\subsubsection',
                            4: '\\paragraph',
                            5: '\\subparagraph',
                            6: '\\subparagraph'
                        }
                        elements[i]['command'] = level_to_command.get(level, '\\section')
                        logger.info(f"调整了标题命令: {text} -> {elements[i]['command']}")
                        break
        
        adjusted_content['elements'] = elements
        return adjusted_content
    
    def _call_openai_api(self, prompt: str) -> str:
        """
        调用OpenAI API
        
        Args:
            prompt: 提示文本
            
        Returns:
            API响应文本
        """
        # 实际应用中，这里应该调用真实的OpenAI API
        # 本demo中仅作为示例
        logger.info(f"模拟调用OpenAI API，提示长度: {len(prompt)}")
        return "模拟的API响应"
