import streamlit as st
import json

# 假设的提取结果
extracted_structure = [
  {
    "type": "常规变量",
    "variables": ["标题", "作者", "日期", "版本号", "内容"]
  },
  {
    "type": "条件变量",
    "condition_var": "项目状态",
    "options": [
      {"value": "完成", "variables": ["已完成明细"]},
      {"value": "进行中", "variables": ["进行中明细"]},
      {"value": "其他", "variables": ["暂停原因"]}
    ]
  },
  {
    "type": "布尔变量",
    "condition_var": "显示详情",
    "true_variables": ["负责人", "团队规模"],
    "false_variables": ["简单概况"]
  },
  {
    "type": "条件变量",
    "condition_var": "项目所在地",
    "options": [
      {"value": "本地", "variables": ["本地名称"]},
      {"value": "外地", "variables": ["外地名称"]},
      {"value": "其他", "variables": ["其他名称"]}
    ]
  },
  {
    "type": "常规变量",
    "variables": ["带引号文本"]
  }
]

def render_template(template, params):
    """简单的模板渲染函数"""
    for key, value in params.items():
        placeholder = "{{ " + key + " }}"
        template = template.replace(placeholder, value)
    
    # 处理条件语句（简化版）
    if "项目状态" in params:
        if params["项目状态"] == "完成":
            template = template.replace("{% if 项目状态 == \"完成\" %}", "")
            template = template.replace("{% elif 项目状态 == \"进行中\" %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
        elif params["项目状态"] == "进行中":
            template = template.replace("{% if 项目状态 == \"完成\" %}", "")
            template = template.replace("{% elif 项目状态 == \"进行中\" %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
        else:
            template = template.replace("{% if 项目状态 == \"完成\" %}", "")
            template = template.replace("{% elif 项目状态 == \"进行中\" %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
    
    # 处理布尔变量
    if "显示详情" in params:
        if params["显示详情"] == "true":
            template = template.replace("{% if 显示详情 %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
        else:
            template = template.replace("{% if 显示详情 %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
    
    # 处理项目所在地
    if "项目所在地" in params:
        if params["项目所在地"] == "本地":
            template = template.replace("{% if 项目所在地 == \"本地\" %}", "")
            template = template.replace("{% elif 项目所在地 == \"外地\" %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
        elif params["项目所在地"] == "外地":
            template = template.replace("{% if 项目所在地 == \"本地\" %}", "")
            template = template.replace("{% elif 项目所在地 == \"外地\" %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
        else:
            template = template.replace("{% if 项目所在地 == \"本地\" %}", "")
            template = template.replace("{% elif 项目所在地 == \"外地\" %}", "")
            template = template.replace("{% else %}", "")
            template = template.replace("{% endif %}", "")
    
    return template

def main():
    st.title("Jinja2 模板参数生成器")
    st.markdown("按层次提供参数值，生成渲染后的文本")
    
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
    
    elif current_element["type"] == "条件变量":
        st.markdown(f"### 条件变量: {current_element['condition_var']}")
        
        # 选择条件值
        options = [opt["value"] for opt in current_element["options"]]
        if current_element['condition_var'] not in st.session_state.params:
            st.session_state.params[current_element['condition_var']] = options[0]
        
        st.session_state.params[current_element['condition_var']] = st.selectbox(
            f"请选择 `{current_element['condition_var']}` 的值", 
            options,
            index=options.index(st.session_state.params[current_element['condition_var']]),
            key=f"step_{st.session_state.current_step}_condition"
        )
        
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
    
    elif current_element["type"] == "布尔变量":
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
    
    # 导航按钮
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
    
    # 显示结果
    if 'show_results' in st.session_state and st.session_state.show_results:
        st.subheader("已提供的参数")
        st.json(st.session_state.params)
        
        st.subheader("模板渲染")
        
        # 示例模板
        template = """
# {{ 标题 }}
**作者**: {{ 作者 }}  
**日期**: {{ 日期 }}  
**版本**: {{ 版本号 }}  
{{ 内容 }}

# 项目状态报告
{% if 项目状态 == "完成" %}
✅ **项目状态**: 已完成
{{ 已完成明细 }}
{% elif 项目状态 == "进行中" %}
⏳ **项目状态**: 进行中
{{ 进行中明细 }}
{% else %}
⚠️ **项目状态**: 暂停
{{ 暂停原因 }}
{% endif %}

{% if 显示详情 %}
## 详细信息
- 负责人: {{ 负责人 }}
- 团队规模: {{ 团队规模 }}人
{% else %}
- {{ 简单概况 }}
{% endif %}

## 项目所在地
{% if 项目所在地 == "本地" %}
{{ 本地名称 }}
{% elif 项目所在地 == "外地" %}
{{ 外地名称 }}
{% else %}
{{ 其他名称 }}
{% endif %}

## 特殊字符测试
- 带引号文本: {{ 带引号文本 }}
"""
        
        # 渲染模板
        rendered_text = render_template(template, st.session_state.params)
        
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

if __name__ == "__main__":
    main()