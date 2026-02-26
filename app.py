## 박수연의 한국 복지패널 대시보드 스트림릿 실행 코드

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# 1. 웹 페이지 설정 및 로고 로드
# 로고 이미지 경로가 정확한지 확인하세요.
logo_path = r"D:\Steamlit\logo.png"
try:
    img = Image.open(logo_path)
except Exception:
    img = None # 이미지 파일이 없을 경우를 대비한 예외 처리

st.set_page_config(
    layout="wide", 
    page_title="박수연의 한국 복지패널 대시보드", 
    page_icon=img
)

# 2. 사이드바 상단 로고 및 타이틀 설정
with st.sidebar:
    if img:
        # 버전 호환성을 위해 use_column_width 사용
        st.image(img, use_column_width=True) 
    st.title("박수연의 한국 복지패널 대시보드")
    st.markdown("---")

# 한글 폰트 지정
plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False


# 데이터 로드 함수
@st.cache_data
def load_welfare(sav_path: str):
    raw_welfare = pd.read_csv(sav_path)
    welfare = raw_welfare.copy()
    welfare = welfare.rename(
        columns={
            "h10_g3": "sex",            # 성별
            "h10_g4": "birth_year",     # 태어난 연도
            "h10_g10": "marital_status", # 혼인 상태
            "h10_g11": "religion",       # 종교
            "h10_eco9": "job_code",      # 직업 코드
            "p1002_8aq1": "income",      # 월급
            "h10_reg7": "region_code",   # 지역 코드
        }
    )

    # 전처리
    if "sex" in welfare.columns:
        welfare["sex"] = welfare["sex"].replace(9, np.nan)
        welfare["sex"] = welfare["sex"].map({1: "male", 2: "female"})

    if "income" in welfare.columns:
        welfare["income"] = welfare["income"].replace(9999, np.nan)
        welfare["income"] = np.where(welfare["income"] == 0, np.nan, welfare["income"])

    if "birth_year" in welfare.columns:
        welfare["birth_year"] = welfare["birth_year"].replace(9999, np.nan)
        welfare["age"] = 2015 - welfare["birth_year"] + 1

        def age_group(age):
            if pd.isnull(age):
                return np.nan
            elif age >= 60:
                return "old"
            elif age >= 30:
                return "middle"
            else:
                return "young"
        welfare["age_group"] = welfare["age"].apply(age_group)

    if "job_code" in welfare.columns:
        welfare["job_code"] = np.where(welfare["job_code"] == 9999, np.nan, welfare["job_code"])
        # 직종 코드북 경로 확인 필요
        try:
            job_list = pd.read_excel("D:/Steamlit/welfare_2015_codebook.xlsx", sheet_name="직종코드")
            welfare = welfare.merge(job_list, how="left", on="job_code")
        except:
            pass

    if "religion" in welfare.columns:
        welfare['religion'] = np.where(welfare['religion'] == 9, np.nan, welfare['religion'])
        welfare['religion'] = welfare['religion'].map({1:'yes', 2:'no'})

    if "marital_status" in welfare.columns:
        def divorce_yn(marital_status):
            if marital_status == 1: return 'marriage'
            elif marital_status == 3: return 'divorce'
            else: return np.nan
        welfare['marriage'] = welfare['marital_status'].apply(divorce_yn)

    if "region_code" in welfare.columns:
        region_list = pd.DataFrame({
            'region_code' : [1, 2, 3, 4, 5, 6, 7],
            'region' : ['서울', '수도권(인천/경기)', '부산/경남/울산', '대구/경북', '대전/충남', '강원/충북', '광주/전남/전북/제주도']
        })
        welfare = welfare.merge(region_list, how='left', on='region_code')

    return welfare


# 3. 사이드바 컨트롤
st.sidebar.header("📂 데이터 로드")
data_path = st.sidebar.text_input("데이터 파일 경로", value="D:/Steamlit/welfare_2015.csv")

