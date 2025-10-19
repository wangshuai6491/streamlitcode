import streamlit as st
import re

# 模板内容
singleSiteTemplate = """三、审查内容模板

（一）单独选址

（用地预审情况）该项目符合基本建设投资管理规定。{[预审年月]}通过{[预审部门]}用地预审（文号{[预审文号]}）或按照{[预审规定]}，审批权下放至{[预审下放部门]}办理，{[预审下放年月]}，该项目通过{[预审下放部门全称]}用地预审（文号{[预审下放文号]}）。

（可研批复情况）{[可研批复年月]}，{[可研批复部门]}批复（或核准、备案）可行性研究报告（或项目申请报告，文号{[可研批复文号]}）或按照{[可研规定]}，审批权下放至{[可研下放部门]}办理，{[可研下放部门全称]}批复（或核准、备案）可行性研究报告（或项目申请报告，文号{[可研下放文号]}），2024年以后通过预审的项目增加表述：可行性研究报告或项目申请报告已包含用地预审审查后的节约集约用地专章相关内容。可研批复情况以下情形中选一：①用地预审在批复可行性研究报告（核准）或项目申请报告之后需增加表述：{[投资主管部门说明]}；②已超出核准有效期需增加表述：{[核准有效期说明]}；③可研变更需增加表述：{[可研变更表述]}。

（初步设计批复情况）{[初设批复年月]}，{[初设批复部门]}批复（或审核通过）工程初步设计（文号{[初设批复文号]}）。初步设计变更情况以下情形中选一：①{[初设变更年月]}，{[初设变更部门]}批复（或审核通过）工程初步设计变更（文号{[初设变更文号]}）。②按照{[初设变更规定]}，审批权下放至{[初设变更下放部门]}办理，{[初设变更下放年月]}，{[初设变更下放部门全称]}批复（或审核通过）工程初步设计变更（文号{[初设变更下放文号]}）。

项目按{[建设标准或规模]}建设，总投资{[总投资]}亿元。分期分段报批情况以下情形中选一：①项目用地涉及{[涉及地市1]}、{[涉及地市2]}，已批准{[已批地市]}用地{[已批面积]}公顷，批准文号为{[已批文号]}，本次呈报{[本次呈报地市]}用地（{[本次建设标准或规模]}），涉及投资{[本次投资]}亿元。②根据项目可行性研究报告确定的方案或可行性研究批复，项目分{[分期总数]}期建设，本次呈报为{[本期]}期用地（{[本期建设标准或规模]}），涉及投资{[本期投资]}亿元。{[永久基本农田或红线表述]}

（核减用地情况）以下情形中选一：
①该项目用地在市、县级审查中未核减用地。
②该项目用地在市、县级审查中核减用地{[核减总面积]}公顷（耕地{[核减耕地]}公顷，含永久基本农田{[核减永久基本农田]}公顷）。

[农用地转用情况] 本次申请将农用地{[转用农用地]}公顷（耕地{[转用耕地]}公顷、含永久基本农田{[转用永久基本农田]}公顷）、未利用地{[转用未利用地]}公顷转为建设用地，其中，{[集体农用地地市]}农民集体所有农用地{[集体农用地]}公顷（耕地{[集体耕地]}公顷、永久基本农田{[集体永久基本农田]}公顷）、未利用地{[集体未利用地]}公顷；国有农用地{[国有农用地]}公顷（耕地{[国有耕地]}公顷、永久基本农田{[国有永久基本农田]}公顷）、未利用地{[国有未利用地]}公顷。

{[矿业用地复垦利用表述]}

（缴纳新增建设用地土地有偿使用费情况）以下情形中选一：
①项目建设涉及国土空间规划确定的城市和村庄、集镇建设用地范围外{[规划范围外说明]}有偿使用新增建设用地{[范围外新增]}公顷，其中：{[范围外等别详情]}；项目用地中{[范围内用地]}公顷位于国土空间规划确定的城市和村庄、集镇建设用地范围内{[规划范围内说明]}，涉及新增建设用地{[范围内新增]}公顷，其中：{[范围内等别详情]}，共需缴纳新增建设用地土地有偿使用费{[应缴费用]}万元。项目所在地{[缴费承诺地市]}人民政府承诺在批准用地后按有关规定及时足额缴纳（或当地市县人民政府已按有关规定预缴）。
②项目以划拨方式供地，不涉及国土空间规划确定的城市和村庄、集镇建设用地范围内{[规划范围内说明]}新增建设用地，按规定不需缴纳新增建设用地土地有偿使用费。

{[违法用地表述]}
"""

