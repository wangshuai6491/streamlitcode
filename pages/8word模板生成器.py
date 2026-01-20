import streamlit as st
from docx import Document
import os
import re
import json
import pandas as pd
from io import BytesIO
import tempfile
import zipfile

# 解析word模板变量的函数
def analyze_template(template_path):
    """
    分析Word模板，提取所有占位符信息
    
    :param template_path: Word模板文件路径(.docx格式)
    :return: 包含普通变量和表格信息的字典
    """
    # 加载Word模板
    doc = Document(template_path)
    
    # 正则表达式匹配占位符 {xxx}
    placeholder_pattern = re.compile(r'{([^{}]*)}')
    all_placeholders = set()
    
    # 遍历所有段落，提取占位符
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            matches = placeholder_pattern.findall(run.text)
            for match in matches:
                all_placeholders.add(f"{{{match}}}")
    
    # 遍历所有表格，提取占位符
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                matches = placeholder_pattern.findall(cell.text)
                for match in matches:
                    all_placeholders.add(f"{{{match}}}")
    
    # 分类占位符：普通变量和表格变量
    normal_placeholders = []
    table_info = {}
    
    for ph in all_placeholders:
        ph_content = ph[1:-1]  # 去掉 {} 括号
        if ph_content.startswith("table."):
            # 分割表格占位符：table.表格名.列名
            parts = ph_content.split(".")
            if len(parts) == 3:
                table_name = parts[1]
                column_name = parts[2]
                
                # 添加到表格信息字典
                if table_name not in table_info:
                    table_info[table_name] = {
                        "columns": set(),
                        "placeholders": []
                    }
                table_info[table_name]["columns"].add(column_name)
                table_info[table_name]["placeholders"].append(ph)
        else:
            normal_placeholders.append(ph)
    
    # 转换columns集合为列表，方便使用
    for table_name in table_info:
        table_info[table_name]["columns"] = sorted(list(table_info[table_name]["columns"]))
    
    return {
        "normal_placeholders": sorted(normal_placeholders),
        "table_info": table_info
    }

