# shenzhen_change_app.py
import streamlit as st
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
from PIL import Image
import os
import tempfile

# 设置页面配置
st.set_page_config(
    page_title="深圳城市变迁可视化",
    page_icon="🏙️",
    layout="wide"
)

# 应用标题
st.title("🏙️ 深圳城市变迁可视化")
st.markdown("---")

# 在侧边栏添加文件上传功能
st.sidebar.title("📁 文件管理")

# 选项：使用本地文件或上传新文件
option = st.sidebar.radio("选择图片来源:", ["使用本地文件", "上传新文件"])

# 初始化图片变量
img_1990 = None
img_2020 = None

if option == "使用本地文件":
    # 显示当前目录
    current_dir = os.getcwd()
    st.sidebar.write(f"当前目录: {current_dir}")

    # 显示当前目录下的文件
    st.sidebar.subheader("📋 目录文件列表")
    try:
        files = os.listdir(current_dir)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]

        if image_files:
            st.sidebar.write("找到的图片文件:")
            for img_file in image_files:
                st.sidebar.write(f"- {img_file}")
        else:
            st.sidebar.warning("没有找到图片文件")
    except Exception as e:
        st.sidebar.error(f"读取目录错误: {e}")

    # 尝试加载本地图片
    try:
        img_1990 = Image.open("1990年.jpg")
        st.sidebar.success("✅ 成功加载: 1990年.jpg")
    except Exception as e:
        st.sidebar.error(f"❌ 无法加载 1990年.jpg: {e}")
        # 创建占位图
        img_1990 = Image.new('RGB', (800, 600), color='#2c3e50')

    try:
        img_2020 = Image.open("2020年.jpg")
        st.sidebar.success("✅ 成功加载: 2020年.jpg")
    except Exception as e:
        st.sidebar.error(f"❌ 无法加载 2020年.jpg: {e}")
        # 创建占位图
        img_2020 = Image.new('RGB', (800, 600), color='#34495e')

else:  # 上传新文件
    st.sidebar.subheader("⬆️ 上传图片")

    # 上传1990年图片
    uploaded_1990 = st.sidebar.file_uploader(
        "选择1990年图片:",
        type=['jpg', 'jpeg', 'png'],
        key="1990"
    )

    if uploaded_1990 is not None:
        img_1990 = Image.open(uploaded_1990)
        st.sidebar.success(f"✅ 已上传: {uploaded_1990.name}")
    else:
        st.sidebar.warning("请上传1990年图片")
        img_1990 = Image.new('RGB', (800, 600), color='#2c3e50')

    # 上传2020年图片
    uploaded_2020 = st.sidebar.file_uploader(
        "选择2020年图片:",
        type=['jpg', 'jpeg', 'png'],
        key="2020"
    )

    if uploaded_2020 is not None:
        img_2020 = Image.open(uploaded_2020)
        st.sidebar.success(f"✅ 已上传: {uploaded_2020.name}")
    else:
        st.sidebar.warning("请上传2020年图片")
        img_2020 = Image.new('RGB', (800, 600), color='#34495e')

# 创建两列布局
col1, col2 = st.columns([3, 1])

with col1:
    # 图片对比滑块
    st.subheader("📸 城市变迁对比")
    st.markdown("使用滑块查看深圳从1990年到2020年的变化")

    # 检查图片是否已加载
    if img_1990 and img_2020:
        # 调整图片尺寸一致
        if img_1990.size != img_2020.size:
            st.info(f"🔄 调整图片尺寸: {img_1990.size} → {img_2020.size}")
            # 使用第二张图片的尺寸
            img_1990 = img_1990.resize(img_2020.size, Image.Resampling.LANCZOS)

        # 图片对比组件
        try:
            image_comparison(
                img1=img_1990,
                img2=img_2020,
                label1="1990年",
                label2="2020年",
                width=700,
                starting_position=50,
                show_labels=True,
                make_responsive=True,
                in_memory=True,
            )
            st.success("✅ 图片对比加载成功！")
        except Exception as e:
            st.error(f"❌ 图片对比组件错误: {e}")
            # 备用方案：显示两张图片并排
            st.warning("使用备用方案显示图片")
            col_a, col_b = st.columns(2)
            with col_a:
                st.image(img_1990, caption="深圳1990年", use_column_width=True)
            with col_b:
                st.image(img_2020, caption="深圳2020年", use_column_width=True)
    else:
        st.error("⚠️ 请确保两张图片都已加载！")
        # 显示占位图
        st.image(img_1990, caption="深圳1990年（占位图）", use_column_width=True)
        st.image(img_2020, caption="深圳2020年（占位图）", use_column_width=True)

    # 添加说明
    st.caption("🔍 拖动滑块可以对比不同时期的深圳城市面貌")

