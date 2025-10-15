import streamlit as st
from jinja2 import Environment, meta, nodes, Template
from pathlib import Path
import json
import re


def extract_variables_in_order(template_content):
    """按变量在模板中出现的顺序提取所有唯一的Jinja2变量"""
    # 使用正则表达式匹配所有变量
    var_pattern = r'\{\{\s*(\w+)\s*\}\}'
    matches = re.finditer(var_pattern, template_content)
    
    # 收集变量并保持顺序，使用字典去重
    variables = []
    seen = set()
    
    for match in matches:
        var_name = match.group(1)
        if var_name not in seen:
            seen.add(var_name)
            variables.append((var_name, match.start()))
    
    return variables


def extract_conditional_blocks(template_content):
    """提取模板中的条件判断块信息"""
    # 解析条件语句的正则表达式
    if_pattern = r'\{%\s*if\s+(\w+)(?:\s*(==|!=|<=|>=|<|>)\s+(?:"([^"]*)"|\'([^\']*)\'|(\w+)))\s*%\}'
    elif_pattern = r'\{%\s*elif\s+(\w+)(?:\s*(==|!=|<=|>=|<|>)\s+(?:"([^"]*)"|\'([^\']*)\'|(\w+)))\s*%\}'
    bool_if_pattern = r'\{%\s*if\s+(\w+)\s*%\}'  # 简单的布尔条件判断
    
    # 收集所有条件信息
    conditions = []
    condition_groups = []
    bool_conditions = []
    current_group = []
    
    # 先处理简单的布尔条件判断
    for match in re.finditer(bool_if_pattern, template_content):
        var_name = match.group(1)
        
        # 检查条件块内的变量
        block_content = get_block_content(template_content, match.start(), is_if=True)
        block_vars = extract_variables_in_order(block_content)
        
        bool_condition = {
            'type': 'boolean',
            'var_name': var_name,
            'block_vars': [var[0] for var in block_vars],  # 只保留变量名
            'start_pos': match.start(),
            'end_pos': match.end()
        }
        
        bool_conditions.append(bool_condition)
    
    # 处理if语句
    for match in re.finditer(if_pattern, template_content):
        var_name = match.group(1)
        operator = match.group(2)
        # 获取比较值（处理引号和非引号情况）
        value = match.group(3) or match.group(4) or match.group(5)
        
        # 检查是否已经被识别为布尔条件
        is_boolean = False
        for bc in bool_conditions:
            if bc['var_name'] == var_name and bc['start_pos'] == match.start():
                is_boolean = True
                break
        
        if is_boolean:
            continue
        
        # 检查条件块内的变量
        block_content = get_block_content(template_content, match.start(), is_if=True)
        block_vars = extract_variables_in_order(block_content)
        
        condition = {
            'type': 'if',
            'var_name': var_name,
            'operator': operator,
            'value': value,
            'block_vars': [var[0] for var in block_vars],  # 只保留变量名
            'start_pos': match.start(),
            'end_pos': match.end()
        }
        
        # 检查是否有对应的elif和else
        remaining_content = template_content[match.end():]
        elif_matches = list(re.finditer(elif_pattern, remaining_content))
        
        # 如果当前有进行中的条件组，先保存
        if current_group:
            condition_groups.append(current_group)
            current_group = []
        
        current_group.append(condition)
        
        # 处理当前if语句后的elif
        for elif_match in elif_matches:
            elif_var = elif_match.group(1)
            # 只有当elif的变量与if的变量相同时，才认为是同一组
            if elif_var == var_name:
                elif_operator = elif_match.group(2)
                elif_value = elif_match.group(3) or elif_match.group(4) or elif_match.group(5)
                
                # 获取elif块内的变量
                elif_block_content = get_block_content(remaining_content, elif_match.start(), is_elif=True)
                elif_block_vars = extract_variables_in_order(elif_block_content)
                
                current_group.append({
                    'type': 'elif',
                    'var_name': elif_var,
                    'operator': elif_operator,
                    'value': elif_value,
                    'block_vars': [var[0] for var in elif_block_vars],  # 只保留变量名
                    'start_pos': match.end() + elif_match.start(),
                    'end_pos': match.end() + elif_match.end()
                })
            else:
                break
        
        # 检查是否有else
        else_match = re.search(r'\{%\s*else\s*%\}', remaining_content)
        if else_match:
            # 获取else块内的变量
            else_block_content = get_block_content(remaining_content, else_match.start(), is_else=True)
            else_block_vars = extract_variables_in_order(else_block_content)
            
            current_group.append({
                'type': 'else',
                'var_name': var_name,
                'operator': None,
                'value': None,
                'block_vars': [var[0] for var in else_block_vars],  # 只保留变量名
                'start_pos': match.end() + else_match.start(),
                'end_pos': match.end() + else_match.end()
            })
    
    # 保存最后一个条件组
    if current_group:
        condition_groups.append(current_group)
    
    # 扁平化条件组，返回所有条件
    for group in condition_groups:
        conditions.extend(group)
    
    return conditions, condition_groups, bool_conditions