batchLandTemplate = """三、审查内容模板

（二）批次用地

[基本情况] 该批次实际申请用地情况为：总面积为{[批次总面积]}公顷，其中，农用地{[批次农用地]}公顷（其中耕地{[批次耕地]}公顷；可调整地类{[可调整地类]}公顷）、建设用地{[批次建设用地]}公顷、未利用地{[批次未利用地]}公顷。{[违法用地可调整说明]}

按权属和地类分：农民集体所有土地{[集体土地总面积]}公顷，其中：农用地{[集体农用地]}公顷（耕地{[集体耕地]}公顷）、建设用地{[集体建设用地]}公顷、未利用地{[集体未利用地]}公顷；国有土地{[国有土地总面积]}公顷，其中：农用地{[国有农用地]}公顷（耕地{[国有耕地]}公顷）、建设用地{[国有建设用地]}公顷、未利用地{[国有未利用地]}公顷，地类和面积准确。

[农用地转用情况] 该批次申请将农用地{[批次转用农用地]}公顷（耕地{[批次转用耕地]}公顷）、未利用地{[批次转用未利用地]}公顷转为建设用地，其中，农民集体所有农用地{[集体转用农用地]}公顷（耕地{[集体转用耕地]}公顷）、未利用地{[集体转用未利用地]}公顷；国有农用地{[国有转用农用地]}公顷（耕地{[国有转用耕地]}公顷）、未利用地{[国有转用未利用地]}公顷。

{[增减挂钩表述]}

[缴纳新增建设用地土地有偿使用费] 该批次涉及新增建设用地{[批次新增建设用地]}公顷，为{[批次等别]}等别，需缴纳新增建设用地土地有偿使用费{[批次应缴费用]}万元。{[批次缴费承诺]}。

{[不缴纳有偿使用费表述]}
"""

# 提取模板中的所有参数
def extract_params(template):
    return re.findall(r"\{\[([^\]]+)\]\}", template)

# 替换模板中的参数为输入框
def render_template_with_inputs(template, params_values):
    # 先替换固定条件文本
    if 'single' in st.session_state.land_use_type:
        if st.session_state.involve_farmland or st.session_state.involve_eco_redline:
            template = template.replace(
                "{[永久基本农田或红线表述]}",
                "【本次报批不涉及占用永久基本农田或生态保护红线，但需报国务院审批的增加表述：该项目整体占用永久基本农田或生态保护红线，本段不涉及永久基本农田或生态保护红线，按规定应呈报国务院审批。】"
            )
        else:
            template = template.replace("{[永久基本农田或红线表述]}", "")

        if st.session_state.has_illegal_land:
            template = template.replace(
                "{[违法用地表述]}",
                "（违法用地占用自然保护区或生态保护红线情况）该项目违法用地涉及自然保护区或生态保护红线，省级林草主管部门对违法用地占用自然保护区或生态保护红线出具了意见，说明项目不涉及破坏森林草原湿地或违反自然保护区风景名胜区等管理规定的情形【或：说明存在上述情形已经处罚】；省级生态环境主管部门对违法用地占用自然保护区或生态保护红线占用出具了意见，说明未发现项目破坏生态环境的行为【或：说明存在破坏生态环境的行为已经处罚】。"
            )
        else:
            template = template.replace("{[违法用地表述]}", "")

        template = template.replace("{[矿业用地复垦利用表述]}", "")
    else:
        if not st.session_state.has_illegal_land:
            template = template.replace(
                "{[违法用地可调整说明]}",
                "（无违法用地或2020年之后发生的违法用地，不需说明占用可调整地类情况）"
            )
        else:
            template = template.replace("{[违法用地可调整说明]}", "")

        template = template.replace("{[增减挂钩表述]}", "")
        template = template.replace("{[不缴纳有偿使用费表述]}", "")

    # 替换参数为输入框
    parts = re.split(r"(\{\[([^\]]+)\]\})", template)
    result = []
    for part in parts:
        m = re.match(r"\{\[([^\]]+)\]\}", part)
        if m:
            param = m.group(1)
            result.append(
                st.text_input(
                    param,
                    value=params_values.get(param, ""),
                    key=f"input_{param}",
                    label_visibility="collapsed"
                )
            )
        else:
            result.append(part)
    return result

