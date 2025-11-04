import re
from typing import List, Dict, Any, Union
import streamlit as st
import os
import sys
import json
# 添加父目录到Python路径，确保可以导入__init__.py中的函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 直接导入__init__.py中的lineinput函数
from __init__ import lineinput

class TemplateParser:
    """模板解析器：仅解析控制标签（{% ... %}），变量语句（{{ ... }}）直接原文输出"""
    
    def __init__(self):
        # 仅匹配控制标签（单选、下拉、条件判断），不解析变量
        self.CONTROL_REGEX = {
            # 条件开始：{% if 条件名 %} (布尔类型)
            'if_bool_start': re.compile(r'{%\s*if\s+([\w\u4e00-\u9fa5]+)\s*%}'),
            # 条件开始：{% if 条件名 = 值 %} (条件表达式类型)
            'if_tj_start': re.compile(r'{%\s*if\s+([\w\u4e00-\u9fa5]+)\s*=\s*"([^"]+)"\s*%}'),
            # 条件分支：{% else %}
            'else': re.compile(r'{%\s*else\s*%}'),
            # 条件分支：{% elif 条件名 = 值 %}
            'elif_tj': re.compile(r'{%\s*elif\s+([\w\u4e00-\u9fa5]+)\s*=\s*"([^"]+)"\s*%}'),
            # 条件结束：{% endif %}
            'if_end': re.compile(r'{%\s*endif\s*%}'),
            # 单选组：{% radio 组名 %}选项1|选项2{% endradio %}
            'radio_start': re.compile(r'{%\s*radio\s+([\w\u4e00-\u9fa5]+)\s*%}'),
            'radio_end': re.compile(r'{%\s*endradio\s*%}'),
            # 下拉列表：{% select 列表名 %}选项1|选项2{% endselect %}
            'select_start': re.compile(r'{%\s*select\s+([\w\u4e00-\u9fa5]+)\s*%}'),
            'select_end': re.compile(r'{%\s*endselect\s*%}')
        }

    def parse(self, template: str) -> List[Dict[str, Any]]:
        """解析模板为AST（仅包含控制标签结构，变量语句保留原文）"""
        tokens = self._tokenize(template)
        return self._build_ast(tokens)

    def _tokenize(self, template: str) -> List[Dict[str, Any]]:
        """将模板转换为令牌流：控制标签拆分为令牌，其他内容（含变量）作为纯文本"""
        tokens: List[Dict[str, Any]] = []
        pos = 0  # 当前解析位置
        len_template = len(template)

        while pos < len_template:
            matched = False

            # 匹配控制标签（{% ... %}）
            for tag_type in [
                'if_bool_start', 'if_tj_start', 'elif_tj', 'else', 'if_end', 
                'radio_start', 'radio_end', 
                'select_start', 'select_end'
            ]:
                regex = self.CONTROL_REGEX[tag_type]
                match = regex.match(template, pos)
                if match:
                    # 提取控制标签信息
                    tokens.append({
                        'type': tag_type,
                        'content': match.group(0),  # 标签原文（如{% if 有信访 %}）
                        'params': match.groups() if tag_type in [
                            'if_bool_start', 'if_tj_start', 'elif_tj', 'radio_start', 'select_start'
                        ] else None
                    })
                    pos = match.end()
                    matched = True
                    break
            if matched:
                continue

            # 非控制标签内容（含变量语句{{ ... }}）全部作为纯文本
            next_control_pos = self._find_next_control_pos(template, pos)
            if pos < next_control_pos:
                text_content = template[pos:next_control_pos]
                tokens.append({
                    'type': 'text',
                    'content': text_content  # 保留原文，包括变量{{ ... }}
                })
                pos = next_control_pos
            else:
                pos += 1  # 避免死循环

        return tokens

    def _find_next_control_pos(self, template: str, start_pos: int) -> int:
        """查找下一个控制标签（{%）的位置，用于分割纯文本"""
        min_pos = len(template)
        control_start = '{%'  # 控制标签的起始标识
        pos = template.find(control_start, start_pos)
        if pos != -1 and pos < min_pos:
            min_pos = pos
        return min_pos

    def _build_ast(self, tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从令牌流构建AST，仅处理控制标签的嵌套结构"""
        ast: List[Dict[str, Any]] = []
        stack: List[Dict[str, Any]] = []  # 处理嵌套逻辑
        current_nodes = ast  # 当前节点容器

        for token in tokens:
            if token['type'] == 'text':
                # 纯文本（含变量语句）直接作为文本节点保留
                current_nodes.append({
                    'type': 'text',
                    'content': token['content']  # 原文输出，不解析{{ ... }}
                })

            elif token['type'] == 'if_bool_start':
                # 布尔类型条件判断开始 {% if 有信访 %}
                condition = token['params'][0].strip() if token['params'] else ''
                if_node: Dict[str, Any] = {
                    'type': 'if_bool',
                    'condition': condition,
                    'if_body': [],
                    'else_body': []
                }
                current_nodes.append(if_node)
                stack.append({
                    'parent_nodes': current_nodes,
                    'if_node': if_node,
                    'in_else': False
                })
                current_nodes = if_node['if_body']
            elif token['type'] == 'if_tj_start':
                # 条件表达式类型条件判断开始 {% if 信访 = "存在" %}
                condition_var = token['params'][0].strip() if token['params'] else ''
                condition_value = token['params'][1].strip() if token['params'] and len(token['params']) > 1 else ''
                if_node: Dict[str, Any] = {
                    'type': 'if_tj',
                    'condition_var': condition_var,
                    'condition_value': condition_value,
                    'if_body': [],
                    'elif_conditions': [],
                    'else_body': []
                }
                current_nodes.append(if_node)
                stack.append({
                    'parent_nodes': current_nodes,
                    'if_node': if_node,
                    'in_else': False
                })
                current_nodes = if_node['if_body']
            elif token['type'] == 'elif_tj':
                # 条件表达式类型条件分支 {% elif 信访 = "不存在" %}
                if not stack or stack[-1]['if_node']['type'] != 'if_tj':
                    raise SyntaxError("Unexpected {% elif %} (no matching {% if %} with condition)")
                # 创建新的elif条件
                elif_var = token['params'][0].strip() if token['params'] else ''
                elif_value = token['params'][1].strip() if token['params'] and len(token['params']) > 1 else ''
                elif_condition = {
                    'condition_var': elif_var,
                    'condition_value': elif_value,
                    'body': []
                }
                stack[-1]['if_node']['elif_conditions'].append(elif_condition)
                # 切换到elif body
                stack[-1]['in_else'] = True  # 标记为非主body
                current_nodes = elif_condition['body']

            elif token['type'] == 'else':
                # 条件分支切换
                if not stack:
                    raise SyntaxError("Unexpected {% else %} (no matching {% if %})")
                stack[-1]['in_else'] = True
                # 根据if类型选择正确的else_body
                current_nodes = stack[-1]['if_node']['else_body']

            elif token['type'] == 'if_end':
                # 条件判断结束
                if not stack:
                    raise SyntaxError("Unexpected {% endif %} (no matching {% if %})")
                stack.pop()
                current_nodes = stack[-1]['parent_nodes'] if stack else ast

            elif token['type'] == 'radio_start':
                # 单选组开始
                radio_name = token['params'][0].strip() if token['params'] else ''
                radio_node: Dict[str, Any] = {
                    'type': 'radio',
                    'name': radio_name,
                    'options': []  # 后续解析选项
                }
                current_nodes.append(radio_node)
                stack.append({
                    'parent_nodes': current_nodes,
                    'current_node': radio_node,
                    'tag_type': 'radio'
                })
                current_nodes = radio_node['options']  # 临时收集选项文本

            elif token['type'] == 'radio_end':
                # 单选组结束（解析选项）
                self._end_group_tag(stack, 'radio')
                current_nodes = stack[-1]['parent_nodes'] if stack else ast

            elif token['type'] == 'select_start':
                # 下拉列表开始
                select_name = token['params'][0].strip() if token['params'] else ''
                select_node: Dict[str, Any] = {
                    'type': 'select',
                    'name': select_name,
                    'options': []  # 后续解析选项
                }
                current_nodes.append(select_node)
                stack.append({
                    'parent_nodes': current_nodes,
                    'current_node': select_node,
                    'tag_type': 'select'
                })
                current_nodes = select_node['options']  # 临时收集选项文本

            elif token['type'] == 'select_end':
                # 下拉列表结束（解析选项）
                self._end_group_tag(stack, 'select')
                current_nodes = stack[-1]['parent_nodes'] if stack else ast

        if stack:
            # 检查未闭合的控制标签
            unclosed = [s['tag_type'] for s in stack if 'tag_type' in s]
            raise SyntaxError(f"Unclosed tags: {', '.join(unclosed)}")

        return ast

    def _end_group_tag(self, stack: List[Dict[str, Any]], tag_type: str) -> None:
        """处理单选/下拉组的结束标签，解析选项（从文本中提取|分隔的选项）"""
        if not stack or stack[-1]['tag_type'] != tag_type:
            raise SyntaxError(f"Unexpected {{% end{tag_type} %}} (no matching {{% {tag_type} %}})")
        
        group_info = stack.pop()
        group_node = group_info['current_node']
        # 从临时收集的文本中提取选项（忽略空文本）
        options_text = ''.join([
            n['content'].strip() for n in group_node['options'] 
            if n.get('type') == 'text' and n['content'].strip()
        ])
        # 按|分割选项并去重
        group_node['options'] = [
            opt.strip() for opt in options_text.split('|') 
            if opt.strip()
        ]
        if not group_node['options']:
            raise ValueError(f"Empty options in {{% {tag_type} {group_node['name']} %}}")

# 自定义按钮样式，用来替带系统的st.radio
def button_group(
    label: str = "",
    options: List[Dict[str, Union[str, bool]]] = None,
    default_value: Union[str, bool] = None,
    key: str = None
) -> Union[str, bool]:
    """
    创建一个选择按钮组
    
    Args:
        label: 组件标签
        options: 选项列表，每个选项包含 label 和 value
        default_value: 默认选中的值
        key: 组件的唯一键
    
    Returns:
        当前选中的值
    """
    if options is None:
        options = [
            {"label": "是", "value": "是"},
            {"label": "否", "value": "否"}
        ]
    
    if default_value is None:
        default_value = options[0]["value"]
    
    # 生成唯一键
    if key is None:
        key = f"button_group_{label}"
    
    # 初始化 session state
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    # 显示标签
    if label:
        st.write(label)
    
    current_value = st.session_state[key]

    cols = st.columns(len(options))
    
    for i, option in enumerate(options):
        with cols[i]:
            is_selected = current_value == option["value"]
            
            # 创建按钮
            if st.button(
                option["label"],
                key=f"{key}_{i}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state[key] = option["value"]
                st.rerun()
    
    return st.session_state[key]

# 更新会话状态中的变量缓存
def update_variable_cache(component_result):
    # 当组件返回结果且包含更新的变量值时，更新会话状态中的缓存
    if component_result and isinstance(component_result, dict):
        # 检查是否有 'variables' 字段，这应该包含用户在组件中修改的变量值
        if 'variables' in component_result and isinstance(component_result['variables'], dict):
            # 更新会话状态中的默认值缓存
            for var_name, var_value in component_result['variables'].items():
                st.session_state.default_values[var_name] = var_value
            # st.success("已更新会话状态中的变量值缓存")
            return True
    return False

# 处理text元素内容
def process_text_content(content):
    """
    处理文本内容，包括解析变量、替换默认值和渲染
    
    Args:
        content: 文本内容
        element_name: 元素名称
        variables: 变量字典
    
    Returns:
        渲染后的结果
    """
    # 如果内容只有换行符或空白字符，直接跳过
    if content.strip() == '':
        return
    
    # 检查是否包含变量,有变量进行名称、默认值提取，并保存到session_state
    if '{{' in content:
        # 有变量解析content中的变量名和默认值
        # 匹配 {{ 变量名 }} 和 {{ 变量名|default:默认值 }} 或 {{ 变量名|default=默认值 }}
        pattern = r'\{\{\s*([^\}|\}]+)(?:\|default:([^\}]+)|\|default=([^\}]+))?\s*\}\}'
        matches = re.findall(pattern, content)

        # 替换default部分为空字符串
        content = re.sub(pattern, r'{{ \1 }}', content)
    
        # 将变量名和默认值统一存储到default_values字典
        for match in matches:
            var_name = match[0].strip()
            # 检查是否有默认值（支持:和=两种格式）
            default_value = match[1].strip() if match[1] else (match[2].strip() if match[2] else '')
            
            # 只存储到default_values字典中
            st.session_state.default_values[var_name] = default_value
        # 调用lineinput组件渲染内容
        component_result = lineinput(
            content, 
            default_values=st.session_state.default_values.copy(),
            key=f"lineinput_{getattr(render_content, '_counter', 0) if hasattr(render_content, '_counter') else 0}"
        )
        # 更新会话状态中的变量缓存
        update_variable_cache(component_result)
        return component_result  
    else:
        st.write(content)
        return content

# 处理判断类元素，如if、radio、select等
def render_element(element, variables=None):
    """
    渲染单个元素
    
    Args:
        element: 要渲染的元素字典
        variables: 变量字典，用于存储和获取用户输入的值
    
    Returns:
        渲染后的结果（如果有）
    """
    # 获取元素类型
    element_type = element.get('type')
    
    if element_type == 'text':
        # 获取文本内容和名称
        content = element.get('content', '')
        # 调用封装的文本处理函数
        return process_text_content(content)

    elif element_type == 'radio':
        # 生成按钮组
        name = element.get('name', '')
        options = element.get('options', [])
        # 转换选项格式为button_group需要的格式
        button_options = [{"label": opt, "value": opt} for opt in options]
        # 使用name作为key的一部分
        key = f"radio_{name}"
        # 渲染按钮组
        value = button_group(f"{name}: ", button_options, default_value=options[0] if options else None, key=key)
        # 保存到变量字典和default_values
        variables[name] = value
        st.session_state.default_values[name] = value
        return value
    
    elif element_type == 'select':
        # 生成下拉列表
        name = element.get('name', '')
        options = element.get('options', [])
        # 使用name作为key
        key = f"select_{name}"
        # 初始化session state
        if key not in st.session_state and options:
            st.session_state[key] = options[0]
        # 渲染下拉列表
        value = st.selectbox(name, options, key=key)
        # 保存到变量字典和default_values
        variables[name] = value
        st.session_state.default_values[name] = value
        return value
    
    # 处理if_bool类型
    elif element_type == 'if_bool':
        condition = element.get('condition', '')
        # 检查条件是否存在于变量中，或者创建一个checkbox
        if condition not in variables:
            variables[condition] = st.checkbox(f"{condition}（勾选表示条件成立）")
        
        # 保存条件结果到default_values和session_state
        st.session_state.default_values[condition] = variables[condition]
        
        # 根据条件渲染相应内容
        if variables[condition]:
            body = element.get('if_body', [])
        else:
            body = element.get('else_body', [])
        
        # 渲染body中的内容
        for item in body:
            render_element(item, variables)
        return
    
    # 处理if_tj类型
    elif element_type == 'if_tj':
        condition_var = element.get('condition_var', '')
        condition_value = element.get('condition_value', '')
        
        # 优先从default_values中获取变量值
        if condition_var in st.session_state.default_values:
            variables[condition_var] = st.session_state.default_values[condition_var]
        # 如果default_values中没有，则检查variables字典
        elif condition_var not in variables:
            # 创建输入框并设置默认值
            variables[condition_var] = st.text_input(f"请输入{condition_var}的值：", value=condition_value)
        
        # 保存变量值到default_values和session_state
        st.session_state.default_values[condition_var] = variables[condition_var]
        
        # 渲染相应内容
        matched = False
        # 检查主条件：比较变量值是否等于条件值
        if variables.get(condition_var) == condition_value:
            body = element.get('if_body', [])
            matched = True
        else:
            # 检查elif条件
            elif_conditions = element.get('elif_conditions', [])
            for elif_cond in elif_conditions:
                if variables.get(condition_var) == elif_cond.get('condition_value', ''):
                    body = elif_cond.get('body', [])
                    matched = True
                    break
            # 如果都不匹配，使用else_body
            if not matched:
                body = element.get('else_body', [])
        
        # 渲染body中的内容
        for item in body:
            render_element(item, variables)
        return
    
    return None

# 渲染内容列表主函数
def render_content(content_list):
    """
    渲染整个内容列表
    
    Args:
        content_list: 内容元素列表
    """
    variables = {}
    for element in content_list:
        render_element(element, variables)
    
    # 同步所有变量到default_values字典
    st.session_state.default_values.update(variables)
    
    # 将所有解析结果保存到session_state（用于展示）
    if 'parsed_results' not in st.session_state:
        st.session_state['parsed_results'] = {}
    # 更新session_state中的解析结果
    st.session_state['parsed_results'].update(variables)

# 解析模板为AST模板json的主函数
def ast(template):
    """
    解析模板为AST模板json,方便程序解析
    """
    parser = TemplateParser()
    try:
        ast = parser.parse(template)
        return ast
    except Exception as e:
        print(f"解析错误：{e}")
        return None

def main(template):
    """
    主函数，包含页面标题、初始化会话状态、测试按钮组和解析模板逻辑
    """
    # 页面标题
    st.title('数据渲染组件')
    # 初始化session_state中的default_values字典
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {}
    
    # 测试按钮组
    st.subheader("1. 自定义选项")
    # 开始解析模板
    neirong = ast(template)
    if neirong:
        # 在侧边栏展示解析后的AST模板json
        with st.sidebar:
            st.json(neirong)
        # 解析成功，继续渲染
        render_content(neirong)
    else:
        # 解析失败，提示用户检查模板
        st.error("模板解析失败，请检查模板语法。")
    

    # 把session_state中的解析结果直接以JSON格式展示
    st.subheader("2. 解析结果")
    st.write(st.session_state.default_values)

if __name__ == "__main__":
    # 自定义语法内容
    template = st.text_area("请输入自定义模板语法：", height=300)
    # 只有template不为空时才解析
    if template.strip():
        main(template)
    