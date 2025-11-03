# 10: 违法用地单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group
def page_10():
    st.subheader("10: 违法用地单元")
    # 头部信息（默认折叠）
    with st.expander("基本信息（点击展开）", expanded=False):
        st.markdown("""
        ### 一、业务指导处室  
        执法局

        ### 二、审查标准  
        1. 应当明确是否存在违法用地，如存在应已查处并落实到位。
        2. 违法用地涉及生态保护红线、自然保护区的，应按规定处理。
        """)
    
    # 添加判断按钮，让用户选择是否涉及违法用地（横向排列）
    st.subheader("违法用地情形")
    illegal_land_case = button_group(
        "",
        options=[{"label": "不涉及违法用地", "value": "不涉及违法用地"}, {"label": "有违法用地", "value": "违法用地"}],
        default_value="不涉及违法用地",
        key="illegal_land_case_select"
    )
    
    # 如果选择不涉及违法用地，再询问临时用地情况
    temp_land_case = None
    if illegal_land_case == '不涉及违法用地':
        temp_land_case = button_group(
            "",
            options=[{"label": "无临时用地", "value": "无临时用地"}, {"label": "有临时用地", "value": "有临时用地"}],
            default_value="无临时用地",
            key="temp_land_case_select"
        )
    
    # 设置默认变量缓存
    defaults = {
        '违法用地情形': illegal_land_case,
        '临时用地情况': temp_land_case,
        '批准临时用地面积': '0.00',
        '临时用地用途': '临时堆放',
        '临时用地批准起始年月': '2025年1月',
        '临时用地批准结束年月': '2025年12月',
        '实际临时用地面积': '0.00',
        '实际临时用途': '临时堆放',
        '违法用地总面积': '0.00',
        '违法新增面积': '0.00',
        '违法农用地': '0.00',
        '违法耕地': '0.00',
        '违法未利用地': '0.00',
        '处罚机关': 'XX自然资源局',
        '处罚决定年月': '2025年6月',
        '处罚决定书文号': 'XX自然资罚[2025]XX号',
        '罚款标准': 'XX元/平方米',
        '罚款金额': '0.00',
        '处罚执行到位年月': '2025年7月',
        '责任人姓名': '张三',
        '处分类型': '警告'
    }
    
    # 根据用户选择生成相应的模板内容
    if illegal_land_case == '不涉及违法用地':
        if temp_land_case == '无临时用地':
            # 无临时用地的模板
            fixed_template = '''〔违法用地情形〕 经我局核查，该批次用地未动工，不存在违法用地问题。'''  
        else:
            # 有临时用地的模板
            fixed_template = '''〔违法用地情形〕 经我局核查，该批次用地范围内存在经批准的临时用地。批准临时用地面积{{ 批准临时用地面积 }}公顷，临时用地用途为{{ 临时用地用途 }}，批准起始年月为{{ 临时用地批准起始年月 }}至{{ 临时用地批准结束年月 }}。实际临时用地面积{{ 实际临时用地面积 }}公顷，实际临时用途为{{ 实际临时用途 }}。目前在临时使用及土地复垦期限内，符合临时用地批准条件。'''  
    else:
        # 违法用地的模板
        fixed_template = '''〔违法用地情形〕 经我局核查，该批次存在违法用地问题，具体情况如下：违法用地总面积{{ 违法用地总面积 }}公顷，涉及新增建设用地面积{{ 违法新增面积 }}公顷。其中农用地{{ 违法农用地 }}公顷（耕地{{ 违法耕地 }}公顷），未利用地{{ 违法未利用地 }}公顷。{{ 处罚机关 }}于{{ 处罚决定年月 }}作出{{ 处罚决定书文号 }}行政处罚决定，罚款标准为{{ 罚款标准 }}，罚款金额{{ 罚款金额 }}万元，并于{{ 处罚执行到位年月 }}执行到位。责任人{{ 责任人姓名 }}受到{{ 处分类型 }}处分。'''  

    # 确保session_state中存在default_values字典
    if 'default_values' not in st.session_state:
        st.session_state.default_values = {}
    
    # 更新默认值到session_state
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)

    # 生成唯一的key
    key_suffix = illegal_land_case
    if temp_land_case:
        key_suffix += "_" + temp_land_case

    # 调用组件，传递模板和默认值字典
    component_result = lineinput(
        fixed_template, 
        default_values=st.session_state.default_values.copy(),
        key="page_10_" + key_suffix
    )
    return component_result