# 生成word的主要函数
def generate_contract_doc(template_path, data, doc_index=1):
    """
    基于Word模板生成文档
    
    :param template_path: Word模板文件路径(.docx格式)
    :param data: 文档数据，字典格式，包含text_data和tables_data
    :param doc_index: 文档序号，用于生成文件名
    
    :return: 生成的文档对象和文件名
    """
    # 加载Word模板
    doc = Document(template_path)

    # 分析模板，获取占位符信息
    template_analysis = analyze_template(template_path)
    
    # ========== 核心功能1：替换所有【普通文本占位符】 {xxx} ==========
    # 遍历文档中所有段落，替换文本占位符
    for paragraph in doc.paragraphs:
        # 遍历段落中的所有文本块，避免替换格式丢失
        for run in paragraph.runs:
            for placeholder, value in data["text_data"].items():
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)

    # ========== 核心功能2：动态填充【表格】并插入多行 ==========
    # 遍历所有表格，处理包含table.xxx.xxx格式占位符的表格
    for table in doc.tables:
        # 检查表格是否包含模板行（包含table.xxx.xxx占位符）
        template_row = None
        table_name_in_row = None
        
        for row_idx, row in enumerate(table.rows):
            row_text = " ".join([cell.text for cell in row.cells])
            if "{table." in row_text:
                # 提取表格名称
                matches = re.findall(r'{table\.([^\.}]+)\.', row_text)
                if matches:
                    table_name_in_row = matches[0]
                    template_row = row
                    break
        
        if template_row and table_name_in_row:
            # 检查是否有对应的数据
            if table_name_in_row not in data.get("tables_data", {}):
                st.warning(f"表格 {table_name_in_row} 没有对应的数据，跳过该表格")
                continue
            
            # 获取表格数据
            table_data = data["tables_data"][table_name_in_row]
            
            # 获取模板行中各占位符的位置映射
            placeholder_positions = {}
            template_cells = template_row.cells
            for i, cell in enumerate(template_cells):
                cell_text = cell.text.strip()
                if cell_text.startswith("{table.") and cell_text.endswith("}"):
                    placeholder_positions[cell_text] = i
            
            # 遍历表格数据，逐行插入
            for index, row_data in enumerate(table_data):
                if index == 0:
                    # 第一行数据：直接使用模板行
                    row = template_row.cells
                    # 保存第一行的单元格作为格式模板
                    format_template_cells = template_row.cells
                else:
                    # 第2-N行数据：在模板行下方新增一行
                    new_row = table.add_row()
                    row = new_row.cells
                    
                    # 复制第一行的格式到新行
                    # 复制行属性
                    new_row.height = template_row.height
                    
                    # 复制每个单元格的格式
                    for i, (new_cell, template_cell) in enumerate(zip(row, format_template_cells)):
                        # 复制单元格宽度
                        new_cell.width = template_cell.width
                        
                        # 复制段落格式
                        for new_paragraph, template_paragraph in zip(new_cell.paragraphs, template_cell.paragraphs):
                            # 复制段落对齐方式
                            new_paragraph.alignment = template_paragraph.alignment
                            
                            # 复制段落样式
                            if template_paragraph.style:
                                new_paragraph.style = template_paragraph.style
                            
                            # 复制段落中的运行元素格式
                            for new_run, template_run in zip(new_paragraph.runs, template_paragraph.runs):
                                # 复制字体格式
                                new_run.font.name = template_run.font.name
                                new_run.font.size = template_run.font.size
                                new_run.font.bold = template_run.font.bold
                                new_run.font.italic = template_run.font.italic
                                new_run.font.underline = template_run.font.underline
                                if template_run.font.color.rgb:
                                    new_run.font.color.rgb = template_run.font.color.rgb
                                
                                # 复制其他字体属性
                                new_run.font.superscript = template_run.font.superscript
                                new_run.font.subscript = template_run.font.subscript
                                new_run.font.shadow = template_run.font.shadow
                                new_run.font.strike = template_run.font.strike
                                new_run.font.double_strike = template_run.font.double_strike
                
                # 给当前行的每个单元格赋值
                for placeholder, pos in placeholder_positions.items():
                    ph_content = placeholder[1:-1]  # 去掉 {} 括号
                    # 分割占位符：table.表格名.列名
                    parts = ph_content.split(".")
                    if len(parts) == 3:
                        column_name = parts[2]
                        
                        if column_name == "序号":
                            row[pos].text = str(index + 1)  # 序号从1开始
                        elif column_name in row_data:
                            row[pos].text = str(row_data[column_name])
                        else:
                            # 如果数据中没有该列，留空或使用默认值
                            row[pos].text = ""

    # 提取提供的数据中有没有文件名
    if "{文件名}" in data.get("text_data", {}):
        file_name = data["text_data"]["{文件名}"]
        if not file_name.endswith(".docx"):
            file_name += ".docx"
    # 没有则按顺序号命名
    else:
        file_name = f"{doc_index}.docx"
    
    # 保存到BytesIO对象
    doc_stream = BytesIO()
    doc.save(doc_stream)
    doc_stream.seek(0)
    
    return doc_stream, file_name

# 侧边栏下载模板的函数
def cebianlan():
    # 模板下载
    st.sidebar.subheader("模板下载")
    # 使用相对路径，相对于应用运行目录
    template_file_path = os.path.join("static", "word批量生成模板.zip")
    if os.path.exists(template_file_path):
        with open(template_file_path, "rb") as f:
            st.sidebar.download_button(
                label="下载示例模板",
                data=f,
                file_name="word批量生成模板.zip",
                mime="application/zip"
            )
    else:
        st.sidebar.warning(f"示例模板文件不存在，路径：{template_file_path}")


