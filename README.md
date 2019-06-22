# EfficientResearchWork
Efficient research work environment setup for Computer Science and general workflow for Deep Learning experiments.

## Contents
- [Work environment setup](#Work-environment-setup)
  - [Terminal](#Terminal)
  - [Shell](#Shell)
  - [Server](#Server)
    - [Connection](#Connection)
    - tmux
  - [Code editor](#Code-editor)
    - python : pycharm
    - C/C++
  - [Cloud Storage](#Cloud-Storage)
- Deep Learning Experiments Workflow
  - Code structure
  - Experiment organization
  - Visualization
- Commonly used CG software
  - Blender
  - MeshLab
  - Unity

## Work environment setup

### Terminal

系统自带的terminal往往比较简单，不支持多窗口和各种定制。而在实验中经常需要开多个terminal窗口（比如我需要同时连多台服务器），所以系统自带的原始terminal使用起来会比较不方便。建议使用以下的terminal软件，以支持多窗口、分屏和快捷切换的特性。

- Linux: Terminator. 安装简单，例如[此处](https://blog.arturofm.com/install-terminator-terminal-emulator-in-ubuntu/)。
- Mac: [iTerm2](https://iterm2.com). 按照官网安装即可。
- Windows: 待补充。

image placeholder

安装完毕之后不需要掌握太多的功能，一般只需要用到多窗口、分屏的功能，掌握切换窗口/分屏的快捷键即可。能用键盘的操作就别用鼠标去点！此外，背景半透明等额外特性看个人需要是否使用。

### Shell

Shell对于工作效率可以说是重中之重了，一个好的shell能成倍提高工作效率！一般系统自带的shell都是未经配置的bash，功能比较简略。

在此，强烈推荐使用[zsh](https://www.zsh.org)及其插件管理工具[oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)!!! 其功能极大的简便了命令行操作，相信用过了都会觉得真香（看看Github 9万多star就知道了）。

- **安装与（推荐）配置过程**：  
  1. 按照[这里](https://github.com/robbyrussell/oh-my-zsh#getting-started)按照zsh和机器插件管理包oh-my-zsh。注意oh-my-zsh是zsh的一个插件管理包，我们还需要通过它来安装其他插件来实现各种强大的功能。
  2. 安装插件[zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)，注意按照[这里](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh)的命令通过oh-my-zsh来方便安装。这个插件的功能是更强大的命令补全。
  3. 安装插件[zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)，注意按照[这里](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md#oh-my-zsh)的命令通过oh-my-zsh来方便安装。这个插件的功能是命令行的语法高亮，方便阅读命令的同时也会让你的命令行更加酷炫。
  4. 安装插件[extract](https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins/extract#extract-plugin)，只需要在zsh的配置文件`~/.zshrc`里加一行即可。这个插件的功能是简化各类解压操作。
  5. 安装插件[git](https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins/git)，可选，简化git的相关操作。

- **常用特性**：  
  -  命令补全。极其强大！系统自带的bash往往只能一个一个顺序地往上恢复历史的命令，而我们配置后的zsh可以迅速地恢复任意历史命令。例如我想恢复我的上一次python命令，简单的敲几个字母`pyt`后，历史的命令就显示出来的了，在按一下方向键⬆️就恢复了：

  gif placeholder

  - 一键解压。linux下各类的压缩文件的解压缩命令往往不同，很难记住，extract插件让我们能够通过`x`这一个字母解压几乎所有类型的压缩文件：

  gif placeholder

  - 各种小的命令简化。我们配置的zsh自己alias了一些命令，如`..` = `cd ..`, `l` = `ls -alh`等等。

### Server
DL的实验基本都需要在服务器上跑，所以一些针对服务器的操作简化是很必要的。

- <a name="Connection"></a> **Connection**  
  通过`ssh username@server_ip`命令连接服务器是大家常用的操作，然而每次都需要输入用户名、服务器ip和密码是不是很麻烦。强烈推荐一个`ssh xxx`一键登录的操作

  1. **免密登录**.  
    原理是通过公私钥登录。我们先通过`ssh-keygen`生成一个rsa公私钥对：  
    ```ssh-keygen -t rsa```  
    这样会在`~/.ssh`文件夹下生成一个公私钥对, `id_ras`和`id_rsa.pub`（或者其他你命的名字）。接下来把公钥拷贝到服务器上：  
    ```ssh-copy-id username@server_ip```  
    这样配置之后再通过`ssh username@server_ip`登录就不需要输密码了。

  2. **配置连接的别名**. 
    我们进一步配置`ssh`连接，通过`vim ~/.ssh/config`创建（打开）ssh的配置文件，写入： 
      ```
      Host lab
        Hostname 111.222.333.4
        User myname
        Port 22
        IdentityFile ~/.ssh/id_rsa
      ```
      这样我们就为`myname@111.222.333.4`建立了一个别名叫做`lab`，并且关联上了之前配置好的rsa的私钥。  
      以后只需要通过`ssh lab`即可直接登录服务器，比原来简便了很多。

- **tmux**  
  [tmux](https://github.com/tmux/tmux)是一个unix-like系统下的命令行多路复用工具，可以帮助我们在命令行中同时开多个窗口，并且保证在其中跑的程序不会因为服务器连接的中断而停止，这对于长时间运行的实验（如神经网络训练）尤为重要。大多数人对tmux应该不陌生，也听过有用其他类似软件的。

  - **安装与推荐配置**：  
  1. 安装tmux，按照[这里](https://linuxize.com/post/getting-started-with-tmux/#installing-tmux)
  2. 配置tmux。同样tmux也可以通过配置来强大其功能并美化其外观，我个人使用的是这个[.tmux](https://github.com/gpakosz/.tmux)配置，安装简介，使用方便，外观好看。

  gif placeholder

  - **常用操作**：  
  推荐阅读这个[指南](https://linuxize.com/post/getting-started-with-tmux/#starting-your-first-tmux-session)来熟悉tmux的常用操作和概念。推荐用一个session来管理一个project，里面的每一个window(或者panel)来管理一个实验，多个实验同时用不同的window(或者panel)来跑。  

  gif placeholder

### Code editor

- **python**  
  强推[PyCharm](https://www.jetbrains.com/pycharm/)！！通过学校邮箱注册即可获得免费的专业版。  

  **常用特性**：
  - 远程服务器直连/同步。按官方指南[creating-a-remote-server-configuration](https://www.jetbrains.com/help/pycharm/creating-a-remote-server-configuration.html)操作即可。本地ide修改代码，文件即刻同步到服务器上，对于在服务器上跑实验但是又想本地改代码的人来说十分方便。
  - 使用远程服务器的python解释器。依旧官方指南[configuring-remote-interpreters-via-ssh](https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html)。本地修改代码可以按照远程服务器的python解释器来进行补全和提示，不必再担心本地和远程环境不一样的问题。
  - 快捷键`crtl+B`（`command+B` for Mac）进行函数或变量声明的一键查询。
  - 快捷键`crtl+W`（`command+W` for Mac）快速关闭当前页。
  - 在pycharm内对一个project进行git管理。[官方指南](https://www.jetbrains.com/help/pycharm/using-git-integration.html?section=Windows%20or%20Linux#Using_Git_Integration.xml)写的比较复杂。

- **c/c++**  
  待补充。

### Cloud Storage
待补充。

## Deep Learning Experiments Workflow

## Commonly used CG software
