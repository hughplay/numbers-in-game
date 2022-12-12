import re

import matplotlib.pyplot as plt
import numpy as np


def flip_matrix(matrix):
    """将AA（rank最大）从右下角翻转到左上角."""
    return np.flip(matrix, axis=[0, 1])


def plot_card_rate(
    matrix,
    title=None,
    row_ticks=["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"],
    col_ticks=["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"],
    path_to_save=None,
):
    """绘制牌的统计数据图
    matrix: 2D矩阵，对角线左上角对应AA，对角线右上方对应不同色牌，对角线左下方对应同色牌
    """

    # 如果标题不为空，且标题包含中文字符，则需要设置字体
    target_font = "Arial"
    if title and re.findall(r"[\u4e00-\u9fff]+", title):
        candidate_fonts = ["Hei", "SimHei", "Microsoft YaHei"]
        import matplotlib.font_manager

        fonts = list(
            sorted(
                [f.name for f in matplotlib.font_manager.fontManager.ttflist]
            )
        )

        for font in candidate_fonts:
            if font in fonts:
                target_font = font
                break
        else:
            print("没有可用的中文字体，禁用标题。")
            title = None

    # 设置matplotlib的参数
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["savefig.format"] = "pdf"
    plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["savefig.pad_inches"] = 0.1

    plt.rcParams["figure.titlesize"] = 12
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["font.family"] = target_font
    plt.rcParams["font.size"] = 7

    plt.rcParams["lines.linewidth"] = 2
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10
    plt.rcParams["legend.fontsize"] = 12
    plt.rcParams["axes.linewidth"] = 1
    plt.rcParams["axes.titlepad"] = 6

    plt.rcParams["mathtext.fontset"] = "dejavuserif"
    plt.rcParams["mathtext.it"] = "serif:italic"
    plt.rcParams["lines.marker"] = ""
    plt.rcParams["legend.frameon"] = False

    fig, ax = plt.subplots()

    # 将矩阵画出来
    ax.imshow(matrix)

    # 设置坐标轴
    ax.set_xticks(np.arange(len(col_ticks)), labels=col_ticks)
    ax.set_yticks(np.arange(len(row_ticks)), labels=row_ticks)

    # 设置每个格子的数字
    for i, row in enumerate(row_ticks):
        for j, column in enumerate(col_ticks):
            # 左下角用s（suited）表示同色，右上角用o（offsuited）表示不同色
            pair_name = f"{column}{row}s" if i > j else f"{row}{column}o"
            ax.text(
                j,
                i,
                f"{pair_name}\n{matrix[i, j] * 100:.2f}",
                ha="center",
                va="center",
                color="w",
            )

    ax.tick_params(
        axis="both", which="both", length=0, labeltop=True, labelbottom=False
    )
    fig.tight_layout()
    if title:
        plt.title(title)
    if path_to_save:
        plt.savefig(path_to_save)
    plt.show()