def get_block_content(template_content, start_pos, is_if=False, is_elif=False, is_else=False):
    """获取条件块内的内容"""
    # 简单实现：根据不同类型的条件语句，找到对应的结束位置
    if is_if or is_elif:
        # 查找对应的endif或elif
        end_patterns = [
            '\\{%\\s*endif\\s*\\%}',
            '\\{%\\s*elif\\s*\\%}',
            '\\{%\\s*else\\s*\\%}'
        ]
    elif is_else:
        # else块到endif结束
        end_patterns = ['\\{%\\s*endif\\s*\\%}']
    else:
        # 默认行为
        end_patterns = [
            '\\{%\\s*endif\\s*\\%}',
            '\\{%\\s*elif\\s*\\%}',
            '\\{%\\s*else\\s*\\%}'
        ]
    
    content = template_content[start_pos:]
    min_pos = float('inf')
    
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match and match.start() < min_pos:
            min_pos = match.start()
    
    if min_pos != float('inf'):
        return content[:min_pos]
    return ''


def render_template(template_content, variables):
    """渲染模板，未提供的变量用*替代"""
    env = Environment()
    template = env.from_string(template_content)
    
    # 处理未提供的变量
    filled_vars = {k: v if v != "" else "*" for k, v in variables.items()}
    return template.render(**filled_vars)


def get_active_block_vars(condition_groups, condition_values):
    """
    根据用户选择的条件值，返回激活条件块中的变量名列表
    """
    active_vars = []

    for group in condition_groups:
        if not group:
            continue

        condition_var = group[0]['var_name']
        user_value = condition_values.get(condition_var)

        active_block = None

        for block in group:
            if block['type'] == 'if':
                if block['operator'] == '==' and user_value == block['value']:
                    active_block = block
                    break
            elif block['type'] == 'elif':
                if block['operator'] == '==' and user_value == block['value']:
                    active_block = block
                    break
            elif block['type'] == 'else':
                # 前面条件都不满足时，else 激活
                all_prev_false = True
                for prev in group:
                    if prev == block:
                        break
                    if prev['operator'] == '==' and user_value == prev['value']:
                        all_prev_false = False
                        break
                if all_prev_false:
                    active_block = block
                    break

        if active_block and active_block['block_vars']:
            active_vars.extend(active_block['block_vars'])

    return list(set(active_vars))  # 去重


