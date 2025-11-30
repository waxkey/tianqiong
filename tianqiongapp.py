import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from io import StringIO

# 页面配置
st.set_page_config(
    page_title="天穹之眼——智能数据处理平台",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# 使用环境变量获取API密钥
TIANQIONG_API_KEY = os.environ.get('TIANQIONG_API_KEY', '')

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
    }
    .analysis-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown('<h1 class="main-header">⛰️ 天穹之眼——智能数据处理平台</h1>', unsafe_allow_html=True)

# 侧边栏 - 配置和API设置
with st.sidebar:
    st.markdown('<h2 class="sub-header">设置</h2>', unsafe_allow_html=True)
    
    # API配置
    st.subheader("天穹之眼 API配置")
    api_key = st.text_input("API密钥", value=TIANQIONG_API_KEY, help="输入您的天穹之眼 API密钥")
    api_url = st.text_input("API端点", value="https://api.tianqiong.com", 
                           help="天穹之眼 API端点URL")
    
    # 模型参数
    st.subheader("模型参数")
    temperature = st.slider("温度", min_value=0.0, max_value=1.0, value=0.7, 
                           help="控制输出的随机性，值越高输出越随机")
    max_tokens = st.slider("最大输出长度", min_value=100, max_value=2000, value=1000,
                          help="控制生成文本的最大长度")
    
    # 数据上传
    st.subheader("数据上传")
    uploaded_file = st.file_uploader("上传地质数据文件", type=['csv', 'xlsx', 'txt'], 
                                    help="支持CSV、Excel或文本文件")

# 主内容区域
tab1, tab2, tab3 = st.tabs(["📊 数据输入", "🔍 数据分析", "📈 可视化"])

with tab1:
    st.markdown('<h2 class="sub-header">地质参数输入</h2>', unsafe_allow_html=True)
    
    # 数据来源选择
    data_source = st.radio("选择数据来源:", 
                          ["手动输入", "上传文件", "示例数据"], 
                          horizontal=True)
    
    if data_source == "手动输入":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("基本地质参数")
            rock_type = st.selectbox("岩石类型", 
                                    ["砂岩", "页岩", "石灰岩", "花岗岩", "玄武岩", "其他"])
            porosity = st.slider("孔隙度 (%)", min_value=0.0, max_value=50.0, value=15.0)
            permeability = st.number_input("渗透率 (mD)", min_value=0.001, max_value=10000.0, value=10.0)
            density = st.number_input("密度 (g/cm³)", min_value=1.0, max_value=3.5, value=2.4)
            
        with col2:
            st.subheader("地球化学参数")
            silica_content = st.slider("二氧化硅含量 (%)", min_value=0.0, max_value=100.0, value=65.0)
            calcium_content = st.slider("钙含量 (%)", min_value=0.0, max_value=100.0, value=15.0)
            depth = st.number_input("深度 (m)", min_value=0, max_value=10000, value=1500)
            temperature = st.number_input("地层温度 (°C)", min_value=0, max_value=500, value=85)
            
        # 创建数据框
        data = {
            "参数": ["岩石类型", "孔隙度(%)", "渗透率(mD)", "密度(g/cm³)", 
                   "二氧化硅含量(%)", "钙含量(%)", "深度(m)", "地层温度(°C)"],
            "数值": [rock_type, porosity, permeability, density, 
                   silica_content, calcium_content, depth, temperature]
        }
        df = pd.DataFrame(data)
        
    elif data_source == "上传文件" and uploaded_file is not None:
        # 处理上传的文件
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                # 尝试读取文本文件
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                df = pd.read_csv(stringio)
            
            st.success("文件上传成功!")
            st.dataframe(df.head(10))
            
        except Exception as e:
            st.error(f"文件读取错误: {e}")
            st.info("使用示例数据继续演示")
            data_source = "示例数据"
    
    if data_source == "示例数据":
        # 生成示例数据
        np.random.seed(42)
        sample_size = 50
        
        sample_data = {
            "井号": [f"WELL_{i+1:03d}" for i in range(sample_size)],
            "深度(m)": np.random.uniform(500, 3000, sample_size),
            "孔隙度(%)": np.random.uniform(5, 25, sample_size),
            "渗透率(mD)": np.random.exponential(10, sample_size),
            "密度(g/cm³)": np.random.uniform(2.2, 2.8, sample_size),
            "二氧化硅含量(%)": np.random.uniform(40, 80, sample_size),
            "钙含量(%)": np.random.uniform(5, 30, sample_size),
            "地层温度(°C)": np.random.uniform(50, 120, sample_size)
        }
        
        df = pd.DataFrame(sample_data)
        st.success("已加载示例数据!")
        st.dataframe(df.head(10))

