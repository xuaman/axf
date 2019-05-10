## axf
```bash
## 个人项目，仅供参考和学习，禁止用于其他项目
```
## 安装相关软件

```bash
# install mysql
sudo apt install mysql-server-5.7 mysql-client-5.7
# 建议账号:root  密码:xxxx
# install redis-server
sudo apt install redis-server
# install python3-dev
sudo apt install pthon3-dev
# install python3-pip
sudo apt install python3-pip
# install develop setting
pip install -r requirements.txt

```
## 安装部署软件 nginx
```bash
# 安装依赖
sudo apt install curl gnupg2 ca-certificates lsb-release
# 选择安装的版本
echo“deb http://nginx.org/packages/mainline/ubuntu`lsb_release-cs`nginx” | sudo tee /etc/apt/sources.list.d/nginx.list
# 添加验证key
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo apt-key add  -
# 验证key
sudo apt-key fingerprint ABF5BD827BD9BF62
# 安装
sudo apt update
sudo apt install nginx
```
## 初始化数据库
```bash
# 创建数据库 axf
mysql -uroot -p
create database axf character set utf8;
# 执行迁移文件
python manange.py migrate 
```
## 项目启动
```bash
# 启动 nginx
nginx -t -c /当前文件夹的绝对路径/axf/config.conf
nginx -c /当前文件夹的绝对路径/axf/config.conf
# 启动 uwsgi
uwsgi --ini uwsgin.ini
# 启动celery
celery -A axf worker -l debug -E
```
