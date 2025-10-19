import streamlit as st
import re

def render_with_inputs(template):
    """
    将模板中的 {[占位符]} 替换为输入框
    """
    # 正则匹配 {[占位符]}
    pattern = r"\{\[([^{}[\]]+)\]\}"
    
    # 分割文本和占位符
    tokens = re.split(pattern, template)
    
    # 用来保存渲染后的部分
    rendered = []
    
    for i, token in enumerate(tokens):
        # 如果是占位符（奇数索引，因为 split 后占位符在奇数位置）
        if i % 2 == 1:
            key = f"input_{i}"
            # 创建输入框，不显示 label
            rendered.append(
                st.text_input(token, key=key, label_visibility="collapsed")
            )
        else:
            # 普通文本直接添加
            rendered.append(token)
    
    return rendered

def get_filled_text(template):
    """
    获取替换后的完整文本
    """
    pattern = r"\{\[([^{}[\]]+)\]\}"
    tokens = re.split(pattern, template)
    
    filled = []
    for i, token in enumerate(tokens):
        if i % 2 == 1:
            key = f"input_{i}"
            filled.append(st.session_state.get(key, f"{{[{token}]}}"))
        else:
            filled.append(token)
    
    return "".join(filled)

# 示例长文本模板
long_template = """
基本情况：
- 项目名称：{[项目名称]}
- 建设单位：{[建设单位]}
- 建设地点：{[建设地点]}
- 建设规模：{[建设规模]}
- 总投资：{[总投资]} 万元

项目概述：
{[项目名称]}由{[建设单位]}投资建设，位于{[建设地点]}，建设内容包括{[建设规模]}，项目总投资为{[总投资]}万元。

建设周期：
计划从{[开工时间]}开工，至{[竣工时间]}竣工。
"""

st.title("多段落长文本填空题测试")

# 渲染模板（带输入框）
st.write("请填写以下内容：")
render_with_inputs(long_template)

# 生成按钮
if st.button("生成完整文本"):
    filled_text = get_filled_text(long_template)
    st.subheader("生成结果：")
    st.text_area("完整文本", filled_text, height=400)