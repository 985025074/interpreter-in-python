# unittest 项目组织架构：

https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
也可看 gaotian 视频

# repl:不支持左右键移动：

import readline # 加到文件顶部
你是在写一个命令行解释器（REPL），并在使用 input(prompt) 接收用户输入，对吧？你发现无法左右移动光标，比如按方向键左，会输出 ^[[D，像这样：

text
复制
编辑

> > > asd^[[D
> > > 这说明 当前运行环境对键盘方向键的支持不完全或输入行为未被 readline 解析。

# 末尾加逗号 变成 tuple


# 不小心把cache 搞进去了：
```bash
git rm -r --cached **/__pycache__/

```
# use assert more!



# there must be a way to change a class method by decorator