with tab2:
    st.markdown('<h2 class="sub-header">智能分析</h2>', unsafe_allow_html=True)
    
    if 'df' in locals():
        # 显示数据统计
        st.subheader("数据概览")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("数据点数", len(df))
        with col2:
            st.metric("参数数量", len(df.columns))
        with col3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            st.metric("数值参数", len(numeric_cols))
        with col4:
            st.metric("缺失值", df.isnull().sum().sum())
        
        # 基本统计分析
        st.subheader("基本统计信息")
        st.dataframe(df.describe())
        
        # 与DeepSeek API交互
        if api_key:
            st.subheader("天穹之眼 数据分析")
            
            # 准备分析提示
            analysis_prompt = f"""
            请分析以下地质数据并提供专业见解:
            
            {df.describe().to_string()}
            
            数据包含以下列: {', '.join(df.columns)}
            
            请从以下角度进行分析:
            1. 数据质量和完整性评估
            2. 关键地质参数的统计特征
            3. 参数间的可能关系和相关性的地质意义
            4. 基于这些参数的储层潜力评估
            5. 进一步分析的建议
            
            请用专业但易于理解的语言回答。
            """
            
            if st.button("开始数据分析", type="primary"):
                with st.spinner("正在分析数据，请稍候..."):
                    try:
                        # 准备API请求
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {TIANQIONG_API_KEY}"
                        }
                        
                        payload = {
                            "model": "deepseek-chat",  # 根据实际情况调整模型名称
                            "messages": [
                                {
                                    "role": "user",
                                    "content": analysis_prompt
                                }
                            ],
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        }
                        
                        # 发送请求到DeepSeek API
                        response = requests.post('https://api.deepseek.com/v1/chat/completions', headers=headers, json=payload)
                        
                        if response.status_code == 200:
                            result = response.json()
                            ai_analysis = result['choices'][0]['message']['content']
                            
                            # 显示分析结果
                            st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                            st.markdown("天穹之眼 数据分析结果")
                            st.write(ai_analysis)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error(f"API请求失败: {response.status_code} - {response.text}")
                            
                    except Exception as e:
                        st.error(f"分析过程中出现错误: {e}")
                        st.info("请检查API配置是否正确，或尝试使用示例响应")
                        
                        # 示例响应（当API不可用时使用）
                        st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                        st.markdown("天穹之眼 数据分析结果 (示例)")
                        st.write("""
                        基于提供的地质参数数据，我进行了以下分析:
                        
                        1. 数据质量评估: 数据集包含50个样本点，参数完整性良好，无明显缺失值。
                        
                        2. 关键参数统计:
                           - 孔隙度范围在5-25%之间，平均值约15%，表明储层具有中等孔隙度特征
                           - 渗透率分布呈指数型，多数值在10-30mD范围内，表明储层渗透性中等
                           - 密度值在2.2-2.8g/cm³之间，符合典型沉积岩特征
                        
                        3. 参数关系分析: 孔隙度与渗透率可能存在正相关关系，这是碎屑岩储层的典型特征。
                        
                        4. 储层潜力评估: 基于孔隙度和渗透率数据，该区域可能具有中等储集能力，建议进一步研究孔隙结构。
                        
                        5. 建议: 进行岩心实验验证孔渗关系，开展测井曲线标定，考虑进行岩石物理建模。
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("请输入天穹之眼 API密钥以启用数据分析功能")

with tab3:
    st.markdown('<h2 class="sub-header">数据可视化</h2>', unsafe_allow_html=True)
    
    if 'df' in locals():
        # 选择可视化类型
        viz_type = st.selectbox("选择可视化类型", 
                               ["分布直方图", "散点图矩阵", "相关性热图", "箱形图"])
        
        if viz_type == "分布直方图":
            st.subheader("参数分布直方图")
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            selected_column = st.selectbox("选择参数", numeric_columns)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df[selected_column].dropna(), bins=15, alpha=0.7, color='steelblue', edgecolor='black')
            ax.set_xlabel(selected_column)
            ax.set_ylabel('频数')
            ax.set_title(f'{selected_column}分布直方图')
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
        elif viz_type == "散点图矩阵":
            st.subheader("散点图矩阵")
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            selected_columns = st.multiselect("选择参数", numeric_columns, default=list(numeric_columns[:4]))
            
            if len(selected_columns) >= 2:
                fig = sns.pairplot(df[selected_columns])
                st.pyplot(fig)
            else:
                st.warning("请至少选择两个参数")
                
        elif viz_type == "相关性热图":
            st.subheader("参数相关性热图")
            numeric_df = df.select_dtypes(include=[np.number])
            
            if len(numeric_df.columns) >= 2:
                fig, ax = plt.subplots(figsize=(10, 8))
                correlation_matrix = numeric_df.corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
                ax.set_title('地质参数相关性热图')
                st.pyplot(fig)
            else:
                st.warning("数值参数不足，无法计算相关性")
                
        elif viz_type == "箱形图":
            st.subheader("参数箱形图")
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            selected_columns = st.multiselect("选择参数", numeric_columns, default=list(numeric_columns[:3]))
            
            if selected_columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                df[selected_columns].boxplot(ax=ax)
                ax.set_ylabel('数值')
                ax.set_title('地质参数箱形图')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "天穹之眼——智能数据处理平台 | 展示版本"
    "</div>", 
    unsafe_allow_html=True
)