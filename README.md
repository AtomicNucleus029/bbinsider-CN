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
  - `python.exe season.py --username XXX --password YYY --leagueid 149 --season 63 --gamelimit 1 --minutelimit 5`
  - 可以在--gamelimit和--minutelimit参数后设置出场次数和场均出场时间的阈值，出场较少的球员将被排除

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
  - `python3.10 ./main.py --username XXX --password YYY --leagueid 149 --season 63 --gamelimit 1 --minutelimit 5`
  - 可以在--gamelimit和--minutelimit参数后设置出场次数和场均出场时间的阈值，出场较少的球员将被排除

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
  - `python ./main.py --username XXX --password YYY --leagueid 149 --season 63 --gamelimit 1 --minutelimit 5`
  - 可以在--gamelimit和--minutelimit参数后设置出场次数和场均出场时间的阈值，出场较少的球员将被排除

### 一些说明
* 在BuzzerBeater的编码中，投篮事件涉及的有且仅有两名球员，其一为投篮者，其二为同队的传球者或对手的干扰者（不会同时出现）。因此投篮分为接传球后的投篮及顶人强投两种，不存在第三种情况。接球投篮可理解为战术成功，传导出空位；顶人强投可理解为战术失败，没有出空位，只能单打。在少数情况下，文字直播只显示投篮者，不显示传球者或干扰者，此时传球者在编码中存在，只是没有显示出来。
* 攻守回合的交换在以下情况发生：
  - 投篮命中（无加罚）
  - 投篮或罚篮不中后防守方抢到防守篮板
  - 投篮不中后双方均未抢到篮板，但球权判给防守方
  - 罚篮中的最后一罚命中
  - 失误
  - 投篮后小节结束
  - （投篮或罚篮不中后抢到进攻篮板不计入回合数）
* 球员的百回合得分为球员在场上时，球队每百回合的得分。失分和净胜分同理。on-off百回合得分是球员在场与不在场时，球队每百回合得分的差值。失分与净胜分同理。这些数据，尤其是on-off值，收到排兵布阵及对手的影响，而且在较大样本下才有参考价值。