# 生成最终文本
def generate_final_text(template, params_values):
    final = template
    # 替换参数值
    for param, value in params_values.items():
        final = final.replace(f "{{[{param}]}}", value or f"{{[{param}（未填写）]}}")
    
    # 替换固定条件文本
    if 'single' in st.session_state.land_use_type:
        if st.session_state.involve_farmland or st.session_state.involve_eco_redline:
            final = final.replace(
                "{[永久基本农田或红线表述]}",
                "【本次报批不涉及占用永久基本农田或生态保护红线，但需报国务院审批的增加表述：该项目整体占用永久基本农田或生态保护红线，本段不涉及永久基本农田或生态保护红线，按规定应呈报国务院审批。】"
            )
        else:
            final = final.replace("{[永久基本农田或红线表述]}", "")

        if st.session_state.has_illegal_land:
            final = final.replace(
                "{[违法用地表述]}",
                "（违法用地占用自然保护区或生态保护红线情况）该项目违法用地涉及自然保护区或生态保护红线，省级林草主管部门对违法用地占用自然保护区或生态保护红线出具了意见，说明项目不涉及破坏森林草原湿地或违反自然保护区风景名胜区等管理规定的情形【或：说明存在上述情形已经处罚】；省级生态环境主管部门对违法用地占用自然保护区或生态保护红线占用出具了意见，说明未发现项目破坏生态环境的行为【或：说明存在破坏生态环境的行为已经处罚】。"
            )
        else:
            final = final.replace("{[违法用地表述]}", "")

        final = final.replace("{[矿业用地复垦利用表述]}", "")
    else:
        if not st.session_state.has_illegal_land:
            final = final.replace(
                "{[违法用地可调整说明]}",
                "（无违法用地或2020年之后发生的违法用地，不需说明占用可调整地类情况）"
            )
        else:
            final = final.replace("{[违法用地可调整说明]}", "")

        final = final.replace("{[增减挂钩表述]}", "")
        final = final.replace("{[不缴纳有偿使用费表述]}", "")
    
    return final

def main():
    st.set_page_config(page_title="基本情况单元 - 填空式模板写作系统", layout="wide")
    
    # 初始化会话状态
    if 'land_use_type' not in st.session_state:
        st.session_state.land_use_type = "single"
    if 'involve_farmland' not in st.session_state:
        st.session_state.involve_farmland = False
    if 'involve_eco_redline' not in st.session_state:
        st.session_state.involve_eco_redline = False
    if 'has_illegal_land' not in st.session_state:
        st.session_state.has_illegal_land = False
    if 'params_values' not in st.session_state:
        st.session_state.params_values = {}
    if 'final_text' not in st.session_state:
        st.session_state.final_text = ""
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False

    # 页面标题
    st.title("基本情况单元 - 填空式模板写作系统")

    # 固定内容
    st.markdown("""
    ## 一、业务指导处室
    国土空间用途管制处

    ## 二、审查标准
    - 符合基本建设投资管理规定。
    - 建设单位已取得建设项目批准（核准或备案）文件、初步设计批准或审核文件，且应当在有效期内。
    - 用地涉及的新增建设用地应按规定缴纳新增建设用地土地有偿使用费，缴纳等级、标准应准确。
    - 1999年1月1日之后经依法批准的集体建设用地，在批准农用地转用时未缴纳新增建设用地有偿使用费的，申请土地征收时按照现行标准补缴。
    """)

    # 条件选择
    st.subheader("条件选择")
    
    col1, col2 = st.columns(2)
    with col1:
        land_use = st.radio("用地类型", ["单独选址", "批次用地"], index=0 if st.session_state.land_use_type == "single" else 1)
        st.session_state.land_use_type = "single" if land_use == "单独选址" else "batch"

        involve_farmland = st.radio("是否涉及永久基本农田", ["否", "是"], index=0 if not st.session_state.involve_farmland else 1)
        st.session_state.involve_farmland = (involve_farmland == "是")
    with col2:
        involve_eco = st.radio("是否涉及生态保护红线", ["否", "是"], index=0 if not st.session_state.involve_eco_redline else 1)
        st.session_state.involve_eco_redline = (involve_eco == "是")

        has_illegal = st.radio("是否存在违法用地", ["否", "是"], index=0 if not st.session_state.has_illegal_land else 1)
        st.session_state.has_illegal_land = (has_illegal == "是")

    # 选择模板
    current_template = singleSiteTemplate if st.session_state.land_use_type == "single" else batchLandTemplate
    
    # 提取参数
    params = extract_params(current_template)
    
    # 保存参数值
    for param in params:
        value = st.session_state.get(f"input_{param}", "")
        st.session_state.params_values[param] = value

    # 渲染模板和输入框
    st.subheader("模板内容（请填写）")
    rendered = render_template_with_inputs(current_template, st.session_state.params_values)
    
    # 按钮
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("生成最终文本"):
            st.session_state.final_text = generate_final_text(current_template, st.session_state.params_values)
            st.session_state.show_result = True
    with col_btn2:
        if st.button("复制结果") and st.session_state.show_result:
            st.write("已复制到剪贴板（Streamlit 内无法直接访问剪贴板，建议手动复制下方结果）")
    with col_btn3:
        if st.button("重置"):
            st.session_state.params_values = {}
            st.session_state.final_text = ""
            st.session_state.show_result = False
            st.experimental_rerun()

    # 结果展示
    if st.session_state.show_result:
        st.subheader("生成结果")
        st.text_area("最终文本", st.session_state.final_text, height=400)

if __name__ == "__main__":
    main()
