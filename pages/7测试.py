import streamlit as st
import re

def render_text_with_inputs(template):
    """将 {[占位符]} 替换成输入框"""
    parts = re.split(r"(\{\[([^{}[\]]+)\]\})", template)
    for i, part in enumerate(parts):
        if re.match(r"\{\[([^{}[\]]+)\]\}", part):
            key = f"input_{i}"
            parts[i] = st.text_input(part, key=key, label_visibility="collapsed")
    return "".join(str(p) for p in parts)

def get_complete_text(template):
    """获取填写后的完整文本"""
    def replace_placeholder(match):
        key = f"input_{match.group(2)}"
        return st.session_state.get(key, match.group(1))
    
    # 为每个占位符生成唯一key
    numbered = re.sub(r"(\{\[([^{}[\]]+)\]\})", r"({\1,\2})", template)
    for idx, match in enumerate(re.finditer(r"\(\{(\{\[([^{}[\]]+)\]\}),([^{}[\]]+)\}\)", numbered)):
        full, name = match.group(1), match.group(3)
        numbered = numbered.replace(full, f"{{[PLACEHOLDER_{idx}]}}")
        st.session_state[f"input_{idx}"] = st.session_state.get(f"input_{name}", full)
    
    # 替换回结果
    result = re.sub(r"\{\[PLACEHOLDER_(\d+)\]\}", 
                   lambda m: st.session_state.get(f"input_{m.group(1)}", m.group(0)), 
                   numbered)
    return result

# 示例长文本
long_text = """
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

st.title("多段落填空题（稳定版）")

st.write("请填写：")
render_text_with_inputs(long_text)

if st.button("生成完整文本"):
    st.subheader("结果：")
    st.text_area("完整文本", get_complete_text(long_text), height=400)
