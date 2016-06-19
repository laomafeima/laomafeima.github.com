## Hadoop 环境搭建

####配置免密码登录
添加 hadoop 用户  
```
$ sudo addgroup hadoop
$ sudo adduser --ingroup hadoop hadoop
```

编辑`/etc/sudoers`文件，在

    root ALL=(ALL:ALL)ALL
    # 行下添加
    hadoop ALL=(ALL:ALL) ALL


否则无法sudo  
然后切换用hadoop登录  

生成ssh密钥
```
$ mkdir .ssh
$ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa 
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
测试登录
```
$ ssh localhost
```
####解压和配置环境变量
解压 jdk 和 hadoop  
```
$ tar zxvf  jdk.tar.gz  
$ tar zxvf  hadoop.tar.gz
```
把目录移动到`/opt/`目录下
```
$ mv -R ./jdk1.8.0_25 /opt/
$ sudo chown -R hadoop:hadoop /opt/jdk1.8.0_25
$ mv -R ./hadoop-2.6.0 /opt/
$ sudo chown -R hadoop:hadoop /opt/hadoop-2.6.0
```
配置环境变量 
```
$ vim .profile
```
```
export JAVA_HOME=/opt/jdk1.8.0_25  
export PATH=$JAVA_HOME/bin:$PATH  
export CLASSPATH=$JAVA_HOME/lib  

export HADOOP_INSTALL=/opt/hadoop-2.6.0  
export PATH=$PATH:$HADOOP_INSTALL/bin  
```
指定 jdk 路径  

修改`$HADOOP_HOME/etc/hadoop/hadoop-env.sh` 和 `yarn-env.sh`
文件把JAVA_HOME指向JDK
```
export JAVA_HOME=/opt/jdk1.8.0_25
```

####修改 hadoop 配置
修改配置`$HADOOP_HOME/etc/hadoop/core-site.xml`

```
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/opt/hadoop-2.6.1/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://0.0.0.0:9000</value>
    </property>
</configuration>
```
修改配置`$HADOOP_HOME/etc/hadoop/hdfs-site.xml`

```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/opt/hadoop-2.6.1/tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/opt/hadoop-2.6.1/tmp/dfs/data</value>
    </property>
</configuration>

```
如果需要修改 `mapred-site.xml` 配置
```
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>     
        <name>mapred.job.tracker</name>    
        <value>localhost:9001</value>     
    </property>
</configuration>
```

####启动
格式化 HDFS 
```
$ hadoop namenode -format 
$ hadoop datanode -format
```
启动
```
$ $HADOOP_HOME/sbin/start-all.sh
```
然后输入 jps 查看进程。
```
2053 ResourceManager
2183 NodeManager
2216 Jps
1560 NameNode
1898 SecondaryNameNode
1694 DataNode
```
要有以上6个进程。缺少一个则配置有误。  
成功之后可以通过 `http://localhost:50070/` 查看 HDFS 状态。
通过 `http://localhost:8088/` 查看 job 状态。

####测试
使用 HDFS 首先要创建用户目录
```
$ bin/hdfs dfs -mkdir -p /user/hadoop
```
创建并上传文件到`input`目录
```
$ bin/hdfs dfs -mkdir input
$ bin/hdfs dfs -put etc/hadoop/*.xml input
$ bin/hdfs dfs -ls input
```
运行
```
$ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar grep input output
```

查看输出结果
```
$ bin/hdfs dfs -cat output/*
```
Hadoop运行程序时，默认输出目录不能存在，因此再次运行需要执行如下命令删除 output文件夹:
```
$ bin/hdfs dfs -rm -r /user/hadoop/output
```
需要关闭的时候一定要显式的调用 `sbin/stop-all.sh`

