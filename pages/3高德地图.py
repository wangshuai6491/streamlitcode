import streamlit as st
import math
import pandas as pd
import re
from urllib.parse import unquote
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

def zuobiaozhuanhuan():
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

def roadjson():
    st.caption("数据接口均采用官方API | 仅供学习和研究使用 | 请在 24 小时内删除下载的文件")
    # 三个tab
    tab1, tab2, tab3 = st.tabs(["📝 工具箱使用说明", "🔗 提取ID,cookie,JSON", "📖 兜底图文教程"])
    with tab1:
        st.markdown("#### 工具箱使用说明")
        # 两种方法，一种是用ID+cookie的模式，这种模式只用提取一次cookie,后续更换不同的ID就可以一直提取，推荐用这个
        # 另一种是用JSON的模式，这种模式每次都需要手动提取JSON，如果只有几个ID,推荐用这个
        st.info("两种方法2选1")
        st.info("方法1：用ID+cookie的模式，这种模式只用提取一次cookie,后续更换不同的ID就可以一直提取，但要注意频繁请求会被拒绝，一旦被拒绝，需要1天时间才能重新请求")
        st.info("方法2：用JSON的模式，这种模式每次都需要手动提取JSON,好处是肯定能用，不会被拒绝")
    with tab2:
        # ---------- 步骤 1：贴网址，自动提 ID ----------
        st.markdown("### ① 获取道路 / 区域 ID")
        st.markdown("1. 打开高德地图网页版并**登录!登录!登录!**: [高德地图](https://ditu.amap.com)")
        st.markdown("2. 在搜索框中输入地名或道路名称，点击搜索后，网址将类似https://ditu.amap.com/place/*****")
        url = st.text_input(
            "把搜索后的完整网址粘贴进来，比如",
            placeholder="https://ditu.amap.com/place/B0FFH43XTQ",
            key="url_input",
        )
        # 先把按钮画出来
        clicked = st.button("提取 ID")

        # 再放示例图（用占位符，方便后面清空）
        img_slot = st.empty()

        # 只在未点击时显示示例图
        if not clicked:
            img_slot.image("static/gd1.png")

        # 点击后的处理
        if clicked:
            img_slot.empty()
            if url:
                import re
                m = re.search(r"place/([A-Z0-9]+)", url)
                if m:
                    road_id = m.group(1)
                    st.session_state["road_id"] = road_id
                    st.success(f"已提取 ID：**{road_id}**")
                else:
                    st.error("未识别到 ID，请检查网址")
            else:
                st.warning("请先粘贴网址")

        # ---------- 步骤 2：一键拼坐标链接 ----------
        if st.session_state.get("road_id"):
            st.markdown("### ② 获取坐标数据")
            link = f"https://www.amap.com/detail/get/detail?id={st.session_state['road_id']}"
            st.markdown(f"[点击获取坐标数据{link}]({link})")
            st.info("复制上方链接到浏览器 → 进行滑块验证等操作 → 全选ctrl+a → 复制ctrl+c")
            # 用来放示例图，稍后清空
            # 示例图占位符（先定义！）
            img_slot1 = st.empty()
            img_slot1.image("static/gd2.png")
            # 让用户粘贴
            json_data = st.text_area(
                "请粘贴复制的 JSON 数据",
                placeholder="粘贴 JSON 数据...",
                height=200,
                key="json_input"
            )
            # 用户粘贴清空示例图
            if json_data:
                img_slot1.empty()

            # ---------- 步骤 3：提醒拿 Cookie ----------
            st.markdown("### ③ 获取 Cookie")
            st.caption("如果你安装了 **Cookie获取器** 等插件，在插件中直接点击 **获取 Cookie** 按钮即可")
            st.markdown(f"[手动获取，仍在上一步的页面：{link}]({link})")
            st.markdown(
                """
                1. 按 **F12** 打开开发者工具  
                2. 切到 **Network或网络**，刷新页面，也就是在地址栏重新输入网址并回车一次
                3. 找到 `detail/****` 请求 → **Headers或标头** → **Cookie**  
                4. 整段复制 Cookie 值
                """
            )
            st.info("提示: Cookie 包含您的登录信息，请妥善保管，不要泄露给他人")
            st.image("static/gd3.png")
    with tab3:
        # ---------- 顶部统一说明书 ----------
        st.markdown("#### 获取道路或面状数据id")
        st.markdown("1. 打开高德地图网页版: [高德地图](https://ditu.amap.com)")
        st.markdown("2. 在搜索框中输入地名或道路名称，点击搜索后，网址将类似https://ditu.amap.com/place/*****")
        st.markdown("3. 观察浏览器地址栏，此时网址会变为类似: `https://ditu.amap.com/place/B0FFH43XTQ`")
        st.markdown("4. 其中 `B0FFH43XTQ` 就是该道路的专属id")
        st.code("示例: https://ditu.amap.com/place/B0FFH43XTQ 中的 B0FFH43XTQ")
        st.image("static/gd1.png")
        # 获取坐标数据部分
        st.markdown("### 获取坐标数据")
        st.markdown("1. 确保已登录您的高德账号")
        st.markdown("2. 修改网址前缀为: `https://www.amap.com/detail/get/detail?id=` 加上您刚才获取的道路专属id")
        st.code("示例: https://www.amap.com/detail/get/detail?id=B0FFH43XTQ")
        st.markdown("3. 页面中的shape属性即为坐标数据(火星坐标系)")
        st.markdown("4. 您可以使用 `Ctrl+A`, `Ctrl+C` 复制页面内容，然后使用 **国土行业工具箱pro.atbx** 中的 **4高德道路及面状json转shp** 工具转为shp格式，该工具会自动处理坐标转换")
        st.image("static/gd2.png")

        # 获取cookie部分
        st.markdown("### 获取cookie")
        st.markdown("1. 打开刚才的坐标数据网址: `https://www.amap.com/detail/get/detail?id=B0FFH43XTQ`")
        st.markdown("2. 打开浏览器的开发者模式 (通常按 F12 或 Ctrl+Shift+I)")
        st.markdown("3. 切换到 '网络'(Network) 标签页")
        st.markdown("4. 刷新页面，找到名称为 'detail' 的请求")
        st.markdown("5. 在 '请求头'(Headers) 部分找到 'Cookie' 字段，复制其值")
        st.image("static/gd3.png")
        st.info("提示: Cookie 包含您的登录信息，请妥善保管，不要泄露给他人")


