import streamlit as st

st.title("环境测试")
st.write("如果你看到这段话，说明 Streamlit 环境运行正常！🎉")

name = st.text_input("请输入你的名字：")
if name:
    st.write(f"你好，{name}！")

st.slider("拖动看看：", 0, 100, 50)
st.success("环境测试完成 ✅")