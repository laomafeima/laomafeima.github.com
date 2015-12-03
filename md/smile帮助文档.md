Smile 手册
====

##关于 Smile 框架
smile 是一个轻量级的 PHP 框架，代码精炼只需要一个 php 文件即可运行。框架封装了开发过程中所需要基本操作，代码不超过 1000 行，去除注释后仅有 500 多行。

##获取 Smile 



##Hello World
这里以一个简单的例子让大家了解 Smile

```
<?php

define("DEBUG", true); // 开启 debug 便于开发调试。在引入框架前定义。
include 'smile.php'; // 引入框架。
// 设置路由规则，并有一个匿名函数响应请求
Application::setRoutes(array('/\//' => function()
{
	echo 'Hello World.'; // 输出信息
}
));
Application::start(); //运行应用
```
##常量定义
在应用开始运行的时候会定义一些如应用目录，是否开启调试等常量。如果需要改变默认配置的话，请在引入框架文件前定义这些常量。  
如有时候配置项目文件不可通过 web 访问，仅有入口文件（如index.php）和静态文件可以通过 web 方式访问，那么可以通过如下代码实现。  

```
<?php

define('APP_PATH', '/var/site/php/'); // 定义应用目录
include 'smile.php'; // 引入框架。

......

Application::start(); //运行应用

```
如要修改 debug 模式，项目路径和日志文件路径等

```
<?php

define("DEBUG", true); // 开启 debug 便于开发调试。在引入框架前定义。
define('APP_PATH', '/var/site/php/'); // 定义应用目录
include 'smile.php'; // 引入框架。

......

Application::start(); //运行应用

```

| 常量  | 作用   |默认值|
| ------| -----: |-----|
| DEBUG  |   |         |
| VERSION|   |         |

## 路由
