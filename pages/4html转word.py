# pages/3_HTML2DOCX.py
import streamlit as st
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, RGBColor
import pandas as pd
import io
import base64

# ---------- 常量：HTML标签级别映射，样式 ----------
LV_MAP = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
LV_CN = {1: "标题1", 2: "标题2", 3: "标题3", 4: "标题4", 5: "标题5", 6: "标题6", 0: "正文"}

STYLE_PRESETS = {
    "正式报告": {
        1: {"size": 18, "bold": True, "color": (0, 0, 0)},
        2: {"size": 16, "bold": True, "color": (0, 0, 0)},
        3: {"size": 14, "bold": True, "color": (0, 0, 0)},
        0: {"size": 12, "bold": False, "color": (0, 0, 0)},
    },
    "科技蓝": {
        1: {"size": 20, "bold": True, "color": (0, 84, 159)},
        2: {"size": 16, "bold": True, "color": (0, 84, 159)},
        3: {"size": 14, "bold": True, "color": (0, 84, 159)},
        0: {"size": 12, "bold": False, "color": (0, 0, 0)},
    },
}

# 默认内容标签列表
DEFAULT_CONTENT_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span']

# ---------- 函数 ----------
def quick_tag_map(html: str, content_tags):
    """快速映射HTML标签及其示例文本"""
    soup = BeautifulSoup(html, "html.parser")
    tag_sample = {}
    # 只收集内容标签
    for tag in soup.find_all(content_tags):
        text = tag.get_text(" ", strip=True)
        if text and tag.name not in tag_sample:
            tag_sample[tag.name] = text[:60]
    # 创建表格数据，只包含标签和示例，级别信息在主流程中添加
    rows = [{"标签": f"<{k}>", "示例": v, "default_level": LV_MAP.get(k, 0)} for k, v in tag_sample.items()]
    return pd.DataFrame(rows)

def process_element(element, content_tags, blocks):
    """递归处理HTML元素，构建文档块"""
    # 处理文本节点
    if element.name is None:
        text = element.strip()
        if text:
            return text
        return ''
    # 跳过script和style标签
    elif element.name in ['script', 'style']:
        return ''
    # 处理内容标签
    elif element.name in content_tags:
        text = ''
        has_content_child = False
        
        # 检查是否有子内容标签
        for child in element.children:
            if child.name in content_tags:
                has_content_child = True
                # 递归处理子内容标签
                process_element(child, content_tags, blocks)
            else:
                # 处理非内容标签的子元素
                child_text = process_element(child, content_tags, blocks) or ''
                text += child_text
        
        # 如果没有子内容标签，才将当前内容标签添加到blocks
        if not has_content_child:
            full_text = text.strip()
            if full_text:
                blocks.append({
                    "text": full_text,
                    "level": LV_MAP.get(element.name, 0)
                })
        
        return ''
    # 处理其他标签（如div等容器标签）
    else:
        text = ''
        for child in element.children:
            child_text = process_element(child, content_tags, blocks) or ''
            text += child_text
        return text

def parse_html_to_blocks(html_raw, content_tags):
    """将HTML解析为文档块列表"""
    soup = BeautifulSoup(html_raw, "html.parser")
    blocks = []
    
    # 递归处理HTML元素
    process_element(soup, content_tags, blocks)
    
    # 如果没有找到任何内容标签，尝试直接从body中提取文本
    if not blocks:
        body = soup.find('body')
        if body:
            text = body.get_text(" ", strip=True)
            if text:
                blocks.append({"text": text, "level": 0})
    
    return blocks

def build_docx(blocks, preset):
    """根据文档块和样式预设构建DOCX文档"""
    doc = Document()
    style = STYLE_PRESETS[preset]
    for blk in blocks:
        level = blk["level"]
        para = doc.add_paragraph()
        run = para.add_run(blk["text"])
        run.font.size = Pt(style[level]["size"])
        run.bold = style[level]["bold"]
        run.font.color.rgb = RGBColor(*style[level]["color"])
        if level >= 1:
            para.style = f"Heading {level}"
    return doc

def create_download_link(doc):
    """创建DOCX文件的下载链接"""
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="export.docx">⏬ 下载 DOCX</a>'
    return href

def preview_document(blocks, tag_lv, preset):
    """预览文档格式效果"""
    # 应用标签级别映射
    preview_blocks = []
    for blk in blocks:
        preview_blk = blk.copy()
        # 用原文本反查标签（只取第一个匹配）
        for tag_name, lvl in tag_lv.items():
            tag_without_brackets = tag_name.strip("<>")
            # 查找原始标签与映射表中的标签匹配
            if blk["level"] == LV_MAP.get(tag_without_brackets, 0):   # 粗略匹配
                preview_blk["level"] = lvl
                break
        preview_blocks.append(preview_blk)
    
    # 使用Streamlit的markdown展示预览
    style = STYLE_PRESETS[preset]
    preview_html = "<div style='font-family: SimSun, serif; padding: 20px; background-color: #f9f9f9; border-radius: 5px;'>"
    
    for blk in preview_blocks:
        level = blk["level"]
        text = blk["text"]
        size = style[level]["size"]
        bold = "font-weight: bold;" if style[level]["bold"] else ""
        color = f"color: rgb{style[level]["color"]};"
        
        if level >= 1:
            heading_tag = f"h{level}"
            preview_html += f"<{heading_tag} style='{bold} {color} margin: 10px 0;'>{text}</{heading_tag}>"
        else:
            preview_html += f"<p style='{bold} {color} font-size: {size}px; margin: 5px 0;'>{text}</p>"
    
    preview_html += "</div>"
    return preview_html

