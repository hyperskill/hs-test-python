from hstest import *


class EDATest(PlottingTest):
    def generate(self):
        return [
            TestCase()
        ]

    def check(self, reply, attach):
        all_figures = self.all_figures()
        if len(all_figures) == 0:
            return CheckResult.wrong("Looks like you didn't present any plots")
        if len(all_figures) != 2:
            return CheckResult.wrong(f"Expected 2 plots, found {len(all_figures)}")

        return CheckResult.correct()


if __name__ == '__main__':
    EDATest().run_tests()
