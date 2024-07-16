# Documentation

### **1. Docker 이미지 빌드 및 컨테이너 실행**

### 1.1. Dockerfile 작성

먼저 `Dockerfile`을 작성합니다. 이 파일은 Docker 이미지를 빌드하는 데 필요한 명령어를 포함합니다.

```python
# 기본 이미지로 Ubuntu 사용 (특정 플랫폼 지정)
ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} ubuntu:latest

# 환경 변수 설정
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR $HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# 필요한 패키지 설치 및 Hadoop 다운로드, 압축 해제
RUN apt-get update && \
    apt-get install -y ssh rsync openjdk-8-jdk-headless wget vim net-tools && \
    wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION /usr/local/hadoop && \
    rm hadoop-$HADOOP_VERSION.tar.gz && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys && \
    mkdir -p /usr/local/hadoop/logs && \
    mkdir -p /hadoop_data/hdfs/namenode && \
    mkdir -p /hadoop_data/hdfs/datanode && \
    rm -rf /var/lib/apt/lists/*

# 설정 파일 복사
COPY core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
COPY mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml

# Start scripts 복사
COPY start-dfs.sh $HADOOP_HOME/sbin/start-dfs.sh
COPY start-yarn.sh $HADOOP_HOME/sbin/start-yarn.sh

# 스크립트 실행 권한 부여
RUN chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    chmod +x $HADOOP_HOME/sbin/start-yarn.sh

# NameNode, DataNode, ResourceManager 및 NodeManager를 위한 포트 노출
EXPOSE 9870 9864 8088 8042

# 포맷 작업을 컨테이너 시작 시 수행하도록 CMD 수정
CMD ["/bin/bash", "-c", "test -d /hadoop_data/hdfs/namenode/current || $HADOOP_HOME/bin/hdfs namenode -format && $HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh && bash"]

```

### 1.2. Docker 이미지 빌드

다음 명령어를 사용하여 Docker 이미지를 빌드합니다.

```

docker build --platform linux/amd64 -t hadoop-single-node .

```

### 1.3. Docker 컨테이너 실행

Docker 컨테이너를 실행합니다. 포트 충돌을 피하기 위해 호스트 포트를 변경할 수 있습니다.

```
docker volume create hadoop-data

docker run -it --platform linux/amd64 --name hadoop-container -p 9870:9870 -p 9864:9864 -p 8088:8088 -p 8042:8042 -v hadoop-data:/usr/local/hadoop/hdfs hadoop-single-node

```

### **2. 컨테이너 내에서 Hadoop 구성 및 서비스 시작**

### 2.1. 환경 변수 설정

컨테이너 내부에서 다음 명령어를 실행하여 환경 변수를 설정합니다.

```
sh코드 복사
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_NODEMANAGER_USER=root
export YARN_RESOURCEMANAGER_USER=root
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin

```

### 2.2. Hadoop 데몬 중지 및 시작

모든 Hadoop 데몬을 중지하고 다시 시작합니다.

```
sh코드 복사
$HADOOP_HOME/sbin/stop-dfs.sh
$HADOOP_HOME/sbin/stop-yarn.sh

rm -f /tmp/hadoop-root-namenode.pid
rm -f /tmp/hadoop-root-datanode.pid
rm -f /tmp/hadoop-root-resourcemanager.pid
rm -f /tmp/hadoop-root-nodemanager.pid

$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

```

### 2.3. DataNode 수동으로 시작 (필요한 경우)

DataNode가 실행되지 않으면 수동으로 시작합니다.

```
sh코드 복사
hdfs --daemon start datanode

```

### 2.4. 프로세스 상태 확인

`jps` 명령어로 NameNode, DataNode, ResourceManager, NodeManager가 모두 실행 중인지 확인합니다.

```
sh코드 복사
jps

```

### **3. 기본적인 HDFS 작업 수행**

### 3.1. 디렉토리 생성

HDFS에 디렉토리를 생성합니다.

```
sh코드 복사
hadoop fs -mkdir -p /user/hadoop

```

### 3.2. 파일 업로드

호스트에서 생성한 파일을 HDFS에 업로드합니다.

```
sh코드 복사
echo "Hello Hadoop" > /root/sample.txt
hadoop fs -put /root/sample.txt /user/hadoop

```

### 3.3. 디렉토리 내용 확인

HDFS에서 파일을 확인합니다.

```
sh코드 복사
hadoop fs -ls /user/hadoop

```

ㅇㅇ

```python

#터미널에서 Docker 컨테이너를 중지합니다.
docker stop hadoop-container

#Docker 컨테이너를 다시 시작
docker start hadoop-container

docker exec -it hadoop-container bash 

rm -f /tmp/hadoop-root-namenode.pid
rm -f /tmp/hadoop-root-datanode.pid
rm -f /tmp/hadoop-root-resourcemanager.pid
rm -f /tmp/hadoop-root-nodemanager.pid

$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

#업로드된 파일 확인:
hadoop fs -ls /user/hadoop/ 
```

*에러처리

동일컨테이너 중지 및 삭제

```docker
docker stop hadoop-container
docker rm hadoop-container

docker stop hadoop-single-node
docker rm hadoop-single-node

```

포트 충돌 해결

```bash
lsof -i :9870

kill -9 

lsof -i :9864

lsof -i :8088

lsof -i :8042
```