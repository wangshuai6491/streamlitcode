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
    
    # 收集所有条件信息
    conditions = []
    condition_groups = []
    current_group = []
    
    # 先处理if语句
    for match in re.finditer(if_pattern, template_content):
        var_name = match.group(1)
        operator = match.group(2)
        # 获取比较值（处理引号和非引号情况）
        value = match.group(3) or match.group(4) or match.group(5)
        
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
    
    return conditions, condition_groups


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
        
        # 提取条件块和条件组
        conditional_blocks, condition_groups = extract_conditional_blocks(template_content)
        
        # 收集所有条件变量
        condition_vars = set()
        for block in conditional_blocks:
            condition_vars.add(block['var_name'])
        
        # 分离普通变量和条件变量
        normal_vars = [var for var in all_variables if var not in condition_vars]
        
        st.write(f"共发现 {len(all_variables)} 个唯一变量（按出现顺序）:")
        st.code(", ".join(all_variables))
        
        if conditional_blocks:
            st.write(f"发现 {len(condition_groups)} 个条件判断组，共 {len(conditional_blocks)} 个条件判断块")
        
        # 3. 收集变量值 - 分阶段展示
        st.subheader("步骤3: 填写变量值")
        var_values = {}
        
        # 首先，找出模板中第一个条件块的位置
        first_condition_pos = float('inf')
        if conditional_blocks:
            first_condition_pos = min(block['start_pos'] for block in conditional_blocks)
        
        # 找出在第一个条件块之前出现的普通变量
        pre_condition_vars = []
        for var, pos in all_variables_with_pos:
            if var not in condition_vars and pos < first_condition_pos:
                pre_condition_vars.append(var)
        
        # 处理第一个条件块之前的变量
        with st.form("variable_form"):
            # 显示第一个条件块之前的变量
            if pre_condition_vars:
                st.write("请填写以下基本变量:")
                cols = st.columns(2)
                for i, var in enumerate(pre_condition_vars):
                    with cols[i % 2]:
                        var_values[var] = st.text_input(f"变量: {var}", value="", placeholder="不填将用*代替")
            
            # 然后处理条件选择
            if condition_groups:
                st.write("\n请选择以下条件:")
                
                # 处理条件组
                handled_condition_vars = set()
                
                for group in condition_groups:
                    # 获取条件组的变量名
                    if group:
                        var_name = group[0]['var_name']
                        if var_name not in handled_condition_vars:
                            handled_condition_vars.add(var_name)
                            
                            # 检查是否为布尔类型条件
                            is_boolean_condition = all(block['operator'] is None for block in group)
                            
                            if is_boolean_condition:
                                # 布尔类型条件，提供是/否选项
                                choice = st.selectbox(f"条件变量: {var_name}", ("是", "否"))
                                var_values[var_name] = choice == "是"  # 转换为布尔值
                            else:
                                # 获取此条件变量可能的所有值
                                possible_values = []
                                for block in group:
                                    if block['type'] != 'else' and block['value']:
                                        possible_values.append(block['value'])
                                
                                # 添加else作为一个选项
                                possible_values.append("其他")
                                
                                # 让用户选择值
                                choice = st.selectbox(f"条件变量: {var_name}", possible_values)
                                
                                if choice == "其他":
                                    var_values[var_name] = st.text_input(f"请输入 {var_name} 的值", key=f"{var_name}_custom")
                                else:
                                    var_values[var_name] = choice
            
            # 根据条件变量的值，决定显示哪些条件块内的变量
            st.write("\n请填写以下条件相关变量:")
            
            # 创建一个字典，映射条件变量到其值
            condition_values = {}
            for var in condition_vars:
                if var in var_values:
                    condition_values[var] = var_values[var]
                else:
                    # 默认设为False
                    condition_values[var] = False
            
            # 找出所有应该显示的变量
            visible_vars = set()
            
            # 首先添加所有普通变量（不包括已经显示的pre_condition_vars）
            for var in normal_vars:
                if var not in pre_condition_vars:
                    visible = True
                    
                    # 检查变量是否在某个条件块中
                    in_any_condition_block = False
                    
                    for block in conditional_blocks:
                        if var in block['block_vars']:
                            in_any_condition_block = True
                            # 检查条件是否满足
                            condition_value = condition_values.get(block['var_name'], False)
                            
                            # 根据条件类型判断
                            if block['type'] == 'if':
                                if block['operator'] == "==" and condition_value != block['value']:
                                    visible = False
                            elif block['type'] == 'elif':
                                if block['operator'] == "==" and condition_value != block['value']:
                                    visible = False
                            # else不需要判断条件
                            
                            # 一旦找到变量所在的条件块，就可以停止检查
                            break
                    
                    # 如果变量不在任何条件块中，或者所在的条件块条件满足，则显示
                    if not in_any_condition_block or visible:
                        visible_vars.add(var)
            
            # 按照模板中的顺序显示可见的变量
            sorted_visible_vars = []
            for var, pos in all_variables_with_pos:
                if var in visible_vars:
                    sorted_visible_vars.append(var)
            
            # 显示变量输入框
            if sorted_visible_vars:
                cols = st.columns(2)
                for i, var in enumerate(sorted_visible_vars):
                    with cols[i % 2]:
                        var_values[var] = st.text_input(f"变量: {var}", value="", placeholder="不填将用*代替")
            else:
                st.info("根据您的条件选择，没有需要填写的条件相关变量")
            
            submitted = st.form_submit_button("生成文档")
        
        # 4. 渲染并下载
        if submitted:
            st.subheader("生成结果")
            rendered = render_template(template_content, var_values)
            
            st.text_area("渲染结果预览", rendered, height=300)
            
            st.download_button(
                label="下载生成的Markdown文件",
                data=rendered,
                file_name="generated_document.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()