if st.sidebar.button("데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()

# 메인 섹션
st.title("한국복지패널 대시보드")
st.markdown("데이터 출처: 복지패널 데이터")

# 데이터 로드 시도
try:
    welfare = load_welfare(data_path)
    st.success(f"데이터 로드 완료: {welfare.shape[0]}행 {welfare.shape[1]}열")
except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
    st.stop()

# 대시보드 레이아웃
# 필터
st.sidebar.header("필터")

# 성별 필터
if "sex" in welfare.columns:
    value_list = ["All"] + sorted(welfare["sex"].dropna().unique().tolist())
    select_sex = st.sidebar.selectbox("성별", value_list, index=0)
else:
    select_sex = "All"

# 연령 범위 필터
if "age" in welfare.columns:
    min_age = int(welfare["age"].dropna().min())
    max_age = int(welfare["age"].dropna().max())
    slider_range = st.sidebar.slider(
        "연령 범위", min_value=min_age, max_value=max_age, value=(min_age, max_age)
    )
    filter_button = st.sidebar.button("필터 적용")
else:
    slider_range = None

# 연령대 필터
# 여러 개 선택할 수 있는 multiselect
value_list = ["All"] + sorted(welfare["age_group"].dropna().unique().tolist())
if "age_group" in welfare.columns:
    select_multi_age_group = st.sidebar.multiselect(
        "확인하고 싶은 연령대를 선택하세요(복수 선택 가능)",
        value_list,
    )
else:
    select_multi_age_group = "All"

# 직업 필터
# 여러 개 선택할 수 있는 multiselect
value_list = ["All"] + sorted(welfare["job"].dropna().unique().tolist())
if "job" in welfare.columns:
    select_multi_job = st.sidebar.multiselect(
        "확인하고 싶은 직업을 선택하세요(복수 선택 가능)",
        value_list,
    )
else:
    select_multi_job = "All"

# 종교 필터
if "religion" in welfare.columns:
    value_list = ["All"] + sorted(welfare["religion"].dropna().unique().tolist())
    select_religion = st.sidebar.selectbox("종교", value_list, index=0)
else:
    select_religion = "All"

# 혼인 필터
if "marriage" in welfare.columns:
    value_list = ["All"] + sorted(welfare["marriage"].dropna().unique().tolist())
    select_marriage = st.sidebar.selectbox("혼인", value_list, index=0)
else:
    select_marriage = "All"

# 지역 필터
# 여러 개 선택할 수 있는 multiselect
value_list = ["All"] + sorted(welfare["region"].dropna().unique().tolist())
if "region" in welfare.columns:
    select_multi_region = st.sidebar.multiselect(
        "확인하고 싶은 지역을 선택하세요(복수 선택 가능)",
        value_list,
    )
else:
    select_multi_region = "All"

# 성별에 따른 월급 차이 - '성별에 따라 월급이 다를까?'
st.subheader("1. 성별에 따른 월급 차이 - '성별에 따라 월급이 다를까?'")

if select_sex != "All" and "sex" in welfare.columns:
    tmp_welfare = welfare[welfare["sex"] == select_sex]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "sex" in welfare.columns and "income" in welfare.columns:
        sex_income = (
            welfare.dropna(subset=["sex", "income"])
            .groupby("sex", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig1, ax1 = plt.subplots()
        sns.barplot(x="sex", y="mean_income", data=sex_income, ax=ax1)
        plt.title("성별에 따른 평균 월급 막대 그래프")
        plt.xlabel("성별")
        plt.ylabel("평균 월급")
        for i, j in enumerate(sex_income["mean_income"]):
            ax1.annotate(
                round(j),
                (i, j),
                xytext=(0, 2),
                textcoords="offset points",
                fontsize=8,
                ha="center",
                color="black",
            )
        st.pyplot(fig1)
    else:
        st.info("성별/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "sex" in welfare.columns and "income" in welfare.columns:
        st.write(sex_income)
    else:
        st.write("변수 없음")

# 나이와 월급의 관계 - '몇 살 때 월급을 가장 많이 받을까?'
st.subheader("2. 나이와 월급의 관계 - '몇 살 때 월급을 가장 많이 받을까?'")

if filter_button:
    tmp_welfare = welfare[
        (welfare["age"] >= slider_range[0]) & (welfare["age"] <= slider_range[1])
    ]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "age" in welfare.columns and "income" in welfare.columns:
        age_income = (
            welfare.dropna(subset=["age", "income"])
            .groupby("age", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig2, ax2 = plt.subplots()
        sns.lineplot(x="age", y="mean_income", data=age_income, ax=ax2)
        plt.title("나이에 따른 평균 월급 선 그래프")
        plt.xlabel("나이")
        plt.ylabel("평균 월급")
        st.pyplot(fig2)
    else:
        st.info("나이/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "age" in welfare.columns and "income" in welfare.columns:
        st.write(age_income)
    else:
        st.write("변수 없음")

# 나머지 주제는 여러분들이 직접 만들어 보아요!
# 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까?
st.subheader("3. 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까?")

if select_multi_age_group != "All" and "age_group" in welfare.columns:
    tmp_welfare = welfare[welfare["age_group"].isin(select_multi_age_group)]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "age_group" in welfare.columns and "income" in welfare.columns:
        age_group_income = (
            welfare.dropna(subset=["age_group", "income"])
            .groupby("age_group", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig3, ax3 = plt.subplots()
        sns.barplot(
            x="age_group",
            y="mean_income",
            data=age_group_income,
            ax=ax3,
            order=["young", "middle", "old"],
        )
        plt.title("연령대에 따른 평균 월급 막대 그래프")
        plt.xlabel("연령대")
        plt.ylabel("평균 월급")
        st.pyplot(fig3)
    else:
        st.info("연령대/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "age_group" in welfare.columns and "income" in welfare.columns:
        st.write(age_group_income)
    else:
        st.write("변수 없음")

# 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까?
st.subheader("4. 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까?")

if (
    select_sex != "All"
    and select_multi_age_group != "All"
    and "sex" in welfare.columns
    and "age_group" in welfare.columns
):
    tmp_welfare = welfare[
        (welfare["sex"] == select_sex)
        & (welfare["age_group"].isin(select_multi_age_group))
    ]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if (
        "sex" in welfare.columns
        and "age_group" in welfare.columns
        and "income" in welfare.columns
    ):
        age_group_sex_income = (
            welfare.dropna(subset=["age_group", "sex", "income"])
            .groupby(["age_group", "sex"], as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        # 시각화
        fig4, ax4 = plt.subplots()
        sns.barplot(
            x="age_group",
            y="mean_income",
            hue="sex",
            data=age_group_sex_income,
            order=["young", "middle", "old"],
            ax=ax4,
        )
        plt.title("연령대 및 성별에 따른 평균 월급 막대 그래프")
        plt.xlabel("연령대 및 성별")
        plt.ylabel("평균 월급")
        st.pyplot(fig4)
    else:
        st.info("연령대/성별/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if (
        "sex" in welfare.columns
        and "age_group" in welfare.columns
        and "income" in welfare.columns
    ):
        st.write(age_group_sex_income)
    else:
        st.write("변수 없음")

# 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까?
st.subheader("5. 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까?")

if select_multi_job != "All" and "job" in welfare.columns:
    tmp_welfare = welfare[welfare["job"].isin(select_multi_job)]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "job" in welfare.columns and "income" in welfare.columns:
        job_income = (
            welfare.dropna(subset=["job", "income"])
            .groupby("job", as_index=False)
            .agg(mean_income=("income", "mean"))
        )
        top10 = job_income.sort_values("mean_income", ascending=False).head(10)
        # 시각화
        fig5, ax5 = plt.subplots()
        sns.barplot(y="job", x="mean_income", data=top10)
        plt.title("직업에 따른 상위 10개 평균 월급 막대 그래프")
        plt.xlabel("직업")
        plt.ylabel("평균 월급")
        st.pyplot(fig5)
    else:
        st.info("직업/월급 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "job" in welfare.columns and "income" in welfare.columns:
        st.write(top10)
    else:
        st.write("변수 없음")

# 성별 직업 빈도 - 성별로 어떤 직업이 가장 많을까?
st.subheader("6. 성별 직업 빈도 - 성별로 어떤 직업이 가장 많을까?")

if (
    select_sex != "All"
    and select_multi_job != "All"
    and "sex" in welfare.columns
    and "job" in welfare.columns
):
    tmp_welfare = welfare[
        (welfare["sex"] == select_sex)
        & (welfare["job"].isin(select_multi_job))
    ]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if (
        "sex" in welfare.columns
        and "job" in welfare.columns
    ):
        job_male = welfare[welfare['sex'] == 'male'].dropna(subset = ['job']) \
                                            .groupby('job', as_index = False) \
                                            .agg(n = ('job', 'count')) \
                                            .sort_values('n', ascending = False) \
                                            .head(10)
        # 시각화
        fig61, ax61 = plt.subplots()
        sns.barplot(y = 'job', x = 'n', data = job_male, ax=ax61)
        plt.title("남성 직업 빈도 막대 그래프")
        plt.xlabel("빈도")
        plt.ylabel("직업")
        st.pyplot(fig61)
    else:
        st.info("성별/직업 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if (
        "sex" in welfare.columns
        and "job" in welfare.columns
    ):
        st.write(job_male)
    else:
        st.write("변수 없음")

col1, col2 = st.columns([2, 1])
with col1:
    if (
        "sex" in welfare.columns
        and "job" in welfare.columns
    ):
        job_female = welfare[welfare['sex'] == 'female'].dropna(subset = ['job']) \
                                                .groupby('job', as_index = False) \
                                                .agg(n = ('job', 'count')) \
                                                .sort_values('n', ascending = False) \
                                                .head(10)
        # 시각화
        fig62, ax62 = plt.subplots()
        sns.barplot(y = 'job', x = 'n', data = job_female, ax=ax62)
        plt.title("여성 직업 빈도 막대 그래프")
        plt.xlabel("빈도")
        plt.ylabel("직업")
        st.pyplot(fig62)
    else:
        st.info("성별/직업 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if (
        "sex" in welfare.columns
        and "job" in welfare.columns
    ):
        st.write(job_female)
    else:
        st.write("변수 없음")

# 종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?
st.subheader("7. 종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?")

if select_religion != "All" and "religion" in welfare.columns and select_marriage != "All" and "marriage" in welfare.columns:
    tmp_welfare = welfare[(welfare["religion"] == select_religion) & (welfare["marriage"] == select_marriage)]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if "religion" in welfare.columns and "marriage" in welfare.columns:
        religion_div = welfare.dropna(subset = ['religion', 'marriage']) \
                      .groupby('religion', as_index = False) \
                      ['marriage'] \
                      .value_counts(normalize = True)
        religion_div = religion_div[religion_div['marriage'] == 'divorce'] \
               .assign(proportion = religion_div['proportion'] * 100) \
               .round(2)
        # 시각화
        fig71, ax71 = plt.subplots()
        sns.barplot(x = "religion", y = 'proportion', data = religion_div, ax=ax71)
        plt.title("종교에 따른 이혼율 막대 그래프")
        plt.xlabel("종교")
        plt.ylabel("이혼율")
        st.pyplot(fig71)
    else:
        st.info("종교/혼인 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "religion" in welfare.columns and "marriage" in welfare.columns:
        st.write(religion_div)
    else:
        st.write("변수 없음")

col1, col2 = st.columns([2, 1])
with col1:
    if "age_group" in welfare.columns and "religion" in welfare.columns:
        # 비율 계산
        age_group_div = welfare.dropna(subset = ['age_group', 'religion']) \
                        .groupby('age_group', as_index = False) \
                        ['marriage'] \
                        .value_counts(normalize = True)
        age_group_div = age_group_div[(age_group_div['marriage'] == 'divorce') & (age_group_div['age_group'] != 'young')] \
                             .assign(proportion = age_group_div['proportion'] * 100) \
                             .round(2)
        # 시각화
        fig72, ax72 = plt.subplots()
        sns.barplot(x = "age_group", y = 'proportion', data = age_group_div, ax=ax72)
        plt.title("연령대에 따른 이혼율 막대 그래프")
        plt.xlabel("연령대")
        plt.ylabel("이혼율")
        st.pyplot(fig72)
    else:
        st.info("연령대/혼인 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "religion" in welfare.columns and "marriage" in welfare.columns:
        st.write(age_group_div)
    else:
        st.write("변수 없음")

col1, col2 = st.columns([2, 1])
with col1:
    if "age_group" in welfare.columns and "religion" in welfare.columns and "marriage" in welfare.columns:
        # 비율 계산
        age_group_rel_div = welfare[welfare['age_group'] != 'young'] \
                      .dropna(subset = ['age_group', 'religion', 'marriage']) \
                      .groupby(['age_group', 'religion'], as_index = False) \
                       ['marriage'] \
                       .value_counts(normalize = True)
        age_group_rel_div = age_group_rel_div[age_group_rel_div['marriage'] == 'divorce'] \
                    .assign(proportion = age_group_rel_div['proportion'] * 100) \
                    .round(2)
        # 시각화
        fig73, ax73 = plt.subplots()
        sns.barplot(x = 'age_group', y = 'proportion', hue = 'religion', data = age_group_rel_div, ax=ax73)
        plt.title("연령대 및 종교 유무에 따른 이혼율 막대 그래프")
        plt.xlabel("연령대 및 종교 유무")
        plt.ylabel("이혼율")
        st.pyplot(fig73)
    else:
        st.info("연령대/종교/혼인 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if "religion" in welfare.columns and "marriage" in welfare.columns:
        st.write(age_group_rel_div)
    else:
        st.write("변수 없음")

# 지역별 연령대 비율 - 어느 지역에 노년층이 많을까?
st.subheader("8. 지역별 연령대 비율 - 어느 지역에 노년층이 많을까?")

if (
    select_multi_region != "All"
    and select_multi_age_group != "All"
    and "region" in welfare.columns
    and "age_group" in welfare.columns
):
    tmp_welfare = welfare[
        (welfare["region"].isin(select_multi_region))
        & (welfare["age_group"].isin(select_multi_age_group))
    ]
    st.write("필터로 선택한 데이터 첫 5행")
    st.table(tmp_welfare.head())

col1, col2 = st.columns([2, 1])
with col1:
    if (
        "region" in welfare.columns
        and "age_group" in welfare.columns
    ):
        region_age_group = welfare.dropna(subset = ['age_group']) \
                     .groupby('region', as_index = False) \
                     ['age_group'] \
                     .value_counts(normalize = True)
        region_age_group = region_age_group.assign(proportion = region_age_group['proportion'] * 100) \
                                   .round(2)
        pivot_region_age_group = region_age_group[['region', 'age_group', 'proportion']] \
                          .pivot(index   = 'region',
                          columns = 'age_group',
                          values  = 'proportion')
        reorder_pivot_region_age_group = pivot_region_age_group.sort_values('old')[['young', 'middle', 'old']]
        # 시각화
        fig8, ax8 = plt.subplots()
        reorder_pivot_region_age_group.plot.barh(stacked = True, ax=ax8)
        plt.legend(bbox_to_anchor=(1.0, 1.0))
        plt.title("지역별 연령대 비율 그래프")
        plt.xlabel("연령대 비율")
        plt.ylabel("지역")
        st.pyplot(fig8)
    else:
        st.info("지역/연령대 변수가 없어 해당 그래프를 표시할 수 없습니다.")
with col2:
    st.markdown("테이블")
    if (
        "region" in welfare.columns
        and "age_group" in welfare.columns
    ):
        st.write(pivot_region_age_group.sort_values('old', ascending = False)[['young', 'middle', 'old']])
    else:
        st.write("변수 없음")

# 끝
