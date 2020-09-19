Django rest framework + vue 的CMDB项目


## 环境

- Python 3.6
    - Django 2.0
    - Django Rest Framework 3.8
    
- Vue.js 2.9
    - iview 3.0
    - iview-admin 2.0


## 功能

- web ssh
    - 页面模拟服务器控制台
- CMDB资源管理
    - 硬件管理：机房/机柜/设备
    - 业务管理：业务线/项目
    - 数据自动化：自动抓取服务器信息做集中化存储
    - 用户和组
- 报表展示
    - 硬件/业务/用户各维度数据图形化
- 定时任务管理
    - 对各服务器的定时任务创建/修改
    - 批量分发同步
    - 任务日志查询
- 历史记录
    - 记录用户的各类变更操作


## 部署
- 推荐容器化部署
git pull myide/opencmdb:v1
docker run -itd --name op1 --network host opencmdb:v1


## 界面

- Dashboard

![image](https://github.com/myide/open-cmdb/blob/master/images/dashboard.png)

- 机房列表

![image](https://github.com/myide/open-cmdb/blob/master/images/idc-list.png)

- 机房详情

![image](https://github.com/myide/open-cmdb/blob/master/images/idc-detail.png)

- 服务器列表

![image](https://github.com/myide/open-cmdb/blob/master/images/server-list.png)

- 服务器详情

![image](https://github.com/myide/open-cmdb/blob/master/images/server-detail.png)

- 服务器webssh

![image](https://github.com/myide/open-cmdb/blob/master/images/server-ssh.png)

- 操作记录列表

![image](https://github.com/myide/open-cmdb/blob/master/images/log-list.png)

- 操作记录详情

![image](https://github.com/myide/open-cmdb/blob/master/images/log-detail.png)


## 交流学习
- QQ群 630791951
