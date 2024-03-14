import cProfile
import pstats
import io
from main import main

# 准备用于性能分析的参数
class Args:
    def __init__(self, source_file, target_file, res_file):
        self.source_file = source_file
        self.target_file = target_file
        self.res_file = res_file

args = Args('E:\\Git仓库\\第二次作业\\测试文本\\orig.txt', 'E:\\Git仓库\\第二次作业\\测试文本\\orig_0.8_add.txt', 'E:\\Git仓库\\第二次作业\\测试文本\\答案.txt')

# 运行性能分析
pr = cProfile.Profile()
pr.enable()
main(args) # 执行你的主函数
pr.disable()

# 生成性能报告
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats()
print(s.getvalue())