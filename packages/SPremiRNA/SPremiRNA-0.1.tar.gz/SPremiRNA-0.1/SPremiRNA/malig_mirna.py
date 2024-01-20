import warnings
warnings.filterwarnings("ignore")

import scanpy as sc
import anndata
import pandas as pd
import numpy as np
import matplotlib as mpl

from cell2location.plt import plot_spatial
import anndata as ad

sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
sc.logging.print_header()
sc.settings.set_figure_params(dpi=300, facecolor='white')



# Now we use cell2location plotter that allows showing multiple cell types in one panel
def Visual_Malignant(adata_vis):
    adata_vis.obs[adata_vis.uns['mod']['factor_names']] = adata_vis.obsm['q05_cell_abundance_w_sf']

    clust_labels = ['Malignant']
    clust_col = ['' + str(i) for i in clust_labels]  # in case column names differ from labels

    with mpl.rc_context({'figure.figsize': (8, 8)}):
        fig = plot_spatial(
            adata_vis,
            # labels to show on a plot
            color=clust_col, labels=clust_labels,
            show_img=True,
            # 'fast' (white background) or 'dark_background'
            style='fast',
            # limit color scale at 99.2% quantile of cell abundance
            max_color_quantile=0.992,
            # size of locations (adjust depending on figure size)
            circle_diameter=6,
            colorbar_position='right'
        )


def Build_STmirna(mirna, sp_mrna):
    mirna = mirna.rank(axis=1, ascending=True, method='min')
    obs_names = mirna.index.to_list()
    obs = pd.DataFrame(index=obs_names)
    # 设置特征名
    var_names = mirna.columns.to_list()
    # 特征数量
    n_vars = len(var_names)
    # 特征注释数据框
    var = pd.DataFrame(index=var_names)
    # 生成数据矩阵
    X = mirna.values

    # 初始化 AnnData 对象
    # AnnoData 对象默认使用数据类型为 `float32`, 可以更精确的存储数据
    mirna_adata = ad.AnnData(X, obs=obs, var=var, dtype='int32')
    # 使用spatial mRNA的空间位置等信息
    mirna_adata.uns = sp_mrna.uns
    mirna_adata.obsm = sp_mrna.obsm
    mirna_adata.obs['clusters'] = sp_mrna.obs['clusters']
    return mirna_adata


def Add_celltype(adata_vis, sp_mirna, sp_mrna,outdir):
    # 取共同样本
    intersect = np.intersect1d(adata_vis.obs_names, sp_mirna.obs_names)
    sp_mrna = adata_vis[intersect]
    # 选择最大值的作为spot主细胞类型
    print(adata_vis.obs.columns[7:])
    sp_mrna.obs['celltype'] = sp_mrna.obs[adata_vis.obs.columns[7:]].idxmax(axis=1)
    # 给miRNA数据增加细胞类型信息
    sp_mirna.obs['celltype'] = sp_mrna.obs['celltype']
    sp_mirna.write(outdir +  '_mirna.h5ad')
    return sp_mirna


def Find_top(sp_mirna, Celltype,outdir):
    sc.tl.rank_genes_groups(sp_mirna, 'celltype', method='wilcoxon')
    sc.pl.rank_genes_groups(sp_mirna, n_genes=10)

    # find all degs
    celltype = sp_mirna.obs['celltype'].unique().tolist()  # 把所有细胞簇种类拿出来
    deg = sc.get.rank_genes_groups_df(sp_mirna, group=celltype)  # 把所有细胞簇对应的deg拿出来
    deg.to_csv(outdir+'_malig_DEG.csv') #存储备份

    groups = deg.groupby('group')
    top10 = groups.get_group(Celltype).sort_values('scores', ascending=False).head(10)
    top10 = top10["names"]
    return top10


