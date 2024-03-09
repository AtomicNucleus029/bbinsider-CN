# 使用 BB Insider CN

### 安装需求
* 最新版本的Python
* Python package: numpy, pandas, requests, Pillow

### Windows
* 安装python和所需的package
  - 前往 https://www.python.org/downloads/ 下载最新的python版本
  - 安装python，在过程中将python.exe添加到PATH(系统路径)
  - 打开cmd命令行窗口(cmd.exe)并执行下列指令:
    - `python.exe -m pip install numpy pandas requests Pillow`
* 解压bbinsider-CN到某个本地文件夹
* 在cmd命令行窗口中继续执行下列指令(XXX是存放bbinsider-CN文件夹的路径)
  - `cd C:\XXX\bbinsider-CN`
  - `chcp 65001`
* 如下指令用于获取单场比赛(需要比赛ID)的分析报告，储存于results文件夹中
  - `python.exe main.py --print-stats --print-events --matchid 128565480`
* 如下指令用于获取某联赛(需要联赛ID，可从网址中获取)某赛季的分析报告，需要输入自己的账号与数据访问密码(同Buzzer-manager)
  - `python.exe season.py --username XXX --password YYY --leagueid 149 --season 63`

### Linux 
* 安装python和所需的package，在terminal中运行
  - `sudo apt update`
  - `sudo apt install software-properties-common -y`
  - `sudo add-apt-repository ppa:deadsnakes/ppa`
  - `sudo apt install Python3.10`
  - `python3.10 -m pip install numpy pandas requests Pillow`
* 解压bbinsider-CN到某个本地文件夹
* 在terminal中继续执行下列指令(XXX是存放bbinsider-CN文件夹的路径)
  - `cd ~/XXX/bbinsider-CN`
* 如下指令用于获取单场比赛(需要比赛ID)的分析报告，储存于results文件夹中
  - `python3.10 ./main.py --print-stats --print-events --matchid 128565480`
* 如下指令用于获取某联赛(需要联赛ID，可从网址中获取)某赛季的分析报告，需要输入自己的账号与数据访问密码(同Buzzer-manager)
  - `python3.10 ./main.py --username XXX --password YYY --leagueid 149 --season 63`

### Mac
* 安装python和所需的package，在terminal中运行
  - `brew install python`
  - `python -m pip install numpy pandas requests Pillow`
* 解压bbinsider-CN到某个本地文件夹
* 在terminal中继续执行下列指令(XXX是存放bbinsider-CN文件夹的路径)
  - `cd ~/XXX/bbinsider-CN`
* 如下指令用于获取单场比赛(需要比赛ID)的分析报告，储存于results文件夹中
  - `python ./main.py --print-stats --print-events --matchid 128565480`
* 如下指令用于获取某联赛(需要联赛ID，可从网址中获取)某赛季的分析报告，需要输入自己的账号与数据访问密码(同Buzzer-manager)
  - `python ./main.py --username XXX --password YYY --leagueid 149 --season 63`
