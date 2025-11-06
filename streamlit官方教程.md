# st.fragment 核心功能总结
`st.fragment` 是 Streamlit 1.41.0+ 内置的装饰器，用于将函数转为独立片段，支持独立重渲染，无需额外安装，核心价值是优化交互体验、减少全量页面重渲染。

---

### 一、核心作用
- 片段内组件交互时，仅重渲染该片段，而非整个应用，避免页面闪烁、提升响应速度。
- 支持定时自动重渲染，或手动触发不同范围的重渲染，灵活控制执行流程。
- 可与 `Session State`、外部导入模块及应用其他元素交互，兼容现有开发逻辑。

---

### 二、关键参数
- **func**：待转为片段的函数（通过装饰器直接作用于函数）。
- **run_every**：自动重渲染间隔，支持多种格式：
  - 数值（int/float）：单位为秒（如 `5` 表示每5秒）；
  - 字符串：支持 Pandas Timedelta 格式（如 `"1h23s"`“1.5 days”）；
  - `timedelta` 对象（如 `datetime.timedelta(days=1)`）；
  - 默认 `None`：仅在用户触发交互时重渲染。

---

### 三、使用规则与限制
1. 片段主体可包含组件，但不能向外部创建的容器中渲染组件。
2. 不支持直接在片段内调用 `st.sidebar`，需在 `with st.sidebar` 上下文管理器中调用片段函数。
3. 片段内直接创建的元素，会在每次片段重渲染时清空重绘；渲染到外部容器的元素会累积，直到下次全应用重渲染。
4. 片段间的 `Session State` 交互是累加的，需自行处理潜在副作用。

---

### 四、核心功能示例场景
1. **基础独立重渲染**：片段内按钮点击仅触发片段重绘，外部耗时操作（如数据加载）不会重复执行。
2. **重渲染范围控制**：
   - 片段内调用 `st.rerun()`：触发全应用重渲染；
   - 调用 `st.rerun(scope="fragment")`：仅触发当前片段重渲染。
3. **定时自动重渲染**：通过 `run_every` 设置间隔，实现数据实时刷新等场景。
4. **状态共享与传递**：片段可读写 `Session State`，实现与外部应用的数据互通。

---

### 五、核心优势
- 减少不必要的重渲染，解决页面闪烁、响应迟缓问题。
- 灵活支持手动交互触发和定时自动触发两种重渲染模式。
- 无需额外依赖，与 Streamlit 现有生态（如 `Session State`、组件系统）无缝兼容。

# st.container()

`st.container()` 是 Streamlit 中用于**组织和分组界面元素**的核心布局工具，本质是一个“容器”组件，能将多个零散的界面元素（按钮、文本、图表等）封装成一个整体，方便控制布局位置和显示/隐藏状态。

---

### 一、核心作用
1. **元素分组**：将相关组件（如表单、结果展示区）归类到同一容器，让代码和界面结构更清晰。
2. **灵活布局**：容器可以嵌套、自由放置在页面任意位置，支持“先创建容器、后填充内容”的延迟渲染。
3. **状态控制**：可通过条件判断控制整个容器的显示/隐藏，或批量操作容器内元素。
4. **避免布局混乱**：防止不同功能模块的元素相互干扰，尤其适合复杂界面的结构化设计。

---

### 二、基础用法
#### 1. 简单分组示例
```python
import streamlit as st

# 创建容器
main_container = st.container()

# 向容器中添加元素
with main_container:
    st.title("用户信息表单")
    name = st.text_input("姓名")
    age = st.number_input("年龄", min_value=0)
    st.button("提交")

# 容器外的元素（独立显示）
st.divider()
st.write("容器外的独立内容")
```

#### 2. 延迟填充内容（先创建容器，后填内容）
```python
import streamlit as st

# 先创建容器并放置在页面顶部
header_container = st.container()
# 再创建一个容器放在下方
content_container = st.container()

# 先填充下方容器，再填充顶部容器（界面上仍按容器创建顺序显示）
with content_container:
    st.write("这是内容区域")
    st.bar_chart({"数据": [1, 3, 2]})

with header_container:
    st.header("这是顶部标题（延迟填充）")
```

---

### 三、高级用法
#### 1. 容器嵌套（复杂布局）
```python
import streamlit as st

# 外层容器
outer_container = st.container()

with outer_container:
    st.subheader("外层容器")
    # 内层容器1
    inner1 = st.container()
    with inner1:
        st.write("内层容器1 - 基本信息")
        st.text_input("邮箱")
    
    # 内层容器2
    inner2 = st.container()
    with inner2:
        st.write("内层容器2 - 偏好设置")
        st.checkbox("接收通知")
```

#### 2. 条件显示容器（批量控制元素）
```python
import streamlit as st

# 初始化状态
if "show_details" not in st.session_state:
    st.session_state.show_details = False

# 创建容器
detail_container = st.container()

# 按钮控制容器显示/隐藏
if st.button("显示/隐藏详情"):
    st.session_state.show_details = not st.session_state.show_details

# 条件渲染容器内容
if st.session_state.show_details:
    with detail_container:
        st.info("这是隐藏的详情内容")
        st.write("可以批量显示多个元素")
        st.dataframe({"列1": [1, 2], "列2": [3, 4]})
```

#### 3. 与片段（st.fragment）结合（优化交互）
```python
import streamlit as st

# 创建容器用于放置可交互片段
interactive_container = st.container()

# 片段函数（独立重渲染）
@st.fragment
def interactive_card():
    st.write("片段内的交互组件")
    if st.button("点击我（仅重渲染片段）"):
        st.success("片段内反馈")

# 将片段放入容器
with interactive_container:
    st.subheader("可交互卡片")
    interactive_card()
```

