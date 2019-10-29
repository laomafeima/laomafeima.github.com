title: 一个 SSH 服务无法启动的问题
date: 2018-09-24
type: note
tags: 服务器

# 一个 SSH 服务无法启动的问题

升级了一下 Ubuntu 到18.04.1 升级后重启发现无法 ssh 上去。查看 ssh 端口发现没有启动，就去启动 ssh 服务发现

```
$ service ssh start
Job for ssh.service failed because the control process exited with error code.
See "systemctl status ssh.service" and "journalctl -xe" for details.
```

然后执行`systemctl status ssh.service` 也并没有给出什么有价值的信息。
通过搜索找到了 `/usr/sbin/sshd -T` 这个命令，运行后直接可以定位到错误
```
$ /usr/sbin/sshd -T
......
/etc/sshd/sshd_config line 83: Bad SSH2 cipher spec 'chacha20-poly1305@openssh.com,aes128-gcm@openssh.com,aes256-gcm@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,aes192-cbc,aes256-cbc'.
```

是有不支持的 Cipher ,可能是因为刚好升级  OpenSSH 的原因。
这样一来问题就变得好解决了，只需要更新一下配置文件即可，首先查看一下现在支持 Ciphers

```
$ ssh -Q cipher
3des-cbc
aes128-cbc
aes192-cbc
aes256-cbc
rijndael-cbc@lysator.liu.se
aes128-ctr
aes192-ctr
aes256-ctr
aes128-gcm@openssh.com
aes256-gcm@openssh.com
chacha20-poly1305@openssh.com
```

接下来更新到`/etc/ssh/sshd_config` 文件就好了

```
Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc,rijndael-cbc@lysator.liu.se,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,chacha20-poly1305@openssh.com
```
然后启动 ssh 服务就成功了。

当然事情的结尾是，我依然没有能连上，因为 网卡配置莫名的丢了😂，懒得继续折腾了。重装好了。
