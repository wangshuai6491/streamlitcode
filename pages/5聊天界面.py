import streamlit as st
import random
import time

# 设置页面标题和图标
st.set_page_config(page_title="AI聊天助手", page_icon="💬")

# 初始化会话状态中的消息历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 显示欢迎消息（如果是首次打开）
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("你好！我是你的AI聊天助手，有什么可以帮助你的吗？")
    st.session_state.messages.append({"role": "assistant", "content": "你好！我是你的AI聊天助手，有什么可以帮助你的吗？"})

# 处理用户输入
if prompt := st.chat_input("请输入您的消息..."):
    # 添加用户消息到聊天历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 生成AI响应
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 模拟AI思考过程
        assistant_response = random.choice([
            "你好！很高兴与你交谈。",
            "这个问题很有趣，让我想想...",
            "我不太确定，你能详细说明一下吗？",
            "根据我的了解，应该是这样的...",
            "非常感谢你的提问，我很乐意帮助你。"
        ])
        
        # 模拟打字效果
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # 添加闪烁的光标
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # 添加AI响应到聊天历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})
