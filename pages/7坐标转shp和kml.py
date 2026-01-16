import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import tempfile
import os
import zipfile
import simplekml
import numpy as np

# ---------------------- 全局变量和配置 ----------------------
crs_mapping = {
    "China Geodetic Coordinate System 2000": "EPSG:4490",
    "World Geodetic System 1984": "EPSG:4326",
    "Beijing 1954": "EPSG:4214",
    "Xian 1980": "EPSG:4610",
    # CGCS2000 3度分带高斯克里格投影
    "CGCS2000 3 Degree GK Zone 36": "EPSG:4524",
    "CGCS2000 3 Degree GK Zone 37": "EPSG:4525",
    "CGCS2000 3 Degree GK Zone 38": "EPSG:4526",
    "CGCS2000 3 Degree GK Zone 25": "EPSG:4513",
    "CGCS2000 3 Degree GK Zone 26": "EPSG:4514",
    "CGCS2000 3 Degree GK Zone 27": "EPSG:4515",
    "CGCS2000 3 Degree GK Zone 28": "EPSG:4516",
    "CGCS2000 3 Degree GK Zone 29": "EPSG:4517",
    "CGCS2000 3 Degree GK Zone 30": "EPSG:4518",
    "CGCS2000 3 Degree GK Zone 31": "EPSG:4519",
    "CGCS2000 3 Degree GK Zone 32": "EPSG:4520",
    "CGCS2000 3 Degree GK Zone 33": "EPSG:4521",
    "CGCS2000 3 Degree GK Zone 34": "EPSG:4522",
    "CGCS2000 3 Degree GK Zone 35": "EPSG:4523",
    "CGCS2000 3 Degree GK Zone 39": "EPSG:4527",
    "CGCS2000 3 Degree GK Zone 40": "EPSG:4528",
    "CGCS2000 3 Degree GK Zone 41": "EPSG:4529",
    "CGCS2000 3 Degree GK Zone 42": "EPSG:4530",
    "CGCS2000 3 Degree GK Zone 43": "EPSG:4531",
    "CGCS2000 3 Degree GK Zone 44": "EPSG:4532",
    "CGCS2000 3 Degree GK Zone 45": "EPSG:4533",
}

# ---------------------- 工具函数 ----------------------

# 检查整数位数
def check_integer_digits(value):
    if pd.isna(value):
        return 0
    integer_part = int(abs(value))
    return len(str(integer_part))

# 将十六进制颜色转换为KML颜色格式（KML使用aabbggrr格式）
def hex_to_kml_color(hex_color, opacity=1.0):
    # 移除#号
    hex_color = hex_color.lstrip('#')
    # 将RGB转换为BGR
    bgr = hex_color[4:6] + hex_color[2:4] + hex_color[0:2]
    # 计算alpha值（00-ff）
    alpha = format(int(opacity * 255), '02x')
    # 返回aabbggrr格式
    return alpha + bgr

# 验证和预处理数据
def validate_and_preprocess(data, coord_type):
    if data.empty:
        return None, "⚠️ 暂无数据，请先添加坐标"
    if coord_type.startswith("经纬"):
        data_clean = data.copy()
        data_clean["X"] = pd.to_numeric(data_clean["X"], errors="coerce").round(6)
        data_clean["Y"] = pd.to_numeric(data_clean["Y"], errors="coerce").round(6)
        invalid_mask = (data_clean["X"].isnull() | data_clean["Y"].isnull() | (data_clean["X"] < -180) | (data_clean["X"] > 180) | (data_clean["Y"] < -90) | (data_clean["Y"] > 90))
    else:
        data_clean = data.copy()
        data_clean["X"] = pd.to_numeric(data_clean["X"], errors="coerce").round(2)
        data_clean["Y"] = pd.to_numeric(data_clean["Y"], errors="coerce").round(2)
        
        # 基本有效性检查
        invalid_mask = data_clean["X"].isnull() | data_clean["Y"].isnull()
        
        # 平面坐标整数位数检查
        # X坐标整数位数必须是6位或8位
        x_digits_mask = data_clean["X"].apply(check_integer_digits).apply(lambda x: x not in [6, 8])
        
        # Y坐标整数位数必须是7位
        y_digits_mask = data_clean["Y"].apply(check_integer_digits).apply(lambda x: x != 7)
        
        # 合并所有无效条件
        invalid_mask = invalid_mask | x_digits_mask | y_digits_mask
        
        if x_digits_mask.any():
            invalid_x_count = x_digits_mask.sum()
            st.warning(f"❌ 过滤{invalid_x_count}行X坐标无效数据（X坐标整数位数必须是6位或8位）")
        
        if y_digits_mask.any():
            invalid_y_count = y_digits_mask.sum()
            st.warning(f"❌ 过滤{invalid_y_count}行Y坐标无效数据（Y坐标整数位数必须是7位）")
    
    if invalid_mask.any():
        total_invalid = invalid_mask.sum()
        st.warning(f"❌ 共过滤{total_invalid}行无效数据")
        data_clean = data_clean[~invalid_mask].reset_index(drop=True)
    return data_clean, "✅ 数据校验完成，可导出文件"

