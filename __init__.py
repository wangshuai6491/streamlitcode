import os

import streamlit.components.v1 as components

# 创建一个 _RELEASE 常量。在开发组件时设为 False，准备打包发布时设为 True。
# （当然，这一步是可选的——发布流程的管理方式有无数种。）
_RELEASE = True  

# 声明一个 Streamlit 组件。`declare_component` 会返回一个函数，
# 用于创建该组件的实例。我们给这个函数起名为 "_component_func" 并加下划线前缀，
# 是因为不想直接暴露给用户；下面我们会再写一个自定义的包装函数作为组件的公开 API。

# 值得注意的是，这里对 `declare_component` 的调用是
# *唯一需要做的事*，就能完成 Streamlit 与组件前端之间的绑定。
# 文件里剩下的内容都只是最佳实践。

if not _RELEASE:
    _component_func = components.declare_component(
        # 给组件起一个简单、有意义的名字（"my_component" 并不合格，
        # 请为自己的组件选个更好的名字 :)
        "my_component",
        # 传入 `url`，告诉 Streamlit 该组件将由本地开发服务器提供
        #（通过 `npm run start` 启动）。这在开发阶段很有用。
        url="http://localhost:5173",
    )
else:
    # 发布正式版时，把 `url` 参数换成 `path`，指向组件的构建目录：
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "my_component",
        path=build_dir
    )


# 为组件创建一个包装函数。这是可选的最佳实践——
# 也可以直接把 `declare_component` 返回的函数暴露出去。
# 包装函数让我们可以定制组件的 API：预处理输入参数、后处理返回值，并为用户添加文档字符串。
def my_component(name, key=None):
    """
    内联式文本输入框组件，将模板中的{{变量}}替换为输入框。
    
    参数:
        name: 包含{{变量名}}的模板字符串
    
    返回值:
        替换后的完整文本字符串
    """
    # 调用底层组件函数，传入name参数
    component_value = _component_func(name=name, key=key, default="等待用户输入...")
    
    # 返回组件的返回值
    return component_value
