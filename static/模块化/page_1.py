# 1: 基本情况单元
import streamlit as st
from __init__ import lineinput
from common_components import button_group

def page_1():
    st.subheader("1: 基本情况单元")
    
    # 使用侧边栏中设置的用地类型
    land_type = st.session_state.land_type
    
    # 设置默认变量缓存
    defaults = {
        # 用地类型
        '用地类型': st.session_state.land_type,
        
        # 预审相关
        '审批权下放': '否',
        '下放依据': '下放依据',
        '审批权下放部门': '*审批权下放至*部门办理',
        '预审通过年月': '*年*月',
        '预审自然资源主管部门': '*省自然资源厅',
        '预审文号': 'XX预审〔202X〕XX号',
        
        # 可研相关
        '可研批复年月': '*年*月',
        '可研批复部门': '**发展改革部门等批复(或核准、备案)可行性研究报告（或项目申请报告）或按照*规定，**审批权下放至*部门办理，**部门批复（或核准、备案)可行性研究报告（或项目申请报告）',
        '可研批复文号': 'XX可研〔2024〕XX号',
        '_2024以后通过预审': '是',
        '用地预审在可研之后': '否',
        '投资主管部门': 'XX发展改革委',
        '核准超期': '未超期',
        '可研变更': '否',
        '可研变更批复年月': '*年*月',
        '可研变更批复部门': '**（国家发展改革委或地方发改部门等）批复（或核准、备案）可行性研究报告变更（或项目申请报告）；或按照**规定，**审批权下放至**部门办理，**部门批复（或核准、备案）可行性研究报告变更（或项目申请报告）。',
        '可研变更文号': 'XX可研变〔2024〕XX号',
        
        # 初设相关
        '初设批复年月': '*年*月',
        '初设审批部门': '**（行业主管部门或设计审核单位)批复（或审核通过）',
        '初设批复文号': 'XX初设〔2024〕XX号',
        '初设变更': '无变更',
        '初设变更审批权下放': '按照*规定，*审批权下放至*部门办理，',
        '初设变更批复年月': '*年*月',
        '初设变更批复部门': '**（行业主管部门或设计审核单位)批复（或审核通过）',
        '初设变更文号': 'XX初设变〔2024〕XX号',
        
        # 项目基本信息
        '建设标准或规模': '*(建设标准或规模)建设',
        '总投资': '0',
        '分期分段': '否',
        '按市报批': '项目用地涉及**市、**市，已批准*市用地*公顷，批准文号为*，本次呈报**市用地（建设标准或规模)，涉及投资**亿元。',
        '分期报批': '根据项目可行性研究报告确定的方案或可行性研究批复，项目分**期建设，本次呈报为*期用地（建设标准或规模），涉及投资**亿元。',
        '本期不涉及永农红线但需报国务院': '否',
        
        # 核减用地情况
        '市县核减': '未核减',
        '核减面积': '0.0000',
        '核减耕地': '0.0000',
        '核减永农': '0.0000',
        
        # 农用地转用情况
        '转用农用地': '0.0000',
        '转用耕地': '0.0000',
        '转用永农': '0.0000',
        '转用未利用地': '0.0000',
        '市县区列表': '**市**区、**县',
        '集体转用农用地': '0.0000',
        '集体转用耕地': '0.0000',
        '集体转用永农': '0.0000',
        '集体转用未利用地': '0.0000',
        '国有转用农用地': '0.0000',
        '国有转用耕地': '0.0000',
        '国有转用永农': '0.0000',
        '国有转用未利用地': '0.0000',
        
        # 矿业复垦
        '矿业复垦': '否',
        '复垦验收自然资源部门': 'XX自然资源局',
        '复垦耕地': '0.0000',
        '复垦水田': '0.0000',
        '复垦产能': '100000',
        '拟用面积': '0.0000',
        '拟用水田': '0.0000',
        '拟用产能': '100',
        
        # 缴纳新增建设用地土地有偿使用费情况
        '缴费情形': '有偿使用',
        '审查机关': 'XX自然资源厅',
        '圈外新增面积': '8.0',
        '圈外县区列表': '[{"name":"XX县","等别":"五","area":"8.0"}]',
        '圈内新增面积': '2.0',
        '圈内县区列表': '[{"name":"XX县","等别":"五","area":"2.0"}]',
        '应缴有偿费': '100',
        '缴费县市区的市县人民政府名称': 'XX县',
        
        # 违法用地占用自然保护区或生态保护红线情况
        '违法涉及保护地': '否',
        '省林草意见': '说明项目不涉及破坏森林草原湿地或违反自然保护区风景名胜区等管理规定的情形【或：说明存在上述情形已经处罚】',
        '省生态环境意见': '说明未发现项目破坏生态环境的行为【或：说明存在破坏生态环境的行为已经处罚】。',
        
        # 批次用地相关
        # 基本情况
        '总面积': '0.0000',
        '农用地面积': '0.0000',
        '耕地面积': '0.0000',
        '可调整地类面积': '0.0000',
        '建设用地面积': '0.0000',
        '未利用地面积': '0.0000',
        '违法用地年份': '*',
        '无违法用地': '否',
        '集体土地总面积': '0.0000',
        '集体农用地': '0.0000',
        '集体耕地': '0.0000',
        '集体建设用地': '0.0000',
        '集体未利用地': '0.0000',
        '国有土地总面积': '0.0000',
        '国有农用地': '0.0000',
        '国有耕地': '0.0000',
        '国有建设用地': '0.0000',
        '国有未利用地': '0.0000',
        # 农转用情况
        '批次类型': '普通批次',
        '指标来源': 'XX县自行复垦的增减挂钩指标（或购买XX县的增减挂钩节余指标',
        '挂钩指标面积': '0.0000',
        '挂钩水田': '0.0000',
        '挂钩产能': '0.0000',
        '新区拟用面积': '0.0000',
        '新区水田': '0.0000',
        '新区产能': '0.0000',
        '分次报批': '否',
        '已用面积': '0.0000',
        '已用水田': '0.0000',
        '已用产能': '0.0000',
        '本次报批面积': '0.0000',
        '本次水田': '0.0000',
        '本次产能': '0.0000',
        '剩余面积': '0.0000',
        '剩余水田': '0.0000',
        '剩余产能': '0.0000',
        '涉及新增建设用地': '是',
        '新增建设用地面积': '0.0000',
        '土地等别': '五',
        '应缴费用': '100',
        '缴存方式': '承诺缴纳',
        '县市区名称': 'XX县'
    }

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
    # 初始化返回结果
    component_result = {}
    
    # 存储每个区块的结果
    all_results = {}
    
    # 根据用地类型分别处理不同区块
    if land_type == '单独选址':
        # 区块1: 用地预审情况
        st.markdown("### 〔用地预审情况〕")
        # 判断区域
        审批权下放 = button_group(
            label="",
            options=[{"label": "审批权下放", "value": "是"}, {"label": "否", "value": "否"}],
            default_value="否",
            key="审批权下放"
        )
        # 根据判断结果生成不同的模板
        if 审批权下放 == "是":
            block1_template = '''该项目符合基本建设投资管理规定。按照{{ 下放依据 }}规定，{{ 审批权下放部门 }}，{{ 预审通过年月 }}，该项目通过{{ 预审自然资源主管部门 }}用地预审（文号：{{ 预审文号 }}）。'''
        else:
            block1_template = '''该项目符合基本建设投资管理规定。{{ 预审通过年月 }}通过{{ 预审自然资源主管部门 }}用地预审（文号：{{ 预审文号 }}）。'''
        all_results['block1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block1"
        )
        
        # 区块2: 可研批复情况
        st.markdown("### 〔可研批复情况〕")
        # 判断条件
        _2024以后通过预审 = button_group(
            label="",
            options=[{"label": "2024年以后通过预审", "value": "是"}, {"label": "不是", "value": "否"}],
            default_value="否",
            key="_2024以后通过预审"
        )
        用地预审在可研之后 = button_group(
            label="",
            options=[{"label": "用地预审在可研之后", "value": "是"}, {"label": "不是", "value": "否"}],
            default_value="否",
            key="用地预审在可研之后"
        )

        可研变更 = button_group(
            label="",
            options=[{"label": "可研有变更", "value": "是"}, {"label": "没变更", "value": "否"}],
            default_value="否",
            key="可研变更"
        )
        核准超期 = st.selectbox(
            label="核准文件超期情况",
            options=[
                "未超期",
                "项目核准文件超出有效期但项目单位在核准有效期内提出用地申请",
                "项目超出核准有效期但已获得原批准机关核准延期批复",
                "项目超出核准有效期但已获得原批准机关核准延期说明"
            ],
            index=0,
            key="核准超期"
        )
        st.session_state.default_values['核准超期'] = 核准超期
        # 根据判断结果生成不同的模板
        block2_template = '''{{ 可研批复年月 }}，{{ 可研批复部门 }}（文号：{{ 可研批复文号 }}）。'''
        
        # 添加附加内容
        if _2024以后通过预审 == "是":
            block2_template += '''可行性研究报告（或项目申请报告）已包含用地预审审查后的节约集约用地专章相关内容。'''
        if 用地预审在可研之后 == "是":
            block2_template += '''{{ 投资主管部门 }}已出具书面说明并检讨。'''
        if 核准超期 == "项目核准文件超出有效期但项目单位在核准有效期内提出用地申请":
            block2_template += '''项目核准文件超出有效期，但项目单位在核准有效期内提出用地申请。'''
        elif 核准超期 == "项目超出核准有效期但已获得原批准机关核准延期批复":
            block2_template += '''项目超出核准有效期，但已获得原批准机关核准延期批复。'''
        elif 核准超期 == "项目超出核准有效期但已获得原批准机关核准延期说明":
            block2_template += '''项目超出核准有效期，但已获得原批准机关核准延期说明。'''
        if 可研变更 == "是":
            block2_template += '''{{ 可研变更批复年月 }}，{{ 可研变更批复部门 }}（文号：{{ 可研变更文号 }}）。'''
        
        all_results['block2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block2"
        )
        
        # 区块3: 初步设计批复情况
        st.markdown("### 〔初步设计批复情况〕")
        # 判断区域
        初设变更 = button_group(
            label="",
            options=[
                {"label": "无变更", "value": "无变更"},
                {"label": "正常审批", "value": "正常审批"},
                {"label": "权力下放审批", "value": "权力下放审批"}
            ],
            default_value="无变更",
            key="初设变更"
        )
        # 更新会话状态
        st.session_state.default_values['初设变更'] = 初设变更
        # 根据判断结果生成不同的模板
        block3_template = '''{{初设批复年月}}，{{初设审批部门}}工程初步设计（文号：{{初设批复文号}}）。'''
        if 初设变更 == "正常审批":
            block3_template += '''{{初设变更批复年月}}，{{初设变更审批部门}}工程初步设计变更（文号：{{初设批复文号}}）。'''
        elif 初设变更 == "权力下放审批":
            block3_template += '''{{初设变更审批权下放}}，{{初设变更批复年月}}，{{初设变更审批部门}}工程初步设计变更（文号：{{初设批复文号}}）。'''
        
        all_results['block3'] = lineinput(
            block3_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block3"
        )
        
        # 判断区域

        分期分段 = button_group(
            label="分期分段",
            options=[{"label": "无分期分段", "value": "无"}, {"label": "按市报批", "value": "按市报批"}, {"label": "分期报批", "value": "分期报批"}],
            default_value="无",
            key="分期分段"
        )

        本期不涉及永农红线但需报国务院 = button_group(
            label="",
            options=[{"label": "本期不涉及永农红线但需报国务院", "value": "是"}, {"label": "不存在此类情况", "value": "否"}],
            default_value="否",
            key="本期不涉及永农红线但需报国务院"
        )

        # 根据判断结果生成不同的模板
        paragraph_template = '''项目按{{ 建设标准或规模 }}，总投资{{ 总投资 }}亿元。'''
        if 分期分段 == "按市报批":
            paragraph_template += '''{{按市报批}}'''
        elif 分期分段 == "分期报批":
            paragraph_template += '''{{分期报批}}'''
        if 本期不涉及永农红线但需报国务院 == "是":
            paragraph_template += '''该项目整体占用永久基本农田或生态保护红线，本段不涉及永久基本农田或生态保护红线，按规定应呈报国务院审批。'''
        
        all_results['paragraph'] = lineinput(
            paragraph_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_paragraph"
        )
        
        # 区块4: 核减用地情况
        st.markdown("### 〔核减用地情况〕")
        # 判断区域
        市县核减 = button_group(
            label="",
            options=[{"label": "未核减", "value": "未核减"}, {"label": "有核减", "value": "有核减"}],
            default_value="未核减",
            key="市县核减"
        )
        # 更新会话状态
        st.session_state.default_values['市县核减'] = 市县核减
        # 根据判断结果生成不同的模板
        if 市县核减 == "有核减":
            block4_template = '''该项目用地在市、县级审查中核减用地{{ 核减面积 }}公顷（耕地{{ 核减耕地 }}公顷，含永久基本农田{{ 核减永农 }}公顷）。'''
        else:
            block4_template = '''该项目用地在市、县级审查中未核减用地。'''
        
        all_results['block4'] = lineinput(
            block4_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block4"
        )
        
        # 区块5: 农用地转用情况
        st.markdown("### 〔农用地转用情况〕")
        # 判断区域
        矿业复垦 = button_group(
            label="",
            options=[{"label": "属于矿业复垦", "value": "是"}, {"label": "不属于矿业复垦", "value": "否"}],
            default_value="否",
            key="矿业复垦"
        )
        # 更新会话状态
        st.session_state.default_values['矿业复垦'] = 矿业复垦
        # 生成基础模板
        block5_template = '''本次申请将农用地{{ 转用农用地 }}公顷（耕地{{ 转用耕地 }}公顷，含永久基本农田{{ 转用永农 }}公顷）、未利用地{{ 转用未利用地 }}公顷转为建设用地，其中，{{ 市县区列表 }}农民集体所有农用地{{ 集体转用农用地 }}公顷（耕地{{ 集体转用耕地 }}公顷，永久基本农田{{ 集体转用永农 }}公顷）、未利用地{{ 集体转用未利用地 }}公顷；国有农用地{{ 国有转用农用地 }}公顷（耕地{{ 国有转用耕地 }}公顷，永久基本农田{{ 国有转用永农 }}公顷）、未利用地{{ 国有转用未利用地 }}公顷。'''
        
        # 根据判断结果添加附加内容
        if 矿业复垦 == "是":
            block5_template += '''{{ 复垦验收自然资源部门 }}已验收该项目复垦区耕地{{ 复垦耕地 }}公顷，其中水田{{ 复垦水田 }}公顷，标准粮食产能{{ 复垦产能 }}公斤；拟使用土地{{ 拟用面积 }}公顷，其中水田{{ 拟用水田 }}公顷，标准粮食产能{{ 拟用产能 }}公斤。建设区土地已全部转为建设用地。'''
        
        all_results['block5'] = lineinput(
            block5_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block5"
        )
        
        # 区块6: 缴纳新增建设用地土地有偿使用费情况
        st.markdown("### 〔缴纳新增建设用地土地有偿使用费情况〕")
        # 判断区域
        表述方式 = button_group(
            label="",
            options=[{"label": "表述方式1", "value": "方式1"}, {"label": "表述方式2", "value": "方式2"}],
            default_value="表述方式1",
            key="表述方式"
        )

        缴费情形 = button_group(
            label="",
            options=[{"label": "有偿使用", "value": "有偿使用"}, {"label": "以划拨方式供地", "value": "以划拨方式供地"}],
            default_value="有偿使用",
            key="缴费情形"
        )

        # 仅在有偿使用情形下显示表格输入
        if 缴费情形 == "有偿使用":
            # 圈外县区列表表格输入
            st.subheader("圈外县区列表")
            # 初始化圈外县区列表
            if '圈外县区_list' not in st.session_state:
                st.session_state['圈外县区_list'] = []
                # 尝试从默认值中解析JSON
                if '圈外县区列表' in st.session_state.default_values:
                    try:
                        import json
                        st.session_state['圈外县区_list'] = json.loads(st.session_state.default_values['圈外县区列表'])
                    except:
                        st.session_state['圈外县区_list'] = [{'name': 'XX县', '等别': '五', 'area': '8.0'}]
            
            # 显示当前表格数据
            for i, item in enumerate(st.session_state['圈外县区_list']):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    item['name'] = st.text_input(f"县区名称 {i+1}", value=item['name'], key=f"圈外名称_{i}")
                with col2:
                    item['等别'] = st.text_input(f"等别 {i+1}", value=item['等别'], key=f"圈外等别_{i}")
                with col3:
                    item['area'] = st.text_input(f"面积(公顷) {i+1}", value=item['area'], key=f"圈外面积_{i}")
                with col4:
                    if st.button("删除", key=f"圈外删除_{i}"):
                        st.session_state['圈外县区_list'].pop(i)
                        st.experimental_rerun()
            
            # 添加新行按钮
            if st.button("添加圈外县区"):
                st.session_state['圈外县区_list'].append({'name': '', '等别': '', 'area': ''})
                st.experimental_rerun()
            
            # 圈内县区列表表格输入
            st.subheader("圈内县区列表")
            # 初始化圈内县区列表
            if '圈内县区_list' not in st.session_state:
                st.session_state['圈内县区_list'] = []
                # 尝试从默认值中解析JSON
                if '圈内县区列表' in st.session_state.default_values:
                    try:
                        import json
                        st.session_state['圈内县区_list'] = json.loads(st.session_state.default_values['圈内县区列表'])
                    except:
                        st.session_state['圈内县区_list'] = [{'name': 'XX县', '等别': '五', 'area': '2.0'}]
            
            # 显示当前表格数据
            for i, item in enumerate(st.session_state['圈内县区_list']):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    item['name'] = st.text_input(f"县区名称 {i+1}", value=item['name'], key=f"圈内名称_{i}")
                with col2:
                    item['等别'] = st.text_input(f"等别 {i+1}", value=item['等别'], key=f"圈内等别_{i}")
                with col3:
                    item['area'] = st.text_input(f"面积(公顷) {i+1}", value=item['area'], key=f"圈内面积_{i}")
                with col4:
                    if st.button("删除", key=f"圈内删除_{i}"):
                        st.session_state['圈内县区_list'].pop(i)
                        st.experimental_rerun()
            
            # 添加新行按钮
            if st.button("添加圈内县区"):
                st.session_state['圈内县区_list'].append({'name': '', '等别': '', 'area': ''})
                st.experimental_rerun()
            
            # 更新会话状态中的JSON字符串
            import json
            st.session_state.default_values['圈外县区列表'] = json.dumps(st.session_state['圈外县区_list'], ensure_ascii=False)
            st.session_state.default_values['圈内县区列表'] = json.dumps(st.session_state['圈内县区_list'], ensure_ascii=False)
        
        # 根据判断结果生成不同的模板
        if 表述方式 == "方式1" and 缴费情形 == "有偿使用":
            # 构建圈外县区文本
            圈外文本 = ""
            for 县区 in st.session_state.get('圈外县区_list', []):
                if 县区['name'] and 县区['等别'] and 县区['area']:
                    圈外文本 += f"{县区['name']}{县区['等别']}等别{县区['area']}公顷、"
            # 构建圈内县区文本
            圈内文本 = ""
            for 县区 in st.session_state.get('圈内县区_list', []):
                if 县区['name'] and 县区['等别'] and 县区['area']:
                    圈内文本 += f"{县区['name']}{县区['等别']}等别{县区['area']}公顷、"
            
            block6_template = f'''项目建设涉及国土空间规划确定的城市和村庄、集镇建设用地范围外有偿使用新增建设用地{{ 圈外新增面积 }}公顷，其中：{圈外文本}；项目用地中{{ 圈内新增面积 }}公顷位于国土空间规划确定的城市和村庄、集镇建设用地范围内【或：{{ 审查机关 }}审查通过的国土空间规划确定的城市和村庄、集镇建设用地范围内】，涉及新增建设用地{{ 圈内新增面积 }}公顷，其中：{圈内文本}，共需缴纳新增建设用地土地有偿使用费{{ 应缴有偿费 }}万元。项目所在地{{ 缴费县市区的市县人民政府名称 }}人民政府承诺在批准用地后按有关规定及时足额缴纳（或已预缴）。'''
        elif 表述方式 == "方式2" and 缴费情形 == "有偿使用":
            # 构建圈外县区文本
            圈外文本 = ""
            for 县区 in st.session_state.get('圈外县区_list', []):
                if 县区['name'] and 县区['等别'] and 县区['area']:
                    圈外文本 += f"{县区['name']}{县区['等别']}等别{县区['area']}公顷、"
            # 构建圈内县区文本
            圈内文本 = ""
            for 县区 in st.session_state.get('圈内县区_list', []):
                if 县区['name'] and 县区['等别'] and 县区['area']:
                    圈内文本 += f"{县区['name']}{县区['等别']}等别{县区['area']}公顷、"
            
            block6_template = f'''项目建设涉及{{ 审查机关 }}审查通过的国土空间规划确定的城市和村庄、集镇建设用地范围外有偿使用新增建设用地{{ 圈外新增面积 }}公顷，其中：{圈外文本}；项目用地中{{ 圈内新增面积 }}公顷位于国土空间规划确定的城市和村庄、集镇建设用地范围内【或：{{ 审查机关 }}审查通过的国土空间规划确定的城市和村庄、集镇建设用地范围内】，涉及新增建设用地{{ 圈内新增面积 }}公顷，其中：{圈内文本}，共需缴纳新增建设用地土地有偿使用费{{ 应缴有偿费 }}万元。项目所在地{{ 缴费县市区的市县人民政府名称 }}人民政府承诺在批准用地后按有关规定及时足额缴纳（或已预缴）。'''
        elif 表述方式 == "方式2" and 缴费情形 == "以划拨方式供地":
            block6_template = '''项目以划拨方式供地，不涉及{{ 审查机关 }}审查通过的国土空间规划确定的城市和村庄、集镇建设用地范围内新增建设用地，按规定不需缴纳新增建设用地土地有偿使用费。'''
        elif 表述方式 == "方式1" and 缴费情形 == "以划拨方式供地":
            block6_template = '''项目以划拨方式供地，不涉及国土空间规划确定的城市和村庄、集镇建设用地范围内新增建设用地，按规定不需缴纳新增建设用地土地有偿使用费。'''
        
        all_results['block6'] = lineinput(
            block6_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block6"
        )
        
        # 区块7: 违法用地占用自然保护区或生态保护红线情况
        st.markdown("### 〔违法用地占用自然保护区或生态保护红线情况〕")
        # 判断区域
        违法涉及保护地 = button_group(
            label="",
            options=[{"label": "否", "value": "否"}, {"label": "是", "value": "是"}],
            default_value="否",
            key="违法涉及保护地"
        )
        # 更新会话状态
        st.session_state.default_values['违法涉及保护地'] = 违法涉及保护地
        # 根据判断结果生成不同的模板
        if 违法涉及保护地 == "是":
            block7_template = '''该项目违法用地涉及自然保护区或生态保护红线，省级林草主管部门对违法用地占用自然保护区或生态保护红线出具了意见，{{省林草意见}}；省级生态环境主管部门对违法用地占用自然保护区或生态保护红线出具了意见，{{省生态环境意见}}'''
        else:
            block7_template = ''''''
        
        all_results['block7'] = lineinput(
            block7_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_block7"
        )
    else:
        # 批次用地模板 - 区块1: 基本情况
        st.markdown("### 〔基本情况〕")
        # 判断区域
        有无可调整地类 = button_group(
            label="",
            options=[{"label": "有可调整地类", "value": "是"}, {"label": "无可调整地类", "value": "否"}],
            default_value="是",
            key="有无可调整地类"
        )
        # 更新会话状态
        st.session_state.default_values['有无可调整地类'] = 有无可调整地类
        # 根据判断结果生成不同的模板
        if 有无可调整地类 == "是":
            block1_template = '''该批次实际申请用地情况为：总面积{{总面积}}公顷，其中：农用地{{农用地面积}}公顷（耕地{{耕地面积}}公顷）、建设用地{{建设用地面积}}公顷、未利用地{{未利用地面积}}公顷。'''
        else:
            block1_template = '''该批次实际申请用地情况为：总面积{{总面积}}公顷，其中：农用地{{农用地面积}}公顷（耕地{{耕地面积}}公顷；可调整地类{{可调整地类面积}}公顷）、建设用地{{建设用地面积}}公顷、未利用地{{未利用地面积}}公顷。'''
        all_results['block1_1'] = lineinput(
            block1_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_batch_block1"
        )
        block1_template2 = '''按权属和地类分：农民集体所有土地{{集体土地总面积}}公顷，其中：农用地{{集体农用地}}公顷（耕地{{集体耕地}}公顷）、建设用地{{集体建设用地}}公顷、未利用地{{集体未利用地}}公顷；国有土地{{国有土地总面积}}公顷，其中：农用地{{国有农用地}}公顷（耕地{{国有耕地}}公顷）、建设用地{{国有建设用地}}公顷、未利用地{{国有未利用地}}公顷，地类和面积准确。'''
        all_results['block1_2'] = lineinput(
            block1_template2,
            default_values=st.session_state.default_values.copy(),
            key="page_1_batch_block1_2"
        )
        # 批次用地模板 - 区块2: 农用地转用情况
        st.markdown("### 〔农用地转用情况〕")
        # 判断区域
        批次类型 = button_group(
            label="",
            options=[{"label": "普通批次", "value": "普通批次"}, {"label": "增减挂钩批次", "value": "增减挂钩批次"}],
            default_value="普通批次",
            key="批次类型"
        )
        # 更新会话状态
        st.session_state.default_values['批次类型'] = 批次类型
         
        # 普通批次
        if 批次类型 == "普通批次":
            block2_template = '''该批次申请将农用地{{转用农用地}}公顷（耕地{{转用耕地}}公顷）、未利用地{{转用未利用地}}公顷转为建设用地，其中：农民集体所有农用地{{集体转用农用地}}公顷（耕地{{集体转用耕地}}公顷）、未利用地{{集体转用未利用地}}公顷；国有农用地{{国有转用农用地}}公顷（耕地{{国有转用耕地}}公顷）、未利用地{{国有转用未利用地}}公顷。'''
        elif 批次类型 == "增减挂钩批次":
            分次报批 = button_group(
                label="",
                options=[{"label": "一次性报批", "value": "否"}, {"label": "分次报批", "value": "是"}],
                default_value="否",
                key="分次报批"
            )
            # 更新会话状态
            st.session_state.default_values['分次报批'] = 分次报批
            block2_template = '''该批次使用{{指标来源}}{{挂钩指标面积}}公顷，其中水田{{挂钩水田}}公顷，标准粮食产能{{挂钩产能}}公斤；'''
            if 分次报批 == "否":
                block2_template += '''建新区拟使用土地{{新区拟用面积}}公顷，其中水田{{新区水田}}公顷，标准粮食产能{{新区产能}}公斤。建新区土地已全部转为建设用地。'''
            elif 分次报批 == "是":
                block2_template += '''建新区已使用{{已用面积}}公顷，其中水田{{已用水田}}公顷，标准粮食产能{{已用产能}}公斤；本次报批{{本次报批面积}}公顷，其中水田{{本次水田}}公顷，标准粮食产能{{本次产能}}公斤；剩余{{剩余面积}}公顷，其中水田{{剩余水田}}公顷，标准粮食产能{{剩余产能}}公斤。建新区土地已全部转为建设用地。'''
        
        all_results['block2'] = lineinput(
            block2_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_batch_block2"
        )
        
        # 批次用地模板 - 区块3: 缴纳新增建设用地土地有偿使用费
        st.markdown("### 〔缴纳新增建设用地土地有偿使用费〕")
        # 判断区域
        涉及新增建设用地 = button_group(
            label="",
            options=[{"label": "涉及新增建设用地", "value": "是"}, {"label": "不涉及", "value": "否"}],
            default_value="否",
            key="涉及新增建设用地"
        )
        # 更新会话状态
        st.session_state.default_values['涉及新增建设用地'] = 涉及新增建设用地
        
        # 嵌套判断
        缴存方式 = "承诺缴纳"
        if 涉及新增建设用地 == "是":
            缴存方式 = button_group(
                label="",
                options=[{"label": "承诺缴纳", "value": "承诺缴纳"}, {"label": "已预缴", "value": "已预缴"}],
                default_value="承诺缴纳",
                key="缴存方式"
            )
            # 更新会话状态
            st.session_state.default_values['缴存方式'] = 缴存方式
        
        # 根据判断结果生成不同的模板
        if 涉及新增建设用地 == "是":
            block3_template = '''〔缴纳新增建设用地土地有偿使用费〕该批次涉及新增建设用地{{新增建设用地面积}}公顷，为{{土地等别}}等别，需缴纳新增建设用地土地有偿使用费{{应缴费用}}万元。'''
            if 缴存方式 == "承诺缴纳":
                block3_template += '''{{县市区名称}}人民政府承诺在用地批准后按有关规定及时足额缴纳。'''
            elif 缴存方式 == "已预缴":
                block3_template += '''{{县市区名称}}人民政府已按有关规定预缴。'''
        else:
            block3_template = '''〔不涉及缴纳新增建设用地土地有偿使用费〕该批次不涉及新增建设用地，不需缴纳新增建设用地土地有偿使用费。'''
        
        all_results['block3'] = lineinput(
            block3_template,
            default_values=st.session_state.default_values.copy(),
            key="page_1_batch_block3"
        )
    
    # 更新默认值缓存
    for k, v in defaults.items():
        st.session_state.default_values.setdefault(k, v)
    
    # 合并所有区块的结果
    for block_result in all_results.values():
        if isinstance(block_result, dict):
            component_result.update(block_result)
    
    return component_result