def bus():
    st.caption("数据接口均采用官方API | 仅供学习和研究使用 | 请在 24 小时内删除下载的文件")
    st.markdown("### 📖 获取公交路线和站点")
    st.markdown("请首先**登录!登录!登录!**[高德地图网页版](https://ditu.amap.com)")

    # ---------- 1. 三种入口收进 tabs ----------
    tab_url, tab_manual, tab_dev = st.tabs([
        "🔗 粘贴高德链接（自动解析）",
        "📝 手动输入城市+线路",
        "⚙️ 兜底开发者模式"
    ])

    # 初始化 session_state
    for k in ("city", "bus_line"):
        if k not in st.session_state:
            st.session_state[k] = ""

    # ---- Tab 1：自动解析 ----
    with tab_url:
        url = st.text_input(
            "切换城市（比如太原），搜索公交（比如801路），粘贴网页地址栏链接,回车确认：",
            placeholder="https://ditu.amap.com/search?query=801路&city=140100…",
            key="url_input"
        )
        if url:
            m = re.search(r"query=([^&]+)&city=(\d+)", url)
            if m:
                st.session_state["bus_line"] = unquote(m.group(1))
                st.session_state["city"] = m.group(2)
                st.success(f"已提取 线路：**{st.session_state['bus_line']}** 城市代码：**{st.session_state['city']}**")
            else:
                st.error("未识别到 ID，请检查网址")

    # ---- Tab 2：手动输入 ----
    with tab_manual:
        c1, c2 = st.columns(2)
        with c1:
            st.session_state["city"] = st.text_input(
                "请输入行政区代码",
                value=st.session_state["city"],
                placeholder="比如太原是140100"
            )
        with c2:
            st.session_state["bus_line"] = st.text_input(
                "请输入公交路线，回车确认",
                value=st.session_state["bus_line"],
                placeholder="比如801路"
            )

    # ---- Tab 3：开发者模式（兜底预留） ----
    with tab_dev:
        st.markdown("1. 确保**登录!登录!登录!**: [高德地图](https://ditu.amap.com)")
        st.markdown("2. 在搜索框中输入公交，比如先切换到太原，搜索801路")
        st.markdown("3. 按F12进入开发者模式，点击网络（net）,刷新页面,搜索以下内容")
        st.code("query_type=TQUERY&pagesize=20&pagenum=1&qii=true", language="text")
        st.image("static/gd4.png")

    # ---------- 2. 公共底部 ----------
    if st.session_state["city"] and st.session_state["bus_line"]:
        url1 = (
            "https://ditu.amap.com/service/poiInfo"
            "?query_type=TQUERY"
            f"&city={st.session_state['city']}"
            f"&keywords={st.session_state['bus_line']}"
        )
        # ① 用按钮代替裸链接，好看一点
        st.link_button("🔗 一键获取公交 JSON 数据", url1, use_container_width=True)


if __name__ == '__main__':
    # Streamlit UI
    st.set_page_config(page_title="高德地图", layout="wide")
    st.markdown("### 高德地图")

    # 侧边导航栏
    option = st.sidebar.radio(
        "功能导航:",
        ["坐标转换", "道路及面状json", "公交","其他功能"]
    )

    if option == "坐标转换":
        zuobiaozhuanhuan()
    elif option == "道路及面状json":
        roadjson()
    elif option == "公交":
        bus()
    elif option == "其他功能":
        st.subheader("其他功能开发中")
        st.info("更多坐标转换相关功能即将上线，敬请期待！")
        # 这里可以预留其他功能的接口

    # ---------- 底部 ----------
    st.markdown("---")
    st.caption("💡 拿到 json/ID/cookie 等数据后，回到 **国土行业工具箱** 即可生成 Shapefile 文件，⬇️ [下载国土行业工具箱](https://share.note.youdao.com/s/5pcwelCC)")

    # 页脚
    st.sidebar.caption("本网站目前只支持WGS84、GCJ02坐标系转换")
    st.sidebar.caption("其他同功能网站：https://www.iamwawa.cn/zuobiao.html")
    st.sidebar.caption("高德坐标拾取工具：https://lbs.amap.com/tools/picker")