Smile 手册
====

##关于 Smile 框架
smile 是一个轻量级的 PHP 框架，代码精炼只需要一个 php 文件即可运行。框架封装了开发过程中所需要基本操作，代码不超过 1000 行，去除注释后仅有 500 多行。

##获取 Smile 

[https://github.com/laomafeima/smile](https://github.com/laomafeima/smile)

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
##环境要求

Smile 需要运行在 PHP 5.3 以及以上版本，而且也能在 PHP 7里面很好的运行。
因为Smile 的路由是 restful 风格的，运行的时候需要开启 pathinfo，
如果要是想使用 Smile 封装的DB操作，需要安装并启用 PDO 扩展。

##命名空间与自动加载

###使用框架类
Smile 框架封装的操作类因为在开发中经常用到，都在根命名空间里，这样开发中可以少打几个字符

```
<?php

namespace app\Handler;

class Indexhandler
{
	public function get($param)
	{
		\Cookie::set('foo', 'foo'); // 使用 Smile 封装的类
	}
}
```
###自动加载

Smiel 默认加载方式遵守 [psr-4](http://www.php-fig.org/psr/psr-4/) 规范。默认命名空间前缀为`App`自动记载基础目录为常量 APP_PATH   

####说明

>1. 术语「类」是一个泛称；它包含类，接口，traits 以及其他类似的结构；
>
>2. 完全限定类名应该类似如下范例：
>
>    \<NamespaceName>(\<SubNamespaceNames>)*\<ClassName>
>
>    1. 完全限定类名必须有一个顶级命名空间（Vendor Name）；
>    2. 完全限定类名可以有多个子命名空间；
>    3. 完全限定类名应该有一个终止类名；
>    4. 下划线在完全限定类名中是没有特殊含义的；
>    5. 字母在完全限定类名中可以是任何大小写的组合；
>    6. 所有类名必须以大小写敏感的方式引用；
>
>3. 当从完全限定类名载入文件时：
>
>    1. 在完全限定类名中，连续的一个或几个子命名空间构成的命名空间前缀（不包括顶级命名空间的分隔符），至少对应着至少一个基础目录。
>    2. 在「命名空间前缀」后的连续子命名空间名称对应一个「基础目录」下的子目录，其中的命名空间分隔符表示目录分隔符。子目录名称必须和子命名空间名大小写匹配；
>    3. 终止类名对应一个以 `.php` 结尾的文件。文件名必须和终止类名大小写匹配；

*引用自[php-fig](https://github.com/php-fig/fig-standards/blob/master/accepted/zh_CN/PSR-4-autoloader.md#2-说明specification)*

####例子
Smile 默认命名空间前缀常量 `CLASS_PREFIX`。默认为 `App\ `。    
*不在命名空间前缀 `CLASS_PREFIX` 的不会去加载它，可以通过自定义实现其他命名空间前缀的自动加载*
自动加载基础目录为常量 `APP_PATH`。默认 APP_PATH 目录为当前文件执行的目。
如果 APP_PATH 的路径为 `/var/www/site/src/` 
下面的 php 文件路径为 `/var/www/site/src/Handler/IndexHandler.php`

```
<?php

namespace app\Handler;

class Indexhandler
{
	public function get($param)
	{
		\Cookie::set('foo', 'foo'); // 使用 Smile 封装的类
	}
}
```

|完整限定名|命名空间前缀|文件路径|
|-------|------|------|
|\App\Handler\IndexHandler|\App|/var/www/site/src/Handler/IndexHandler.php|
|\App\Model\UserModel|\App|/var/www/site/src/Model/UserModel.php|
|\App\Event\Login_LogoutEvent|\App|/var/www/site/src/Event/Login_LogoutEvent.php|
|\App\Model\Dao\UserTable|\App|/var/www/site/src/Model/Dao/UserTable.php|

####自定义

Smile 默认命名空间前缀 CLASS_PREFIX
如果想要改变命名空间前缀或者自动加载基础目录可以在引入框架文件前定义 `CLASS_PREFIX` `APP_PATH` 两个常量

```
<?php

define('APP_PATH', '/var/site/php/'); // 定义自动加载基础目录
define('CLASS_PREFIX', 'Foo\\'); // 定义默认命名空间前缀
include 'smile.php'; // 引入框架。
......

Application::start(); //运行应用

```

如果不想使用 Smile 默认的加载规则或者自定义另外一个命名前缀的加载规则，可以自定一个加载规则，自实现任何自动加载方式。这样做也很简单。只需要在引入框架文件前注册一个自动加载函数即可。
*这样多种加载规则并存*

```

<?php

//注册自动加载函数
spl_autoload_register(function($class)
	{
		$len = strlen('Foo//');
        if (strncmp('Foo//', $class, $len) !== 0)
        {
            return;
        }
		$relative_class = substr($class, $len);
        $file = APP_PATH . str_replace('\\', '/', $relative_class) . '.class..php';
        if (file_exists($file))
        {
            require $file;
        }	
	}
);
include 'smile.php'; // 引入框架。
......

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
| CLASS_PREFIX			|   命名空间前缀|   App\   |
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
	'/\/test/' => 'App\Handler\TestHandler',
	// 用一个对象去相应请求
	'/\/test2/' => new App\Handler\TestHandler(),
	// 用一个对象去相应请求，并获取参数
	'/\/test3/(\d*)/(.*)' => new App\Handler\TestParamHandler(),
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

namespace app\Handler;

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

namespace app\Handler;

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

##参数获取
###GET 参数获取
###POST 参数获取
##模版
##数据库操作
##MVC 实现
##Cookie 操作
##事件广播机制
##日志
##多语言
##类反射
##建议反馈