# 展示模板占位符信息
def display_template_info(uploaded_template, tmp_path):
    """
    显示Word模板中的占位符信息
    
    :param uploaded_template: 上传的Word模板文件对象
    :param tmp_path: 临时文件路径
    """
    if uploaded_template and tmp_path:
        # 分析模板，显示占位符信息
        try:
            template_info = analyze_template(tmp_path)
            
            with st.expander("📋 已解析占位符信息", expanded=True):
                # 显示普通变量
                st.subheader("📝 普通变量")
                if template_info["normal_placeholders"]:
                    # 将所有普通变量拼接成一个字符串，每个占一行
                    normal_vars_text = "\n".join(template_info["normal_placeholders"])
                    st.code(normal_vars_text, language="plaintext")
                else:
                    st.info("无普通变量")
                
                # 显示表格变量
                st.subheader("📊 表格变量")
                if template_info["table_info"]:
                    # 构建表格变量文本，按表格分组，每个占一行
                    table_vars_lines = []
                    for table_name, info in template_info["table_info"].items():
                        table_vars_lines.append(f"=== {table_name} ===")
                        table_vars_lines.extend(info["placeholders"])
                        table_vars_lines.append("")  # 表格之间空一行
                    # 移除最后一个空行
                    if table_vars_lines and table_vars_lines[-1] == "":
                        table_vars_lines.pop()
                    # 拼接成一个字符串
                    table_vars_text = "\n".join(table_vars_lines)
                    st.code(table_vars_text, language="plaintext")
                else:
                    st.info("无表格变量")
        except Exception as e:
            st.error(f"模板分析失败：{e}")

# 只有普通变量的数据解析函数，最终处理为json
def only_normal_vars():
    """
    处理只有普通变量的情况：用户上传Excel后，选择表格，以A1单元格为基础读取连续区域的内容并解析为JSON格式
    """
    # 上传Excel文件
    uploaded_excel = st.file_uploader("上传Excel文件（仅含普通变量）", type=["xlsx", "xls"], key="only_normal_vars_excel")
    
    if uploaded_excel:
        try:
            # 读取Excel文件
            excel_data = pd.ExcelFile(uploaded_excel)
            
            # 让用户选择表格（工作表）
            selected_sheet = st.selectbox(
                "选择工作表",
                excel_data.sheet_names,
                key="only_normal_vars_sheet"
            )
            
            # 读取选中工作表的所有数据
            df = excel_data.parse(selected_sheet, header=0)  # 明确指定第一行为表头
            
            # 以A1为基础，读取连续区域的内容
            # 连续区域：从A1开始，向右直到最后一个有数据的列，向下直到最后一个有数据的行
            # 找到最后一个有数据的行和列
            # 方法：去掉全为空的行和列
            df_clean = df.dropna(how='all').dropna(axis=1, how='all')
            
            # 显示连续区域的范围
            if not df_clean.empty:
                last_row = df_clean.shape[0]
                last_col = df_clean.shape[1]
                # 转换为Excel列名（例如：1->A, 2->B, ...）
                last_col_name = chr(ord('A') + last_col - 1)
                st.info(f"检测到连续数据区域：A1:{last_col_name}{last_row+1}（含表头）")
                
                # 显示处理后的数据
                st.subheader("连续数据区域")
                st.dataframe(df_clean)
                
                # 解析为JSON格式
                if st.button("解析普通变量数据", key="parse_normal_vars"):
                    try:
                        # 确保列名是字符串类型
                        df_clean.columns = df_clean.columns.astype(str)
                        
                        # 假设第一行为列名，从第二行开始为数据
                        # 列名对应占位符名称（例如："户主姓名" -> "{户主姓名}"）
                        # 每一行对应一个word的数据
                        all_family_data = []
                        
                        # 遍历每一行数据
                        for index, row in df_clean.iterrows():
                            family_data = {
                                "text_data": {},
                                "tables_data": {}
                            }
                            
                            # 将每一列转换为占位符
                            for col_name, value in row.items():
                                # 跳过空值
                                if pd.notna(value) and value != "" and str(value).strip() != "":
                                    # 转换为占位符格式（例如："姓名" -> "{姓名}"）
                                    placeholder = f"{{{col_name.strip()}}}"
                                    family_data["text_data"][placeholder] = str(value).strip()
                            
                            # 只有当text_data不为空时才添加
                            if family_data["text_data"]:
                                all_family_data.append(family_data)
                        
                        # 保存到session state
                        st.session_state.all_family_data = all_family_data
                        st.success(f"成功解析 {len(all_family_data)} 条普通变量数据")
                        
                        # 显示解析后的数据结构
                        with st.expander("查看解析后的数据结构", expanded=False):
                            st.json(all_family_data)
                        
                        # 显示调试信息
                        st.write(f"已存入session_state.all_family_data，数据条数：{len(all_family_data)}")
                        
                    except Exception as e:
                        st.error(f"数据解析失败：{e}")
                        import traceback
                        st.code(traceback.format_exc())
            else:
                st.warning("未检测到有效数据，请检查Excel文件")
        
        except Exception as e:
            st.error(f"Excel读取失败：{e}")
            import traceback
            st.code(traceback.format_exc())

