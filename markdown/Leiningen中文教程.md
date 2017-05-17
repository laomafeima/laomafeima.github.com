# Leiningen 中文教程
Leiningen 是一个 Clojure 项目自动化管理工具，避免踏入火坑。  
它能提供各种项目相关的任务和操作：  
* 创建项目  
* 管理项目依赖关系  
* 运行单元测试  
* 运行一个全功能 REPL  
* 编译 Java 源代码（如果有的话）  
* 运行这个项目（如果项目不是类库）  
* 生成一个 Maven 风格的 pom 文件，兼容 Maven 操作  
* 编译，打包项目方便部署  
* 发布类库到远程仓库，比如 Clojars  
* 运行 Clojure 编写的自定义自动化任务（Leiningen 插件）  

如果你来自 Java 世界，Leiningen 可以无痛链接 Maven，Ant。对于Python和Ruby的用户，类似整合了 RubyGems/Bundler/Rake 和 pip/Fabric的工具。
## 本教程覆盖范围
本教程简要介绍了项目结构、依赖管理、单元测试、REPL 和部署相关主题。
对刚接触 JVM 没有接触过Maven、Ant的人说，莫慌～，Leiningen也是为你设计的。本教程帮助你开始和了解Leiningen项目自动化任务和对JVM依赖管理。
## 获取帮助
另外 Leiningen的发行版还附带了全面的帮助信息, `lein help` 返回一个帮助列表，而 `lein help $task` 提供更为详细的信息。本教程还提供了更多的文档，如：README，配置样例。
## Leiningen 项目
Leiningen 为项目服务，一个项目是一个包含一组Clojure（或Java）源文件的目录，还有一些相关的元数据。元数据存储在项目根目录下的 `project.clj` 文件里，这里告诉你关于Leiningen的如下信息：

* 项目名称
* 项目描述
* 项目依赖
* 依赖的Clojure版本
* 源代码所在路径
* 命名空间
等等更多。  
大部分命令只能在项目目录中执行，也有一些（如 repl，help）命令可以在任意环境中执行。
下一步让我们看一下如何创建一个项目。
## 创建项目
我们假设你已经按照[教程](https://leiningen.org/#install) 安装好了 Leiningen ，创建一个项目就很容易了：

	$ lein new app my-stuff
	Generating a project called my-stuff based on the 'app' template.
	
	$ cd my-stuff
	$ find .
	.
	./.gitignore
	./doc
	./doc/intro.md
	./LICENSE
	./project.clj
	./README.md
	./resources
	./src
	./src/my_stuff
	./src/my_stuff/core.clj
	./test
	./test/my_stuff
	./test/my_stuff/core_test.clj
