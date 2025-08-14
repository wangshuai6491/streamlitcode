import streamlit as st
import math
import pandas as pd

# -------------常量定义-----------
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

# -----------函数定义-----------
def _out_of_china(lng, lat):
    return lng < 72.004 or lng > 137.8347 or lat < 0.8293 or lat > 55.8271

def _transform_lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transform_lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def gcj02_to_wgs84(lng, lat):
    """GCJ02 -> WGS84"""
    if _out_of_china(lng, lat):
        return lng, lat
    dlat = _transform_lat(lng - 105.0, lat - 35.0)
    dlng = _transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def wgs84_to_gcj02(lng, lat):
    """WGS84 -> GCJ02"""
    if _out_of_china(lng, lat):
        return lng, lat
    dlat = _transform_lat(lng - 105.0, lat - 35.0)
    dlng = _transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def main():
    # 原坐标系选择
    original_system = st.radio("选择转换模式：", ["高德坐标GCJ02→通用WGS84", "通用WGS84→高德坐标GCJ02"], horizontal=True)

    # 表格输入
    st.subheader("输入坐标")
    # 创建一个空的DataFrame作为模板
    input_data = pd.DataFrame({
        '经度': [112.59],
        '纬度': [37.85]
    })

    # 使用data_editor让用户输入多个坐标
    edited_data = st.data_editor(
        input_data,
        num_rows="dynamic",  # 允许用户添加/删除行
        use_container_width=True,
        column_config={
            '经度': st.column_config.NumberColumn(format="%.15f"),
            '纬度': st.column_config.NumberColumn(format="%.15f")
        }
    )

    # 转换按钮
    if st.button("批量转换"):
        if not edited_data.empty:
            try:
                # 准备结果数据
                results = []
                for _, row in edited_data.iterrows():
                    lng = row['经度']
                    lat = row['纬度']

                    if original_system == "高德坐标GCJ02→通用WGS84":
                        converted_coords = gcj02_to_wgs84(lng, lat)
                    elif original_system == "通用WGS84→高德坐标GCJ02":
                        converted_coords = wgs84_to_gcj02(lng, lat)
                    else:
                        st.error("暂不支持转换")
                        converted_coords = None

                    if converted_coords:
                        converted_lng, converted_lat = converted_coords
                        results.append({
                            '原经度': lng,
                            '原纬度': lat,
                            '转换后经度': converted_lng,
                            '转换后纬度': converted_lat
                        })
                    else:
                        results.append({
                            '原经度': lng,
                            '原纬度': lat,
                            '转换后经度': '转换失败',
                            '转换后纬度': '转换失败'
                        })

                # 显示结果表格
                st.subheader("转换结果")
                results_df = pd.DataFrame(results)
                st.dataframe(
                    results_df,
                    use_container_width=True,
                    column_config={
                        '原经度': st.column_config.NumberColumn(format="%.15f"),
                        '原纬度': st.column_config.NumberColumn(format="%.15f"),
                        '转换后经度': st.column_config.NumberColumn(format="%.15f"),
                        '转换后纬度': st.column_config.NumberColumn(format="%.15f")
                    }
                )

            except Exception as e:
                st.error(f"转换过程中出错: {str(e)}")
        else:
            st.warning("请输入坐标")

if __name__ == '__main__':
    # Streamlit UI
    st.set_page_config(page_title="地理坐标系转换", layout="wide")
    st.title("地理坐标系转换")

    # 侧边导航栏
    option = st.sidebar.radio(
        "功能导航:",
        ["坐标转换", "其他功能"]
    )

    if option == "坐标转换":
        main()
    elif option == "其他功能":
        st.subheader("其他功能开发中")
        st.info("更多坐标转换相关功能即将上线，敬请期待！")
        # 这里可以预留其他功能的接口
    # 页脚
    st.sidebar.caption("本网站目前只支持WGS84、GCJ02坐标系转换")
    st.sidebar.caption("其他同功能网站：https://www.iamwawa.cn/zuobiao.html")
    st.sidebar.caption("高德坐标拾取工具：https://lbs.amap.com/tools/picker")