# -------------------------- Streamlit应用 --------------------------
if __name__ == "__main__":
    # 设置页面标题和布局
    st.set_page_config(page_title="Word模板批量生成", layout="wide")
    
    # 主标题（使用markdown格式）
    st.markdown("### Word模板批量生成")
    
    # 调用模板函数
    cebianlan()
    
    # 初始化session state
    if 'all_family_data' not in st.session_state:
        st.session_state.all_family_data = []
    if 'uploaded_template' not in st.session_state:
        st.session_state.uploaded_template = None
    if 'tmp_path' not in st.session_state:
        st.session_state.tmp_path = None
    if 'template_file_name' not in st.session_state:
        st.session_state.template_file_name = None
    if 'generate_documents' not in st.session_state:
        st.session_state.generate_documents = False
    
    # 初始化局部变量
    uploaded_template = st.session_state.uploaded_template
    tmp_path = st.session_state.tmp_path
    template_file_name = st.session_state.template_file_name
    
    # Word模板上传（使用session_state保存模板信息）
    st.subheader("📄 Word模板上传")
    new_uploaded_template = st.file_uploader("请上传Word模板文件(.docx)", type="docx")
    
    # 检查是否上传了新模板
    if new_uploaded_template:
        # 上传新模板时清除之前的数据
        st.session_state.all_family_data = []
        
        # 保存上传的模板到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(new_uploaded_template.getvalue())
            tmp_path = tmp.name
        
        template_file_name = new_uploaded_template.name
        
        # 更新session state和局部变量
        st.session_state.uploaded_template = uploaded_template = new_uploaded_template
        st.session_state.tmp_path = tmp_path
        st.session_state.template_file_name = template_file_name
        
        # 在侧边栏显示模板信息
        with st.sidebar:
            display_template_info(new_uploaded_template, tmp_path)
    
    # 主内容区只显示数据输入部分
    st.markdown("### 📊 数据输入")
    # 数据输入方式选择
    input_tab1, input_tab2, input_tab3 = st.tabs(["只有普通变量","按基础变量和表格变量生成word","JSON格式"])

    # 只有普通变量（一个sheet表生成一个word）
    with input_tab1:
        only_normal_vars()
    # Excel输入方式（基础变量+表格变量）
    with input_tab2:
        pass
    
    # JSON输入方式
    with input_tab3:
        # JSON输入框
        json_input = st.text_area("输入JSON数据（支持多个家庭，用数组包裹）", height=150, placeholder='例如：[{"text_data": {...}, "tables_data": {...}}]')
        
        if st.button("解析JSON数据"):
            try:
                st.session_state.all_family_data = json.loads(json_input)
                # 确保是数组格式
                if not isinstance(st.session_state.all_family_data, list):
                    st.session_state.all_family_data = [st.session_state.all_family_data]
                st.success(f"成功解析 {len(st.session_state.all_family_data)} 条数据")
            except json.JSONDecodeError as e:
                st.error(f"JSON解析失败：{e}")
        
    # 批量生成文档按钮
    st.write("---")
    
    # 添加调试信息，展示session_state数据
    with st.expander("调试信息（点击展开）", expanded=False):
        st.write(f"uploaded_template是否存在: {uploaded_template is not None}")
        st.write(f"tmp_path是否存在: {tmp_path is not None}")
        st.write(f"all_family_data是否存在: {st.session_state.get('all_family_data') is not None}")
        if st.session_state.get('all_family_data'):
            st.write(f"all_family_data长度: {len(st.session_state.get('all_family_data'))}")
            if len(st.session_state.get('all_family_data')) > 0:
                st.write(f"第一条数据内容: {st.session_state.get('all_family_data')[0]}")
        st.write(f"session_state中的键: {list(st.session_state.keys())}")
    
    # 判断按钮是否禁用
    disabled = False
    disable_reason = ""
    if not uploaded_template:
        disabled = True
        disable_reason = "没有上传Word模板"
    elif not st.session_state.get("all_family_data") or len(st.session_state.get("all_family_data")) == 0:
        disabled = True
        disable_reason = "没有解析到有效数据"
    elif not tmp_path or not os.path.exists(tmp_path):
        disabled = True
        disable_reason = "模板临时文件不存在"
    
    st.info(f"按钮状态：{'禁用' if disabled else '启用'} - {disable_reason if disabled else '所有条件都满足'}")
    
    # 批量生成文档按钮
    if st.button("批量生成文档", 
                disabled=disabled, 
                type="primary",
                use_container_width=True):
        st.session_state.generate_documents = True
    
    # 生成文档逻辑
    if st.session_state.generate_documents:
        if st.session_state.get("all_family_data") and uploaded_template and tmp_path and os.path.exists(tmp_path):
            st.write("🚀 开始生成文档...")
            
            # 创建生成的文档列表
            generated_docs = []
            
            # 创建一个固定高度的容器，用于显示滚动消息
            with st.container(height=200, border=True):
                for index, family in enumerate(st.session_state.all_family_data, start=1):
                    try:
                        doc_stream, file_name = generate_contract_doc(tmp_path, family, doc_index=index)
                        generated_docs.append((doc_stream, file_name))
                        st.success(f"✅ {file_name} 生成成功")
                    except Exception as e:
                        st.error(f"❌ 生成 {index} 号文档失败：{e}")
                        import traceback
                        st.code(traceback.format_exc())
            
            # 提供下载链接
            if generated_docs:
                st.write("---")
                st.subheader("下载生成的文档")
                
                # 创建ZIP文件
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for doc_stream, file_name in generated_docs:
                        # 将文档流写入ZIP文件
                        zip_file.writestr(file_name, doc_stream.getvalue())
                zip_buffer.seek(0)
                
                # 提供ZIP下载
                st.download_button(
                    label=f"📦 批量下载所有文档 ({len(generated_docs)}个)",
                    data=zip_buffer,
                    file_name="批量生成文档.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                
                # 保留单个文件下载选项
                st.markdown("<div style='margin-top: 20px; font-size: 14px; color: #666;'>或单独下载：</div>", unsafe_allow_html=True)
                for doc_stream, file_name in generated_docs:
                    st.download_button(
                        label=f"下载 {file_name}",
                        data=doc_stream,
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
        
        # 重置生成标志
        st.session_state.generate_documents = False
    
    # 最后删除临时文件（在应用结束时）
    def cleanup_temp_files():
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
                st.sidebar.success("临时文件已清理")
            except:
                pass
    
    # 在侧边栏添加清理按钮（可选）
    with st.sidebar:
        st.write("---")
        if st.button("清理临时文件"):
            cleanup_temp_files()