# 导出SHP文件
def export_shp(data, feature_types):
    crs = st.session_state.selected_crs
    selected_crs_name = st.session_state.selected_crs_name
    st.info(f"正在导出SHP文件，使用坐标系: {selected_crs_name} ({crs})")
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "data_shp.zip")
        coords = list(zip(data["X"], data["Y"]))
        with zipfile.ZipFile(zip_path, "w") as zipf:
            if "点" in feature_types:
                gdf_points = gpd.GeoDataFrame(data, geometry=[Point(xy) for xy in coords], crs=crs)
                shp_path_points = os.path.join(tmp_dir, "points.shp")
                gdf_points.to_file(shp_path_points, driver="ESRI Shapefile", encoding="utf-8")
                for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                    file = f"points{ext}"
                    if os.path.exists(os.path.join(tmp_dir, file)):
                        zipf.write(os.path.join(tmp_dir, file), file)
            if "线" in feature_types:
                gdf_line = gpd.GeoDataFrame([{}], geometry=[LineString(coords)], crs=crs)
                shp_path_line = os.path.join(tmp_dir, "line.shp")
                gdf_line.to_file(shp_path_line, driver="ESRI Shapefile", encoding="utf-8")
                for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                    file = f"line{ext}"
                    if os.path.exists(os.path.join(tmp_dir, file)):
                        zipf.write(os.path.join(tmp_dir, file), file)
            if "面" in feature_types:
                gdf_polygon = gpd.GeoDataFrame([{}], geometry=[Polygon(coords)], crs=crs)
                shp_path_polygon = os.path.join(tmp_dir, "polygon.shp")
                gdf_polygon.to_file(shp_path_polygon, driver="ESRI Shapefile", encoding="utf-8")
                for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                    file = f"polygon{ext}"
                    if os.path.exists(os.path.join(tmp_dir, file)):
                        zipf.write(os.path.join(tmp_dir, file), file)
        with open(zip_path, "rb") as f:
            shp_zip_data = f.read()
    return shp_zip_data

