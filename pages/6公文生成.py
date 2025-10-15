import streamlit as st
import re
import os
from jinja2 import Template, TemplateSyntaxError

def extract_jinja_variables(template):
    results = []
    current_condition = None
    condition_type = None
    current_branch = None
    
    lines = template.split('\n')
    
    for line in lines:
        # 跳过空行
        if not line.strip():
            continue
            
        # 检查是否是条件开始
        if_match = re.match(r'\{%\s*if\s+(.*?)\s*%\}', line)
        if if_match:
            expr = if_match.group(1).strip()
            
            # 确定条件类型
            if '==' in expr:
                # 条件变量
                parts = expr.split('==', 1)
                var = parts[0].strip()
                value = parts[1].strip().strip('"\'')
                
                current_condition = {
                    'type': '条件变量',
                    'condition_var': var,
                    'options': [{
                        'value': value,
                        'variables': []
                    }]
                }
                condition_type = '条件变量'
                current_branch = 0
            else:
                # 布尔变量
                current_condition = {
                    'type': '布尔变量',
                    'condition_var': expr,
                    'true_variables': [],
                    'false_variables': []
                }
                condition_type = '布尔变量'
                current_branch = 'true'
            
            continue
        
        # 检查是否是elif分支
        elif_match = re.match(r'\{%\s*elif\s+(.*?)\s*%\}', line)
        if elif_match and current_condition and condition_type == '条件变量':
            expr = elif_match.group(1).strip()
            parts = expr.split('==', 1)
            var = parts[0].strip()
            value = parts[1].strip().strip('"\'')
            
            # 添加新选项
            current_condition['options'].append({
                'value': value,
                'variables': []
            })
            current_branch = len(current_condition['options']) - 1
            continue
        
        # 检查是否是else分支
        elif re.match(r'\{%\s*else\s*%\}', line) and current_condition:
            if condition_type == '条件变量':
                # 添加else选项
                current_condition['options'].append({
                    'value': '其他',
                    'variables': []
                })
                current_branch = len(current_condition['options']) - 1
            elif condition_type == '布尔变量':
                current_branch = 'false'
            continue
        
        # 检查是否是条件结束
        if re.match(r'\{%\s*endif\s*%\}', line) and current_condition:
            # 将当前条件块添加到结果
            results.append(current_condition)
            current_condition = None
            condition_type = None
            current_branch = None
            continue
        
        # 提取变量
        var_matches = re.findall(r'\{\{\s*([^\}\s]+)\s*\}\}', line)
        if var_matches:
            cleaned_vars = [v.strip() for v in var_matches]
            
            if current_condition:
                # 在当前条件块中添加变量，并去重
                if condition_type == '条件变量':
                    if current_branch is not None and current_branch < len(current_condition['options']):
                        # 添加新变量但避免重复
                        for var in cleaned_vars:
                            if var not in current_condition['options'][current_branch]['variables']:
                                current_condition['options'][current_branch]['variables'].append(var)
                elif condition_type == '布尔变量':
                    if current_branch == 'true':
                        # 添加新变量但避免重复
                        for var in cleaned_vars:
                            if var not in current_condition['true_variables']:
                                current_condition['true_variables'].append(var)
                    else:
                        # 添加新变量但避免重复
                        for var in cleaned_vars:
                            if var not in current_condition['false_variables']:
                                current_condition['false_variables'].append(var)
            else:
                # 不在任何条件块中，添加到常规变量，并去重
                # 检查是否可以将变量添加到现有的常规变量组
                if results and results[-1]['type'] == '常规变量':
                    # 添加新变量但避免重复
                    for var in cleaned_vars:
                        if var not in results[-1]['variables']:
                            results[-1]['variables'].append(var)
                else:
                    results.append({
                        'type': '常规变量',
                        'variables': cleaned_vars.copy()  # 创建副本以避免引用问题
                    })
    
    # 处理可能未关闭的条件块
    if current_condition:
        results.append(current_condition)
    
    return results

