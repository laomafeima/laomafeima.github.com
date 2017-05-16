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