# 导出KML文件
def export_kml(data, feature_types, point_color, line_color, line_width, polygon_outline_color, polygon_fill_color, polygon_fill_opacity, polygon_outline_width):
    kml = simplekml.Kml()
    # 获取当前坐标系和WGS84坐标系
    current_crs = st.session_state.selected_crs
    wgs84_crs = "EPSG:4326"
    
    # 显示当前坐标系信息，方便调试
    st.info(f"当前坐标系：{current_crs}，正在转换为KML标准WGS84坐标系（EPSG:4326）")
    
    # 将数据转换为GeoDataFrame，使用当前坐标系
    coords = list(zip(data["X"], data["Y"]))
    # 创建点几何对象
    geometries = [Point(xy) for xy in coords]
    # 创建GeoDataFrame
    gdf = gpd.GeoDataFrame(data, geometry=geometries, crs=current_crs)
    
    # 确保坐标转换正确执行
    try:
        # 将坐标转换为WGS84经纬度坐标系（KML标准坐标系）
        gdf_wgs84 = gdf.to_crs(wgs84_crs)
        st.success(f"坐标转换成功，共处理{len(gdf_wgs84)}个坐标")
        
        # 提取转换后的坐标并过滤无效值
        valid_coords = []
        for geom in gdf_wgs84.geometry:
            lon, lat = geom.x, geom.y
            # 检查坐标是否在KML允许的范围内（经度-180到180，纬度-90到90）
            if (-180 <= lon <= 180) and (-90 <= lat <= 90) and not (pd.isna(lon) or pd.isna(lat)):
                valid_coords.append((lon, lat))
            else:
                st.warning(f"过滤无效坐标：经度={lon}，纬度={lat}（超出范围或为无效值）")
        
        if not valid_coords:
            st.error("❌ 所有坐标转换后均为无效值，请检查输入坐标和所选坐标系是否匹配")
            return None
        
        st.success(f"有效坐标数量：{len(valid_coords)}个")
        
        # 显示转换前后的坐标示例，方便调试
        if len(valid_coords) > 0:
            st.info(f"转换前示例坐标：{coords[0]}，转换后示例坐标：{valid_coords[0]}")
        
        # 生成点
        if "点" in feature_types:
            for i, (lon, lat) in enumerate(valid_coords, 1):
                point = kml.newpoint(name=f"点{i}", coords=[(lon, lat)])
                # 设置点样式
                point.style.iconstyle.color = hex_to_kml_color(point_color)
                point.style.iconstyle.scale = 1.0  # 点大小
        
        # 生成线
        if "线" in feature_types:
            line = kml.newlinestring(name="线要素", coords=valid_coords)
            # 设置线样式
            line.style.linestyle.color = hex_to_kml_color(line_color)
            line.style.linestyle.width = line_width
        
        # 生成面（闭合）
        if "面" in feature_types:
            polygon = kml.newpolygon(name="面要素", outerboundaryis=valid_coords)
            # 设置面样式
            # 边框样式
            polygon.style.linestyle.color = hex_to_kml_color(polygon_outline_color)
            polygon.style.linestyle.width = polygon_outline_width
            # 填充样式
            polygon.style.polystyle.color = hex_to_kml_color(polygon_fill_color, polygon_fill_opacity)
        
        # 保存KML到临时文件，读取二进制数据
        tmp_path = tempfile.mktemp(suffix=".kml")
        kml.save(tmp_path)
        with open(tmp_path, "rb") as f:
            kml_data = f.read()
        os.unlink(tmp_path)  # 删除临时文件
        return kml_data
    except Exception as e:
        st.error(f"坐标转换失败：{str(e)}")
        # 显示更详细的错误信息，帮助调试
        st.error(f"错误详情：{type(e).__name__}: {e}")
        return None

def zuobiaoxi():
    # 坐标类型选择
    col1, col2, col3 = st.columns(3)
    # 选类型
    with col1:
        coord_type = st.radio(
            "🔍 选择坐标类型",
            options=["经纬度", "平面直角坐标"],
            index=1,
            horizontal=True,
            help="经纬度：如WGS84、CGCS2000等全球坐标系；平面坐标：如高斯克里格投影坐标"
        )
    
    # 坐标系选择
    with col2:
        if coord_type == "经纬度":
            lonlat_options = [crs for crs in crs_mapping.keys() if "Geodetic" in crs or "System" in crs or "1954" in crs or "1980" in crs]
            selected_crs_name = st.selectbox("📍 选择经纬度坐标系", options=lonlat_options, index=lonlat_options.index("China Geodetic Coordinate System 2000"), help="选择对应的地理坐标系", key="lonlat_crs_select")
        else:
            plane_options = [crs for crs in crs_mapping.keys() if "GK" in crs]
            selected_crs_name = st.selectbox("📍 选择平面坐标系", options=plane_options, index=plane_options.index("CGCS2000 3 Degree GK Zone 37"), help="选择对应的投影坐标系", key="plane_crs_select")
    
    selected_crs = crs_mapping[selected_crs_name]
    if "selected_crs" not in st.session_state:
        st.session_state.selected_crs = selected_crs
        st.session_state.selected_crs_name = selected_crs_name
    if selected_crs != st.session_state.selected_crs:
        st.session_state.selected_crs = selected_crs
        st.session_state.selected_crs_name = selected_crs_name
    
    # 数据验证
    if st.session_state.data.empty:
        clean_data, msg = None, ""
    else:
        clean_data, msg = validate_and_preprocess(st.session_state.data, coord_type)
    
    # 存储到session_state供其他地方使用
    st.session_state.clean_data = clean_data
    
    # 第3列：消息框，使用占位符方式显示
    with col3:
        message_placeholder = st.empty()
        messages = []
        # 添加坐标系选择消息
        coord_msg = f"当前选择的坐标系：{selected_crs_name} ({selected_crs})"
        messages.append(coord_msg)
        # 添加数据验证消息
        if msg:
            messages.append(msg)
        # 如果有消息，显示在占位符中
        if messages:
            message_placeholder.info("\n".join(messages))
        else:
            message_placeholder.empty()

