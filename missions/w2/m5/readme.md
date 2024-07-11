# 워드클라우드 작동 방법

`konlpy` 라이브러리를 사용하여 텍스트에서 명사를 추출하고, `Counter`를 이용해 단어 빈도를 계산합니다. 이후 `WordCloud`를 사용하여 단어 빈도에 따라 워드 클라우드를 생성하고 시각화합니다.

```python
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt

def make_word_cloud(arg, description):
    okt = Okt()
    nouns = okt.nouns(arg)  # 명사만 추출
    words = [n for n in nouns if len(n) > 1]  # 단어의 길이가 1개인 것은 제외
    cons = Counter(words)  # 단어별 빈도수 딕셔너리 데이터 생성
    # 특정 단어와 그 횟수 제거하기
    words_to_remove = ["회사",'직원','자동차','장점','사람','가능']
    for remove_word in words_to_remove:
        if remove_word in cons:
            del cons[remove_word]
    # 특정 단어 교체하기
    if "라벨" in cons:
        cons["워라벨"] = cons.pop("라벨")
    wc = WordCloud(
        font_path="AppleGothic",
        width=400,
        height=400,
        scale=2.0,
        max_font_size=250,
        background_color="white",
    )
    result = wc.generate_from_frequencies(cons)
    plt.figure()
    plt.title(description)  # 제목 추가
    plt.imshow(result, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    return result
```

```python
# 점수가 3 이하인 단점 텍스트를 연결
point = df[df["총점"] < 3]["단점"].str.cat(sep=" ")

# 점수가 3 이하인 단점 텍스트 워드 클라우드 생성
make_word_cloud(point, "총점이 3점 미만인 단점 워드 클라우드")
```
![image](https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/56ef969b-d964-46a4-bb9f-02dc0a641f94)

- **단어 크기 결정**: 단어의 빈도에 비례하여 단어의 크기를 결정함. 빈도가 높은 단어일수록 큰 글씨로 표시됨.
- **단어 배치**:
    - 지정된 캔버스 내에서 단어를 배치함. 일반적으로 중심(0.0)에서 시작하여 빈도가 높은 단어 순으로 나선형 경로를 따라 이동하며 배치함. 이때, 각 단어는 가능한 빈 공간을 찾아 배치됨.
    - 배치 위치에서 충돌 검사를 수행하여 기존 단어와 겹치는지 확인합니다.
    - 겹칠 경우, 나선형 경로를 따라 다음 위치로 이동하여 다시 충돌 검사를 수행
- **랜덤 색상 적용**: 단어에 무작위 색상을 적용하여 시각적 다양성을 제공
