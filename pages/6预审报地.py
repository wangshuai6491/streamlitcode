import re
from typing import List, Dict, Any, Union
import streamlit as st
import os
import sys
import json,time
# 添加父目录到Python路径，确保可以导入__init__.py中的函数
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 直接导入__init__.py中的lineinput函数
from __init__ import main
def page1():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处  

        ### 二、审查标准  
        1. 符合基本建设投资管理规定。  
        2. 建设单位已取得建设项目批准（核准或备案）文件、初步设计批准或审核文件，且应当在有效期内。  
        3. 用地涉及的新增建设用地应按规定缴纳新增建设用地土地有偿使用费，缴纳等级、标准应准确。  
        4. 1999 年 1 月 1 日之后经依法批准的集体建设用地，在批准农用地转用时未缴纳新增建设用地有偿使用费的，申请土地征收时按照现行标准补缴。  

        ### 三、审查内容模板  
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page2():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处  

        ### 二、审查标准  
        1. 涉及占用林地的，应当取得使用林地审核同意书，且应当在有效期内。涉及占用各类保护地的，需取得相关主管部门同意的意见。  
        2. 采矿用地需取得采矿许可证。  
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page3():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处  

        ### 二、审查标准  
        1. 土地利用计划指标安排应符合自然资源部和省自然资源厅年度土地利用计划管理规定。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page4():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        行政审批管理处、国土空间用途管制处  

        ### 二、审查标准  
        1. 已按规定通过用地预审，预审层级应符合要求，应在预审批准后且有效期内批复可研报告或核准项目。  
        2. 重新预审的符合有关规定。  
        3. 用地规模和用地预审控制规模比对情况应符合有关要求。  
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page5():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室
        自然资源确权登记局、自然资源调查监测处

        ### 二、审查标准
        1. 勘测定界符合《土地勘测定界规程》(TD/T1008-2007)、《土地利用现状分类》(GB/T21010-2017)等规定。
        2. 集体土地和国有土地宗地数正确，登记发证情况符合要求，权属清楚，无争议。
        3. 现状地类以"三调"地类为基础、组卷时最新年度变更调查数据为准，总面积、农用地、耕地、建设用地、未利用地面积差异均在合理误差范围内(总面积差异在1%以内或各地类面积差异在1%以内)或无差异。
        4. 已按照自然资源部办公厅《关于以"三调"成果为基础做好建设用地审查报批地类认定的通知》(自然资办发(2022)411号)、《关于第三次全国国土调查成果为基础明确林地管理边界规范林地管理的通知》(自然资发(2023)53号)等规定完成报批地类认定。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page6():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间规划局

        ### 二、审查标准  
        1. 符合国土空间规划。
        2. 项目涉及生态保护红线的，应符合《自然资源部生态环境部国家林业和草原局关于加强生态保护红线管理的通知(试行)》(自然资发(2022)142号)有关要求，并取得省政府出具的认定意见或不可避让论证意见。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page7():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        耕地保护监督处

        ### 二、审查标准  
        1. 建设占用耕地(包括占用可调整地类、无合法来源的建设用地占用时为耕地)数据准确，已按有关规定落实耕地占补平衡。
        2. 补充耕地方式属于委托补充，建设单位已足额缴纳耕地开垦费，其中涉及永久基本农田的按照不低于两倍缴纳。
        3. 项目占用补划永久基本农田的具体数量、质量符合要求。
        4. 省厅已按照有关规定组织踏勘论证，已说明占用永久基本农田的必要性、合理性，占用和补划永久基本农田方案可行。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page8():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        国土空间用途管制处

        ### 二、审查标准  
        1. 涉及征收农民集体所有的土地的，应符合《土地管理法》第四十五条规定的情形和条件。
        2. 征收土地应符合国民经济和社会发展规划、国土空间规划、专项规划；扶贫搬迁、保障性安居工程、成片开发还应符合国民经济和社会发展年度计划；以成片开发方式报批的城镇用地还应当符合已经批准的成片开发方案。
        3. 县级以上地方人民政府应依法完成征地前期工作后，方可申请征收土地，并就按规定履行土地征收报批前期有关程序出具结论性意见。
        4. 以成片开发方式报批用地的，应纳入经批准的成片开发方案范围内；以成片开发方式实施土地征收的，应按规定完成成片开发年度实施计划。
        5. 县级人民政府已依法履行征地报批前期程序，涉及的被征地农民社保情况已按规定通过审核。
        6. 张贴公告后，应拍摄公告张贴的远景概貌照片、近景位置照片和重点位置照片，做好资料留存。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page9():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        自然保护地管理处、历史文化保护处

        ### 二、审查标准  
        1. 项目用地应避让古树名木、历史文化名镇名村、传统村落、文物保护单位等。
        2. 确实无法避让的，应按规定取得相关主管部门同意意见。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page10():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        执法局

        ### 二、审查标准  
        1. 应当明确是否存在违法用地，如存在应已查处并落实到位。
        2. 违法用地涉及生态保护红线、自然保护区的，应按规定处理。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page11():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        矿产资源保护监督处、行政审批管理处

        ### 二、审查标准  
        1. 单独选址项目应核实是否压覆重要矿产资源。
        2. 单独选址项目压覆重要矿产资源的，应取得同意压覆的意见。
        3. 单独选址项目压覆重要矿产资源的，按规定组织安全论证，且结论为项目建设不影响矿产资源合理开采利用的，不做压覆处理。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page12():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        地质勘查管理处

        ### 二、审查标准  
        1. 单独选址项目不位于地质灾害易发区的，建设单位不需要对项目进行地质灾害危险性评估。
        2. 单独选址项目位于地质灾害易发区的，建设单位已按规定完成地质灾害危险性评估。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template

