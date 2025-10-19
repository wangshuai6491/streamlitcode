 
import streamlit as st

st.title("填空题示例（Markdown方式）")

# 使用expander让界面更整洁
with st.expander("开始答题", expanded=True):
    # 获取用户输入
    name = st.text_input("你的姓名", key="name_q")
    sports = st.text_input("你会的运动", key="sports_q")
    cooking = st.text_input("你会的菜肴", key="cook_q")
    
    # 使用Markdown和f-string动态生成题目
    # 如果用户已经输入，则显示答案，否则显示输入框的引用
    answer_display1 = name if name else "**_________________**"
    answer_display2 = sports if sports else "**_________________**"
    answer_display3 = cooking if cooking else "**_________________**"
    
    question_text = f"""
    ### 请根据你的情况填空：
    
    我的姓名是 **{answer_display1}**，我会很多运动，有 **{answer_display2}**，我还会做饭，比如 **{answer_display3}**。
    """
    
    st.markdown(question_text, unsafe_allow_html=True)
    
    if st.button("生成我的介绍"):
        if name and sports and cooking:
            st.balloons()
            st.success("你的个人介绍已生成！")
            # 这里可以执行后续逻辑，如保存答案或显示结果
        else:
            st.info("请先完成上方的所有填空。")
 