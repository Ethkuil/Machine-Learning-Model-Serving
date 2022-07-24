# 如何贡献

开发新功能、修复BUG.

本次大作业功能较复杂，故采用issue管理需求与追踪Bug.

1. 可在GitHub上提`issue`，以及认领自己打算做的功能。

2. 认领任务后，则新建`分支`进行开发。**包括测试用例**。若更改了API，需修改`API.md`文档。
```bash
git checkout -b <branch> # 基于当前分支创建新分支，并切换到新分支
git push -u origin <branch> # 在远程仓库创建同名分支. -u表示指定为当前分支的upstream, 这样之后的push、pull可省略参数
```

* 在commit message中添加`#<issue-number>`，表示该commit与某一issue相关。
* 在commit message中添加`close/fix/resolve #<issue-number>`，则关闭相应issue。例：`close #1`.

3. 开发完毕后，若对内容不太自信或遇到问题，可发起`pull request`，以便讨论。

4. 测试通过后，merge入主分支.
```bash
git checkout main
git pull --rebase # 同步远程修改，解决可能的冲突. --rebase避免产生多余节点
git merge --no-ff <branch> # 将功能合并到主分支. --no-ff可使commit历史逻辑清晰
git push
git branch -d <branch> # 删除本地分支
git push origin --delete <branch> # 删除远程分支
```

若**非常简单**，则可直接改完后提交到主分支。

*有问题可随时在群内交流。*

---

其他供参考，可能会带来便利的指令：
```bash
# cherry-pick 提取commit到HEAD之后(复制)
git cherry-pick <commit> # 可1次提取多个commit, 空格分隔. 提取顺序从左到右

# rebase 以<commit>为基，将HEAD相对于它的更新，提取到其后(移动)
git rebase <commit>
git rebase -i <commit> # 若使用-i选项，则在移动前有调整步骤，通过交互界面
git rebase <commit1> <commit2> # 以<commit1>为基，将<commit2>相对于它的更新提取到其后
git rebase --continue # 继续上次提取的过程
git rebase --abort # 取消上次提取的过程

# 修改最近的1次commit
git commit --amend

# 使用 -f 选项让分支指向另一个位置
git branch -f <branch> <commit>
```