import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import tempfile
import os
import zipfile
import simplekml

def main():
    st.set_page_config(page_title="坐标转SHP/KML", layout="wide")
    st.title("📊 坐标转SHP/KML")
    # ---------------------- 原有坐标类型、坐标系选择逻辑不变 ----------------------
    col1, col2 = st.columns(2)
    with col1:
        coord_type = st.radio(
            "🔍 选择坐标类型",
            options=["经纬度", "平面直角坐标"],
            index=1,
            horizontal=True,
            help="经纬度：如WGS84、CGCS2000等全球坐标系；平面坐标：如高斯克里格投影坐标"
        )
    crs_mapping = {
        "China Geodetic Coordinate System 2000": "EPSG:4490",
        "World Geodetic System 1984": "EPSG:4326",
        "Beijing 1954": "EPSG:4214",
        "Xian 1980": "EPSG:4610",
        "CGCS2000 3 Degree GK CM 75E": "EPSG:4534",
        "CGCS2000 3 Degree GK Zone 25": "EPSG:4513",
        "CGCS2000 3 Degree GK Zone 37": "EPSG:4525",
        # 其余坐标系映射不变，省略重复代码...
    }
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
    st.info(f"当前选择的坐标系：{selected_crs_name} ({selected_crs})")

    # ---------------------- 原有数据编辑、校验逻辑不变 ----------------------
    fixed_headers = ["X", "Y"]
    column_config = {
        "X": st.column_config.NumberColumn("经度/X坐标", required=True, format="%.6f" if coord_type.startswith("经纬") else "%.2f", help="经纬度输入-180~180/0~90，平面坐标直接输数字"),
        "Y": st.column_config.NumberColumn("纬度/Y坐标", required=True, format="%.6f" if coord_type.startswith("经纬") else "%.2f")
    }
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame([{"X": 12345678.1234, "Y": 123456.1234}], columns=fixed_headers)
    with st.form("data_input_form"):
        st.subheader("🖋️ 坐标数据输入")
        edited_df = st.data_editor(st.session_state.data, column_config=column_config, num_rows="dynamic", use_container_width=True, key="data_editor")
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

    def validate_and_preprocess(data):
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
            invalid_mask = data_clean["X"].isnull() | data_clean["Y"].isnull()
        if invalid_mask.any():
            st.warning(f"❌ 过滤{invalid_mask.sum()}行无效数据（坐标异常或为空）")
            data_clean = data_clean[~invalid_mask].reset_index(drop=True)
        return data_clean, "✅ 数据校验完成，可导出文件"
    if st.session_state.data.empty:
        clean_data, msg = None, ""
    else:
        clean_data, msg = validate_and_preprocess(st.session_state.data)
    st.info(msg)

    # ---------------------- 原有SHP导出逻辑不变 ----------------------
    feature_types = st.multiselect(
        "🔶 选择导出几何类型",
        options=["点", "线", "面"],
        default=["面"],
        help="点：每个坐标作为一个点；线：将所有坐标按顺序连接成一条线；面：将所有坐标按顺序连接成一个闭合多边形"
    )
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

    # ---------------------- 新增：KML生成函数 ----------------------
    def export_kml(data, feature_types):
        kml = simplekml.Kml()
        coords = list(zip(data["X"], data["Y"]))  # (X=经度/平面X, Y=纬度/平面Y)
        # 生成点
        if "点" in feature_types:
            for i, (x, y) in enumerate(coords, 1):
                kml.newpoint(name=f"点{i}", coords=[(x, y)])
        # 生成线
        if "线" in feature_types:
            kml.newlinestring(name="线要素", coords=coords)
        # 生成面（闭合）
        if "面" in feature_types:
            kml.newpolygon(name="面要素", outerboundaryis=coords)
        # 保存KML到临时文件，读取二进制数据
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".kml", delete=False) as tmp:
            kml.save(tmp)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            kml_data = f.read()
        os.unlink(tmp_path)  # 删除临时文件
        return kml_data

    # ---------------------- 按钮区：保留SHP按钮，新增KML按钮 ----------------------
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if clean_data is not None and not clean_data.empty:
            if st.button("📤 生成SHP文件", type="primary"):
                try:
                    shp_zip_data = export_shp(clean_data, feature_types)
                    st.download_button(label="✅ 点击下载SHP文件", data=shp_zip_data, file_name="data_shp.zip", mime="application/zip", key="download_shp")
                except Exception as e:
                    st.error(f"SHP导出失败：{str(e)}")
        else:
            st.button("📤 生成SHP文件", disabled=True, help="请先添加有效坐标数据")
    
    with btn_col2:
        if clean_data is not None and not clean_data.empty:
            if st.button("📤 生成KML文件", type="primary"):
                try:
                    kml_data = export_kml(clean_data, feature_types)
                    st.download_button(label="✅ 点击下载KML文件", data=kml_data, file_name="data_kml.kml", mime="application/vnd.google-earth.kml+xml", key="download_kml")
                except Exception as e:
                    st.error(f"KML导出失败：{str(e)}")
        else:
            st.button("📤 生成KML文件", disabled=True, help="请先添加有效坐标数据")

if __name__ == "__main__":
    main()
