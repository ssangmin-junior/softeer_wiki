<img width="407" alt="image" src="https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/7f50d05c-8645-45d9-8159-b456f82c4cee">
위와 같이 숫자 데이터가 정수형 타입에 담겨있지 않은 상황일 때 
<img width="535" alt="image" src="https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/49c3aba5-526e-4bbe-9d93-9649a0b5f16c">
이러한 코드를 실행하게 되면  다음과 같이 출력되어야 하지만 1,2,3,4 같이 첫자리가 5보다 작은경우 출력결과물에 포함되는 케이스가 있음.
[![image](https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/dd256271-e853-4317-98f9-cb392235b5a1)
](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Feaadccbf-fa7b-4f0f-8726-0ed6710bfdda%2F06b5071d-d340-4341-9179-158e17436d89%2FUntitled.png?table=block&id=8bc8cacb-55f8-4d8c-8f3f-94e119f74c6a&spaceId=eaadccbf-fa7b-4f0f-8726-0ed6710bfdda&width=2000&userId=771d6d77-3ef8-4868-aada-55c140cbf030&cache=v2)
팀과의 회의를 통해 오류를 찾고 해결책을 모색 하였음. 
데이터를 불러들이는 과정에서의 오류로 판단되어 데이터를 읽을 때 숫자가 담긴 컬럼의 데이터 타입을 정수형으로 지정 해주어 오류 해결하였음.
