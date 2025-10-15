import streamlit as st
from jinja2 import Environment, meta
import re
import os


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
                # 在当前条件块中添加变量
                if condition_type == '条件变量':
                    if current_branch is not None and current_branch < len(current_condition['options']):
                        current_condition['options'][current_branch]['variables'].extend(cleaned_vars)
                elif condition_type == '布尔变量':
                    if current_branch == 'true':
                        current_condition['true_variables'].extend(cleaned_vars)
                    else:
                        current_condition['false_variables'].extend(cleaned_vars)
            else:
                # 不在任何条件块中，添加到常规变量
                # 检查是否可以将变量添加到现有的常规变量组
                if results and results[-1]['type'] == '常规变量':
                    results[-1]['variables'].extend(cleaned_vars)
                else:
                    results.append({
                        'type': '常规变量',
                        'variables': cleaned_vars
                    })
    
    # 处理可能未关闭的条件块
    if current_condition:
        results.append(current_condition)
    
    return results

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
        ("测试模板"),
        horizontal=True
    )
    template_content = None
    if uploaded_file:
        template_content = uploaded_file.getvalue().decode("utf-8")
    elif example_choice == "测试模板":
        try:
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 拼接示例模板文件路径
            template_path = os.path.join(script_dir, "../static/公文/测试.md")
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
        except Exception as e:
            st.error(f"读取示例模板失败: {e}")
    
    if template_content:
        # 2. 提取变量和条件
        st.subheader("步骤2: 变量和条件分析结果")
        
        # 变量提取逻辑
        variable_structure = extract_jinja_variables(template_content)
    
        # 3. 收集变量值
        st.subheader("步骤3: 填写变量值")
        # 这里需要用户根据variable_structure提供参数值

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