def extract_variables_with_structure(template_content):
    """提取模板中的变量并按照结构组织成列表"""
    # 提取所有变量及其位置
    all_variables_with_pos = extract_variables_in_order(template_content)
    
    # 提取条件块和布尔条件
    conditional_blocks, condition_groups, bool_conditions = extract_conditional_blocks(template_content)
    
    # 收集所有条件变量
    condition_vars = set()
    for block in conditional_blocks:
        condition_vars.add(block['var_name'])
    
    # 收集所有布尔变量
    bool_vars = set()
    for bc in bool_conditions:
        bool_vars.add(bc['var_name'])
    
    # 确定第一个条件语句的位置
    first_condition_pos = float('inf')
    all_conditions = conditional_blocks + bool_conditions
    if all_conditions:
        first_condition_pos = min(bc['start_pos'] for bc in all_conditions)
    
    # 组织变量结构
    variable_structure = []
    
    # 1. 添加常规变量部分（条件语句之前的变量）
    pre_condition_vars = [v for v, p in all_variables_with_pos
                          if v not in condition_vars and v not in bool_vars and p < first_condition_pos]
    
    if pre_condition_vars:
        variable_structure.append({
            'type': '常规变量',
            'variables': pre_condition_vars
        })
    
    # 2. 处理条件变量部分（if-elif-else结构）
    for group in condition_groups:
        if not group:
            continue
        
        cond_var = group[0]['var_name']
        options = []
        
        for block in group:
            if block['type'] == 'if' or block['type'] == 'elif':
                # 直接使用该条件块内的变量，不进行额外过滤
                options.append({
                    'value': block['value'],
                    'variables': block['block_vars']
                })
            elif block['type'] == 'else':
                options.append({
                    'value': '其他',
                    'variables': block['block_vars']
                })
        
        variable_structure.append({
            'type': '条件变量',
            'condition_var': cond_var,
            'options': options
        })
    
    # 3. 处理布尔变量部分（简单的if条件判断）
    for bc in bool_conditions:
        variable_structure.append({
            'type': '布尔变量',
            'condition_var': bc['var_name'],
            'true_variables': bc['block_vars']
        })
    
    # 4. 处理条件语句之后的变量（如果有的话）
    last_condition_pos = 0
    if all_conditions:
        last_condition_pos = max(bc['end_pos'] for bc in all_conditions)
    
    post_condition_vars = [v for v, p in all_variables_with_pos
                           if v not in condition_vars and v not in bool_vars and p > last_condition_pos]
    
    if post_condition_vars:
        variable_structure.append({
            'type': '常规变量',
            'variables': post_condition_vars
        })
    
    print(variable_structure)
    return variable_structure