def render_template(template, params):
    """使用Jinja2库进行通用模板渲染
    
    Args:
        template (str): Jinja2格式的模板字符串
        params (dict): 包含变量值的字典
        
    Returns:
        str: 渲染后的结果字符串
    """
    try:
        # 创建Jinja2模板对象
        jinja_template = Template(template)
        
        # 使用提供的参数渲染模板
        rendered_content = jinja_template.render(**params)
        
        return rendered_content
    except TemplateSyntaxError as e:
        st.error(f"模板语法错误: {e}")
        return f"错误: 模板语法错误 - {e}"
    except Exception as e:
        st.error(f"渲染模板时出错: {e}")
        return f"错误: 渲染模板时出错 - {e}"

def load_template():
    """加载用户上传的模板或选择的示例模板"""
    uploaded_file = st.file_uploader("选择Markdown模板文件", type=["md"])
    
    try:
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接示例模板文件夹路径
        template_dir = os.path.join(script_dir, "../static/公文")
        
        # 列出文件夹中的所有md文件
        if os.path.exists(template_dir):
            md_files = [f for f in os.listdir(template_dir) if f.endswith('.md')]
            if md_files:
                example_choice = st.radio(
                    "或者选择示例模板",
                    md_files,
                    horizontal=True
                )
            else:
                example_choice = None
                st.warning("示例模板文件夹中没有找到Markdown文件")
        else:
            example_choice = None
            st.error("示例模板文件夹不存在")
    except Exception as e:
        st.error(f"获取示例模板列表失败: {e}")
        example_choice = None
    
    if uploaded_file:
        return uploaded_file.getvalue().decode("utf-8")
    elif example_choice:
        try:
            # 拼接选中的示例模板文件路径
            template_path = os.path.join(script_dir, "../static/公文", example_choice)
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            st.error(f"读取示例模板 {example_choice} 失败: {e}")
    return None


def display_variable_analysis(template_content):
    """显示模板变量和条件分析结果"""
    st.subheader("步骤2: 变量和条件分析结果")
    return extract_jinja_variables(template_content)


def process_regular_variables(current_element):
    """处理常规变量输入"""
    st.markdown("### 常规变量")
    st.write("请提供以下变量的值：")
    
    for var in current_element["variables"]:
        if var not in st.session_state.params:
            st.session_state.params[var] = ""
        
        st.session_state.params[var] = st.text_input(
            f"请输入 `{var}` 的值", 
            value=st.session_state.params[var],
            key=f"step_{st.session_state.current_step}_{var}"
        )


def process_conditional_variables(current_element):
    """处理条件变量输入"""
    st.markdown(f"### 条件变量: {current_element['condition_var']}")
    
    # 选择条件值
    options = [opt["value"] for opt in current_element["options"]]
    if current_element['condition_var'] not in st.session_state.params:
        st.session_state.params[current_element['condition_var']] = options[0]
    
    # 使用按钮组替代下拉选择框
    st.markdown(f"请选择 `{current_element['condition_var']}` 的值：")
    cols = st.columns(len(options))
    for i, opt in enumerate(options):
        with cols[i]:
            if st.button(opt, key=f"btn_{current_element['condition_var']}_{opt}"):
                st.session_state.params[current_element['condition_var']] = opt
                st.rerun()
    
    # 显示当前选中的值
    st.info(f"当前选择: {st.session_state.params[current_element['condition_var']]}")
    
    # 根据选择显示对应的变量
    selected_option = next(
        opt for opt in current_element["options"] 
        if opt["value"] == st.session_state.params[current_element['condition_var']]
    )
    
    st.write(f"请提供 `{st.session_state.params[current_element['condition_var']]}` 分支的变量值：")
    
    for var in selected_option["variables"]:
        if var not in st.session_state.params:
            st.session_state.params[var] = ""
        
        st.session_state.params[var] = st.text_input(
            f"请输入 `{var}` 的值", 
            value=st.session_state.params[var],
            key=f"step_{st.session_state.current_step}_{var}"
        )


