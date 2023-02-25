# 校园网脚本食用方法

## 使用步骤

1. 安装python依赖：

    > ```batch
    > pip install requests
    > ```

2. 下载俩脚本（或本文件夹）
3. 运行脚本
    - 开始中断重连挂机：
        1. 双击运行Network_Alive.py
        2. 按照提示输入账号密码
        3. 挂机
    - 只想用来登录、登出（命令行）
        1. `python .\AIO_login.py -a 登录`（或‘登出’）
        2. 按照提示输入账号密码

## 运行截图

<img width="674" alt="截图_20230225145105" src="https://user-images.githubusercontent.com/53437291/221343217-6487f476-0b0e-4c2b-87f1-2eefafdf16dd.png">

## 冷知识

1. 参数：
    - AIO的启动参数暂时只有-a/--action
    - 这个参数可选字段有`login`, `登录`, `登陆`, `上线`, `logout`, `登出`, `下线`, `退出`
2. 脚本故事
    - 本脚本依据模组10_0_0_55版本混合改编（2022），其最新版名称是[bitsrun](https://github.com/BITNP/bitsrun)
    - 缩编为AIO的初衷是减少调用错误，原模组很多bug，外部调用依托答辩，于是缩编
    - 而10_0_0_55模组的祖先是[Aloxaf](https://github.com/Aloxaf/10_0_0_55_login)
    - 一开始我写这个是为了自己和几位朋友用（b校园网老是断联）
3. 安全
    - 密码是在本地明文储存的`.\bit_user_detail.json`
    - 由`.\AIO-login.py`在初次使用时创建（或在密码错误等情况下修改）
    - 你可以随时删除，并在下一次登陆的时候重新输入账号密码
    - 注意，自动重连依赖于账号密码的保存

4. 因为身边没有用macos/linux的，也没有经验，故不确定是否支持
5. 欢迎Issue可能的bug
