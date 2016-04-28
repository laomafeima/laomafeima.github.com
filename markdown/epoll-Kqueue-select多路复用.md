epoll 事件的检测
1

epoll 事件中发现
就EPOLLIN , EPOLLOUT , EPOLLPRI可以用.

EPOLLERR 和 EPOLLHUP什么情况下才能监测出这种问题啊.

我的内核是2.6.20
可是用EPOLLRDHUP的时候编译包错.
RecvMessThread.cpp:48: error: ‘EPOLLRDHUP’ was not declared in this scope


2.

1、listen fd，有新连接请求，触发EPOLLIN。
2、对端发送普通数据，触发EPOLLIN。
3、带外数据，只触发EPOLLPRI。
4、对端正常关闭（程序里close()，shell下kill或ctr+c），触发EPOLLIN和EPOLLRDHUP，但是不触发EPOLLERR和EPOLLHUP。
    关于这点，以前一直以为会触发EPOLLERR或者EPOLLHUP。
    再man epoll_ctl看下后两个事件的说明，这两个应该是本端（server端）出错才触发的。
5、对端异常断开连接（只测了拔网线），没触发任何事件。


附man：

EPOLLIN       连接到达；有数据来临；
              The associated file is available for read(2) operations.
EPOLLOUT      有数据要写
              The associated file is available for write(2) operations.
EPOLLRDHUP    这个好像有些系统检测不到，可以使用EPOLLIN，read返回0，删除掉事件，关闭close(fd);
              如果有EPOLLRDHUP，检测它就可以直到是对方关闭；否则就用上面方法。
              Stream socket peer closed connection, or shut down writing half
              of connection. (This flag is especially useful for writing sim-
              ple code to detect peer shutdown when using Edge Triggered moni-
              toring.)
EPOLLPRI      外带数据
              There is urgent data available for read(2) operations.

              
EPOLLERR      只有采取动作时，才能知道是否对方异常。即对方突然断掉，是不可能
              有此事件发生的。只有自己采取动作（当然自己此刻也不知道），read，
              write时，出EPOLLERR错，说明对方已经异常断开。
              
              EPOLLERR 是服务器这边出错（自己出错当然能检测到，对方出错你咋能
              直到啊）
              
              Error condition happened on the associated file descriptor.
              epoll_wait(2) will always wait for this event; it is not neces-
              sary to set it in events.
              
EPOLLHUP
              Hang up   happened   on   the   associated   file   descriptor.
              epoll_wait(2) will always wait for this event; it is not neces-
              sary to set it in events.
              
EPOLLET       边缘触发模式
              Sets the Edge Triggered behavior for the associated file
              descriptor.   The default behavior for epoll is Level Triggered.
              See epoll(7) for more detailed information about Edge and Level
              Triggered event distribution architectures.
              
EPOLLONESHOT (since Linux 2.6.2)
              Sets the one-shot behavior for the associated file descriptor.
              This means that after an event is pulled out with epoll_wait(2)
              the associated file descriptor is internally disabled and no
              other events will be reported by the epoll interface. The user
              must call epoll_ctl() with EPOLL_CTL_MOD to re-enable the file
              descriptor with a new event mask.

关于EPOLLERR：
！！！！！！socket能检测到对方出错吗？目前为止，好像我还不知道如何检测。
但是，在给已经关闭的socket写时，会发生EPOLLERR，也就是说，只有在采取行动（比如
读一个已经关闭的socket，或者写一个已经关闭的socket）时候，才知道对方是否关闭了。
这个时候，如果对方异常关闭了，则会出现EPOLLERR，出现Error把对方DEL掉，close就可以
了。！！！！！！！

关于EPOLLHUP：
！！！！！！socket能检测到对方出错吗？目前为止，好像我还不知道如何检测。
但是，在给已经关闭的socket写时，会发生EPOLLERR，也就是说，只有在采取行动（比如
读一个已经关闭的socket，或者写一个已经关闭的socket）时候，才知道对方是否关闭了。
这个时候，如果对方异常关闭了，则会出现EPOLLERR，出现Error把对方DEL掉，close就可以
了。！！！！！！！

3.各类事件

1）监听的fd，此fd的设置等待事件：
    EPOLLIN ；或者EPOLLET |EPOLLIN 
    
    由于此socket只监听有无连接，谈不上写和其他操作。
    故只有这两类。（默认是LT模式，即EPOLLLT |EPOLLIN）。
    
    说明：如果在这个socket上也设置EPOLLOUT等，也不会出错，
    只是这个socket不会收到这样的消息。

2）客户端正常关闭
client 端close()联接

server 会报某个sockfd可读，即epollin来临。 
然后recv一下 ， 如果返回0再掉用epoll_ctl 中的EPOLL_CTL_DEL , 同时close(sockfd)。

有些系统会收到一个EPOLLRDHUP，当然检测这个是最好不过了。只可惜是有些系统，
上面的方法最保险；如果能加上对EPOLLRDHUP的处理那就是万能的了。


3）客户端异常关闭：

     客户端异常关闭，并不会通知服务器（如果会通知，以前的socket当然会有与此相关
     的api）。正常关闭时read到0后，异常断开时检测不到的。服务器再给一个已经关闭
     的socket写数据时，会出错，这时候，服务器才明白对方可能已经异常断开了（读也
     可以）。
     
     Epoll中就是向已经断开的socket写或者读，会发生EPollErr，即表明已经断开。

4）EpollIn：
     
     
     
5）监听的skocket只需要EpollIn就足够了，EpollErr和EpollHup会自动加上。
    监听的socket又不会写，一个EpollIn足矣。
    
        
4. 补充 EpollErr

当客户端的机器在发送“请求”前，就崩溃了（或者网络断掉了），则服务器一端是无从知晓的。

按照你现在的这个“请求响应方式”，无论是否使用epoll，都必须要做超时检查。

因此，这个问题与epoll无关。

因此，EpollErr这种错误必须是有动作才能检测出来。
服务器不可能经常的向客户端写一个东西，依照有没有EpollErr来判断
客户端是不是死了。

因此，服务器中的超时检查是很重要的。这也是以前服务器中作死后确认的原因。
新的代码里也是时间循环，时间循环....

