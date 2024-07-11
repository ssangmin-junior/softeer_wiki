# AWS EC2에 배포하기

# Mission: AWS EC2에 배포하기

**User-data**

```python
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
```

 **AWS CLI 구성**

`aws configure`

```python
AWS Access Key ID [None]: <your-access-key-id> # AK******
AWS Secret Access Key [None]: <your-secret-access-key> # *******
Default region name [None]: <your-region>   # ap-northeast-2
Default output format [None]: json
```

```python
aws ecr create-repository --repository-name aws --region ap-northeast-2

```

```python
cd /Users/admin/aws

docker build -t aws:latest .
docker tag aws:latest  992382854808.dkr.ecr.ap-southeast-2.amazonaws.com/aws:latest
docker push 992382854808.dkr.ecr.ap-southeast-2.amazonaws.com/aws:latest

```

ec2에서 수행

```python
# EC2 인스턴스에 접속 
ssh -i ~/.ssh/key.pem ec2-user@44.220.139.182

# Docker 이미지 가져오기
docker pull 992382854808.dkr.ecr.ap-northeast-2.amazonaws.com/aws:latest
docker run -d -p 8888:8888 992382854808.dkr.ecr.ap-northeast-2.amazonaws.com/aws:latest
```

Docker 컨테이너 실행

```python
docker run -d -p 8888:8888 --name python_jupyter_3_9 992382854808.dkr.ecr.ap-northeast-2.amazonaws.com/python_jupyter:3.9
docker run -d -p 8888:8888 --name python_jupyter_3_9 992382854808.dkr.ecr.ap-northeast-2.amazonaws.com/aws:latest
```

```python
# Jupyter Notebook 실행
$ docker exec -it python_jupyter_3_9 /bin/bash
$ jupyter notebook --no-browser --allow-root --ip=0.0.0.0 --port=8888

```

### 만약에 서버를 사야 한다면? 어떤 일들을 해야 할까?

- 보안은?
    - 방화벽 설정:
    - SSH 보안
    - 
- 단기간만 필요하다면?
    - 클라우드 서비스 이용
    - EC2 스팟 인스턴스

### AWS EC2에 Docker Image를 배포하려면 어디에 뭐가 있어야 할까?

1. **AWS 계정**:
    - AWS 서비스에 접근하기 위한 AWS 계정이 필요합니다.
2. **EC2 인스턴스**:
    - Docker를 실행할 EC2 인스턴스를 생성합니다.
    - EC2 인스턴스에 SSH로 접근할 수 있어야 합니다.
3. **Docker 설치**:
    - EC2 인스턴스에 Docker를 설치합니다.
    - 설치 명령 예시: `sudo apt-get update && sudo apt-get install -y docker.io`
4. **Docker 이미지**:
    - Docker Hub 또는 자체 Docker Registry에 배포할 Docker 이미지를 준비합니다.

### 배포 절차

1. **EC2 인스턴스 생성 및 설정**:
    - AWS 관리 콘솔에서 EC2 인스턴스를 생성하고, 필요한 보안 그룹 설정을 합니다.
    - SSH 키 페어를 사용하여 인스턴스에 접근할 수 있도록 합니다.
