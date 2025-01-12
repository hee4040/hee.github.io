# 라이브러리 임포트
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import plotly.express as px
import numpy as np

# Streamlit 페이지 설정
st.set_page_config(page_title="수면 건강 및 라이프스타일 데이터셋 정리", 
                   layout="wide", 
                   menu_items={
                       'About': """# AI와데이터기초 프로젝트   
                                  AI융합학부 
                                  김지율 장수인 최희우"""
                   })
st.title("수면 건강 및 라이프스타일 데이터셋 📊")  # 앱 제목 표시

# 프로젝트 동기 설명
st.markdown("""수면 질은 건강에 많은 영향을 미칩니다.<br>
            수면의 질을 높이기 위하여 어떤 요소가 영향을 미치는 지를 데이터들을 정리해서 알아내는 작업은 꼭 필요하다고 생각했습니다."""
            , unsafe_allow_html=True)

# 데이터 로드
data = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")  # 데이터셋 로드

# 'Quality of Sleep'에 따른 평균값 계산
average_values = data.groupby('Quality of Sleep').mean()  # 수면 품질에 따라 평균 계산

# 중요한 열 강조
important_columns = ['Sleep Duration', 'Stress Level', 'Heart Rate']
def highlight_columns(s):
    color = 'background-color: #99CCFF'  # 강조할 셀의 배경색 설정
    return [color if col in important_columns else '' for col in s.index]

# 강조된 스타일 적용
average_values = average_values.style.apply(highlight_columns, axis=1)

# 평균 테이블 출력
st.subheader("Quality of Sleep에 따른 평균 값 😪")
st.write(average_values)

st.markdown("""같은 Quality of Sleep 값에 따라 각 칼럼의 평균을 계산했습니다. 
특히 **'Sleep Duration'**, **'Stress Level'**, **'Heart Rate'** 값들이 눈에 띄는 관계를 보였습니다.""")

# 특정 변수와 수면의 질 간의 산점도와 추세선 그리는 함수 정의
# 순서대로 색, x축, (y축), (데이터)를 입력받아 사용하는 함수 -> 뒤에 두 정보는 기본값이 있기 때문에 입력하지 않아도 된다.
def plot_scatter_with_trend(color_c, x_label, x, y='Quality of Sleep', data=data):

    plt.figure(figsize=(15, 6))  # 그래프 크기 설정
    x_data = data[x]  # x축 데이터 설정 : 입력된 x값
    y_data = data[y]  # y축 데이터 설정 : 'Quality of Sleep'

    # 산점도 생성
    plt.scatter(x_data, y_data, color=color_c, label=f"{y} vs {x}", alpha=0.7)
    # 다른 그래프들과 차이점을 주고, 요인별 Quality of Sleep의 결합 산점도에서 확인이 편하도록 색(color_c)을 지정해준다.

    # 1차 회귀선(추세선) 추가
    z = np.polyfit(x_data, y_data, 1)
    p = np.poly1d(z)
    plt.plot(x_data, p(x_data), color='red', linestyle='--', label='Trend Line')

    # 축 레이블 및 제목 설정
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.title(f'Scatter Plot of {y} vs {x} with Trend Line', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True)

    # 그래프 출력
    st.write("")
    st.pyplot(plt)

# 플롯 출력
st.write("")
st.write("")
st.subheader('Quality of Sleep과 Sleep Duration 분석 🌀')
plot_scatter_with_trend('green', 'Sleep Duration(h)', 'Sleep Duration')

# 상관관계 해석
st.markdown('''
수면 시간이 짧을수록 수면의 질이 낮아지는 경향이 관찰됩니다. <br>
7~9시간의 수면이 가장 높은 수면의 질을 보이며,<br>
<u><b>추세선을 통해 수면 시간이 길수록 수면의 질이 향상될 가능성이 있음을 확인할 수 있습니다.</b></u><br>
이에 따라 수면 시간과 수면의 질 사이에는 상관관계가 존재한다고 결론지을 수 있습니다.
''', unsafe_allow_html=True)



# 스트레스 수준과 수면의 질 관계 시각화
st.write("")
st.write("")
st.subheader("Stress Level과 Quality of Sleep의 관계 💢")
plot_scatter_with_trend('blue', 'Stress Level(1~10lv)', 'Stress Level')  # 스트레스 수준과 수면의 질 그래프 생성

# 상관관계 해석
st.markdown('''
스트레스 지수가 높을 수록 수면의 질이 떨어질 수 있다는 패턴이 관찰됩니다.<br>
<u><b>추세선으로 보았을 때 스트레스 지수가 낮을 수록 수면의 질이 높아질 것으로 예측됩니다.</b></u><br>
따라서 스트레스 지수과 수면의 질 사이에는 상관관계가 존재한다고 결론지을 수 있습니다.
''', unsafe_allow_html=True)

# 심박수와 수면의 질 관계 시각화
st.write("")
st.write("")
st.subheader("Heart Rate와 Quality of Sleep의 관계 ❤️‍🔥")
plot_scatter_with_trend('red', 'Heart Rate(bpm)', 'Heart Rate')  # 심박수와 수면의 질 그래프 생성

# 상관관계 해석
st.markdown('''
<u><b>추세선을 보았을 때 심박수가 낮을 수록 수면의 질이 높아지는 것을 확인할 수 있습니다.</b></u><br>
일관되진 않지만 대부분의 점들이 추세선을 따라 왼쪽의 경우에는 위쪽에 분포해있고, 오른쪽의 경우에는 아래쪽에 분포해있는 것을 확인할 수 있습니다.<br>
따라서 수면 시간과 수면의 질 사이에는 상관관계가 존재한다고 결론지을 수 있습니다.
''', unsafe_allow_html=True)

