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
Application::setRoutes(array(
			'/\//' => function()
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
define('LOG_PATH', APP_PATH . 'Log/'); // 日志生成目录
define('LANG_PATH', APP_PATH . 'Lang/'); // 语言包目录
define('TPL_PATH', APP_PATH . 'TPL/'); // 模版文件目录
define('LOG_LEVEL', 4); // 默认日志记录级别
define('DEFAULT_LANG', 'zh-CN'); // 默认使用语言
define('DEFAULT_ERROR_MESSAGE', '网站暂时遇到一些问题'); // 遇到错误时默认提示信息
include 'smile.php'; // 引入框架。

......

Application::start(); //运行应用

```

| 常量					| 作用   |默认值|
| ------				| ----- |-----|
| DEBUG					|   是否开启调试模式|    false     |
| VERSION				|   框架版本号|     跟随框架版本    |
| APP_PATH				|   应用目录| 当前脚本所在目录  |
| LOG_PATH				|  生成日志文件目录 |  根目录（APP_PATH）下 Log 目录 |
| LANG_PATH				|  多语言语言包所在目录 |  根目录（APP_PATH）下 Lang 目录 |
| TPL_PATH				|  模版文件所在目录 |  根目录（APP_PATH）下 TPL 目录 |
| LOG_LEVEL				|  日志记录级别 | Log::WARNING   |
| DEFAULT_LANG			| 多语言默认语言  | zh-CN  |
| DEFAULT_ERROR_MESSAGE	|  网站遇到问题时，默认给出的提示 | We encountered some problems, please try again later.|


## 路由
Smile 的路由规则必须开启 pathinfo，根据正则，提供了灵活的路由规则，只要正则表达式做得到的，smile 的路由规则也能做到。
支持 restful 风格
注：`?` 以后的不是pathinfo部分，不会参与正则匹配
引入框架文件以后首先要设定路由规则，

```
<?php

define("DEBUG", true); // 开启 debug 便于开发调试。在引入框架前定义。
include 'smile.php'; // 引入框架。
// 设置路由规则，并有一个匿名函数响应请求
Application::setRoutes(array(
	// 设置匿名函数响应请求
	'/\//' => function()
			{
			echo 'Hello World.'; // 输出信息
			},
	// 设定一个类的完整限定名，自动实例化这个类相应请求
	'/\/test/' => 'Handler\TestHandler',
	// 用一个对象去相应请求
	'/\/test2/' => new Handler\TestHandler(),
	// 用一个对象去相应请求，并获取参数
	'/\/test3/(\d*)/(.*)' => new Handler\TestParamHandler(),
	)
);
Application::start(); //运行应用
```
如果设置用匿名函数来响应请求，那么符合url规则的请求，无论是get，post请求等。都会用这个匿名函数去处理请求
如果设置指定一个对象去响应url符合规则的请求，框架会根据当前是get，post，delete，put等请求方式分别去调用对象的`$object->get()` 的方法。方法名全小写。  
如果想一个方法相应所有的请求方式，只需要在类里面添加 `any` 方法，无论get还是post请求。框架都会去调用`any`方法去相应这个请求。 any 方法的优先级低于其他方法，比如，get 请求时，如果对象包含get方法，那么就会动用get方法去处理请求。而不会去掉用any方法。
指定一个类名去相应请求的时候。框架会在每次请求到来的时候自动去实例化这个对象。然后和指定对象一样的规则去处理请求。
如果想获取URL里面的参数，可以使用正则表达式去捕获参数。框架会在调用处理函数/方法的时候自动传参。如 url `/test3/12/read`  
根据上面设置的路由规则，可以在Handler中这样获取参数。

```
<?php

class TestParamHandler
{
	public function get($id, $param)
	{
		var_dump($id, $param);
	}
}
```
正则匹配参数不会影响到get `?` 以后的参数使用。依然可以在Handler中获取get参数 如url `/test3/12/read?user=smile`

```
<?php

class TestParamHandler
{
	public function get($id, $param)
	{
		var_dump($id, $param);
		var_dump($_GET['user']);
		var_dump(Request::get('user'));
	}
}
```
