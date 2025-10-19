# pages/8_blank_like_html.py
import streamlit as st
from jinja2 import Template
import pyperclip

st.set_page_config(page_title="基本情况单元-填空式生成", layout="wide")

# ---------------- 模板 ----------------
single_site_tpl = """三、审查内容模板

（一）单独选址

（用地预审情况）该项目符合基本建设投资管理规定。{{ 预审年月 }}通过{{ 预审部门 }}用地预审（文号{{ 预审文号 }}）。

（可研批复情况）{{ 可研批复年月 }}，{{ 可研批复部门 }}批复（或核准、备案）可行性研究报告（文号{{ 可研批复文号 }}）。

（初步设计批复情况）{{ 初设批复年月 }}，{{ 初设批复部门 }}批复（或审核通过）工程初步设计（文号{{ 初设批复文号 }}）。

项目按{{ 建设标准或规模 }}建设，总投资{{ 总投资 }}亿元。

{{ 永久基本农田或红线表述 }}

{{ 违法用地表述 }}
"""

batch_land_tpl = """三、审查内容模板

（二）批次用地

[基本情况] 该批次实际申请用地情况为：总面积为{{ 批次总面积 }}公顷，其中，农用地{{ 批次农用地 }}公顷（其中耕地{{ 批次耕地 }}公顷）、建设用地{{ 批次建设用地 }}公顷、未利用地{{ 批次未利用地 }}公顷。

{{ 违法用地可调整说明 }}

[农用地转用情况] 该批次申请将农用地{{ 批次转用农用地 }}公顷（耕地{{ 批次转用耕地 }}公顷）、未利用地{{ 批次转用未利用地 }}公顷转为建设用地。

{{ 增减挂钩表述 }}

[缴纳新增建设用地土地有偿使用费] 该批次涉及新增建设用地{{ 批次新增建设用地 }}公顷，为{{ 批次等别 }}等别，需缴纳新增建设用地土地有偿使用费{{ 批次应缴费用 }}万元。{{ 批次缴费承诺 }}。

{{ 不缴纳有偿使用费表述 }}
"""

# ---------------- 状态初始化 ----------------
def init_state():
    keys = [
        "用地类型", "是否涉及永久基本农田", "是否涉及生态保护红线", "是否存在违法用地",
        "预审年月", "预审部门", "预审文号", "可研批复年月", "可研批复部门",
        "初设批复年月", "初设批复部门", "建设标准或规模", "总投资",
        "批次总面积", "批次农用地", "批次耕地", "批次建设用地", "批次未利用地",
        "批次转用农用地", "批次转用耕地", "批次转用未利用地",
        "批次新增建设用地", "批次等别", "批次应缴费用", "批次缴费承诺"
    ]
    for k in keys:
        if k not in st.session_state:
            st.session_state[k] = ""
    # 单选默认值
    for k, v in {
        "用地类型": "单独选址",
        "是否涉及永久基本农田": "否",
        "是否涉及生态保护红线": "否",
        "是否存在违法用地": "否"
    }.items():
        if st.session_state[k] == "":
            st.session_state[k] = v

init_state()

# ---------------- 顶部固定内容 ----------------
st.header("基本情况单元")
with st.container(border=True):
    st.markdown("**一、业务指导处室**  
国土空间用途管制处")
    st.markdown("**二、审查标准**")
    st.markdown("""
- 符合基本建设投资管理规定。  
- 建设单位已取得建设项目批准（核准或备案）文件、初步设计批准或审核文件，且应当在有效期内。  
- 用地涉及的新增建设用地应按规定缴纳新增建设用地土地有偿使用费，缴纳等级、标准应准确。  
- 1999年1月1日之后经依法批准的集体建设用地，在批准农用地转用时未缴纳新增建设用地有偿使用费的，申请土地征收时按照现行标准补缴。
""")

# ---------------- 条件选择 ----------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    land_type = st.segmented_control("用地类型", ["单独选址", "批次用地"], key="用地类型")
with col2:
    farmland = st.segmented_control("是否涉及永久基本农田", ["否", "是"], key="是否涉及永久基本农田")
with col3:
    eco = st.segmented_control("是否涉及生态保护红线", ["否", "是"], key="是否涉及生态保护红线")
with col4:
    illegal = st.segmented_control("是否存在违法用地", ["否", "是"], key="是否存在违法用地")

template = single_site_tpl if land_type == "单独选址" else batch_land_tpl
jinja_vars = sorted({node.name for node in Template(template).find_all()})

# ---------------- 填空区 ----------------
st.subheader("🔤 请填空")
inputs = {}
cols = st.columns(2)
for idx, var in enumerate(jinja_vars):
    with cols[idx % 2]:
        inputs[var] = st.text_input(var, placeholder=var, key=var)

# ---------------- 按钮 ----------------
left, mid, right = st.columns(3)
with left:
    generate = st.button("生成最终文本", type="primary")
with mid:
    copy_btn = st.button("复制结果")
with right:
    reset = st.button("重置")

# ---------------- 渲染 ----------------
if generate:
    text = template
    if land_type == "单独选址":
        if farmland == "是" or eco == "是":
            text = text.replace(
                "{{ 永久基本农田或红线表述 }}",
                "【本次报批不涉及占用永久基本农田或生态保护红线，但需报国务院审批的增加表述：该项目整体占用永久基本农田或生态保护红线，本段不涉及永久基本农田或生态保护红线，按规定应呈报国务院审批。】"
            )
        else:
            text = text.replace("{{ 永久基本农田或红线表述 }}", "")
        if illegal == "是":
            text = text.replace(
                "{{ 违法用地表述 }}",
                "（违法用地占用自然保护区或生态保护红线情况）该项目违法用地涉及自然保护区或生态保护红线，省级林草主管部门对违法用地占用自然保护区或生态保护红线出具了意见，说明项目不涉及破坏森林草原湿地或违反自然保护区风景名胜区等管理规定的情形【或：说明存在上述情形已经处罚】；省级生态环境主管部门对违法用地占用自然保护区或生态保护红线占用出具了意见，说明未发现项目破坏生态环境的行为【或：说明存在破坏生态环境的行为已经处罚】。"
            )
        else:
            text = text.replace("{{ 违法用地表述 }}", "")
    else:
        if illegal == "否":
            text = text.replace(
                "{{ 违法用地可调整说明 }}",
                "（无违法用地或2020年之后发生的违法用地，不需说明占用可调整地类情况）"
            )
        else:
            text = text.replace("{{ 违法用地可调整说明 }}", "")
    rendered = Template(text).render(**{k: inputs[k] or f"{{{k}}}" for k in jinja_vars})
    st.session_state["final"] = rendered

if "final" in st.session_state:
    st.subheader("📄 生成结果")
    st.code(st.session_state["final"], language="text")

if copy_btn and "final" in st.session_state:
    pyperclip.copy(st.session_state["final"])
    st.toast("已复制到剪贴板！", icon="✅")

if reset:
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()