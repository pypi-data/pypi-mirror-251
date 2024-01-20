import warnings
warnings.filterwarnings("ignore")

import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import spearmanr

sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
sc.logging.print_header()
sc.settings.set_figure_params(dpi=300, facecolor='white')



def ProcessST(adata, min_counts, max_counts):
    sc.pp.filter_cells(adata, min_counts=min_counts)
    sc.pp.filter_cells(adata, max_counts=max_counts)
    print(f"#cells after MT filter: {adata.n_obs}")
    sc.pp.filter_genes(adata, min_cells=10)

    # 标准化
    sc.pp.normalize_total(adata, inplace=True)
    sc.pp.log1p(adata)
    # 归一化
    sc.pp.scale(adata, max_value=10)
    st_mrna = adata.to_df()
    return st_mrna

def plot_heatmap(cor_df,mirna):
    # 计算斯皮尔曼相关性系数和p值
    correlation_matrix, p_values = spearmanr(cor_df)
    last_row = correlation_matrix[-1, :-1]
    last_p = p_values[-1,:-1].reshape(1,-1)
    plt.figure(figsize=(20,3),dpi=300)

    # 设置热图
    heatmap = sns.heatmap(
        last_row.reshape(1, -1),
        annot=True,
        cmap='RdBu_r',
        fmt=".2f", vmin=-1, vmax=1,
        linewidths=2,cbar_kws={"shrink": .8}, square=True
    )

    # 在热图上显示p值的星号标记
    for i in range(last_p.shape[0]):
        for j in range(last_p.shape[1]):
            if last_p[i, j] < 0.001:
                plt.text(j + 0.5, i + 0.5, '***', ha='center', va='bottom', color='black', fontsize=12)
            elif last_p[i, j] < 0.005:
                plt.text(j + 0.5, i + 0.5, '**', ha='center', va='bottom', color='black', fontsize=12)
            elif last_p[i, j] < 0.05:
                plt.text(j + 0.5, i + 0.5, '*', ha='center', va='bottom', color='black', fontsize=12)

    yticks = [cor_df.columns[-1]]
    xticks = [i for i in cor_df.columns[:-1]]
    plt.xticks(plt.xticks()[0], labels=xticks)
    plt.yticks(plt.yticks()[0], labels=yticks, rotation=0)

    # 显示图形
    title = 'correlation matrix\n%s targeted gene\n'%mirna
    plt.title(title,fontsize=10)
    plt.savefig("heatmap-%s.png" % mirna)
    plt.show()
