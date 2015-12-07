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

##响应请求
##参数获取

Request 类封装了获取外部数据的一些操作，比如 `Request::get()`可以获取 GET 参数，是`?`之后的参数，即 URL 里面的 Query 字段参数如 URL `http://test.com/read?id=3`  可以通过`\Requst::get()` 获取参数
Smile 封装了`Request::get()`,`Request::post()`，分别用以获取get，post参数。
另外还有一个`Request::param()`方法，会自动根据参数名字检查是get或是post参数，并返回。如果get和post 都有这个参数，那么有限返回 post 参数。
`Request::get()`,`Request::post()`,`Request::param()`三个方法用法一样，分别有三个参数，第一个参数是要获取的参数名字。第二个参数是默认值，如果这个变量不存在就返货默认值，默认值为`null`，第三个参数为过滤规则，可以根据自己的需要传入参数。规则与`filter_input`一致。参见[php.net](http://php.net/manual/zh/filter.constants.php)
如果要获取的参数是个数组，不用担心，框架会根据参数类型自动转换的，如果是个数组，那么这三个方法也会返回一个数组的。

```
<?php

.......
$data = \Request::get('foo');
var_dump($data);
$data = \Request::post('foo');
var_dump($data);
$data = \Request::param('foo');
var_dump($data);
$test = \Request::get('test', 100);
var_dump($test);
$email = \Request::get('email', false, FILTER_VALIDATE_EMAIL);
var_dump($email);
```

除此之外。Request 类海封装了。`isAjax`,`getClientIP`等方法，方便开发。

|方法名字|函数作用|其他|
|--------|--------|----|
|isAjax|是否是Ajax请求|如果传入一个参数名字，只要这个请求中参数存在且值为 true 也会通过这个判断|
|getClientIP|返回用户IP||
|getAcceptLang|返回用户可以接受的语言|多语言情况下根据用户返回不同语言|
|getAccept|返回用户接受的文档类型|在restful风格下，可以判断需要返回的文件类型|

##模版
Smile 没有去实现一套模版语言，直接在模版文件中使用 php 代码。这样使用起来既灵活又方便，不需要增加额外的学习负担。
项目中模版文件存在 `TPL_PATH` 中，默认在 `APP_PATH . '/TPL'` 目录中。可以通过定义常量`TPL_PATH` 改变目录位置。
使用时，可以使用`TPL::assgin()`方法给模版复制，因为处于变量安全的考虑，模版中只剋使用允许使用的变量。
然后可以调用`TPL::render()`方法来渲染模版。需要在参数中指定模版文件的名字。这个模版文件位于常量 `TPL_PATH` 定义的目录下。也可以指定使用其子目录的模版文件。只需要在参数中指明即可，如`TPL::render('User/login.html')`，那么就会去使用`{TPL_PATH}/User/login.html`的模版文件。

```
<?php

......
\TPL::assign('data', $data); // 给模版文件复制一个变量
\TPL::render('index.html'); // 指定渲染一个模版文件
//这个模版文件路径就是 {TPL_PATH}/index.html

\TPL::render('User/login.html') //模版文件支持多目录。
//这个模版文件路径是 {TPL_PATH}/User/login.html 
......

```

此外render方法还有第二个参数，这个参数必须是个数组，是模版文件可以使用的变量。这个数组索引为何变量名字，值是变量，相当与`assign`方法。

```
\TPL::assign('data', $data); // 给模版文件复制一个变量
\TPL::render('index.html'); // 指定渲染一个模版文件
```

相当与

```
\TPL::render('index.html', array('data', $data)); // 指定渲染一个模版文件
```

以上这两种用法作用是一样的。都可以在模版中使用变量`$data`了

```
<html>
	<header>
	......
	</header>
	<body>
	......
	<?php echo $data;?>
	......
	</body>
</html>
```
##数据库操作
##MVC 实现
##Cookie 操作
Smile 封装对 Cookie 的操作。开发过程中可以方便的对 Cookie 进行操作。
`Cookie::set()` 方法可以设置一个 cookie 值。第一个参数为cookie 名字，第二个参数为cookie的值，这两个是必须参数。
第三个参数是 cookie 有效时间事件，单位是秒，只需要传来一个数字即可，默认为0
第四个参数为cookie的路径，第五个参数为 Cookie 允许使用的域名。  

`Cookie::get()`可以获取一个cookie 值，只需要参数里传递cookie的名字即可
`Cookie::delete()` 删除一个cookie ，参数里指定 cookie 名字即可删除cookie
`Cookie::clear()` 调用此方法可以删除所有的cookie

##事件广播机制
在一个项目里，一个特定的操作，会经常触发要一些列的操作。比如，当用户登录的时候，
1.会去检查用户有没有未读的消息。
2.检查是不是有未完成订单，提醒支付。
3.检查IP是不是常用IP。
4.添加登录日志。
等等操作。
如果未来用户登录的时候要添加其他功能。那就只有去修改原来的逻辑代码。
如果我们在用户登录的时候触发一个名字叫`UserLogin`的事件。在用户登录的时候需要处理的操作都去关注这个事件。当这个事件发生的时候，会触发所有的操作。当添加或者删除功能的时候，只需要添加或移除处理代码即可。当然事件广播机制还有更多的用处。

##错误与异常处理
##日志
##多语言
##类反射
##建议反馈
