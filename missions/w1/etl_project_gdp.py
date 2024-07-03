import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

# 로그 기록 함수
def log_progress(message, etl_path):
    timestamp_format = '%Y-%b-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # 현재 시간 가져오기 
    timestamp = now.strftime(timestamp_format) 
    with open(os.path.join(etl_path, 'etl_project_log.txt'), "a") as f: 
        f.write(f"{timestamp}, {message}\n")

# 추출 (Extract) 함수
def extract(url, table_attribs, etl_path):
    log_progress('데이터 추출 시작', etl_path)
    html_page = requests.get(url).text
    HTML_object = BeautifulSoup(html_page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)

    # 테이블에서 필요한 데이터 스크래핑
    tables = HTML_object.find_all('tbody')
    rows = tables[2].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df1], ignore_index=True)
    
    log_progress('데이터 추출 완료', etl_path)
    return df

# 변환 (Transform) 함수
def transform(df, etl_path):
    log_progress('데이터 변환 시작', etl_path)
    df["GDP_USD_millions"] = df["GDP_USD_millions"].str.replace(',', '').str.strip()
    df["GDP_USD_millions"] = df["GDP_USD_millions"].astype(float)
    df["GDP_USD_billions"] = df["GDP_USD_millions"].div(1000).round(2)
    df.drop(columns=['GDP_USD_millions'], inplace=True)  # 원래 컬럼 삭제
    log_progress('데이터 변환 완료', etl_path)
    return df

# 로드 (Load) 함수 - CSV 파일로 저장
def load_to_csv(df, csv_path, etl_path): 
    log_progress('CSV 파일로 데이터 저장 시작', etl_path)
    df.to_csv(csv_path, index=False)
    log_progress('CSV 파일로 데이터 저장 완료', etl_path)

# JSON 파일로 로드하는 함수
def load_gdp_data(df, etl_path):
    log_progress('JSON 파일로 데이터 저장 시작', etl_path)
    df.to_json(os.path.join(etl_path, 'Countries_by_GDP.json'), orient='records', lines=True)
    log_progress('JSON 파일로 데이터 저장 완료', etl_path)

# Main
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
