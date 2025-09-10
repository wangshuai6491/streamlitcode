import math
import json
import arcpy
import os
from yanzheng import yanzheng


# 获取当前工作空间
workspace = arcpy.env.workspace
#全局变量
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def gcj02towgs84(lng, lat):
   """
   GCJ02(火星坐标系)转GPS84
   :param lng:火星坐标系的经度
   :param lat:火星坐标系纬度
   :return:
   """
   if out_of_china(lng, lat):
      return lng, lat
   dlat = transformlat(lng - 105.0, lat - 35.0)
   dlng = transformlng(lng - 105.0, lat - 35.0)
   radlat = lat / 180.0 * pi
   magic = math.sin(radlat)
   magic = 1 - ee * magic * magic
   sqrtmagic = math.sqrt(magic)
   dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
   dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
   mglat = lat + dlat
   mglng = lng + dlng
   return [lng * 2 - mglng, lat * 2 - mglat]
def transformlat(lng, lat):
   ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
      0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
   ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
         math.sin(2.0 * lng * pi)) * 2.0 / 3.0
   ret += (20.0 * math.sin(lat * pi) + 40.0 *
         math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
   ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
         math.sin(lat * pi / 30.0)) * 2.0 / 3.0
   return ret
def transformlng(lng, lat):
   ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
      0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
   ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
         math.sin(2.0 * lng * pi)) * 2.0 / 3.0
   ret += (20.0 * math.sin(lng * pi) + 40.0 *
         math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
   ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
         math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
   return ret
def out_of_china(lng, lat):
   """
   判断是否在国内，不在国内不做偏移
   :param lng:
   :param lat:
   :return:
   """
   if lng < 72.004 or lng > 137.8347:
      return True
   if lat < 0.8293 or lat > 55.8271:
      return True
   return False
def huoqu(buslines_list):
    # 用于存储结果
    x =[]
    xx = []
    bianhao = 0
    # 对buslines_list逐个处理
    for busline in buslines_list:
        bianhao = bianhao + 1  # 得到线路编号
        name = busline['name']
        lng = busline['xs']
        lat = busline['ys']

        # 将x按，分割后赋值为列表x1
        x1 = lng.split(',')
        y1 = lat.split(',')
        # 将x和y按顺序配对后，组成新的数据，赋值为列表A
        for cc in range(len(x1)):
            i = gcj02towgs84(float(x1[cc]), float(y1[cc]))  # 进行坐标转换
            x.append([bianhao, cc, i[0], i[1]])  # 得到可生产shp的表

        # 获取站点
        stations = busline['stations']
        for dd in stations:
            zdname = dd['name']
            xyzb = dd['xy_coords']
            zdzb = xyzb.split(';')
            zdi = gcj02towgs84(float(zdzb[0]), float(zdzb[1]))  # 进行坐标转换
            xx.append([zdname,  zdi[0], zdi[1]])  # 得到可生产shp的表
    return x, name, xx
def xtoshp(x, name, xx):
   arcpy.AddMessage("开始处理路线")
   output_table = 'newPOINT'
   arcpy.CreateTable_management(workspace, output_table)
   # 添加字段,字段名称为xdbh,类型为整数型
   arcpy.AddField_management(output_table, 'xdbh', 'LONG')
   arcpy.AddField_management(output_table, 'xuhao', 'LONG')
   arcpy.AddField_management(output_table, 'LONGITUDE', 'DOUBLE')
   arcpy.AddField_management(output_table, 'LATITUDE', 'DOUBLE')

   arcpy.AddMessage("开始添加数据")
   # 遍历列表x，将数据添加到shp中
   with arcpy.da.InsertCursor(output_table,['xdbh', 'xuhao', 'LONGITUDE', 'LATITUDE']) as cursor:
      for item in x:
         cursor.insertRow((item[0], item[1], item[2], item[3]))

   arcpy.AddMessage("完成添加，开始转换shp")
   arcpy.management.XYTableToPoint(output_table,"GJ","LONGITUDE", "LATITUDE", None,
                                   'GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')
   arcpy.management.PointsToLine("GJ",name,"xdbh", "xuhao", "NO_CLOSE")

   arcpy.AddMessage("开始处理站点")
   output_table = 'newPOINT'
   arcpy.CreateTable_management(workspace, output_table)
   # 添加字段,字段名称为xdbh,类型为整数型
   arcpy.AddField_management(output_table, 'name', 'TEXT')
   arcpy.AddField_management(output_table, 'LONGITUDE', 'DOUBLE')
   arcpy.AddField_management(output_table, 'LATITUDE', 'DOUBLE')

   arcpy.AddMessage("开始添加数据")
   # 遍历列表x，将数据添加到shp中
   with arcpy.da.InsertCursor(output_table, ['name', 'LONGITUDE', 'LATITUDE']) as cursor:
       for item in xx:
           cursor.insertRow((item[0], item[1], item[2]))

   arcpy.AddMessage("完成添加，开始转换shp")
   arcpy.management.XYTableToPoint(output_table, "公交站点_" + name, "LONGITUDE", "LATITUDE", None,
                                   'GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')
# 清理文件名，确保没有无效字符
def sanitize_name(name):
    # 替换空格和其他无效字符
    for ch in [' ', '-', '&', '#', '(', ')']:
        if ch in name:
            name = name.replace(ch, '_')
    # 确保名称不以数字开头
    if name[0].isdigit():
        name = 'T_' + name
    return name

def run_zhucema_ws(proname):
    yz = yanzheng(proname)
    if yz[0]:
        arcpy.AddMessage(f"程序验证完成，{yz[1]}")
        arcpy.AddMessage("开始执行程序")
    else:
        arcpy.AddError(f"验证失败，{yz[1]}")
        sys.exit(1)


def load_json_parameter(param_text):
    """
    兼容两种输入：
    1. 磁盘文件路径 → 读取文件
    2. 直接粘贴的 JSON 字符串 → 直接解析
    返回解析后的 Python 对象
    """
    param_text = param_text.strip()
    if not param_text:
        raise ValueError("输入为空，请粘贴 JSON 或选择 JSON 文件！")

    # 1. 先按文件处理
    if os.path.isfile(param_text):
        try:
            with open(param_text, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"无法读取/解析文件：{e}")

    # 2. 不是文件就当纯文本 JSON
    try:
        return json.loads(param_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"输入既不是有效文件，也不是合法 JSON：{e}")   

if __name__ == '__main__':
    run_zhucema_ws("15GDDT3")

    try:
        raw_input = arcpy.GetParameterAsText(0)
        gj = load_json_parameter(raw_input)
        arcpy.AddMessage("已读取 JSON，开始运行……")

        if not gj.get('data'):
            arcpy.AddMessage("未找到 data 数据")
            exit(0)

        gj_bus = gj['data']
        # 用 Python 对象判断，比字符串 in 更可靠
        if 'busline_list' not in gj_bus:
            arcpy.AddMessage("未找到 busline_list 数据")
            exit(0)

        arcpy.AddMessage("找到路线及站点信息，开始处理")
        buslines_list = gj_bus['busline_list']
        x, name, xx = huoqu(buslines_list)
        name = sanitize_name(name)

        xtoshp(x, name, xx)

        # 自动加载到当前地图
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        mapx = aprx.activeMap
        ws = arcpy.env.workspace

        line_lyr_path = os.path.join(ws, name)
        stop_lyr_path = os.path.join(ws, "公交站点_" + name)

        mapx.addDataFromPath(line_lyr_path)
        mapx.addDataFromPath(stop_lyr_path)

        arcpy.AddMessage("运行成功！")

    except Exception as e:
        # 把 Python 异常原样抛到 ArcGIS，方便脚本工具弹窗
        arcpy.AddError(str(e))
        raise