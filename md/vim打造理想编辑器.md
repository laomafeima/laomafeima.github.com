#打造理想 Vim 编辑器
尝试过很多种编辑器，Emacs，Notepad++，Sublime Text，Komodo Edit，EditPlus等。都因种种原因始终难以顺手。最终还是走上了 Vim 这条道路。这里介绍一下如何把 Vim 打造成理想的编辑器。  
当然，这里只介绍 Vim 相关的信息，不涉及编辑器之战。

认识 Vim
----
Vim 是一个学习曲线陡峭的编辑器，上手难度大。Vim 的强大在于普通模式下的命令。要想驾驭 Vim 就要熟练掌握哪些命令。  
同样 Vim 还是可高度定制化的编辑器，可以根据自己的习惯配置它，或者通过插件来扩展 Vim 的功能。
Vim 同样支持终端和 GUI 模式下使用。在 GUI 模式的 Vim 一般都叫 GVim   
*Unix 系统一般默认都有 Vim 如果需要安装 GUI 版本的，可以在这里下载: [Windows GVim](http://www.vim.org/download.php#pc), [MacVim](https://github.com/b4winckler/macvim/releases)
Linux 用户我相信都有自己解决这个问题的能力。
####配置文件
在 *Unix 环境下，`/etc/vim/vimrc` 是全局配置文件，修改这个文件会对所有用户生效。(会因不同的版本目录有所不同)  
在 `~/.vimrc` 目录下时针对当前用户的生效的配置。如果想仅对 GUI 版本生效，命名 .gvimrc 这样，这个文件只会在 GUI 版本中生效。 后面会附上 我的 vimrc 配置

####目录
一般安装插件，主题等的时候，不需要在安装目录进行安装，我们可以在  `~/.vim/` 目录下进行安装，在 Vim 运行的时候，会自动去这个目录寻找插件文件。
在 Win 环境下，这个目录在安装目录下的 `vimfiles` 目录。

在安装插件和配置 Vim 的时候在 `~/.vimrc` 和 `~/.vim/` 目录进行。优点是我们在重新安装或者转移机器的时候，只需要复制配置文件，和目录过去即可。方便易用。   
打开这个 目录会看到很多子目录

```
autoload
colors
doc
ftdetect
lib
plugin
syntax
```
安装插件和主题的时候，把配置插件内容复制到这些目录即可。重启 Vim 生效。

配置 Vim
----
修改 Vim  的默认配置可以在 vimrc  文件中修改
以下是常用配置信息说明  

```
olorscheme solarized " 设置默认主题
set background=dark " 默认使用 dark 模式
set number " 显示行号
set tabstop=4 " tab 的宽度
set shiftwidth=4 "自动缩进的时候 tab 的宽度
set softtabstop=4 "退格键的时候 tab 宽度
hi Pmenu guibg=darkslategray " 下拉菜单的颜色
set scrolloff=2 " 当光标距离下面两行的时候就进行滚动
set lines=40 columns=140 " 设置默认启动窗口大小
set cc=80 " 设置第80 列显示一根线
set guifont=Monaco:h14 " 设置字体， 如果多种字体，用 "," 隔开
hi ColorColumn ctermbg=darkgray guibg=darkgray " 设置第 80 行线的颜色
set helplang=cn " 默认使用中文帮助信息
set laststatus=2 " 默认显示状态栏 
set statusline=%<[%n][%f]%m%r%h%w%{'['.(&fenc!=''?&fenc:&enc).':'.&ff.']'}%y%=[POS=%04l,%04v][LEN=%L][%p%%] " 配置状态栏显示的信息
set ruler " 在编辑过程中，在右下角显示光标位置的状态行

if version >= 700 " 进入插入模式时改变状态栏颜色（仅限于Vim 7）
        au InsertEnter * hi StatusLine guibg=darkred guifg=darkgray gui=none
        au InsertLeave * hi StatusLine guibg=darkgreen guifg=darkgray gui=none
endif

"alt+数字切换Table快捷键设置
:nn <M-1> 1gt
:nn <M-2> 2gt
:nn <M-3> 3gt
:nn <M-4> 4gt
:nn <M-5> 5gt
:nn <M-6> 6gt
:nn <M-7> 7gt
:nn <M-8> 8gt
:nn <M-9> 9gt
:nn <M-0> :tablast<CR>
```

扩展 Vim
----
如果默认的 Vim 满足不了需求，可以通过安装插件来满足需求，下面介绍一些常用的插件。
####中文帮助信息
下载[Vimcdoc](http://sourceforge.net/projects/vimcdoc/files/) 根据自己系统选择不同的文件，下载并安装。重启 Vim ，执行 `help` 即可看到中文帮助信息。

####NERDTree 目录浏览
NERDTree 可以显示目录与文件结构。方便浏览。同时它也支持书签（Bookmark）可以方便的保存项目路径。  
同时，NERDTree 也支持插件，可以显示 git 状态等。插件目录位于 `~/.vim/nerdtree_plugin/`  
下载地址 [NERDTree](https://github.com/scrooloose/nerdtree)  
下载完成后把文件复制到 `~/.vim/` 在配置文件里添加一下配置  
这里推荐两个插件 [vim-nerdtree-tabs](https://github.com/jistr/vim-nerdtree-tabs)，[nerdtree-git-plugin](https://github.com/Xuyuanp/nerdtree-git-plugin)

```
autocmd VimEnter * NERDTree " 在 vim 启动的时候默认开启 NERDTree（autocmd 可以缩写为 au）
nmap <F2> :NERDTreeTabsToggle<CR> " 按下 F2 调出/隐藏 NERDTree

" 当打开 NERDTree 窗口时，自动显示 Bookmarks
let NERDTreeShowBookmarks=1
let NERDTreeWinSize=40 " 窗口宽度
let g:nerdtree_tabs_focus_on_files=1 " 自动焦点在文件
```
####Gitgutter 显示 Git 修改状态

Gitgutter 是一个可以显示每行的 Git 状态的插件。和nerdtree-git-plugin 不同的是，前者可以具体每行的变换。后者只能显示目录和文件的状态。  
下载 [vim-Gitgutter](https://github.com/airblade/vim-gitgutter) 下载后，把文件复制到 `~/.vim／` 目录即可。当然，你必须已经安装的有git。  
在这里可以得到更为详细的帮助信息[Gitgutter 帮助文档](https://github.com/airblade/vim-gitgutter#usage)

####Vim-Signify 显示 SVN 状态
和 Git gutter 一样 Signify 是一个针对 SVN 的插件功能和需求一样，安装之前，也需要你本地安装有 SVN 客户端 

下载地址 [Vim-Signify](https://github.com/mhinz/vim-signify)，帮助信息[Signify Documentation](https://github.com/mhinz/vim-signify#installation--documentation)

####Neocomplcache 自动补全插件

如果你记不住太多的函数名字，可能这个插件就是你需要的。和其他 IDE 一样 Vim 也可以提供一样的功能，设置还能补全目录结构。  
当然如果有折腾的精力，可以了解下坐着另一个作品 [neocomplete.vim](https://github.com/Shougo/neocomplete.vim)  
下载地址 [neocomplcache.vim](https://github.com/Shougo/neocomplcache.vim) 
下载后安装到 `~/.vim/` 目录，并在 vimrc 文件中添加以下配置 

```
let g:neocomplcache_enable_at_startup = 1 " 默认启动 Neocomplcache 
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"  "支持 Tab 选择补全项
```

周边
----
习惯了 Vim 的操作方式后，会觉得非常方便，尤其对我这种用鼠标手疼的人来说简直就是福音。
如果能在浏览网页的时候也能使用 Vim 的操作该多好，vimium 插件就是来实现这个功能的。  
下载地址[Vimium 插件](https://chrome.google.com/webstore/detail/dbepggeogbaibhgnhhndojpepiihcmeb) 