from streamlit_extras.st_horizontal_radio import st_horizontal_radio

choice = st_horizontal_radio(
    label="请选择一个水果",
    options=["🍎 苹果", "🍌 香蕉", "🍇 葡萄"],
    default="🍌 香蕉",
    key="fruit"
)
st.write("当前选中：", choice)