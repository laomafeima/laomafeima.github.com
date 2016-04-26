# Let's Encrypt Nginx 配置
{2016-02-22}
## 配置 Let's Encrypt 客户端
本地需要安装 Let's Encrypt 客户端。可以直接从 Github 下载

    $ git clone https://github.com/letsencrypt/letsencrypt
    $ cd letsencrypt
    $ ./letsencrypt-auto --help


执行后可能会下载一些依赖的库

输入命令，指定目录和域名

    ./letsencrypt-auto certonly -a webroot --webroot-path=/usr/share/nginx/html -d example.com


会在 ｀ls -l /etc/letsencrypt/live/example.com/｀ 目录下生成

    cert.pem: Your domain's certificate
    chain.pem: The Let's Encrypt chain certificate
    fullchain.pem: cert.pem and chain.pem combined
    privkey.pem: Your certificate's private key

配置 Nginx 

    listen 443 ssl;
    server_name example.com www.example.com;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;


配置 HTTP 转发 HTTPS

    server {
        listen 80;
        server_name example.com www.example.com;
        return 301 https://$host$request_uri;
    }

配置自动更新

    30 0 */60 * * /home/ma/work/letsencrypt/letsencrypt-auto renew >> /var/log/le-renew.log                                                                                                                     
    35 0 */60 * * /etc/init.d/nginx reload

