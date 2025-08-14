# My Icon


- 原项目：[heizicao/My Icon](https://gitee.com/heizicao/my-icon)
- 修改版：[Siriling/my-icons](https://github.com/Siriling/my-icons)
- 参考布局：[oliver556/my-icons](https://github.com/oliver556/my-icons)

基于My Icons项目修改，提供在线图标链接，用于个人NAS设备显示使用，禁止用于商业用途！

---

### 使用

- [Github-Pages](https://davidblackcn.github.io/my-icons)
- [EdgeOne镜像](https://icon.davidblackcn.cc)
- 点击相应图标即可获取URL

![show](public/show.png)

---

### 本地部署

开发要求：[Node.js](http://nodejs.org/)

克隆代码仓库：
```shell
git clone https://github.com/DavidBlackCN/my-icons.git
```

安装依赖：
```shell
npm install
```

启动开发服务：
```shell
npm run serve
```

### 部署须知

此版本修改内容：

- 操作简化，自动识别 `./public/icon` 内文件夹名作为图标分类名称
- 修改 `./src/views/index.vue` 修复不同格式图片的加载问题
- 添加python脚本以自动生成数据储存文件db.json

使用须知：

1. 在 `./public/icon/<Your_Category_Name>` 内储存图标
2. 在 `./src/views/index.vue` 中修改CDN链接使其指向自己的仓库
```
let iconurlCdn = "https://cdn.jsdelivr.net/gh/DavidBlackCN/my-icons@main/dist/icon/" + url; // 此处修改CDN Url
```
3. 运行根目录下 `generate_icon_db.py` ，将自动根据icon文件夹内容生成db.json
4. 上传仓库并部署服务






