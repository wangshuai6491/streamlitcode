# md2docx_app.py
import streamlit as st
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import markdown, re, io, base64, pathlib

st.set_page_config(page_title="MD→DOCX 在线转换", layout="centered")
st.title("📄 Markdown 转 Word 工具")
st.caption("上传 `.md` 文件 → 点击按钮 → 下载 `.docx`")

@st.cache_data(show_spinner=False)
def md2docx_bytes(md_text: str) -> io.BytesIO:
    """把 Markdown 文本转成 DOCX 并返回内存文件"""
    doc = Document()

    # 基本样式
    def style():
        doc.styles['Normal'].font.name = '微软雅黑'
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        doc.styles['Normal'].font.size = Pt(11)

    from docx.oxml.ns import qn
    style()

    # 解析成 HTML
    html = markdown.markdown(md_text, extensions=['extra', 'codehilite', 'toc'])
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    def add_para(text, style=None, bold=False, italic=False):
        p = doc.add_paragraph(style=style)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        return p

    for tag in soup:
        if tag.name == 'h1':
            doc.add_heading(tag.get_text(), level=1)
        elif tag.name == 'h2':
            doc.add_heading(tag.get_text(), level=2)
        elif tag.name == 'h3':
            doc.add_heading(tag.get_text(), level=3)
        elif tag.name in ('h4', 'h5', 'h6'):
            doc.add_heading(tag.get_text(), level=4)
        elif tag.name == 'p':
            # 简单处理行内 ** ** * *
            txt = tag.get_text()
            if '**' not in txt and '*' not in txt:
                add_para(txt)
            else:
                p = doc.add_paragraph()
                parts = re.split(r'(\*\*.*?\*\*|\*[^*]*\*)', txt)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        p.add_run(part[2:-2]).bold = True
                    elif part.startswith('*') and part.endswith('*'):
                        p.add_run(part[1:-1]).italic = True
                    else:
                        p.add_run(part)
        elif tag.name == 'ul':
            for li in tag.find_all('li', recursive=False):
                add_para(li.get_text(), style='List Bullet')
        elif tag.name == 'ol':
            for li in tag.find_all('li', recursive=False):
                add_para(li.get_text(), style='List Number')
        elif tag.name == 'blockquote':
            p = add_para(tag.get_text())
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.left_indent = Cm(0.8)
            p.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        elif tag.name == 'pre':
            # 代码块
            p = add_para(tag.get_text())
            p.runs[0].font.name = 'Consolas'
            shading = parse_xml(r'<w:shd {} w:fill="F5F5F5"/>'.format(nsdecls('w')))
            p.paragraph_format.element.get_or_add_pPr().append(shading)
        elif tag.name == 'table':
            # 简单表格
            rows = tag.find_all('tr')
            if not rows:
                continue
            cols = len(rows[0].find_all('th') or rows[0].find_all('td'))
            table = doc.add_table(rows=1, cols=cols)
            table.style = 'Table Grid'
            hdr_cells = table.rows[0].cells
            for i, th in enumerate(rows[0].find_all('th')):
                hdr_cells[i].text = th.get_text()
            for tr in rows[1:]:
                row_cells = table.add_row().cells
                for i, td in enumerate(tr.find_all('td')):
                    row_cells[i].text = td.get_text()
        elif tag.name == 'img':
            # 网络图片直接下载嵌入
            src = tag.get('src')
            if src and src.startswith('http'):
                try:
                    from docx.shared import Cm
                    response = st.session_state.get('__img_resp', None)
                    if response is None:
                        import requests
                        response = requests.get(src, timeout=10)
                        st.session_state['__img_resp'] = response
                    img_io = io.BytesIO(response.content)
                    doc.add_picture(img_io, width=Cm(12))
                except Exception as e:
                    st.warning(f"图片插入失败：{e}")
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# 页面逻辑
uploaded = st.file_uploader("1. 选择 Markdown 文件", type=['md'])
if uploaded is not None:
    md_text = uploaded.read().decode('utf-8')
    with st.expander("2. 预览 Markdown 内容"):
        st.code(md_text, language='markdown')

    if st.button("3. 生成 Word 文件"):
        with st.spinner("正在转换..."):
            docx_buffer = md2docx_bytes(md_text)
        st.success("转换完成！")
        st.download_button(
            label="⬇️ 下载 converted.docx",
            data=docx_buffer,
            file_name=uploaded.name.replace('.md', '.docx'),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )