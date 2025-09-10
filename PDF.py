import streamlit as st
import pandas as pd
import fitz
from typing import Union
from io import BytesIO
import os

# 统一类型别名
PathOrBuffer = Union[str, BytesIO]

# 功能函数
def _open_document(src: PathOrBuffer) -> fitz.Document:
    """
    统一入口：无论 src 是路径还是 BytesIO，都返回 fitz.Document
    """
    if isinstance(src, str) and os.path.isfile(src):
        return fitz.open(src)
    elif isinstance(src, BytesIO):
        src.seek(0)
        return fitz.open(stream=src.read(), filetype="pdf")
    else:
        raise TypeError("src 必须是文件路径或 BytesIO")

def extract_pdf_chapters(src: PathOrBuffer) -> list:
    """
    从 PDF 中提取章节标题及其起始和结束页码。
    参数:
        src: PDF 文件路径（str）或内存文件对象（BytesIO）
    返回:
        chapters: 列表，每个元素是一个字典，包含：
            - level: 章节层级
            - title: 章节标题
            - start_page: 起始页码（1-based）
            - end_page: 结束页码（1-based）
    """
    chapters = []
    doc = _open_document(src)

    toc = doc.get_toc()
    if not toc:
        doc.close()
        return []

    # 1. 先收集所有书签条目
    for entry in toc:
        level, title, page_num = entry[0], entry[1], entry[2]
        # 防止负数或超界
        start_page = max(1, page_num + 1) if page_num >= 0 else 1
        chapters.append({'level': level, 'title': title, 'start_page': start_page})

    # 2. 计算每个章节的结束页码
    total_pages = doc.page_count
    for i, current in enumerate(chapters):
        if i == len(chapters) - 1:
            current['end_page'] = total_pages
        else:
            # 找到下一个同级或更高级别章节
            j = i + 1
            while j < len(chapters) and chapters[j]['level'] > current['level']:
                j += 1
            if j < len(chapters):
                current['end_page'] = chapters[j]['start_page'] - 1
            else:
                current['end_page'] = total_pages

    doc.close()
    return chapters


# ---------- 文件上传 ----------
def handle_file_upload() -> BytesIO | None:
    """返回上传 PDF 的 BytesIO；纯内存，不写磁盘"""
    uploaded = st.file_uploader("上传 PDF 文件", type=["pdf"])
    if uploaded:
        uploaded.seek(0)
        return uploaded
    return None

# ---------- Streamlit ----------
def main():
    # ---------- 页面配置 ----------
    st.set_page_config(page_title="PDF章节信息提取", page_icon="📑")
    # ---------- 主界面 ----------
    st.markdown("### 📑 PDF 章节信息提取")

    # ---------- 功能 1：章节提取 ----------
    pdf_bytes = handle_file_upload()
    if pdf_bytes:
        with st.spinner("正在解析文档结构..."):
            chapters = extract_pdf_chapters(pdf_bytes)

        if chapters:
            df_chapters = pd.DataFrame(chapters)

            # 级别筛选
            level_opts = ["全部"] + sorted(df_chapters["level"].astype(str).unique())
            selected = st.selectbox("选择标题级别", level_opts)
            if selected != "全部":
                df_chapters = df_chapters[df_chapters["level"] <= int(selected)]

            # 展示表格
            st.subheader("📖 文档结构")
            df_show = df_chapters.copy()
            df_show["page_range"] = df_show.apply(
                lambda r: f"{r.start_page}-{r.end_page}", axis=1
            )
            st.dataframe(
                df_show[["level", "title", "page_range"]],
                use_container_width=True,
                hide_index=True,
            )

            # 展开 JSON
            with st.expander("📂 章节详情"):
                st.json(chapters)
        else:
            st.warning("⚠️ 未检测到章节信息")

    # ---------- 功能 2：在线工具推荐 ----------
    st.sidebar.caption("在线 PDF 工具推荐")
    st.sidebar.markdown(
        """
        <div style="display:flex;flex-direction:column;margin-bottom:20px;">
            <a href="https://jiheutools-knvf60mx.maozi.io/" target="_blank">
                <button style="padding:8px 16px;margin-bottom:10px;background:#FF5722;color:white;border:none;border-radius:4px;cursor:pointer;width:100%;">
                    uTools 多功能插件
                </button>
            </a>
            <a href="https://www.ilovepdf.com/zh-cn/compress_pdf" target="_blank">
                <button style="padding:8px 16px;margin-bottom:10px;background:#FF5722;color:white;border:none;border-radius:4px;cursor:pointer;width:100%;">
                    iLovePDF
                </button>
            </a>
            <a href="https://www.pdf2go.com/zh/compress-pdf" target="_blank">
                <button style="padding:8px 16px;background:#FF5722;color:white;border:none;border-radius:4px;cursor:pointer;width:100%;">
                    PDF2Go
                </button>
            </a>
            <a href="https://www.pdfgear.com/zh/" target="_blank">
                <button style="padding:8px 16px;background:#FF5722;color:white;border:none;border-radius:4px;cursor:pointer;width:100%;">
                    pdfgear
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # ---------- 底部 ----------
    st.markdown("---")
    st.caption("🚀 页面缓存可通过 Ctrl+Shift+R 强制刷新")

    with st.expander("📦 使用说明"):
        st.markdown(
            "由于前端 JS 可在浏览器本地完成数据处理，私密文件不会上传到服务器，"
            "因此前端能实现的功能已全部迁移。\n\n"
            "🔗 **前端地址**：[uTools 多功能插件](https://jiheutools-knvf60mx.maozi.io/)\n\n"
            "已迁移：分析页数、转换图片、按页码拆分 PDF、PDF 合并。"
            "未迁移：章节信息提取、按章节拆分 PDF、PDF 压缩。"
        )

    with st.expander("💡 小贴士 & 高级用法"):
        st.markdown(
            "- **ArcGIS 矢量 PDF**：如果常规压缩效果差，可先 **转图片型 PDF** 再压缩；\n"
            "- 也可尝试 **缩小页面尺寸** 为 A4/A3。\n"
            "- 多工具组合，效果往往更好！"
        )

if __name__ == "__main__":
    main()