def yangshi():
    # 点样式设置
    st.markdown("### 点样式")
    point_color = st.color_picker("点颜色", value="#FF0000", help="选择点的颜色")
    
    # 线样式设置
    st.markdown("### 线样式")
    line_color = st.color_picker("线条颜色", value="#FF0000", help="选择线的颜色")
    line_width = st.slider("线条宽度", min_value=1, max_value=10, value=5, help="选择线的宽度")
    
    # 面样式设置
    st.markdown("### 面样式")
    polygon_outline_color = st.color_picker("面边框颜色", value="#FF0000", help="选择面的边框颜色")
    polygon_fill_color = st.color_picker("面填充颜色", value="#FF0000", help="选择面的填充颜色")
    polygon_fill_opacity = st.slider("面填充透明度", min_value=0, max_value=100, value=20, step=10, format="%d%%", help="选择面的填充透明度（0% 完全透明，100% 完全不透明）") / 100
    polygon_outline_width = st.slider("面边框宽度", min_value=1, max_value=10, value=5, help="选择面的边框宽度")
    
    # 存储样式设置到session_state
    st.session_state.point_color = point_color
    st.session_state.line_color = line_color
    st.session_state.line_width = line_width
    st.session_state.polygon_outline_color = polygon_outline_color
    st.session_state.polygon_fill_color = polygon_fill_color
    st.session_state.polygon_fill_opacity = polygon_fill_opacity
    st.session_state.polygon_outline_width = polygon_outline_width

def excel_input():
    
    with st.form("data_input_form"):
        edited_df = st.data_editor(st.session_state.data, column_config={
            "X": st.column_config.NumberColumn("经度/X坐标", required=True, format="%.6f", help="经纬度输入-180~180/0~90，平面坐标直接输数字"),
            "Y": st.column_config.NumberColumn("纬度/Y坐标", required=True, format="%.6f")
        }, num_rows="dynamic", use_container_width=True, key="data_editor")

        submitted = st.form_submit_button("💾 表格输入完毕，点击保存")
        if submitted:
            st.session_state.data = edited_df
            st.success("数据已更新！")
            st.rerun()

def wenben():
    with st.form("text_input_form"):
        # 添加XY对调选项
        swap_xy = st.checkbox("🔄 需要对调XY坐标", value=False, help="勾选后将交换X和Y坐标的顺序")
        
        text_input = st.text_area(
            "输入坐标文本",
            placeholder="国土类格式：\nJ1,1,x1,y1\nJ2,1,x2,y2\n每行一组坐标，逗号分隔，格式为：点号,类型,Y坐标,X坐标",
            height=200
        )
        submitted = st.form_submit_button("💾 文本输入完毕，点击保存")
        
        if submitted and text_input.strip():
            try:
                # 解析文本数据
                data = []
                lines = text_input.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            # 格式：点号,类型,Y坐标,X坐标
                            raw_x = float(parts[3])
                            raw_y = float(parts[2])
                            
                            # 根据用户选择处理坐标顺序
                            if swap_xy:
                                x = raw_y
                                y = raw_x
                            else:
                                x = raw_x
                                y = raw_y
                            
                            data.append({"X": x, "Y": y})
                
                if data:
                    st.session_state.data = pd.DataFrame(data, columns=fixed_headers)
                    st.success(f"成功导入 {len(data)} 条坐标数据！")
                    st.rerun()
                else:
                    st.error("❌ 未解析到有效坐标数据，请检查输入格式")
            except Exception as e:
                st.error(f"❌ 解析失败：{str(e)}")
        elif submitted and not text_input.strip():
            st.warning("⚠️ 文本框为空，请输入坐标数据")

