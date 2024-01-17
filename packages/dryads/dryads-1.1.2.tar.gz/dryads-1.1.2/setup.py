# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dryads']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ds = dryads.execute:main']}

setup_kwargs = {
    'name': 'dryads',
    'version': '1.1.2',
    'description': '',
    'long_description': '# Dryad\n\n非侵入式命令行构建工具以及脚本管理工具\n\n+ 类似工具: [Just](https://github.com/casey/just)\n+ 如果构建工业级命令行项目，推荐其他框架，比如argparse，click，typer，不过理论上本框架也行\n+ 推荐阅读：[Line Interface Guidelines](https://clig.dev/)\n\n+ 使用该框架的实例：\n  + [BusTub lab test script](https://github.com/zweix123/bustub_2023spring_backup/blob/master/script.py#L146): [介绍](https://github.com/zweix123/CS-notes/blob/master/README.md#CMU15445)\n  + [Note Analysis Tool](https://github.com/zweix123/CS-notes/blob/master/script.py#L205)\n\n+ 发心：\n\n  命令行软件也是软件，那么人类是怎么将需求传达给机器的呢？即参数和选项，形象的说，如果把命令行软件当作人类与机器交通的工具的话，参数和选项就是修饰词。而围绕某一个事物的各种修饰词，将其相同的部分汇总并依次连接，很容易形成树形结构。即很多命令行软件的选项设计可以总结为树形结构。\n\n  拿我在CMU15445 Lab的过程遇到的需求来说，这个过程，测试、格式化、打包等等每个动作都对应一系列命令，而每个动作还能细分，比如Lab分成多个Project，每个Project分成多个Task，于是就可能出现“测试Project1 Task1相关代码”，同理，格式化和打包操作也类似，所以形成了如下树形结构（以Json表示）：\n  ```json\n  {\n    "Test": {\n      "Project1": {\n        "Task1": ...,\n        "Task2": ..., \n        ..., \n      },\n      "Project2": ..., \n      ...\n    },\n    "Format": ...,\n    "Submit": ..., \n  }\n  ```\n  而这里的每个指令，都是由一系列Shell命令实现的；几乎不可能记忆所有的命令，而将对应的命令放在对应的指令下，则可以自由使用\n\n  如果把Shell脚本换成一个个Python函数，则这就形成了一个命令行程序\n\n  即使不考虑命令行程序，即使同是脚本语言，Python的表意能力要比Bash强得多，如果运维相关的操作有点复杂，使用Python实现可能要比Bash实现容易的多。\n\n  这个工具极大的提高了我的工作效率。\n\n## Install\n\n目前该库没有放到PyPI，但是可以通过下面命令安装\n```bash\npip install git+https://github.com/zweix123/dryad.git@master\n```\n如果是在Linux系统，通过在脚本前添加shebang\n```python\n#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n```\n则可以通过`./script.py`这种很接近命令的形式使用\n\n对比`make`和`just`，我们希望直接运行某命令，可以通过\n```bash\npython3 setup.py sdist bdist_wheel\npython3 -m pip install --force-reinstall dist/dryad-1.0.0-py3-none-any.whl\n```\n得到`dryad`命令，它会执行路径为`~/dryadfile`的使用该框架的正常脚本，来实现类似效果\n\n## Use\n\n我们只需要描述好树形结构即可，即通过`dict`类型的变量，参数解析和执行交给框架，下面是一个简单的例子\n```python\n# test/example.py\nfrom dryad import Dryad, DryadContainer, DryadFlag, run_shell_cmd\n\ndef create_python():\n    run_shell_cmd(f"poetry new {DryadContainer.DryadArg}")\n\ndef create_rust():\n    run_shell_cmd(f"cargo new {DryadContainer.DryadArg}")\n\nCMDS = {\n    "echo": {\n        "English": "echo Hello World",\n        "Chinese": "echo 我可以吞下玻璃而不受到伤害",\n        "Math": ["echo 42", "echo 3.14"],\n    },\n    "work": {\n        DryadFlag.PrefixCmd: ["cd Project"],\n        "build": "cd build && make -j`nproc`",\n        "run": "./build/bin/work",\n    },\n    "create": {\n        "python": [\n            DryadFlag.Anchoring,\n            DryadFlag.AcceptArg,\n            create_python,\n        ],\n        "rust": [\n            DryadFlag.Anchoring,\n            DryadFlag.AcceptArg,\n            create_rust,\n        ],\n    },\n    ("-d", "--dryad"): "echo Hello Dryad",\n}\n\nDryad(CMDS)\n```\n\n+ 基本元素：\n  + 以嵌套的`dict`来描述树形结构\n  + `dict`的键只能是`str`或者`tuple[str]`来描述选项\n    + `tuple`即多选项\n  + 叶子节点为`str`/`Callable`/`list[str | Callable]`类型表示具体的命令执行内容\n    + 每个str作为一个shell脚本一起交给shellypx\n      + 如果命令中包含`cd`，需要放在一个`str`字面量中\n\n+ `--help`: help option必不可少\n  + 根help option：`python3 script.py`/`python3 script.py -h`/`python3 script.py --help`\n    ```bash\n    该脚本命令可分为两大类\n      Shell Commands, help会输出命令本身\n      Python Function, help会输出函数的__doc__\n    echo English: echo Hello World\n    echo Chinese: echo 我可以吞下玻璃而不受到伤害\n    echo Math: echo 42\n              echo 3.14\n    work DryadFlag.PrefixCmd: cd Project\n    work build: cd build && make -j`nproc`\n    work run: ./build/bin/work\n    create python: DryadFlag.Anchoring\n                  DryadFlag.AcceptArg\n                  Create Python\n    create rust: DryadFlag.Anchoring\n                DryadFlag.AcceptArg\n                Create Rust\n    -d/--dryad: echo Hello Dryad\n    env: Print Dryad environment variable.\n    ```\n\n  + 各选项help option：在任意选项后，都可以添加help option查看之后的命令\n    ```bash\n    > python example.py echo --help\n    该脚本命令可分为两大类\n      Shell Commands, help会输出命令本身\n      Python Function, help会输出函数的__doc__\n    echo English: echo Hello World\n    echo Chinese: echo 我可以吞下玻璃而不收到伤害\n    echo Math: echo 42\n               echo 3.14\n    ```\n\n+ 执行：一个命令相当于从根到叶子的路径\n  + 叶子节点：\n    ```bash\n    > python example.py echo Chinese\n    echo 我可以吞下玻璃而不收到伤害\n    我可以吞下玻璃而不收到伤害\n    ```\n\n  + 中间节点：执行该节点子树中的所有叶子节点\n    ```bash\n    > python example.py echo \n    echo Hello World\n    Hello\n    World\n    echo 我可以吞下玻璃而不收到伤害\n    我可以吞下玻璃而不收到伤害\n    echo 42\n    42\n    echo 3.14\n    3.14\n    ```\n\n+ 标记\n  + `DryadFlag.Anchoring`: 作为叶子的值, 表示该叶子中的命令都是以执行脚本的路径开始, 默认从脚本所在的路径开始, 例子在[Anchoring](./test/flag_anchring.py)\n  + `DryadFlag.AcceptArg`: 作为叶子的值, 表示该选项还接收一个可选参数, 并将参数放在变量DryadArg中, 例子在[AcceptArg](./test/flag_accept_arg_valid.py), 还有两个非法的例子, [AcceptArg Invalid](./test/flag_accept_arg_invalid1.py) | [AcceptArg Invalid](./test/flag_accept_arg_invalid2.py)\n  + `DryadFlag.InVisible`: 作为叶子的值, 表示执行的脚本是否打印, 默认打印, 使用该标志表示不打印, 例子在[InVisible](./test/flag_invisiable.py)\n  + `DryadFlag.IgnoreErr`: 作为叶子的值, 表示命令执行出错后是否停止, 默认停止, 使用该标志表示不停止, 例子在[IgnoreErr](./test/flag_ignore_err.py)\n  + `DryadFlag.PrefixCmd`: 作为某个节点的键, 其值对应的脚本为子树中所有脚本的前置脚本, 例子在[PrefixCmd](./test/flag_prefix_cmd.py)\n    + 该标记只能用于`dict`不能用于`list`，但是我们往往是对叶子节点`list`中的一系列命令设置前置脚本，通过再套一层dict解决。\n\n## TODO\n\n+ 缩进支持中文\n+ 美化`help`效果\n+ debug: help option显示`-h/--help`本身\n',
    'author': 'zweix123',
    'author_email': '1979803044@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
