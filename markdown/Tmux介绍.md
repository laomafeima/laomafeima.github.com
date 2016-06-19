＃tmux
## tmux 简介
tmux 是一个终端复用软件，类似 Linux 下的 Screen。但是相比之下 Tmux 窗口功能，能在终端下提供类似窗口的功能操作。  
只要在服务器上运行起 tmux 服务端之后，无论 ssh 掉线还是其它原因。那么所有的操作和输出都还在。可以再次恢复。很适合多台电脑或者工作厂地切换的时候，都能实现无缝切换，一致的体验。

## 概念模型
|  模块  |  介绍  |
|:-:|:-|
|Server |服务，服务运行基础服务，维持每一个 seesion|
|Session|会话，一个服务可以有多个会话，每个会话之间相互独立|
|Window |窗口，一个会话里面的可以有多个窗口。一个窗口可以包含多个面板，显示的时候只会显示一个窗口|
|Panel  |面板，每个窗口可以包含并显示多个面板，每个面板都可以独立的运行命令或程序，可以在面板之间自由切换|

运行 tmux 命令后就会自动创建一个服务，会话，窗口，面板。一个服务可以维持多个会话，当最后一个会话被关闭的时候服务也会关闭。

## 基本操作
### 牛刀小试
运行 `tmux` 命令，会自动创建一个临时会话，可以看到似乎和普通的终端没什么区别，只是在最下面多了一行类似 Vim 的状态栏。后面我们会介绍如何配置状态栏。  
在里面输入几条命令和往常一样没有什么区别。输入 `exit` 可以退出 tmux 而不是退出终端。
### 快捷键前缀（Prefix）
为了避免 tmux 自身的快捷键与其它软件冲突，所以在使用 tmux 快捷键的时候需要先按前缀键然后在操作，这样可以很好的避免快捷冲突，尤其是在和 Vim 搭配的时候。
tmux 默认的前缀键为 `Control+b` 即同时按下 `Control` 键和 `b` 键。如果觉得这两个按键操作不方便可以在用户目录下创建一个 `.tmux.conf` 文件。在里面添加上

	unbind C-b
	set -g prefix C-a
这样前缀键就修改为了 `Control+a`。
为了方面叙述，后面会用`{前缀键}`代表这一操作。
### 会话
一个服务可以有多个会话，每个会话可以有不同的操作，可以在不同的会话之间来回切换，以适应不同的场景。
输入：

	tmux new -s work

可以创建一个名字为 `work` 的会话，指定会话名字可以让我们后续的操作更为方便。

	exit
在窗口中输入 `exit`可以退出会话。也可以输入命令：

	tmux kill-session -t work
来关闭一个会话

如果不想退出会话，但是又想切换到普通终端的时候可以按`{前缀键}＋d` 即可切换到普通而不退出会话。或者输入命令：

	tmux detach -s work
来实现同样的效果。

退出后，如果想回到之前的会话可以输入：

	tmux attach -t work
这样就能回到名为 `work` 的会话。
如果想修改会话名字可以输入：

	tmux rename -t work test
这样会话`work`变为了`test`，而会话内容不变。
如果有多个会话可以输入

	tmux ls
查看当前有多少个会话。
如果在会话里面可以使用`{前缀键}＋s`查看所有会话，并可以在会话间自由切换。

### 窗口
进入一个会话，其实所看到的，所操作的就是一个窗口。一个会话可以有多个窗口，并可以自由切换。
每个窗口都有自己的编号，默认从 0 开始。也可以给每个窗口定义一个名字。方便了解每个窗口。
进入会话后，默认只有一个窗口，`{前缀键＋c}` 会创建一个新窗口。
`{前缀键＋,}` 可以重命名一个窗口，比如一个叫 edit 一个叫 console 这样就能明确指导窗口的用处了。
窗口操作相关的快捷键

| 快捷键 | 功能 |
|:-|:-|
| {前缀键+c} | 创建一个窗口 |
| {前缀键+,} | 重命名当前窗口 |
| {前缀键+n} | 切换到前一个窗口 |
| {前缀键+p} | 切换到后一个窗口 |
| {前缀键+l} | 在两个窗口间来回切换 |

## 我的配置
### 配置

	# 绑定快捷键
	unbind C-b
	set -g prefix C-a
	# 调整窗口大小快捷键
	bind H resize-pane -L 5
	bind J resize-pane -D 5
	bind K resize-pane -U 5
	bind L resize-pane -R 5
	# 显示256色
	set -g default-terminal "screen-256color"
	# 设置状态栏颜色
	set -g status-fg white
	set -g status-bg black
	set -g status-left-length 40
	set -g status-left "#[fg=green]#(whoami):#S #[fg=yellow]#I #[fg=cyan]#P"
	set -g status-right "#[fg=cyan]%Y/%m/%d %H:%M"
	set -g status-utf8 on
	# 窗口活动通知
	setw -g monitor-activity on
	set -g visual-activity on
	# 处理鼠标
	set -g mouse-utf8 on
	setw -g mouse on
	# 设置 vim 模式操作缓冲区
	setw -g mode-keys vi

### 脚本

	session_exists() {
	  tmux has-session -t "$1" 2>/dev/null
	}
	if session_exists "python"
	then
		tmux attach -t python
	else
		tmux new-session -s python -n editor -d
		tmux split-window -v -p 15 -t python:0.0
		tmux new-window -n console -t python
		tmux select-window -t python:0
		tmux select-pane -t python:0.0
		#tmux send-keys -t development 'cd ~/devproject' C-m
		tmux attach -t python
	fi
