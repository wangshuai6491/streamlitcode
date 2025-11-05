# 注册自定义函数lineinput的固定代码，不要修改
import streamlit.components.v1 as components
import re
from typing import List, Dict, Any, Union
import streamlit as st
import os
import json,time
import hashlib

_RELEASE = True
if not _RELEASE:
    _component_func = components.declare_component(
        "lineinput",
        url="http://localhost:5173",
    )
else:
    # 直接使用当前目录的frontend/dist
    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/dist")
    _component_func = components.declare_component(
        "lineinput",
        path=build_dir
    )

def lineinput(name, default_values=None, key=None):
    """
    内联式文本输入框组件，将模板中的{{变量}}替换为输入框。
    
    参数:
        name: 包含{{变量名}}的模板字符串
        default_values: 可选，包含变量默认值的字典
    
    返回值:
        包含变量值字典和拼接后文本的字典
    """
    # 如果没有提供默认值，设置为空字典
    if default_values is None:
        default_values = {}
    if key is None:
         key = 'linetext_' + hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
    # 调用底层组件函数，传入name和default_values参数
    component_value = _component_func(name=name, default_values=default_values, key=key, default={"variables": {}, "content": "等待用户输入..."})
    
    # 返回组件的返回值
    return component_value

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
            'select_end': re.compile(r'{%\s*endselect\s*%}'),
            # 开关组：{% toggle 内容标签 %}内容{% endtoggle %}
            'toggle_start': re.compile(r'{%\s*toggle\s+([\w\u4e00-\u9fa5]+)\s*%}'),
            'toggle_end': re.compile(r'{%\s*endtoggle\s*%}')
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
                'select_start', 'select_end',
                'toggle_start', 'toggle_end'
            ]:
                regex = self.CONTROL_REGEX[tag_type]
                match = regex.match(template, pos)
                if match:
                    # 提取控制标签信息
                    tokens.append({
                        'type': tag_type,
                        'content': match.group(0),  # 标签原文（如{% if 有信访 %}）
                        'params': match.groups() if tag_type in [
                            'if_bool_start', 'if_tj_start', 'elif_tj', 'radio_start', 'select_start', 'toggle_start'
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

            elif token['type'] == 'toggle_start':
                # 开关组开始
                toggle_name = token['params'][0].strip() if token['params'] else ''
                toggle_node: Dict[str, Any] = {
                    'type': 'toggle',
                    'name': toggle_name,
                    'content': []  # 收集开关内的内容
                }
                current_nodes.append(toggle_node)
                stack.append({
                    'parent_nodes': current_nodes,
                    'current_node': toggle_node,
                    'tag_type': 'toggle'
                })
                current_nodes = toggle_node['content']  # 临时收集开关内的内容

            elif token['type'] == 'toggle_end':
                # 开关组结束
                if not stack or stack[-1]['tag_type'] != 'toggle':
                    raise SyntaxError(f"Unexpected {{% endtoggle %}} (no matching {{% toggle %}})")
                
                # 弹出栈顶元素，切换回父节点容器
                group_info = stack.pop()
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

# 自定义按钮组样式
def button_group(label: str = "",options: List[Dict[str, Union[str, bool]]] = None,default_value: Union[str, bool] = None,key: str = None) -> Union[str, bool]:
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
    
    # 初始化 session state
    if key is None:
        key = f"button_group_{label}"
    # 如果session_state中没有该key，初始化默认值
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    # 显示标签
    if label:
        st.write(label)
    
    # 创建按钮组布局
    cols = st.columns(len(options))
    
    # ---- 回调：立即改状态，无需 rerun 两次 ----
    def _switch(sel):
        st.session_state[key] = sel

    current_value = st.session_state[key]
    
    for i, option in enumerate(options):
        with cols[i]:
            is_selected = current_value == option["value"]
            
            # 按钮样式
            button_style = """
            <style>
            .btn-group-button {
                width: 100%;
                padding: 0.5rem 1rem;
                border: 1px solid #d1d5db;
                background-color: white;
                color: #374151;
                font-size: 0.875rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .btn-group-button:hover {
                background-color: #f3f4f6;
            }
            .btn-group-button.selected {
                background-color: #3b82f6;
                color: white;
                border-color: #3b82f6;
            }
            .btn-group-button:first-child {
                border-top-left-radius: 0.5rem;
                border-bottom-left-radius: 0.5rem;
            }
            .btn-group-button:last-child {
                border-top-right-radius: 0.5rem;
                border-bottom-right-radius: 0.5rem;
            }
            .btn-group-button:not(:first-child):not(:last-child) {
                border-radius: 0;
            }
            </style>
            """
            
            # 按钮类名
            button_class = "btn-group-button"
            if is_selected:
                button_class += " selected"
            
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
                st.session_state[var_name] = var_value
            # st.success("已更新会话状态中的变量值缓存")
            return True
    return False

# 处理text元素内容
def process_text_content(content):
    """
    处理文本内容，包括解析变量、替换默认值和渲染
    
    Args:
        content: 文本内容
    
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
            
            # 只有在default_values中没有对应变量或值为空时才存储默认值
            if var_name not in st.session_state or st.session_state[var_name] == '':
                st.session_state[var_name] = default_value
        # 调用lineinput组件渲染内容，使用session_state中的计数器确保唯一性
        component_result = lineinput(
            content, 
            default_values=st.session_state.copy()
        )
        # 更新会话状态中的变量缓存
        update_variable_cache(component_result)
        return component_result  
    else:
        st.markdown(content)
        return content

def radio(name, options):
    # 1. 确保 session_state 有默认值
    if name not in st.session_state:
        # 取第一个元素的 value 作为默认
        st.session_state[name] = options[0]["value"] if options else None

    default = st.session_state[name]

    # 2. 原生分支
    if st.session_state.get("use_native", True):
        # 把 options 转成字符串列表
        labels = [o["label"] for o in options]
        val_label = st.radio(name, labels, key=f"{name}", horizontal=True)
        # 同步结果到session_state
        st.session_state[name] = val_label
        return val_label

    # 3. 自定义按钮组分支 —— 直接传原格式
    return button_group(
        label=name,
        options=options,
        default_value=default,
        key=name
    )

# 处理下拉列表
def select(name,options):
    value = st.selectbox(name, options, key=name)
    # 同步结果到session_state
    st.session_state[name] = value
    return value


# 处理开关组件toggle
def toggle(name, value=True):
    value = st.toggle(name, value=value)
    # 同步结果到session_state
    st.session_state[name] = value
    return value
    
# 处理判断类元素，如if、radio、select等
def render_element(element):
    """
    渲染单个元素
    Args:
        element: 要渲染的元素字典
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
        name   = element.get("name", "")
        # 将字符串列表转成 dict 列表，确保 radio 函数拿到正确格式
        raw_options = element.get("options", [])
        options = [{"label": opt, "value": opt} for opt in raw_options]
        return radio(name, options)
    
    elif element_type == 'select':
        name = element.get('name', '')
        options = element.get('options', [])
        return select(name,options)
    
    # 处理开关组件toggle
    elif element_type == 'toggle':
        name = element.get('name', '')
        return toggle(name, value=True)
    
    # 处理if_bool类型
    elif element_type == 'if_bool':
        # 获取布尔判断条件
        condition = element.get('condition', '')
        value = st.session_state[condition]
        # 根据条件渲染相应内容
        if value:
            body = element.get('if_body', [])
        else:
            body = element.get('else_body', [])
        
        # 渲染body中的内容
        for item in body:
            render_element(item)
        return
    
    # 处理if_tj类型
    elif element_type == 'if_tj':
        condition_var = element.get('condition_var', '')
        condition_value = element.get('condition_value', '')
        
        # 收集所有可能的条件值作为按钮选项
        button_options = [{'label': condition_value, 'value': condition_value}]
        elif_conditions = element.get('elif_conditions', [])
        for elif_cond in elif_conditions:
            elif_value = elif_cond.get('condition_value', '')
            if elif_value and elif_value not in [opt['value'] for opt in button_options]:
                button_options.append({'label': elif_value, 'value': elif_value})
        
        # 如果有else_body，添加一个"其他"选项
        if element.get('else_body'):
            # 使用一个特殊标记来表示"其他"选项
            other_value = '都不满足'
            # 确保"其他"选项不会与已有选项冲突
            if other_value not in [opt['value'] for opt in button_options]:
                button_options.append({'label': '其他', 'value': other_value})
        
        # 如果 session_state 中已有该布尔变量，则不再重复渲染，直接复用已有值
        if condition_var in st.session_state:
            value = st.session_state[condition_var]
        else:
            # 渲染按钮组 - button_group内部会自动更新default_values
            value = radio(condition_var, button_options)
        
        # 渲染相应内容
        # 特殊处理"都不满足"值 - 直接显示else内容
        if value == "都不满足":
            body = element.get('else_body', [])
        else:
            matched = False
            # 检查主条件：比较变量值是否等于条件值
            if value == condition_value:
                body = element.get('if_body', [])
                matched = True
            else:
                # 检查elif条件
                for elif_cond in elif_conditions:
                    if value == elif_cond.get('condition_value', ''):
                        body = elif_cond.get('body', [])
                        matched = True
                        break
                # 如果都不匹配，使用else_body
                if not matched:
                    body = element.get('else_body', [])
        
        # 渲染body中的内容
        for item in body:
            render_element(item)
        return
    
    return None

# 渲染内容列表主函数
def render_content(content_list):
    """
    渲染整个内容列表
    
    Args:
        content_list: 内容元素列表
    """
    # 开始逐个元素渲染
    for element in content_list:
        render_element(element)

# 解析模板为AST模板json的主函数，并作为不变因素
@st.cache_data(show_spinner=False)
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

# 设置侧边栏功能
def setup_sidebar():
    """
    设置侧边栏功能，包括状态管理和模板展示
    
    Args:
        template: 模板字符串
    """
    # 侧边栏顶部放个 toggle
    use_native = st.sidebar.toggle("♻️ 使用原生组件（极速）", value=True)
    st.session_state["use_native"] = use_native
    # 状态管理功能
    col1, col2 = st.sidebar.columns(2)
    # 保存当前状态
    if col1.button("保存输入"):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"session_state_{timestamp}.json"
        
        # 将 default_values 转为 JSON 字符串
        json_str = json.dumps(st.session_state, ensure_ascii=False, indent=2)
        
        # 提供下载
        st.sidebar.download_button(
            label="点击下载状态文件",
            data=json_str,
            file_name=filename,
            mime="application/json"
        )
    
    # 导入状态
    uploaded_file = st.sidebar.file_uploader("导入已填数据文件", type=["json"])
    if uploaded_file is not None:
        try:
            # 读取上传的文件内容
            file_content = uploaded_file.read().decode('utf-8')
            imported_state = json.loads(file_content)
            
            # 更新default_values字典
            st.session_state = imported_state
            st.sidebar.success("状态导入成功")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"导入失败: {str(e)}")
    
    # 一键清空
    if col2.button("清空输入"):
        st.session_state = {}
        st.rerun()

def parse_and_render(template):
    """
    解析模板并渲染内容
    
    Args:
        template: 模板字符串或列表
    """
    # 展示模板和变量
    with st.sidebar.expander("当前处理模板", expanded=False):
        st.write(template)    
    # 开始解析模板
    if isinstance(template, list):
        template = ''.join(template)
    neirong = ast(template)
    if neirong:
        # 在侧边栏展示解析后的AST模板json
        with st.sidebar.expander("解析后的AST模板", expanded=False):
            st.json(neirong)
        # 解析成功，继续渲染
        placeholder = st.empty()
        with placeholder.container():
            render_content(neirong)
    else:
        # 解析失败，提示用户检查模板
        st.error("模板解析失败，请检查模板语法。")

def main(template):
    """
    主函数，整合侧边栏设置和模板解析渲染
    
    Args:
        template: 模板字符串
    """
    # 设置侧边栏
    setup_sidebar()
    # 解析并渲染模板
    parse_and_render(template)

if __name__ == "__main__":
    # 教学用折叠块
    with st.expander("📚 自定义模板语法使用指南", expanded=False):
        st.markdown("""
            请模仿下面正确语法示例，编写自己的模板
            #### 1. 变量引用
            ```
            {{ 变量名 }}
            {{ 变量名|default=默认值 }}
            ```

            #### 2. 条件判断
            ```
            {% if 布尔变量 %}
            条件成立时显示
            {% else %}
            条件不成立时显示
            {% endif %}
            ```

            #### 3. 表达式条件判断
            ```
            {% if 变量名 = "值" %}
            条件成立内容
            {% elif 变量名 = "其他值" %}
            其他条件内容
            {% else %}
            默认内容
            {% endif %}
            ```

            #### 4. 单选按钮组
            ```
            {% radio 组名 %}
            选项1|选项2|选项3
            {% endradio %}
            ```

            #### 5. 下拉选择框
            ```
            {% select 列表名 %}
            选项1|选项2|选项3
            {% endselect %}
            ```

            #### 示例模板
            ```
            {% radio 信访渠道 %}
            来信|来访|网上信访|电话信访
            {% endradio %}

            {% select 信访类型 %}
            征地补偿|安置方案|土地权属|违法占地
            {% endselect %}

            {% if 有信访 %}
            存在信访事项
            {% else %}
            未收到信访事项
            {% endif %}

            {% if 信访渠道 = "来信" %}
            情况1：来信处理
            {% elif 信访渠道 = "来访" %}
            情况2：来访处理
            {% else %}
            其他渠道处理方式
            {% endif %}
            ```
        """)
    
    # 页面标题
    st.title('数据渲染组件')
    # 自定义语法内容
    template = st.text_area("请输入自定义模板语法：", height=300)

    # 只有template不为空时才解析
    if template.strip():
        main(template)
    
