import streamlit as st

# 为 toggle 组件指定 key，使其状态存入 session_state
kaiguan = st.toggle("分次报批", key="kaiguan_toggle")

# 此时 session_state 中就会有对应的键值对了
st.write(st.session_state)