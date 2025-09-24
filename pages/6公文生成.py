import streamlit as st
import jinja2
import yaml
import os
import pandas as pd
from pathlib import Path
import re

# 获取所有markdown模板文件
@st.cache_data
def get_template_files(template_dir):
    """获取模板目录中所有的markdown文件"""
    # 查找所有.md文件
    md_files = list(Path(template_dir).glob("*.md"))
    return [str(file) for file in md_files]

# 解析markdown文件的YAML头部和内容
def parse_md_template(file_path):
    """解析markdown文件，提取YAML头部和内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分离YAML头部和内容
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not match:
            st.error("模板文件格式不正确，缺少YAML头部")
            return None, None
        
        yaml_str = match.group(1)
        template_content = match.group(2)
        
        # 解析YAML
        yaml_data = yaml.safe_load(yaml_str)
        return yaml_data, template_content
    except Exception as e:
        st.error(f"解析模板文件失败: {str(e)}")
        return None, None

# 渲染模板
def render_template(template_content, variables):
    """使用Jinja2渲染模板"""
    try:
        template = jinja2.Template(template_content)
        return template.render(**variables)
    except Exception as e:
        st.error(f"渲染模板失败: {str(e)}")
        return None

# 主逻辑
def main():
    # 获取模板目录
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', '公文')
    
    # 检查目录是否存在
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        st.warning(f"模板目录不存在，已自动创建: {template_dir}")
    
    # 获取模板文件列表
    template_files = get_template_files(template_dir)
    
    if not template_files:
        st.info(f"在目录 {template_dir} 中未找到任何Markdown模板文件")
        return
    
    # 让用户选择模板文件
    file_names = [os.path.basename(file) for file in template_files]
    selected_file_idx = st.selectbox(
        "请选择一个模板文件",
        range(len(file_names)),
        format_func=lambda x: file_names[x]
    )
    selected_file_path = template_files[selected_file_idx]
    
    # 解析选中的模板文件
    yaml_data, template_content = parse_md_template(selected_file_path)
    if not yaml_data or not template_content:
        return
    
    # 显示模板标题
    st.subheader(f"模板: {yaml_data.get('title', '未命名模板')}")
    
    # 收集变量值
    st.subheader("请填写变量值")
    variables = {}
    
    # 如果有变量定义
    if 'variables' in yaml_data and isinstance(yaml_data['variables'], list):
        # 将变量转换为DataFrame
        variables_df = pd.DataFrame(yaml_data['variables'])
        # 添加一个空列用于用户输入值
        variables_df['value'] = ''
        
        # 使用Streamlit的data_editor展示和编辑表格
        edited_df = st.data_editor(
            variables_df[['label', 'name', 'type', 'value']],  # 只显示需要的列
            column_config={
                'label': st.column_config.TextColumn('变量标签', disabled=True),
                'name': st.column_config.TextColumn('变量名', disabled=True),
                'type': st.column_config.TextColumn('类型', disabled=True),
                'value': st.column_config.TextColumn('变量值', required=False)  # 改为非必填
            },
            hide_index=True,
            num_rows="fixed"
        )
        
        # 从编辑后的DataFrame中提取变量值
        for _, row in edited_df.iterrows():
            var_name = row['name']
            var_value = row['value']
            var_type = row['type']
            
            # 处理未填写的变量，用*代替
            if not var_value and var_value != 0:
                var_value = '*'
            else:
                # 根据变量类型转换值
                if var_type == 'number':
                    try:
                        var_value = float(var_value)
                    except ValueError:
                        st.warning(f"变量 {row['label']} 应输入数字类型的值，已使用原始输入")
            
            variables[var_name] = var_value
    else:
        st.info("该模板没有定义变量")
    
    # 生成文档
    st.subheader("生成结果")
    if st.button("生成文档"):
        # 检查是否有未填写的变量
        missing_vars = [var for var, value in variables.items() if value == '*']
        if missing_vars:
            # 找到缺失变量的标签
            missing_labels = []
            if 'variables' in yaml_data:
                for var_info in yaml_data['variables']:
                    if var_info['name'] in missing_vars:
                        missing_labels.append(var_info['label'])
            
            st.warning(f"以下变量尚未填写，将使用*代替: {', '.join(missing_labels)}")
        
        # 渲染模板（即使有未填写的变量也继续）
        result = render_template(template_content, variables)
        if result:
            # 显示生成的文档内容
            st.text_area("生成的文档内容", result, height=400)
            
            # 提供下载功能
            st.download_button(
                label="下载生成的文档",
                data=result,
                file_name=f"{yaml_data.get('title', 'generated')}.md",
                mime="text/markdown"
            )

if __name__ == '__main__':
    # 设置页面配置
    st.set_page_config(
        page_title="公文模板生成器",
        page_icon="📄",
        layout="wide"
    )

    # 标题
    st.title("📄 公文模板生成器")
    main()
    