import io
import numpy as np
import matplotlib.pyplot as plt

"""
描画するグラフの値を設定する。
"""


class SetGraph():
    def __init__(self, graph_data1, column_name1, graph_data2, column_name2):
        self.graph_data1 = graph_data1
        self.column_name1 = column_name1
        self.graph_data2 = graph_data2
        self.column_name2 = column_name2

    def set_hist(self):
        """
        ヒストグラムを作成する
        :return:
        """
        # x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        # y = np.array([20, 100, 50, 110, 100, 80, 20, 60, 20, 70])
        # plt.plot(x, y)
        plt.title('Number of {0} and {1} Distribution'.format(self.column_name1, self.column_name2))
        plt.xlabel('{0} and {1}'.format(self.column_name1, self.column_name2))
        plt.ylabel('frq')
        plt.hist(self.graph_data1, alpha=0.5, label=self.column_name1)
        plt.hist(self.graph_data2, alpha=0.3, label=self.column_name2)
        plt.legend(loc="upper left", fontsize=13) # (5)凡例表示

    def plt_to_svg(self):
        """
        svg形式に変換する
        :return:
        """
        buf = io.BytesIO()
        plt.savefig(buf, format='svg', bbox_inches='tight')
        s = buf.getvalue()
        buf.close()
        return s

    def main(self):
        self.set_hist()       # create the plot
        svg = self.plt_to_svg()  # convert plot to SVG
        plt.cla()        # clean up plt so it can be re-used
        return svg