with col2:
    # 信息面板
    st.subheader("ℹ️ 项目信息")

    st.info("""
    **项目简介**

    本应用展示深圳从1990年至2020年
    的城市发展变迁。

    **技术栈**
    - Python Streamlit
    - 遥感图像对比
    - 地理信息系统
    """)

    # 图片信息
    if img_1990 and img_2020:
        st.subheader("📊 图片信息")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.write("**1990年图片**")
            st.write(f"尺寸: {img_1990.size}")
            st.write(f"格式: {img_1990.format if hasattr(img_1990, 'format') else 'Unknown'}")
            st.write(f"模式: {img_1990.mode}")
        with col_info2:
            st.write("**2020年图片**")
            st.write(f"尺寸: {img_2020.size}")
            st.write(f"格式: {img_2020.format if hasattr(img_2020, 'format') else 'Unknown'}")
            st.write(f"模式: {img_2020.mode}")

# 分隔线
st.markdown("---")

# 地图部分（保持原来的地图代码不变）
st.subheader("🗺️ 深圳地理位置")

# 创建两列布局用于地图和城市信息
map_col, info_col = st.columns([2, 1])

with map_col:
    # 深圳的经纬度（中心位置）
    shenzhen_coords = [22.5431, 114.0579]

    # 创建地图
    m = folium.Map(
        location=shenzhen_coords,
        zoom_start=11,
        tiles="cartodbpositron",  # 使用浅色地图
        width='100%',
        height=500
    )

    # 添加深圳标记
    folium.Marker(
        location=shenzhen_coords,
        popup="<b>深圳市</b><br>中国经济特区",
        tooltip="点击查看详情",
        icon=folium.Icon(color="red", icon="info-sign", prefix="fa")
    ).add_to(m)

    # 添加圆形区域表示城市范围
    folium.Circle(
        location=shenzhen_coords,
        radius=10000,  # 10公里半径
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.1,
        popup="深圳主要城区范围"
    ).add_to(m)

    # 添加一些重要的地点标记
    locations = {
        "福田区": [22.5410, 114.0596],
        "南山区": [22.5319, 113.9305],
        "罗湖区": [22.5483, 114.1120],
        "宝安区": [22.5550, 113.8840],
    }

    for name, coords in locations.items():
        folium.Marker(
            location=coords,
            popup=f"<b>{name}</b>",
            icon=folium.Icon(color="green", icon="building", prefix="fa")
        ).add_to(m)

    # 显示地图
    st_folium(m, width=700, height=500)

with info_col:
    st.markdown("### 📍 深圳城市信息")

    # 城市基本信息
    st.metric("📍 地理位置", "中国广东省")
    st.metric("🗺️ 坐标", "22.5431°N, 114.0579°E")
    st.metric("🏙️ 城市面积", "1,997 km²")
    st.metric("👥 人口 (2020)", "约1,756万")

    st.markdown("---")

    # 时间线信息
    st.markdown("### 📅 发展时间线")
    timeline_data = {
        "1979年": "设立深圳经济特区",
        "1990年": "特区建立10周年，快速发展期",
        "2000年": "高新技术产业崛起",
        "2010年": "成为国际化大都市",
        "2020年": "粤港澳大湾区核心城市"
    }

    for year, event in timeline_data.items():
        st.markdown(f"**{year}** - {event}")

# 数据统计部分（保持不变）
st.markdown("---")
st.subheader("📊 城市发展统计")

# 创建三列显示统计数据
stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown("##### 🏗️ 城市建设")
    st.markdown("""
    - 1990年建筑面积: 约200 km²
    - 2020年建筑面积: 约900 km²
    - 增长率: **350%**
    """)

with stat_col2:
    st.markdown("##### 🌳 绿地变化")
    st.markdown("""
    - 1990年绿地覆盖率: 约45%
    - 2020年绿地覆盖率: 约40%
    - 公园数量: 从50个增加到1200+
    """)

with stat_col3:
    st.markdown("##### 🏢 经济发展")
    st.markdown("""
    - GDP增长: 从1990年的170亿元
    - 到2020年的2.76万亿元
    - 增长约 **160倍**
    """)

# 添加使用说明
st.markdown("---")
st.subheader("📝 使用说明")

st.markdown("""
### 方法一：使用本地文件
1. 将图片命名为 `1990年.jpg` 和 `2020年.jpg`
2. 放在与 `shenzhen_change_app.py` 相同的目录下
3. 在左侧边栏选择"使用本地文件"

### 方法二：上传文件
1. 在左侧边栏选择"上传新文件"
2. 分别上传1990年和2020年的图片
3. 支持格式: JPG, PNG, BMP

### 常见问题
1. **图片不显示**: 检查文件名是否正确，注意大小写
2. **灰色图片**: 图片路径错误或文件不存在
3. **尺寸不一致**: 应用会自动调整图片尺寸
""")

# 添加页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>深圳城市变迁可视化项目 | 大一遥感对比项目 | 使用Python Streamlit构建</p>
    <p>© 2024 城市发展研究 | 数据仅供参考</p>
</div>
""", unsafe_allow_html=True)

# 添加一个刷新按钮
if st.button("🔄 刷新应用"):
    st.rerun()