# pages/8_blank_like_html.py
import streamlit as st
from jinja2 import Template
import pyperclip

st.set_page_config(page_title="基本情况单元-填空式生成", layout="wide")

# --------------------------------------------------
# 1. 模板库（和 HTML 里完全一致，变量名也保持）
# --------------------------------------------------
single_site_tpl = """三、审查内容模板

（一）单独选址

（用地预审情况）该项目符合基本建设投资管理规定。{{ 预审年月 }}通过{{ 预审部门 }}用地预审（文号{{ 预审文号 }}）……

（可研批复情况）{{ 可研批复年月 }}，{{ 可研批复部门 }}批复（或核准、备案）可行性研究报告……
"""

batch_land_tpl = """三、审查内容模板

（二）批次用地

[基本情况] 该批次实际申请用地情况为：总面积为{{ 批次总面积 }}公顷……
"""

# --------------------------------------------------
# 2. 状态初始化
# --------------------------------------------------
def init_state():
    for k in [
        "用地类型", "是否涉及永久基本农田", "是否涉及生态保护红线", "是否存在违法用地",
        "预审年月", "预审部门", "预审文号", "可研批复年月", "可研批复部门",
        "批次总面积", "批次农用地", "批次耕地"
    ]:
        if k not in st.session_state:
            st.session_state[k] = ""

init_state()

# --------------------------------------------------
# 3. 顶部固定内容
# --------------------------------------------------
st.header("基本情况单元")
with st.container(border=True):
    st.markdown("**一、业务指导处室**  \n国土空间用途管制处")
    st.markdown("**二、审查标准**")
    st.markdown("""
- 符合基本建设投资管理规定。  
- 建设单位已取得建设项目批准（核准或备案）文件……
""")

# --------------------------------------------------
# 4. 条件选择（按钮组）
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    land_type = st.segmented_control(
        "用地类型", ["单独选址", "批次用地"], default="单独选址", key="用地类型"
    )
with col2:
    farmland = st.segmented_control(
        "是否涉及永久基本农田", ["否", "是"], default="否", key="是否涉及永久基本农田"
    )
with col3:
    eco = st.segmented_control(
        "是否涉及生态保护红线", ["否", "是"], default="否", key="是否涉及生态保护红线"
    )
with col4:
    illegal = st.segmented_control(
        "是否存在违法用地", ["否", "是"], default="否", key="是否存在违法用地"
    )

# 根据用地类型选模板
template = single_site_tpl if land_type == "单独选址" else batch_land_tpl
jinja_vars = sorted({node.name for node in Template(template).find_all()})

# --------------------------------------------------
# 5. 动态生成填空区（下划线输入框）
# --------------------------------------------------
st.subheader("🔤 请填空")
inputs = {}
cols = st.columns(3)
for idx, var in enumerate(jinja_vars):
    with cols[idx % 3]:
        inputs[var] = st.text_input(var, placeholder=var, key=var)

# --------------------------------------------------
# 6. 渲染 & 下载 & 复制 & 重置
# --------------------------------------------------
left, mid, right = st.columns(3)
with left:
    generate = st.button("生成最终文本", type="primary")
with mid:
    copy_btn = st.button("复制结果")
with right:
    reset = st.button("重置")

if generate:
    # 把条件性文字先替换掉（同 HTML 逻辑）
    text = template
    if land_type == "单独选址":
        if farmland == "是" or eco == "是":
            text = text.replace(
                "[永久基本农田或红线表述]",
                "【本次报批不涉及占用永久基本农田或生态保护红线，但需报国务院审批……】"
            )
        else:
            text = text.replace("[永久基本农田或红线表述]", "")
        if illegal == "是":
            text = text.replace(
                "[违法用地表述]",
                "（违法用地占用自然保护区或生态保护红线情况）该项目违法用地涉及……"
            )
        else:
            text = text.replace("[违法用地表述]", "")
    else:  # 批次
        if illegal == "否":
            text = text.replace(
                "[违法用地可调整说明]",
                "（无违法用地或2020年之后发生的违法用地，不需说明占用可调整地类情况）"
            )
        else:
            text = text.replace("[违法用地可调整说明]", "")

    # Jinja2 渲染
    rendered = Template(text).render(**{k: inputs[k] or f"{{{k}}}" for k in jinja_vars})
    st.session_state["final"] = rendered

if "final" in st.session_state:
    st.subheader("📄 生成结果")
    st.code(st.session_state["final"], language="text")

if copy_btn and "final" in st.session_state:
    pyperclip.copy(st.session_state["final"])
    st.toast("已复制到剪贴板！", icon="✅")

if reset:
    for k in st.session_state.keys():
        del st.session_state[k]
    st.rerun()