# 결합 산점도: 여러 요인과 수면의 질의 관계
def plot_combined_scatter(data):
    plt.figure(figsize=(15, 6))  # 그래프 크기 설정

    # Stress Level vs. Quality of Sleep
    x1 = data['Stress Level']
    y = data['Quality of Sleep']
    plt.scatter(x1, y, color='blue', label='Stress Level', alpha=0.7)
    z1 = np.polyfit(x1, y, 1)
    plt.plot(x1, np.poly1d(z1)(x1), color='blue', linestyle='--', label='Trend: Stress Level')

    # Sleep Duration vs. Quality of Sleep
    x2 = data['Sleep Duration']
    plt.scatter(x2, y, color='green', label='Sleep Duration', alpha=0.7)
    z2 = np.polyfit(x2, y, 1)
    plt.plot(x2, np.poly1d(z2)(x2), color='green', linestyle='--', label='Trend: Sleep Duration')

    # Normalized Heart Rate vs. Quality of Sleep
    x3 = data['Heart Rate']
    plt.scatter(x3, y, color='red', label='Heart Rate', alpha=0.7)
    z3 = np.polyfit(x3, y, 1)
    plt.plot(x3, np.poly1d(z3)(x3), color='red', linestyle='--', label='Trend: Heart Rate (Normalized)')

    plt.xlabel('Factors (Stress Leve(1~10lv)), Sleep Duration(h), Heart Rate(bpm))', fontsize=12)
    plt.ylabel('Quality of Sleep', fontsize=12)
    plt.title('Combined Scatter Plot of Sleep Quality by Factors', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True)
    st.pyplot(plt)

    

# 결합 산점도 출력
st.write("")
st.write("")
st.subheader("요인별 Quality of Sleep의 결합 산점도 ➕")
plot_combined_scatter(data)
st.markdown("""
세가지 요인과 수면의 질(Quality of Sleep)을 한 그래프로 확인한 결과 다음과 같은 관계를 한 눈에 확인할 수 있다.
""")

# 숙면 팁 제공
st.write("")
st.write("")
container = st.container()
container.markdown("---")

st.header(" 숙면하기 위한 스트레스 줄이는 방법 💤")


st.markdown(""" <br>
        <div style="padding: 20px; border-radius: 15px; border: 2px solid #ccc;">
        <h3><b>✅  일관성 갖기</b></h3> 
        <u>휴일에도 빠짐없이 매일 같은 시간에 잠자리에 들고 일어나면 우리 몸이 규칙적인 수면 각성 주기를 강화합니다.</u> 결국 우리 몸은 잠잘 시간을 자동으로 알게 되어 잠들기가 훨씬 쉬워지는데요. 이렇게 습관이 들면 알람이 울리기 전에 몸이 먼저 일어날 시간을 알아 개운하게 일어날 수 있습니다. 이에 <u>일관성을 가지고 수면을 취할 필요가 있습니다.</u>
        <h3><b>✅  잠들기 전 스크린을 피하기</b></h3>
        텔레비전이나 컴퓨터, 태블릿, 휴대폰 스크린 조명은 우리 수면에 엄청난 영향을 미친다는 연구가 많이 있습니다. <u>스크린에서 나오는 빛은 졸음이 오는 수준을 인공적으로 바꾸고 멜라토닌 수치를 낮춰 잠들기 더 어렵게 하며 수면의 질을 떨어뜨린다고 합니다.</u> 심지어 잠들기 전 텔레비전 시청이나 이메일 확인은 겉보기에 무해한 것 같아도 스크린 조명 때문만이 아니라 그 내용 자체의 자극 때문에 수면에 영향을 미칠 수 있다고 합니다. 우리 뇌는 텔레비전을 끄거나 책을 덮은 후에도 보고 읽은 내용을 계속 처리하기 때문에 편안히 쉬고 잠들기가 어렵습니다. 이에 잠들기 전에 스크린을 보는 것은 숙면을 방해할 수 있으므로 가능한 <u>스크린을 피하는 것이 좋겠습니다.</u>
        <h3><b>✅  취침 의식 만들기</b></h3>
        <u>잠들기 전 간단한 의식을 만들면 우리 뇌와 몸이 긴장을 풀 시간을 알게 하는데 효과적이라고 합니다.</u> 양치나 잠옷 입기처럼 간단해도 좋지만 숙면을 취하는데 문제가 있다면 이 의식에 좀 더 노력을 들여야 합니다. 허브티 마시기나 아로마 오일 바르기, 15~20분 동안 책 읽기(전자책 제외), 혹은 가볍게 그림 그리기도 좋습니다. 오래 걸리지 않는 간단한 과정이지만 <u>긴장 상태와 상관없이 내 몸과 뇌가 잠들 준비를 하기에 충분한 나만의 취침 의식을 만들어 보는 것이 좋습니다.</u>
        <h3><b>✅  정오 이후로 카페인 삼가기</b></h3>
        <u>카페인 과다 복용은 숙면 시간을 단축시키고 자다가 자주 깨게 하여 수면을 방해한다고 합니다.</u> 한 연구에 따르면 소량의 카페인도 수면을 방해할 수 있다고 하며, 취침 전 6시간 이내에 섭취한 카페인이 가장 해롭다고 합니다. 그러므로 <u>오후에는 카페인을 피한다면 전반적인 수면의 질을 향상시킬 수 있습니다.</u>
    </div>
            """, unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")
st.write("출처: [스트레스 해소 방법 - 숙면](http://www.samsunghospital.com/webzine/smcdmedu/279/webzine_279_5.html)")