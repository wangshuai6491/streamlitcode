import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import tempfile
import os
import zipfile

def main():
    # 页面配置
    st.set_page_config(page_title="坐标转shp", layout="wide")
    st.title("📊 坐标转shp")
    
    # ---------------------- 1. 坐标类型选择+表头配置 ----------------------
    # 使用两列布局放置坐标类型选择和坐标系选择控件
    col1, col2 = st.columns(2)
    
    # 左侧列：坐标类型选择（兼容经纬度平面坐标）
    with col1:
        coord_type = st.radio(
            "🔍 选择坐标类型",
            options=["经纬度", "平面直角坐标"],
            index=1,
            horizontal=True,
            help="经纬度：如WGS84、CGCS2000等全球坐标系；平面坐标：如高斯克里格投影坐标"
        )
    
    # 坐标系映射字典
    crs_mapping = {
        # 经纬度坐标系
        "China Geodetic Coordinate System 2000": "EPSG:4490",
        "World Geodetic System 1984": "EPSG:4326",
        "Beijing 1954": "EPSG:4214",
        "Xian 1980": "EPSG:4610",
        # 平面坐标（3度带，CM格式，我国常用范围：75E-135E，间隔3度）
        "CGCS2000 3 Degree GK CM 75E": "EPSG:4534",  # 75度经线
        "CGCS2000 3 Degree GK CM 78E": "EPSG:4535",  # 78度经线
        "CGCS2000 3 Degree GK CM 81E": "EPSG:4536",  # 81度经线
        "CGCS2000 3 Degree GK CM 84E": "EPSG:4537",  # 84度经线
        "CGCS2000 3 Degree GK CM 87E": "EPSG:4538",  # 87度经线
        "CGCS2000 3 Degree GK CM 90E": "EPSG:4539",  # 90度经线
        "CGCS2000 3 Degree GK CM 93E": "EPSG:4540",  # 93度经线
        "CGCS2000 3 Degree GK CM 96E": "EPSG:4541",  # 96度经线
        "CGCS2000 3 Degree GK CM 99E": "EPSG:4542",  # 99度经线
        "CGCS2000 3 Degree GK CM 102E": "EPSG:4543",  # 102度经线
        "CGCS2000 3 Degree GK CM 105E": "EPSG:4544",  # 105度经线
        "CGCS2000 3 Degree GK CM 108E": "EPSG:4545",  # 108度经线
        "CGCS2000 3 Degree GK CM 111E": "EPSG:4546",  # 111度经线
        "CGCS2000 3 Degree GK CM 114E": "EPSG:4547",  # 114度经线
        "CGCS2000 3 Degree GK CM 117E": "EPSG:4548",  # 117度经线
        "CGCS2000 3 Degree GK CM 120E": "EPSG:4549",  # 120度经线
        "CGCS2000 3 Degree GK CM 123E": "EPSG:4550",  # 123度经线
        "CGCS2000 3 Degree GK CM 126E": "EPSG:4551",  # 126度经线
        "CGCS2000 3 Degree GK CM 129E": "EPSG:4552",  # 129度经线
        "CGCS2000 3 Degree GK CM 132E": "EPSG:4553",  # 132度经线
        "CGCS2000 3 Degree GK CM 135E": "EPSG:4554",  # 135度经线
        # 平面坐标（3度带，Zone格式，我国常用范围：25-45带）
        "CGCS2000 3 Degree GK Zone 25": "EPSG:4513",  # 25度带
        "CGCS2000 3 Degree GK Zone 26": "EPSG:4514",  # 26度带
        "CGCS2000 3 Degree GK Zone 27": "EPSG:4515",  # 27度带
        "CGCS2000 3 Degree GK Zone 28": "EPSG:4516",  # 28度带
        "CGCS2000 3 Degree GK Zone 29": "EPSG:4517",  # 29度带
        "CGCS2000 3 Degree GK Zone 30": "EPSG:4518",  # 30度带
        "CGCS2000 3 Degree GK Zone 31": "EPSG:4519",  # 31度带
        "CGCS2000 3 Degree GK Zone 32": "EPSG:4520",  # 32度带
        "CGCS2000 3 Degree GK Zone 33": "EPSG:4521",  # 33度带
        "CGCS2000 3 Degree GK Zone 34": "EPSG:4522",  # 34度带
        "CGCS2000 3 Degree GK Zone 35": "EPSG:4523",  # 35度带
        "CGCS2000 3 Degree GK Zone 36": "EPSG:4524",  # 36度带
        "CGCS2000 3 Degree GK Zone 37": "EPSG:4525",  # 37度带
        "CGCS2000 3 Degree GK Zone 38": "EPSG:4526",  # 38度带
        "CGCS2000 3 Degree GK Zone 39": "EPSG:4527",  # 39度带
        "CGCS2000 3 Degree GK Zone 40": "EPSG:4528",  # 40度带
        "CGCS2000 3 Degree GK Zone 41": "EPSG:4529",  # 41度带
        "CGCS2000 3 Degree GK Zone 42": "EPSG:4530",  # 42度带
        "CGCS2000 3 Degree GK Zone 43": "EPSG:4531",  # 43度带
        "CGCS2000 3 Degree GK Zone 44": "EPSG:4532",  # 44度带
        "CGCS2000 3 Degree GK Zone 45": "EPSG:4533"   # 45度带
    }
    
    # 右侧列：根据坐标类型选择坐标系
    with col2:
        if coord_type == "经纬度":
            # 经纬度坐标系选项
            lonlat_options = [crs for crs in crs_mapping.keys() if "Geodetic" in crs or "System" in crs or "1954" in crs or "1980" in crs]
            selected_crs_name = st.selectbox(
                "📍 选择经纬度坐标系",
                options=lonlat_options,
                index=lonlat_options.index("China Geodetic Coordinate System 2000"),
                help="选择对应的地理坐标系",
                key="lonlat_crs_select"
            )
        else:
            # 平面坐标选项
            plane_options = [crs for crs in crs_mapping.keys() if "GK" in crs]
            selected_crs_name = st.selectbox(
                "📍 选择平面坐标系",
                options=plane_options,
                index=plane_options.index("CGCS2000 3 Degree GK Zone 37"),
                help="选择对应的投影坐标系",
                key="plane_crs_select"
            )
    
    # 获取选中的EPSG代码
    selected_crs = crs_mapping[selected_crs_name]
    
    # 保存用户选择到session_state，确保按钮点击时能保持选择
    if "selected_crs" not in st.session_state:
        st.session_state.selected_crs = selected_crs
        st.session_state.selected_crs_name = selected_crs_name
    
    # 当用户改变选择时更新session_state
    if selected_crs != st.session_state.selected_crs:
        st.session_state.selected_crs = selected_crs
        st.session_state.selected_crs_name = selected_crs_name
    
    # 显示当前选择的坐标系信息
    st.info(f"当前选择的坐标系：{selected_crs_name} ({selected_crs})")
    # 简化表头，使用短英文名称避免SHP字段名截断
    fixed_headers = ["X", "Y"]
    # 配置字段校验规则（仅XY坐标）
    column_config = {
        "X": st.column_config.NumberColumn(
            "经度/X坐标", 
            required=True, 
            format="%.6f" if coord_type.startswith("经纬") else "%.2f",
            help="经纬度输入-180~180/0~90，平面坐标直接输数字"
        ),
        "Y": st.column_config.NumberColumn(
            "纬度/Y坐标", 
            required=True, 
            format="%.6f" if coord_type.startswith("经纬") else "%.2f"
        )
    }

    # ---------------------- 2. 初始化数据 ----------------------
    if "data" not in st.session_state:
        # 添加默认数据行
        st.session_state.data = pd.DataFrame([{"X": 12345678.1234, "Y": 123456.1234}], columns=fixed_headers)

    # ---------------------- 3. 数据交互编辑 ----------------------
    with st.form("data_input_form"):
        st.subheader("🖋️ 坐标数据输入")
        
        edited_df = st.data_editor(
            st.session_state.data,
            column_config=column_config,
            num_rows="dynamic",
            use_container_width=True,
            key="data_editor"
        )
        
        # 在表单内添加提交按钮
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 应用更改")
        with col2:
            reset = st.form_submit_button("🔄 重置")
        
        if submitted:
            st.session_state.data = edited_df
            st.success("数据已更新！")
            st.rerun()
        
        if reset:
            st.session_state.data = pd.DataFrame([{"X": 12345678.1234, "Y": 123456.1234}], columns=fixed_headers)
            st.rerun()

    # ---------------------- 4. 数据校验与预处理 ----------------------
    def validate_and_preprocess(data):
        if data.empty:
            return None, "⚠️ 暂无数据，请先添加坐标"
        
        # 坐标类型适配校验
        if coord_type.startswith("经纬"):
            # 经纬度范围约束
            data_clean = data.copy()
            data_clean["X"] = pd.to_numeric(data_clean["X"], errors="coerce").round(6)
            data_clean["Y"] = pd.to_numeric(data_clean["Y"], errors="coerce").round(6)
            invalid_mask = (data_clean["X"].isnull() | data_clean["Y"].isnull() |
                           (data_clean["X"] < -180) | (data_clean["X"] > 180) |
                           (data_clean["Y"] < -90) | (data_clean["Y"] > 90))
        else:
            # 平面坐标仅非空校验
            data_clean = data.copy()
            data_clean["X"] = pd.to_numeric(data_clean["X"], errors="coerce").round(2)
            data_clean["Y"] = pd.to_numeric(data_clean["Y"], errors="coerce").round(2)
            invalid_mask = data_clean["X"].isnull() | data_clean["Y"].isnull()
        
        # 过滤无效数据
        if invalid_mask.any():
            st.warning(f"❌ 过滤{invalid_mask.sum()}行无效数据（坐标异常或为空）")
            data_clean = data_clean[~invalid_mask].reset_index(drop=True)
        
        return data_clean, "✅ 数据校验完成，可导出SHP"

    # 校验结果展示
    if st.session_state.data.empty:
        clean_data, msg = None, ""
    else:
        clean_data, msg = validate_and_preprocess(st.session_state.data)
        st.info(msg)

    # ---------------------- 5. SHP导出功能 ----------------------
    st.subheader("📥 SHP文件导出")
    
    # 选择导出几何类型（点、线、面）
    feature_types = st.multiselect(
        "🔶 选择导出几何类型",
        options=["点", "线", "面"],
        default=["面"],
        help="点：每个坐标作为一个点；线：将所有坐标按顺序连接成一条线；面：将所有坐标按顺序连接成一个闭合多边形"
    )
    
    def export_shp(data, feature_types):
        # 使用session_state中保存的用户选择的坐标系
        crs = st.session_state.selected_crs
        selected_crs_name = st.session_state.selected_crs_name
        
        # 显示导出信息
        st.info(f"正在导出SHP文件，使用坐标系: {selected_crs_name} ({crs})")
        
        # 生成SHP文件并打包为ZIP
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "data_shp.zip")
            
            # 准备坐标数据
            coords = list(zip(data["X"], data["Y"]))
            
            with zipfile.ZipFile(zip_path, "w") as zipf:
                # 导出点类型
                if "点" in feature_types:
                    # 创建点GeoDataFrame
                    gdf_points = gpd.GeoDataFrame(
                        data,
                        geometry=[Point(xy) for xy in coords],
                        crs=crs
                    )
                    # 保存点SHP文件
                    shp_path_points = os.path.join(tmp_dir, "points.shp")
                    gdf_points.to_file(shp_path_points, driver="ESRI Shapefile", encoding="utf-8")
                    # 添加到ZIP
                    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                        file = f"points{ext}"
                        if os.path.exists(os.path.join(tmp_dir, file)):
                            zipf.write(os.path.join(tmp_dir, file), file)
                
                # 导出线类型
                if "线" in feature_types:
                    # 创建线GeoDataFrame
                    gdf_line = gpd.GeoDataFrame(
                        [{}],
                        geometry=[LineString(coords)],
                        crs=crs
                    )
                    # 保存线SHP文件
                    shp_path_line = os.path.join(tmp_dir, "line.shp")
                    gdf_line.to_file(shp_path_line, driver="ESRI Shapefile", encoding="utf-8")
                    # 添加到ZIP
                    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                        file = f"line{ext}"
                        if os.path.exists(os.path.join(tmp_dir, file)):
                            zipf.write(os.path.join(tmp_dir, file), file)
                
                # 导出面类型
                if "面" in feature_types:
                    # 创建面GeoDataFrame（闭合多边形）
                    gdf_polygon = gpd.GeoDataFrame(
                        [{}],
                        geometry=[Polygon(coords)],
                        crs=crs
                    )
                    # 保存面SHP文件
                    shp_path_polygon = os.path.join(tmp_dir, "polygon.shp")
                    gdf_polygon.to_file(shp_path_polygon, driver="ESRI Shapefile", encoding="utf-8")
                    # 添加到ZIP
                    for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                        file = f"polygon{ext}"
                        if os.path.exists(os.path.join(tmp_dir, file)):
                            zipf.write(os.path.join(tmp_dir, file), file)
            
            # 读取ZIP文件数据
            with open(zip_path, "rb") as f:
                shp_zip_data = f.read()
        
        return shp_zip_data

    # 导出按钮逻辑
    if clean_data is not None and not clean_data.empty:
        if st.button("📤 导出SHP文件", type="primary"):
            try:
                shp_zip_data = export_shp(clean_data, feature_types)
                st.download_button(
                    label="✅ 下载SHP文件",
                    data=shp_zip_data,
                    file_name="data_shp.zip",
                    mime="application/zip",
                    key="download_shp"
                )
            except Exception as e:
                st.error(f"导出失败：{str(e)}，请检查数据格式后重试")
    else:
        st.button("📤 导出SHP文件", disabled=True, help="请先添加有效坐标数据")


# 程序入口
if __name__ == "__main__":
    main()