def get_sidebar_input():
    """获取侧边栏用户输入"""
    with st.sidebar:
        html_raw = st.text_area("粘贴 HTML", height=150, help="在此粘贴您想要转换的HTML代码")
        
        # 添加自定义内容标签配置
        st.markdown("### 自定义内容标签")
        default_tags_str = ", ".join(DEFAULT_CONTENT_TAGS)
        custom_tags = st.text_input("作为独立段落的标签（逗号分隔）", value=default_tags_str, 
                                   help="例如: h1, h2, p, li, span, div")
        content_tags = [tag.strip() for tag in custom_tags.split(",") if tag.strip()]
        
        # 侧边栏的解析按钮
        parsed = False
        if st.button("🔍 开始解析", type="primary"):
            if html_raw:
                parsed = True
            else:
                st.warning("请先在左侧粘贴HTML代码")
        
        return html_raw, content_tags, parsed

# ---------- 主流程 ----------
if __name__ == "__main__":
    st.set_page_config(page_title="HTML → DOCX 精调导出", layout="wide")
    st.markdown("### 🚀 HTML 转 DOCX 精调工作台")
    
    # 初始化会话状态
    if "parsed_data" not in st.session_state:
        st.session_state["parsed_data"] = None
    if "preview_html" not in st.session_state:
        st.session_state["preview_html"] = None
    if "tag_lv" not in st.session_state:
        st.session_state["tag_lv"] = None
    
    # 获取侧边栏输入
    html_raw, content_tags, parsed = get_sidebar_input()
    
    # 如果点击了解析按钮
    if parsed:
        # 解析HTML结构，生成标签映射表
        df_map = quick_tag_map(html_raw, content_tags)
        
        # 解析HTML为文档块
        blocks = parse_html_to_blocks(html_raw, content_tags)
        
        # 保存解析结果到会话状态
        st.session_state["parsed_data"] = {
            "df_map": df_map,
            "blocks": blocks
        }
        
        # 初始化标签级别映射
        df = df_map.copy()
        df.insert(1, "级别", df["default_level"].map(LV_CN))
        rev_cn = {v: k for k, v in LV_CN.items()}
        st.session_state["tag_lv"] = {row["标签"]: rev_cn[row["级别"]] for _, row in df.iterrows()}
        
        st.success("HTML解析完成！")
    
    # 如果已经解析过数据，显示功能界面
    if st.session_state["parsed_data"]:
        # 获取解析数据
        df = st.session_state["parsed_data"]["df_map"].copy()
        blocks = st.session_state["parsed_data"]["blocks"].copy()
        
        # 用两个tab
        tab1, tab2 = st.tabs(["预览导出", "自定义修改"])
        
        with tab1:
            # 将样式选择功能移至级别映射表格之前
            st.markdown("### 选择样式")
            preset = st.selectbox("样式模板", list(STYLE_PRESETS.keys()))

            # 预览和导出功能
            rev_cn = {v: k for k, v in LV_CN.items()}
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👁️ 预览文档"):
                    with st.spinner("生成预览中..."):
                        st.session_state["preview_html"] = preview_document(
                            blocks, 
                            st.session_state["tag_lv"], 
                            preset
                        )
            
            with col2:
                if st.button("📄 生成 DOCX 文档", type="primary"):
                    with st.spinner("生成DOCX文档中..."):
                        # 在生成DOCX时进行级别更新
                        for blk in blocks:
                            # 用原文本反查标签（只取第一个匹配）
                            for tag_name, lvl in st.session_state["tag_lv"].items():
                                tag_without_brackets = tag_name.strip("<>")
                                # 查找原始标签与映射表中的标签匹配
                                if blk["level"] == LV_MAP.get(tag_without_brackets, 0):   # 粗略匹配
                                    blk["level"] = lvl
                                    break
                        
                        # 构建并提供下载链接
                        doc = build_docx(blocks, preset)
                        download_link = create_download_link(doc)
                        st.markdown(download_link, unsafe_allow_html=True)
                        st.balloons()
            
            # 显示预览结果
            if st.session_state["preview_html"]:
                st.markdown(st.session_state["preview_html"], unsafe_allow_html=True)
        
        with tab2:
            # 级别映射表格
            st.markdown("### 调整HTML标签对应的文档级别")
            # 添加级别列，并设置为可编辑
            df.insert(1, "级别", df["default_level"].map(LV_CN))
            # 删除默认级别数字列
            df = df.drop(columns=["default_level"])
            
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                column_config={"级别": st.column_config.SelectboxColumn(options=list(LV_CN.values()))},
                disabled=["标签", "示例"],
                key="editor"
            )
            
            # 保存映射结果到会话状态
            rev_cn = {v: k for k, v in LV_CN.items()}
            st.session_state["tag_lv"] = {row["标签"]: rev_cn[row["级别"]] for _, row in edited_df.iterrows()}
            
            st.info("级别映射已更新！请切换到'预览导出'标签页查看效果。")
            