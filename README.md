# ApkMultiChannel
Android 多渠道 打包 python脚本
一步解决应用加固导致Walle渠道信息失效的自动化脚本，自动生成渠道包

----------
## 用法：

- 修改lib目录下的config.py，需要修改一下信息
    - keystorePath
    - keyAlias
    - keystorePassword
    - keyPassword
    - sdkBuildToolPath
- 修改lib目录下channel.txt中的渠道信息
- 将已经加固好的包【未签名的包，请不要使用加固客户端签名工具】放到脚本工具根目录下
    - 保证目录下有且只有一个apk文件
    - apk文件名称可以为任何名字
    - 加固好的包
    - 未签名的包，请不要使用加固客户端签名工具
- 各种渠道的定义是在out这个文件中
- 运行命令 `python ApkResigner.py`,即可自动生成所有渠道包。


----------
## 支持平台：（需要python环境）
- Windows (Test)
- Mac OS (Test)
- Linux

----------



