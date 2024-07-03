
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

# 로그 기록 함수
def log_progress(message, etl_path):
    # 시간 형식 정의
    timestamp_format = '%Y-%b-%d-%H:%M:%S'  # 년-월이름-일-시간-분-초 형식
    now = datetime.now()  # 현재 시간 가져오기
    timestamp = now.strftime(timestamp_format)  # 형식에 맞게 시간 문자열로 변환
    # 로그 파일에 기록
    with open(os.path.join(etl_path, 'etl_project_log.txt'), "a") as f:
        f.write(f"{timestamp}, {message}\n")

# 추출 (Extract) 함수
def extract(url, table_attribs, etl_path):
    log_progress('데이터 추출 시작', etl_path)
    html_page = requests.get(url).text  # URL에서 HTML 페이지 가져오기
    html_object = BeautifulSoup(html_page, 'html.parser')  # HTML 파싱
    df = pd.DataFrame(columns=table_attribs)  # 데이터 프레임 초기화

    # 테이블에서 필요한 데이터 스크래핑
    tables = html_object.find_all('tbody')  # 모든 테이블 본문 찾기
    rows = tables[2].find_all('tr')  # 세 번째 테이블 본문에서 모든 행 찾기
    for row in rows:
        col = row.find_all('td')  # 각 행에서 모든 열 찾기
        if len(col) != 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                # 열 데이터 딕셔너리 생성
                data_dict = {
                    "Country": col[0].a.contents[0],
                    "GDP_USD_millions": col[2].contents[0]
                }
                df1 = pd.DataFrame(data_dict, index=[0])  # 데이터 프레임 생성
                df = pd.concat([df, df1], ignore_index=True)  # 데이터 프레임 합치기
    
    log_progress('데이터 추출 완료', etl_path)
    return df

# 변환 (Transform) 함수
def transform(df, etl_path):
    log_progress('데이터 변환 시작', etl_path)
    # GDP 값을 문자열에서 숫자로 변환
    df["GDP_USD_millions"] = df["GDP_USD_millions"].str.replace(',', '').str.strip()
    df["GDP_USD_millions"] = df["GDP_USD_millions"].astype(float)
    df["GDP_USD_billions"] = df["GDP_USD_millions"].div(1000).round(2)  # 단위를 억 달러로 변환
    df.drop(columns=['GDP_USD_millions'], inplace=True)  # 원래 컬럼 삭제
    log_progress('데이터 변환 완료', etl_path)
    return df

# 로드 (Load) 함수 - CSV 파일로 저장
def load_to_csv(df, csv_path, etl_path):
    log_progress('CSV 파일로 데이터 저장 시작', etl_path)
    df.to_csv(csv_path, index=False)  # CSV 파일로 저장
    log_progress('CSV 파일로 데이터 저장 완료', etl_path)

# JSON 파일로 로드하는 함수
def load_gdp_data(df, etl_path):
    log_progress('JSON 파일로 데이터 저장 시작', etl_path)
    # JSON 파일로 저장
    df.to_json(os.path.join(etl_path, 'Countries_by_GDP.json'), orient='records', lines=True)
    log_progress('JSON 파일로 데이터 저장 완료', etl_path)

# 메인 함수
def main():
    # 지정된 경로에 ETL 폴더 생성
    etl_path = '/Users/admin/Documents/GitHub/softeer_wiki/missions/w1/ETL'

    if not os.path.exists(etl_path):
        os.makedirs(etl_path)

    url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
    table_attribs = ["Country", "GDP_USD_millions"]
    csv_path = os.path.join(etl_path, 'Countries_by_GDP.csv')

    log_progress('ETL 프로세스 시작', etl_path)

    # 추출 단계
    df = extract(url, table_attribs, etl_path)
    load_gdp_data(df, etl_path)

    # 변환 단계
    df = transform(df, etl_path)

    # 로드 단계
    load_to_csv(df, csv_path, etl_path)

    log_progress('ETL 프로세스 완료', etl_path)
    log_progress('------------------------------------------', etl_path)

if __name__ == "__main__":
    main()
