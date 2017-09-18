## todo list
- [X]把分析的点的位置show出来
- [-]把小迪数的帧数位置的图片保存出来, 看在他的帧数的情况下, 白色区域是如何变化的
- [0]将结果转换成分和秒导出csv
- [X]看原始数据和judge能否对应上: 某种程度上可以对上
- [X]导出所有通过judge的结果的图片, 并保存下来
- [X]把在没有被threshold筛出来的图单独另一个文件夹保存起来, 看看有没有漏网之鱼
- [X]272,445依旧过于保守, 需要再向左上角移动
- [X]把judge的段数判定做修改, 相邻间隔1s = 25帧以上判定为1次, 提供间距的API
- [X]确认位置参数情况, 左上角要贴着小鼠的'白毛'
- [X]将软件交给刘小迪, 让它的电脑可以运转和调试
- [X]为什么drink的段数有差异?: 好像仿佛解决了问题, 但感觉没有想通为什么通过对中间数token的判断没法达到预期结果
- [X]导出每一次舔的段数的开始和结束帧数: 结果放在了result_judge.csv中
- [ ]对老大哥新的视频进行分析
- [ ]看下巴变化时多个像素点进行组合的判定
- [ ]我观察到, 在判断judge的段数上存在问题, 不能仅仅看datarise, 而要看datarise后的持续情况.  如视频中观察到的情况是从下巴张开到一次舔舐结束, 大约持续5帧, 其中3帧都是张开的状态
- [X]思考如何更好的判定结果是否符合预期
判断下巴运动是可行的, 可以定义老鼠一次舔舐的行为为一次下巴的开合

## idea
- [ ]舔和不舔期间的像素平均值是不一样的, 如果能够得到平均值的话, 那应该能够去掉突出来的点
- [ ]数细胞方面可以把图片反相, 看交联处的角度, 来帮助判断靠的很近的细胞之间的关系


# my_python_code
update my Python code

## bkg和result关系
像素点下移10pixel
