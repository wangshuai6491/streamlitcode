import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import tempfile
import os
import zipfile

def main():
    # 页面配置
    st.set_page_config(page_title="地理数据编辑导出工具", layout="wide")
    st.title("📊 地理数据交互编辑与多格式导出")

    # ---------------------- 1. 坐标类型选择+表头配置 ----------------------
    # 新增坐标类型选择（兼容经纬度/平面坐标）
    coord_type = st.radio(
        "🔍 选择坐标类型",
        options=["经纬度（WGS84/大地2000）", "平面直角坐标（如大地2000 37度带）"],
        index=0,
        help="平面坐标直接输入数字（如X=40500000，Y=5300000），无需符号约束"
    )
    # 固定表头（复用经度/纬度列为X/Y坐标）
    fixed_headers = ["序号", "名称", "经度/X坐标", "纬度/Y坐标", "属性值1", "属性值2", "备注"]
    # 动态配置字段校验规则（按坐标类型适配）
    column_config = {
        "序号": st.column_config.NumberColumn("序号", required=True, step=1, min_value=1),
        "名称": st.column_config.TextColumn("名称", max_chars=50),
        "经度/X坐标": st.column_config.NumberColumn(
            "经度/X坐标", 
            required=True, 
            format="%.6f" if coord_type.startswith("经纬") else "%.2f",
            help="经纬度输入-180~180/0~90，平面坐标直接输数字"
        ),
        "纬度/Y坐标": st.column_config.NumberColumn(
            "纬度/Y坐标", 
            required=True, 
            format="%.6f" if coord_type.startswith("经纬") else "%.2f"
        ),
        "属性值1": st.column_config.NumberColumn("属性值1", format="%.2f"),
        "属性值2": st.column_config.TextColumn("属性值2", max_chars=100),
        "备注": st.column_config.TextColumn("备注", max_chars=200)
    }

    # ---------------------- 2. 初始化数据 ----------------------
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=fixed_headers)

    # ---------------------- 3. 数据交互编辑 ----------------------
    st.subheader("🖋️ 数据编辑区")
    edited_data = st.data_editor(
        st.session_state.data,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor"
    )
    st.session_state.data = edited_data

    # ---------------------- 4. 数据校验与预处理 ----------------------
    def validate_and_preprocess(data):
        if data.empty:
            return None, "⚠️ 暂无数据，请先添加内容"
        
        # 去重+补全序号
        data_clean = data.drop_duplicates(subset=["序号", "经度/X坐标", "纬度/Y坐标"], keep="last")
        if data_clean["序号"].isnull().any():
            max_seq = data_clean["序号"].max() if not data_clean["序号"].isna().all() else 0
            missing_seq = data_clean["序号"].isnull()
            data_clean.loc[missing_seq, "序号"] = range(int(max_seq)+1, int(max_seq)+1+missing_seq.sum())
        
        # 坐标类型适配校验
        if coord_type.startswith("经纬"):
            # 经纬度范围约束
            data_clean["经度/X坐标"] = pd.to_numeric(data_clean["经度/X坐标"], errors="coerce").round(6)
            data_clean["纬度/Y坐标"] = pd.to_numeric(data_clean["纬度/Y坐标"], errors="coerce").round(6)
            invalid_mask = (data_clean["经度/X坐标"].isnull() | data_clean["纬度/Y坐标"].isnull() |
                           (data_clean["经度/X坐标"] < -180) | (data_clean["经度/X坐标"] > 180) |
                           (data_clean["纬度/Y坐标"] < -90) | (data_clean["纬度/Y坐标"] > 90))
        else:
            # 平面坐标仅非空校验
            data_clean["经度/X坐标"] = pd.to_numeric(data_clean["经度/X坐标"], errors="coerce").round(2)
            data_clean["纬度/Y坐标"] = pd.to_numeric(data_clean["纬度/Y坐标"], errors="coerce").round(2)
            invalid_mask = data_clean["经度/X坐标"].isnull() | data_clean["纬度/Y坐标"].isnull()
        
        # 过滤无效数据
        if invalid_mask.any():
            st.warning(f"❌ 过滤{invalid_mask.sum()}行无效数据（坐标异常或为空）")
            data_clean = data_clean[~invalid_mask].reset_index(drop=True)
        return data_clean, "✅ 数据校验完成，可导出"

    # 校验结果展示
    if st.session_state.data.empty:
        clean_data, msg = None, ""
    else:
        clean_data, msg = validate_and_preprocess(st.session_state.data)
        st.info(msg)

    # ---------------------- 5. 多格式导出（适配坐标类型） ----------------------
    st.subheader("📥 数据导出")
    export_formats = st.multiselect("选择导出格式", ["CSV", "Excel", "GeoJSON", "SHP"], default=["CSV"])

    def export_data(data):
        exports = {}
        # 坐标系映射（按选择的坐标类型绑定）
        crs = "EPSG:4326" if coord_type.startswith("经纬") else "EPSG:4547"  # 大地2000 37度带
        
        # CSV导出
        if "CSV" in export_formats:
            csv_data = data.to_csv(index=False, encoding="utf-8-sig")
            exports["CSV"] = ("data.csv", csv_data, "text/csv")
        
        # Excel导出（含坐标类型说明）
        if "Excel" in export_formats:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                with pd.ExcelWriter(tmp.name, engine="openpyxl") as writer:
                    data.to_excel(writer, sheet_name="数据", index=False)
                    # 补充坐标说明
                    desc_df = pd.DataFrame({
                        "字段名": fixed_headers,
                        "说明": [
                            "唯一标识序号", "数据名称", 
                            f"{'经度' if coord_type.startswith('经纬') else 'X坐标'}（{crs}）",
                            f"{'纬度' if coord_type.startswith('经纬') else 'Y坐标'}（{crs}）",
                            "数值属性1", "文本/数值属性2", "补充说明"
                        ]
                    })
                    desc_df.to_excel(writer, sheet_name="字段说明", index=False)
            with open(tmp.name, "rb") as f:
                excel_data = f.read()
            exports["Excel"] = ("data.xlsx", excel_data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            os.unlink(tmp.name)
        
        # GeoJSON/SHP导出（地理格式）
        if clean_data is not None and not clean_data.empty:
            gdf = gpd.GeoDataFrame(
                data,
                geometry=[Point(xy) for xy in zip(data["经度/X坐标"], data["纬度/Y坐标"])],
                crs=crs
            )
            # GeoJSON
            if "GeoJSON" in export_formats:
                geojson_data = gdf.to_json(index=False)
                exports["GeoJSON"] = ("data.geojson", geojson_data, "application/geo+json")
            # SHP（打包为ZIP）
            if "SHP" in export_formats:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    shp_path = os.path.join(tmp_dir, "data.shp")
                    gdf.to_file(shp_path, driver="ESRI Shapefile", encoding="utf-8")
                    zip_path = os.path.join(tmp_dir, "data_shp.zip")
                    with zipfile.ZipFile(zip_path, "w") as zipf:
                        for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                            file = f"data{ext}"
                            zipf.write(os.path.join(tmp_dir, file), file)
                    with open(zip_path, "rb") as f:
                        shp_zip_data = f.read()
                exports["SHP"] = ("data_shp.zip", shp_zip_data, "application/zip")
        return exports

    # 导出按钮逻辑
    if clean_data is not None and not clean_data.empty:
        exports = export_data(clean_data)
        col1, col2 = st.columns(2)
        with col1:
            # 批量打包下载
            if st.button("📤 批量下载选中格式", type="primary"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                    with zipfile.ZipFile(tmp_zip.name, "w") as zipf:
                        for name, (filename, data, _) in exports.items():
                            zipf.writestr(filename, data)
                with open(tmp_zip.name, "rb") as f:
                    st.download_button(
                        label="下载全部打包文件",
                        data=f,
                        file_name="地理数据导出包.zip",
                        mime="application/zip"
                    )
                os.unlink(tmp_zip.name)
        with col2:
            # 单独下载
            st.write("单独下载：")
            for name, (filename, data, mime) in exports.items():
                st.download_button(
                    label=f"下载{name}文件",
                    data=data,
                    file_name=filename,
                    mime=mime,
                    key=f"download_{name}"
                )
    else:
        st.button("📤 批量下载选中格式", disabled=True, help="请先添加有效数据")

    # ---------------------- 6. 辅助功能 ----------------------
    st.subheader("🔧 辅助工具")
    col1, col2, col3 = st.columns(3)
    with col1:
        # 下载空白模板
        if st.button("📥 下载空白模板"):
            template = pd.DataFrame(columns=fixed_headers)
            csv_template = template.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="下载CSV模板",
                data=csv_template,
                file_name="地理数据编辑模板.csv",
                mime="text/csv",
                key="template"
            )
    with col2:
        # 清空数据
        if st.button("🗑️ 清空表格", type="secondary"):
            st.session_state.data = pd.DataFrame(columns=fixed_headers)
            st.rerun()
    with col3:
        # 数据统计
        if clean_data is not None and not clean_data.empty:
            st.write(f"📊 有效数据：{len(clean_data)}行")
            x_min, x_max = clean_data["经度/X坐标"].min(), clean_data["经度/X坐标"].max()
            y_min, y_max = clean_data["纬度/Y坐标"].min(), clean_data["纬度/Y坐标"].max()
            st.write(f"🌍 坐标范围：\n{x_min:.6f}~{x_max:.6f}\n{y_min:.6f}~{y_max:.6f}")

    # ---------------------- 7. 异常处理 ----------------------
    st.markdown("""
        <style>
        .warning {color: #dc3545;}
        .success {color: #28a745;}
        </style>
        """, unsafe_allow_html=True)
    try:
        if "exports" in locals():
            pass
    except Exception as e:
        st.error(f"导出失败：{str(e)}，请检查数据格式后重试")

# 程序入口
if __name__ == "__main__":
    main()