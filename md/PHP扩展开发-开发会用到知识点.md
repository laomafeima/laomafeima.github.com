#PHP 扩展开发-会用到的函数以及知识点

用来记录 扩展开发过程中，遇到的，发现的一些知识点。  
*持续更新……*
PHP 导入并运行 php 脚本文件
----
在开发的过程中经常遇到导入并运行 php 脚本文件。  
这里封装函数可以直接导入并运行脚本

```
int include_file_scripts(char *file_name) {

    zend_file_handle fh;
    fh.filename = file_name;
    fh.opened_path = NULL;
    fh.free_filename = 0;
    fh.type = ZEND_HANDLE_FILENAME;
    zend_execute_scripts(ZEND_INCLUDE TSRMLS_CC, NULL, 1, &fh);
    return SUCCESS;
}
```

调用的时候直接传入 php 脚本文件的路径即可。
正则表达式的使用
----
因为 C 开发的过程中经常遇到使用正则的情况，而 php 正好是正则模块可以使用，这里简单介绍一下PHP 正则的扩展使用