def page13():
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        办公室

        ### 二、审查标准  
        存在的信访问题已妥善解决。
        """)
    
    template = """
        这里先空着，后续再补充
        """
    return template
if __name__ == "__main__":
    # 选择用地类型
    land_type = st.sidebar.radio(
        "选择用地类型:",
        ('单独选址', '批次用地'),
        index=1,
        horizontal=False
    )
    # 确保default_values是字典类型
    if 'default_values' not in st.session_state or not isinstance(st.session_state.default_values, dict):
        st.session_state.default_values = {}
    # 将用地类型存储在字典中
    st.session_state.default_values['用地类型'] = land_type
    # 单元选择下拉列表
    unit_options = {
        1: "1. 基本情况",
        2: "2. 审核许可",
        3: "3. 计划指标",
        4: "4. 土地预审",
        5: "5. 权属地类",
        6: "6. 国土空间规划",
        7: "7. 耕地占补平衡及永久基本农田占用补划",
        8: "8. 土地征收",
        9: "9. 土地利用",
        10: "10. 违法用地",
        11: "11. 压矿情况",
        12: "12. 地灾情况",
        13: "13. 信访情况"
    }
    selected_unit = st.sidebar.selectbox("选择单元:", options=list(unit_options.keys()), format_func=lambda x: unit_options[x])
    
    # 根据selected_unit提供不同的template
    if selected_unit == 1:
        template = page1()
    elif selected_unit == 2:
        template = page2()
    elif selected_unit == 3:
        template = page3()
    elif selected_unit == 4:
        template = page4()
    elif selected_unit == 5:
        template = page5()
    elif selected_unit == 6:
        template = page6()
    elif selected_unit == 7:
        template = page7()
    elif selected_unit == 8:
        template = page8()
    elif selected_unit == 9:
        template = page9()
    elif selected_unit == 10:
        template = page10()
    elif selected_unit == 11:
        template = page11()
    elif selected_unit == 12:
        template = page12()
    elif selected_unit == 13:
        template = page13()
    else:
        template = ""
    
    # 开始解析并渲染
    if template.strip():
        main(template)