# test_radio_blue.py
import streamlit as st
from streamlit_extras.st_horizontal_radio import st_horizontal_radio

# 蓝色选中样式
st.markdown("""
<style>
/* 整个 radio 组横向排布 */
div.stHorizontalRadio > div {
    flex-direction: row;
    gap: 0.5rem;
}

/* 未选中 label */
div.stHorizontalRadio label {
    background-color: #f7f7f7 !important;
    color: #333 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
    padding: 0.4rem 0.8rem !important;
    cursor: pointer !important;
    transition: all .2s ease;
}

/* 选中 label（蓝色高亮） */
div.stHorizontalRadio input:checked + label {
    background-color: #0066ff !important;
    color: #ffffff !important;
    border-color: #0066ff !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# 组件
choice = st_horizontal_radio(
    label="请选择一个水果：",
    options=["🍎 苹果", "🍌 香蕉", "🍇 葡萄"],
    default="🍌 香蕉",
    key="fruit"
)

st.write("当前选中：", choice)