---

### 四、关键区别：st.container() vs st.columns() vs st.expander()
| 组件          | 核心用途                  | 特点                          |
|---------------|---------------------------|-------------------------------|
| `st.container()` | 通用元素分组、自由布局    | 无默认样式，可嵌套，灵活度最高 |
| `st.columns(n)`  | 横向分栏布局              | 按列分割页面，适合并排显示元素 |
| `st.expander()`  | 折叠/展开内容             | 节省页面空间，默认折叠        |

---

### 总结
`st.container()` 是 Streamlit 布局的“基础积木”，核心价值是**结构化组织界面**。无论是简单的元素分组，还是复杂的嵌套布局、条件显示，都能通过它实现，让你的应用界面更整洁、逻辑更清晰。


# st.empty()
`st.empty()` 是 Streamlit 中一个特殊的布局组件，用于创建一个**空白占位符**，可以在后续代码中动态填充或替换内容。它的核心作用是**预留位置并支持内容的动态更新**，避免因内容变化导致的页面布局抖动。


### 一、核心特点
- **占位符特性**：创建时不显示任何内容，但会在页面中占据一块空白区域。
- **动态替换**：后续可以通过 `empty_container.write()`、`empty_container.plotly_chart()` 等方法，向占位符中填充内容；再次填充时，旧内容会被**直接替换**（而非追加）。
- **布局稳定**：无论内容如何变化，占位符的位置固定，避免页面元素“跳动”。


### 二、基础用法
#### 1. 动态更新单元素
```python
import streamlit as st
import time

# 创建空白占位符
placeholder = st.empty()

# 初始内容
placeholder.write("准备开始...")

# 动态更新内容（模拟进度）
for i in range(1, 11):
    time.sleep(0.5)  # 模拟耗时操作
    placeholder.write(f"进度：{i*10}%")  # 替换旧内容

# 最终内容
placeholder.success("完成！")
```

运行后会看到：占位符位置从“准备开始”→“进度10%”→...→“完成！”逐步更新，位置始终固定。


#### 2. 替换复杂内容（多元素）
```python
import streamlit as st

placeholder = st.empty()

# 第一次填充：表单
with placeholder.container():  # 用 container 包裹多元素
    st.write("请输入信息")
    name = st.text_input("姓名")
    age = st.number_input("年龄")

# 点击按钮后替换为结果
if st.button("提交"):
    with placeholder.container():  # 替换整个表单
        st.success(f"提交成功！姓名：{name}，年龄：{age}")
```


### 三、典型应用场景
#### 1. 进度提示/状态更新
在循环、API调用等耗时操作中，用 `st.empty()` 实时更新进度，避免重复创建多个状态提示框。

```python
import streamlit as st
import time

status = st.empty()
progress_bar = st.progress(0)

for i in range(100):
    time.sleep(0.05)
    status.text(f"处理中... {i+1}/100")  # 动态更新文本
    progress_bar.progress(i+1)

status.success("处理完成！")
```


#### 2. 条件切换内容
根据用户操作动态切换同一位置的内容（如从“表单”切换到“结果”，从“列表”切换到“详情”）。

```python
import streamlit as st

content_area = st.empty()

if st.button("显示数据"):
    content_area.dataframe({"A": [1,2], "B": [3,4]})  # 显示表格
elif st.button("显示图表"):
    content_area.line_chart({"A": [1,3,2], "B": [4,2,5]})  # 替换为图表
```


#### 3. 清除内容
通过向占位符写入空内容，实现“清空”效果：

```python
placeholder = st.empty()
placeholder.write("这是一段临时内容")

if st.button("清空"):
    placeholder.write("")  # 清空占位符
```


### 四、与 `st.container()` 的区别
| 特性                | `st.empty()`               | `st.container()`            |
|---------------------|----------------------------|-----------------------------|
| 初始状态            | 完全空白（不占可见空间）   | 空白容器（占一行可见空间）  |
| 内容更新方式        | 替换旧内容（覆盖）         | 追加新内容（累积）          |
| 典型用途            | 动态替换单块内容           | 分组管理多个元素            |

简单说：`st.empty()` 适合“**同一位置内容会变**”的场景，`st.container()` 适合“**同一组内容固定**”的场景。


### 总结
`st.empty()` 是 Streamlit 动态界面设计的核心工具，通过“占位-替换”机制，既能保持布局稳定，又能实现内容的灵活更新，尤其适合进度展示、条件内容切换等场景。

需要结合之前的按钮组或片段功能，做一个动态内容更新的综合示例吗？

# st.session_state
在 Streamlit 中，`st.toggle` 组件的状态默认不会自动保存到 `st.session_state` 中，需要显式指定 `key` 参数才能将其状态存入会话状态。

你可以这样修改代码：

```python
import streamlit as st

# 为 toggle 组件指定 key，使其状态存入 session_state
kaiguan = st.toggle("分次报批", key="kaiguan_toggle")

# 此时 session_state 中就会有对应的键值对了
st.write(st.session_state)
```

运行修改后的代码，当你点击切换开关时，会在页面上看到 `st.session_state` 中包含 `kaiguan_toggle` 这个键，其值为 `True` 或 `False`（对应开关的开启/关闭状态）。

所有需要在会话状态中保存的交互组件（如 `st.button`、`st.text_input`、`st.selectbox` 等），都需要通过指定 `key` 参数来实现状态持久化。