def simple_text_input():
    with st.form("simple_text_input_form"):
        # 添加XY对调选项
        swap_xy = st.checkbox("🔄 需要对调XY坐标", value=False, help="勾选后将交换X和Y坐标的顺序")
        
        text_input = st.text_area(
            "输入x1,y1格式坐标",
            placeholder="示例格式：\n37470546.123,3938462.159\n37470591.494,3938465.881\n37470599.307,3938403.289\n每行一组坐标，逗号分隔，格式为：X坐标,Y坐标",
            height=200
        )
        submitted = st.form_submit_button("💾 简单文本输入完毕，点击保存")
        
        if submitted and text_input.strip():
            try:
                # 解析简单文本数据
                data = []
                lines = text_input.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            # 格式：X坐标,Y坐标
                            raw_x = float(parts[0])
                            raw_y = float(parts[1])
                            
                            # 根据用户选择处理坐标顺序
                            if swap_xy:
                                x = raw_y
                                y = raw_x
                            else:
                                x = raw_x
                                y = raw_y
                            
                            data.append({"X": x, "Y": y})
                
                if data:
                    st.session_state.data = pd.DataFrame(data, columns=fixed_headers)
                    st.success(f"成功导入 {len(data)} 条坐标数据！")
                    st.rerun()
                else:
                    st.error("❌ 未解析到有效坐标数据，请检查输入格式")
            except Exception as e:
                st.error(f"❌ 解析失败：{str(e)}")
        elif submitted and not text_input.strip():
            st.warning("⚠️ 文本框为空，请输入坐标数据")


def md_input():
    # 提示用户点击保存后将自动跳转到EXCEL输入页面
    st.info("⚠️ 注意：点击保存后将自动跳转到EXCEL输入页面，并自动处理为数字格式。")
    with st.form("md_input_form"):
        # 添加XY对调选项
        swap_xy = st.checkbox("🔄 需要对调XY坐标", value=False, help="勾选后将交换X和Y坐标的顺序")
        
        text_input = st.text_area(
            "输入Markdown表格坐标",
            placeholder="示例格式：\n| x1 | y1 | \n| x2 | y2 | \n| x3 | y3 |\n表格格式为：| X坐标 | Y坐标 |",
            height=200
        )
        submitted = st.form_submit_button("💾 Markdown输入完毕，点击保存")
        
        if submitted and text_input.strip():
            try:
                # 解析Markdown表格数据
                data = []
                lines = text_input.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.strip().startswith('| ---') and not line.strip().startswith('| --'):
                        # 移除行首尾的|和空格
                        line = line.strip()[1:-1].strip()
                        # 按|分割列
                        parts = [part.strip() for part in line.split('|')]
                        # 过滤掉空字符串
                        parts = [part for part in parts if part]
                        if len(parts) >= 2:
                            # 格式：| X坐标 | Y坐标 |，先移除所有空格
                            raw_x = float(parts[0].replace(' ', ''))
                            raw_y = float(parts[1].replace(' ', ''))
                            
                            # 根据用户选择处理坐标顺序
                            if swap_xy:
                                x = raw_y
                                y = raw_x
                            else:
                                x = raw_x
                                y = raw_y
                            
                            data.append({"X": x, "Y": y})
                
                if data:
                    st.session_state.data = pd.DataFrame(data, columns=fixed_headers)
                    st.success(f"成功导入 {len(data)} 条坐标数据！")
                    st.rerun()
                else:
                    st.error("❌ 未解析到有效坐标数据，请检查输入格式")
            except Exception as e:
                st.error(f"❌ 解析失败：{str(e)}")
        elif submitted and not text_input.strip():
            st.warning("⚠️ 文本框为空，请输入坐标数据")

