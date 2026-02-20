import streamlit as st
import requests
import html2text
import io
import json
import streamlit.components.v1 as components
import re

# 定义网站清洗规则函数
def clean_markdown_by_website(markdown_text, url):
    """
    根据不同网站的规则清洗 Markdown 内容
    
    Args:
        markdown_text: 原始 Markdown 文本
        url: 原始网址
        
    Returns:
        清洗后的 Markdown 文本
    """
    # 中国政府网站规则 (gov.cn)
    if 'gov.cn' in url:
        # 1. 删除头部导航信息（通常包含logo、导航菜单等）
        # 规则：删除从开始到第一个标题（以#开头）之前的内容
        header_pattern = r'^.*?(?=^#)' 
        markdown_text = re.sub(header_pattern, '', markdown_text, flags=re.DOTALL | re.MULTILINE)
        
        # 2. 删除底部信息（通常包含版权、备案号、相关链接等）
        # 规则1：删除包含"相关稿件"的部分
        related_articles_pattern = r'相关稿件.*$'
        markdown_text = re.sub(related_articles_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则2：删除包含"版权所有"的部分
        copyright_pattern = r'版权所有.*$'
        markdown_text = re.sub(copyright_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则3：删除包含"主办单位"的部分
        organizer_pattern = r'主办单位.*$'
        markdown_text = re.sub(organizer_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则4：删除包含"网站标识码"的部分
        site_id_pattern = r'网站标识码.*$'
        markdown_text = re.sub(site_id_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则5：删除包含"京ICP备"的部分
        icp_pattern = r'京ICP备.*$'
        markdown_text = re.sub(icp_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则6：删除包含"京公网安备"的部分
        security_pattern = r'京公网安备.*$'
        markdown_text = re.sub(security_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则7：删除包含"客户端"的部分
        client_pattern = r'客户端.*$'
        markdown_text = re.sub(client_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则8：删除包含"登录 注册"的部分
        login_pattern = r'登录 注册.*$'
        markdown_text = re.sub(login_pattern, '', markdown_text, flags=re.DOTALL)
        
        # 规则9：删除多余的空行
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
        
        # 规则10：删除开头和结尾的空行
        markdown_text = markdown_text.strip()
    
    # 可以在这里添加其他网站的清洗规则
    
    return markdown_text

# 设置页面标题
st.title('HTML 转 Markdown 工具')

# 创建文本输入框，让用户输入网址
url = st.text_input('请输入网址', placeholder='例如: https://www.example.com')

# 添加一个按钮，触发转换功能
if st.button('转换为 Markdown'):
    if url:
        try:
            # 显示加载状态
            with st.spinner('正在获取网页内容并转换...'):
                # 使用 requests 获取网页内容
                response = requests.get(url)
                response.raise_for_status()  # 检查请求是否成功
                
                # 确保使用正确的编码
                response.encoding = response.apparent_encoding
                
                # 使用 html2text 将 HTML 转换为 Markdown
                h = html2text.HTML2Text()
                h.ignore_links = False  # 保留链接
                h.ignore_images = False  # 保留图片
                h.unicode_snob = True  # 确保正确处理 Unicode
                markdown_text = h.handle(response.text)
                
                # 根据网站规则清洗 Markdown 内容
                markdown_text = clean_markdown_by_website(markdown_text, url)
                
                # 在文档开头添加原文链接
                markdown_text = f"原文链接\n{url}\n\n{markdown_text}"
                
                # 创建一个下载按钮，让用户可以下载转换后的 Markdown 文件
                buffer = io.BytesIO()
                buffer.write(markdown_text.encode('utf-8'))
                buffer.seek(0)
                
                st.download_button(
                    label='下载 Markdown 文件',
                    data=buffer,
                    file_name='converted.md',
                    mime='text/markdown'
                )
                
                # 添加一键复制按钮
                
                # 创建复制按钮的 HTML 和 JavaScript
                copy_button_html = """
                <button id="copyButton" style="padding: 0.5rem 1rem; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    一键复制结果
                </button>
                <script>
                    document.getElementById('copyButton').addEventListener('click', function() {
                        const textToCopy = '{markdown_text}';
                        navigator.clipboard.writeText(textToCopy).then(function() {
                            alert('已成功复制到剪贴板！');
                        }).catch(function(err) {
                            alert('复制失败: ' + err);
                        });
                    });
                </script>
                """
                
                # 替换 markdown_text 为实际内容，确保转义正确
                escaped_markdown = json.dumps(markdown_text)[1:-1]  # 移除首尾引号
                copy_button_html = copy_button_html.replace('{markdown_text}', escaped_markdown)
                
                # 渲染复制按钮
                components.html(copy_button_html, height=60)
                
                # 显示转换后的 Markdown 内容
                st.subheader('转换结果')
                st.markdown(markdown_text)
                
        except Exception as e:
            st.error(f'转换失败: {str(e)}')
    else:
        st.warning('请输入有效的网址')

# 添加使用说明
st.sidebar.markdown('''
## 同功能网站推荐
- [HelloWorld HTML to Markdown](https://www.helloworld.net/html2md)
- [DevTool HTML to MD](https://devtool.tech/html-md)
## 油猴脚本插件
- [网页转md](https://gtjs-9gjbu0mx.maozi.io/2026/02/20/you-hou/wang-ye-zhuan-md/)

''')