def process_boolean_variables(current_element):
    """处理布尔变量输入"""
    st.markdown(f"### 布尔变量: {current_element['condition_var']}")
    
    # 选择布尔值
    if current_element['condition_var'] not in st.session_state.params:
        st.session_state.params[current_element['condition_var']] = "true"
    
    show_details = st.checkbox(
        f"是否显示详情 (`{current_element['condition_var']}`)", 
        value=(st.session_state.params[current_element['condition_var']] == "true"),
        key=f"step_{st.session_state.current_step}_bool"
    )
    
    st.session_state.params[current_element['condition_var']] = "true" if show_details else "false"
    
    # 根据选择显示对应的变量
    if show_details:
        st.write("请提供详情变量值：")
        for var in current_element["true_variables"]:
            if var not in st.session_state.params:
                st.session_state.params[var] = ""
            
            st.session_state.params[var] = st.text_input(
                f"请输入 `{var}` 的值", 
                value=st.session_state.params[var],
                key=f"step_{st.session_state.current_step}_{var}"
            )
    else:
        st.write("请提供概况变量值：")
        for var in current_element["false_variables"]:
            if var not in st.session_state.params:
                st.session_state.params[var] = ""
            
            st.session_state.params[var] = st.text_input(
                f"请输入 `{var}` 的值", 
                value=st.session_state.params[var],
                key=f"step_{st.session_state.current_step}_{var}"
            )


def display_navigation_buttons(extracted_structure):
    """显示导航按钮"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.current_step > 0:
            if st.button("上一步"):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col2:
        if st.session_state.current_step < len(extracted_structure) - 1:
            if st.button("下一步"):
                st.session_state.current_step += 1
                st.rerun()
        else:
            if st.button("完成并渲染"):
                st.session_state.show_results = True


def display_results(template_content):
    """显示渲染结果"""
    if 'show_results' in st.session_state and st.session_state.show_results:
        st.subheader("已提供的参数")
        st.json(st.session_state.params)
        
        st.subheader("模板渲染")
        
        # 渲染模板
        rendered_text = render_template(template_content, st.session_state.params)
        
        # 显示渲染结果
        st.text_area("渲染结果", rendered_text, height=400)
        
        # 提供下载按钮
        st.download_button(
            label="下载渲染结果",
            data=rendered_text,
            file_name="rendered_template.txt",
            mime="text/plain"
        )
        
        # 重置按钮
        if st.button("重新开始"):
            st.session_state.clear()
            st.rerun()

def main():
    st.title("Jinja2模板自动化生成工具")
    
    # 1. 上传模板文件
    st.subheader("步骤1: 上传或选择带有Jinja2特性的Markdown模板")
    template_content = load_template()
    
    if template_content:
        # 2. 提取变量和条件
        extracted_structure = display_variable_analysis(template_content)
    
        # 3. 收集变量值
        st.subheader("步骤3: 填写变量值")
        # 初始化session_state
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
            st.session_state.params = {}
        
        # 显示当前步骤
        st.subheader(f"步骤 {st.session_state.current_step + 1}/{len(extracted_structure)}")
        
        # 获取当前步骤的元素
        current_element = extracted_structure[st.session_state.current_step]
        
        # 处理不同类型的元素
        if current_element["type"] == "常规变量":
            process_regular_variables(current_element)
        elif current_element["type"] == "条件变量":
            process_conditional_variables(current_element)
        elif current_element["type"] == "布尔变量":
            process_boolean_variables(current_element)
        
        # 显示导航按钮
        display_navigation_buttons(extracted_structure)
        
        # 显示结果
        display_results(template_content)
if __name__ == "__main__":
    main()