def main():
    st.title("Jinja2模板自动化生成工具")
    
    # 1. 上传模板文件
    st.subheader("步骤1: 上传Markdown模板")
    uploaded_file = st.file_uploader("选择Markdown模板文件", type=["md"])
    
    # 也可以选择示例模板
    st.subheader("或者选择示例模板")
    example_choice = st.radio(
        "选择示例模板",
        ("无", "测试模板"),
        horizontal=True
    )
    
    template_content = None
    
    if uploaded_file:
        template_content = uploaded_file.getvalue().decode("utf-8")
    elif example_choice == "测试模板":
        # 读取测试模板文件
        try:
            with open("e:\\trae\\gitte\\streamlitcode\\static\\公文\\测试.md", "r", encoding="utf-8") as f:
                template_content = f.read()
        except Exception as e:
            st.error(f"读取示例模板失败: {e}")
    
    if template_content:
        # 2. 提取变量和条件
        st.subheader("步骤2: 变量和条件分析结果")
        
        # 提取所有变量（按顺序，去重）
        all_variables_with_pos = extract_variables_in_order(template_content)
        all_variables = [var[0] for var in all_variables_with_pos]
        
        # 提取条件块、条件组和布尔条件
        conditional_blocks, condition_groups, bool_conditions = extract_conditional_blocks(template_content)
        
        # 使用新的结构提取变量
        variable_structure = extract_variables_with_structure(template_content)
        
        st.write(f"共发现 {len(all_variables)} 个唯一变量（按出现顺序）:")
        st.code(", ".join(all_variables))
        
        if conditional_blocks:
            st.write(f"发现 {len(condition_groups)} 个条件判断组，共 {len(conditional_blocks)} 个条件判断块")
        
        if bool_conditions:
            st.write(f"发现 {len(bool_conditions)} 个布尔条件判断")
        
        # 3. 收集变量值
        st.subheader("步骤3: 填写变量值")
        
        # ---------- 1. 表单开始 ----------
        with st.form("variable_form"):
            var_values = {}
            
            # 为每个条件变量初始化session_state
            for item in variable_structure:
                if item['type'] == '条件变量':
                    cond_var = item['condition_var']
                    if cond_var not in st.session_state:
                        st.session_state[cond_var] = None
                elif item['type'] == '布尔变量':
                    cond_var = item['condition_var']
                    if cond_var not in st.session_state:
                        st.session_state[cond_var] = False
            
            # 逐个处理变量结构中的元素
            for item in variable_structure:
                if item['type'] == '常规变量':
                    # 显示常规变量，使用两列布局
                    st.write("📌 常规变量")
                    # 显示提取的变量结构，用于调试
                    st.subheader("变量结构调试信息")
                    st.json(variable_structure)
                    cols = st.columns(2)
                    for i, v in enumerate(item['variables']):
                        with cols[i % 2]:
                            var_values[v] = st.text_input(f"{v}", placeholder="不填用*代替")
                
                elif item['type'] == '条件变量':
                    # 显示条件变量，使用折叠块
                    cond_var = item['condition_var']
                    selected = st.session_state.get(cond_var)
                    
                    title = f"📂 条件组：{cond_var}" + (f"（当前选中：{selected}）" if selected else "")
                    with st.expander(title, expanded=(selected is not None)):
                        # 获取所有可能的选项值
                        possible_values = [opt['value'] for opt in item['options']]
                        possible_values.append("自定义")
                        
                        # 确定当前选中值的索引
                        if selected in possible_values:
                            index = possible_values.index(selected)
                        else:
                            index = 0
                        
                        # 创建选择框
                        selected_value = st.selectbox(
                            f"请选择 {cond_var}",
                            possible_values,
                            index=index,
                            key=f"sel_{cond_var}"
                        )
                        
                        # 处理自定义值
                        if selected_value == "自定义":
                            custom_val = st.text_input(f"请输入 {cond_var} 的自定义值", key=f"custom_{cond_var}")
                            st.session_state[cond_var] = custom_val
                        else:
                            st.session_state[cond_var] = selected_value
                        
                        # 显示当前选项对应的变量
                        current_value = custom_val if selected_value == "自定义" else selected_value
                        for opt in item['options']:
                            if opt['value'] == current_value:
                                if opt['variables']:
                                    st.write("**需要填写的变量：**")
                                    cols = st.columns(2)
                                    for i, v in enumerate(opt['variables']):
                                        with cols[i % 2]:
                                            var_values[v] = st.text_input(f"{v}", placeholder="不填用*代替")
                                else:
                                    st.info("该选项下无额外变量")
                                break
                        # 处理未匹配到的情况
                        else:
                            st.info("请选择一个有效的选项")
                
                elif item['type'] == '布尔变量':
                    # 显示布尔变量，使用折叠块
                    cond_var = item['condition_var']
                    show = st.session_state.get(cond_var, False)
                    
                    # 创建复选框来控制是否显示详情
                    show_details = st.checkbox(f"是否显示 {cond_var}", value=show, key=f"bool_{cond_var}")
                    st.session_state[cond_var] = show_details
                    
                    # 如果选择显示，则展示对应的变量
                    if show_details:
                        if item['true_variables']:
                            st.write("**需要填写的变量：**")
                            cols = st.columns(2)
                            for i, v in enumerate(item['true_variables']):
                                with cols[i % 2]:
                                    var_values[v] = st.text_input(f"{v}", placeholder="不填用*代替")
                        else:
                            st.info("该条件下无额外变量")
            
            # 提交按钮
            submitted = st.form_submit_button("生成文档")
        
        # ---------- 2. 渲染 & 下载 ----------
        if submitted:
            # 把 session_state 里的条件值合并进来
            for item in variable_structure:
                if item['type'] == '条件变量' or item['type'] == '布尔变量':
                    cond_var = item['condition_var']
                    var_values[cond_var] = st.session_state.get(cond_var)
        
            rendered = render_template(template_content, var_values)
            st.subheader("生成结果")
            st.text_area("预览", rendered, height=300)
            st.download_button("下载Markdown", rendered, file_name="generated.md")

if __name__ == "__main__":
    main()