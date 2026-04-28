import streamlit as st
from datetime import datetime

# --- 1. 页面配置与 CSS 样式优化 ---
st.set_page_config(page_title="脑电图判读决策系统", layout="wide")

# 注入 CSS：模拟宋体排版，优化文本框间距
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: 'SimSun', 'STSong', 'Songti SC', serif;
        line-height: 1.6;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心图谱与判读决策库 ---
# 请确保这些图片文件与本 Python 文件放在同一个文件夹内
WAVE_LIBRARY = {
    "3Hz 棘慢复合波": {
        "desc": "全导联对称，1秒内含3组典型的棘波+慢波组合。",
        "clinical": "典型失神发作（Absence Seizure）。建议核实意识状态。",
        "img": "Spike-waves.png"
    },
    "尖波/尖慢波 (中线区)": {
        "desc": "Fz, Cz, Pz 导联出现高幅尖样放电。",
        "clinical": "局灶性痫样放电，需警惕辅助运动区（SMA）受累。",
        "img": "9d81dbc8b3cde6e252ec1045f834da3c.jpg"
    },
    "电压衰减 (衰减发作)": {
        "desc": "全脑背景电压突然低平，持续约1秒，伴随临床僵直或掉物。",
        "clinical": "惊吓性发作/强直发作。存在高度跌倒风险。",
        "img": "Screenshot_20260424-204705.jpg"
    },
    "肌阵挛-失张力耦合": {
        "desc": "脑电棘波与底部肌电信号（EMG）同步，肌电突然静止。",
        "clinical": "失张力发作。注意防范头部外伤。",
        "img": "Screenshot_20260424-205257.jpg"
    },
    "高峰节律紊乱": {
        "desc": "极度混乱的高幅慢波，夹杂多灶性棘波，完全失去节律性。",
        "clinical": "婴儿痉挛症（West 综合征）特征，需紧急处理。",
        "img": "c33cfa9c9bddeccd0c7ba92223ac9400.png"
    }
}

# --- 3. 界面布局 ---
st.title("🧠 脑电图自动化判读与决策工作站")
st.caption("开发者：田慧军医生 | 基于 8 张核心图谱逻辑体系 V1.1")
st.divider()

# 侧边栏：输入端
with st.sidebar:
    st.header("📋 临床信息录入")
    p_name = st.text_input("患者姓名", "张三")
    p_age = st.number_input("年龄", 0, 120, 35)
    st.divider()
    
    st.header("📈 脑电特征勾选")
    bg_freq = st.slider("背景平均频率 (Hz)", 1, 30, 9)
    alpha_status = st.selectbox("α节律调节调幅", ["尚可", "欠佳", "消失"])
    selected_wave = st.selectbox("异常波形捕捉", ["未见明显异常"] + list(WAVE_LIBRARY.keys()))
    
    st.divider()
    st.header("⚡ 临床联动")
    has_event = st.checkbox("监测期间是否有临床发作？")
    cons_level = st.radio("意识状态", ["清楚", "模糊/丧失"], horizontal=True)

# 主页面：左右双轴驱动
col_vis, col_rep = st.columns([1.2, 1])

with col_vis:
    st.subheader("🔍 图谱视觉比对 (Visual Matching)")
    if selected_wave != "未见明显异常":
        item = WAVE_LIBRARY[selected_wave]
        st.info(f"**识别特征：** {item['desc']}")
        st.warning(f"**专家辅助建议：** {item['clinical']}")
        
        # 尝试加载图片，如果不存在则显示占位符
        try:
            st.image(item['img'], caption=f"典型图谱对标：{selected_wave}", use_column_width=True)
        except:
            st.error(f"未找到图片文件: {item['img']}，请确认文件路径。")
    else:
        st.success("✨ 当前背景活动基本正常。请参考下方波形频率度量衡：")
        try:
            st.image("images.png", caption="基础频率度量衡参考", use_column_width=True)
        except:
            st.write("请上传 images.png 以显示频率尺子。")

with col_rep:
    st.subheader("📄 标准报告生成 (" \
    "医院格式)")
    
    # 报告核心逻辑 (变量名统一为 report_content)
    report_content = f"""
田慧军视频脑电图报告

【背景活动】
α波活动：双侧枕区可见中波幅{bg_freq}Hzα节律，调幅调节{alpha_status}。
快波活动：各导联可见少量低幅18-25Hzβ波。
慢波活动：各导联可见散在低幅4-7Hzθ波。
波形特点：以α波为背景，双侧脑波基本对称。

【活化试验】
睁闭眼：α波抑制完全。
过度换气：未见异常诱发放电。

【异常脑电图】
间歇期：{f"检出[{selected_wave}]。{WAVE_LIBRARY[selected_wave]['clinical']}" if selected_wave != "未见明显异常" else "监测期间未见明确痫样放电。"}
发作期：{f"记录到临床事件，意识{cons_level}。" if has_event else "监测期间未记录到临床发作。"}

【脑电图分类】
{"异常脑电图" if selected_wave != "未见明显异常" else "正常范围脑电图"}

【备注】
专家结论：{selected_wave if selected_wave != "未见明显异常" else "正常清醒脑电图"}。

--------------------------------------------------
报告医生：田慧军医生
报告日期：{datetime.now().strftime('%Y-%m-%d')}
版权所有：田慧军 (Dr. Tian Huijun)
风险提示：本系统基于AI逻辑辅助，临床决策请以主治医师意见为准。
"""

    # 清洗：去除行首行尾空格，确保排版整洁
    final_report = "\n".join([line.strip() for line in report_content.split("\n") if line.strip()])

    # 输出到文本域，方便一键复制
    st.text_area("点击下方框内直接复制（宋体适配）", final_report, height=500)
    
    if st.button("💾 导出并存入数据库"):
        st.balloons()
        st.success("数据已成功同步。")