# ---------------------- 主函数 ----------------------
if __name__ == "__main__":
    st.set_page_config(page_title="坐标转SHP/KML", layout="wide")
    st.title("📊 坐标转SHP/KML")
    
    # 默认测试数据 - 在调用任何函数前先初始化
    fixed_headers = ["X", "Y"]
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame([{"X": 12345678.1234, "Y": 1234567.1234}], columns=fixed_headers)
    
    # ---------------------- 坐标设置TAB ----------------------
    zuobiaoxi()
    # 使用TAB标签组织界面
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["✏️ x1,y1文本输入", "📝 J1,1,x1,y1文本输入", "🖋️ EXCEL输入",  "📋 Markdown表格输入", "🎨 样式设置"])
    # ---------------------- x1,y1文本输入TAB ----------------------
    with tab1:
        simple_text_input()
    # ---------------------- J1,1,x1,y1文本输入TAB ----------------------
    with tab2:
        wenben()
    # ---------------------- EXCEL输入TAB ----------------------
    with tab3:
        excel_input()
    # ---------------------- Markdown输入TAB ----------------------
    with tab4:
        md_input()
    # ---------------------- 样式设置TAB ----------------------
    with tab5:
        yangshi()
    
    # ---------------------- 导出界面 ----------------------
 
    # 导出几何类型选择
    feature_types = st.pills(
        "🔶 选择导出几何类型",
        options=["点", "线", "面"],
        default=["面"],
        selection_mode="multi",
        help="点：每个坐标作为一个点；线：将所有坐标按顺序连接成一条线；面：将所有坐标按顺序连接成一个闭合多边形"
    )
    
    # 导出按钮
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if hasattr(st.session_state, 'clean_data') and st.session_state.clean_data is not None and not st.session_state.clean_data.empty:
            if st.button("📤 生成SHP文件", type="primary"):
                try:
                    shp_zip_data = export_shp(st.session_state.clean_data, feature_types)
                    st.download_button(label="✅ 点击下载SHP文件", data=shp_zip_data, file_name="data_shp.zip", mime="application/zip", key="download_shp")
                except Exception as e:
                    st.error(f"SHP导出失败：{str(e)}")
        else:
            st.button("📤 生成SHP文件", disabled=True, help="请先添加有效坐标数据")
    
    with btn_col2:
        if hasattr(st.session_state, 'clean_data') and st.session_state.clean_data is not None and not st.session_state.clean_data.empty:
            if st.button("📤 生成KML文件", type="primary"):
                try:
                    # 确保所有样式变量都在session_state中
                    style_vars = ['point_color', 'line_color', 'line_width', 
                                    'polygon_outline_color', 'polygon_fill_color', 
                                    'polygon_fill_opacity', 'polygon_outline_width']
                    
                    # 设置默认值以防样式设置还未执行
                    for var in style_vars:
                        if var not in st.session_state:
                            if 'color' in var:
                                st.session_state[var] = '#FF0000'
                            elif 'width' in var:
                                st.session_state[var] = 5
                            elif 'opacity' in var:
                                st.session_state[var] = 0.2
                    
                    kml_data = export_kml(
                        st.session_state.clean_data, 
                        feature_types, 
                        st.session_state.point_color, 
                        st.session_state.line_color, 
                        st.session_state.line_width, 
                        st.session_state.polygon_outline_color, 
                        st.session_state.polygon_fill_color, 
                        st.session_state.polygon_fill_opacity, 
                        st.session_state.polygon_outline_width
                    )
                    if kml_data is not None:
                        st.download_button(label="✅ 点击下载KML文件", data=kml_data, file_name="data_kml.kml", mime="application/vnd.google-earth.kml+xml", key="download_kml")
                except Exception as e:
                    st.error(f"KML导出失败：{str(e)}")
        else:
            st.button("📤 生成KML文件", disabled=True, help="请先添加有效坐标数据")

