import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
sc.logging.print_header()
sc.settings.set_figure_params(dpi=300, facecolor='white')


# 进行基因计数和添加到 adata.obs 中
def QC(adata):
    sc.pp.calculate_qc_metrics(adata, inplace=True)
    warnings.filterwarnings("ignore", "is_categorical_dtype")
    warnings.filterwarnings("ignore", "use_inf_as_na")
    sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts'], jitter=0.4, multi_panel=True)

    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    pd.option_context('mode.use_inf_as_na', True)
    sns.histplot(adata.obs["total_counts"], kde=False, ax=axs[0])
    sns.histplot(adata.obs["total_counts"][adata.obs["total_counts"] < 80000],
                 kde=False,
                 bins=40,
                 ax=axs[1])
    sns.histplot(adata.obs["n_genes_by_counts"], kde=False, bins=60, ax=axs[2])
    sns.histplot(
        adata.obs["n_genes_by_counts"][adata.obs["n_genes_by_counts"] < 2000],
        kde=False,
        bins=60,
        ax=axs[3])


def QC_filter(adata, min_counts, max_counts):
    sc.pp.filter_cells(adata, min_counts=min_counts)
    sc.pp.filter_cells(adata, max_counts=max_counts)
    print(f"#cells after filter: {adata.n_obs}")
    sc.pp.filter_genes(adata, min_cells=10)


# 标准化
def Standard(adata):
    sc.pp.normalize_total(adata, inplace=True)
    sc.pp.log1p(adata)


# 识别高变基因
def Select_highly(adata):
    sc.pp.highly_variable_genes(adata, flavor="seurat", n_top_genes=2000)
    sc.pl.highly_variable_genes(adata)
    # 只保留高变基因
    adata.raw = adata
    adata = adata[:, adata.var.highly_variable]
    return adata


# 找出bulk data和ST data的common gene,进行排序和整合
def Save_ranked_mrna(tcga_mrna, ccle_mrna, adata,outdir):
    # 删除重复的行索引
    dup_index = ccle_mrna.columns.duplicated()
    ccle_mrna = ccle_mrna.loc[:, ~dup_index]
    dup_index = tcga_mrna.columns.duplicated()
    tcga_mrna = tcga_mrna.loc[:, ~dup_index]
    # 选择共同基因
    tcga_gene = tcga_mrna.columns
    ccle_gene = ccle_mrna.columns
    st_gene = adata.var_names
    common_gene1 = list(set(tcga_gene).intersection(st_gene))
    common_gene = list(set(common_gene1).intersection(ccle_gene))
    # 保存有common gene的tcga mrna表达数据
    com_tcga_data = tcga_mrna[common_gene]
    # # 对每一行进行排名
    ranked_tcga_mrna = com_tcga_data.rank(axis=1, ascending=True, method='min')


    # 保存有common gene的ccle mrna表达数据
    com_ccle_data = ccle_mrna[common_gene]
    # # 对每一行进行排名
    ranked_ccle_mrna = com_ccle_data.rank(axis=1, ascending=True, method='min')

    # 将按列tcga和ccle的数据合并，保存
    ranked_tcga_ccle_mrna = pd.concat([ranked_tcga_mrna, ranked_ccle_mrna])
    ranked_tcga_ccle_mrna.to_csv(outdir + "_ranked_tcga_ccle_mrna.csv")

    # 保存有common gene的ST表达数据
    st_exp = adata.to_df()
    st_exp = st_exp[common_gene]
    st_exp.to_csv(outdir +  '_st_mrna.csv')


def Save_ranked_mirna(tcga_mirna, ccle_mirna,outdir):
    # 删除重复的行索引
    dup_index = ccle_mirna.columns.duplicated()
    ccle_mirna = ccle_mirna.loc[:, ~dup_index]
    dup_index = tcga_mirna.columns.duplicated()
    tcga_mirna = tcga_mirna.loc[:, ~dup_index]
    # 处理miRNA的名称，把p去掉
    ccle_mirna.columns = ccle_mirna.columns.str.replace(r'-\d+p$', '', regex=True)
    # 去重并以平均值替换
    ccle_mirna = ccle_mirna.groupby(ccle_mirna.columns, axis=1).mean()
    # 处理miRNA的名称，把p去掉
    tcga_mirna.columns = tcga_mirna.columns.str.replace(r'-\d+p$', '', regex=True)
    # 去重并以平均值替换
    tcga_mirna = tcga_mirna.groupby(tcga_mirna.columns, axis=1).mean()
    # 删除重复的行索引
    dup_index = ccle_mirna.columns.duplicated()
    ccle_mirna = ccle_mirna.loc[:, ~dup_index]
    dup_index = tcga_mirna.columns.duplicated()
    tcga_mirna = tcga_mirna.loc[:, ~dup_index]
    # 处理miRNA的名称，把p去掉
    ccle_mirna.columns = ccle_mirna.columns.str.replace(r'-\d+p$', '', regex=True)
    # 去重并以平均值替换
    ccle_mirna = ccle_mirna.groupby(ccle_mirna.columns, axis=1).mean()
    # 处理miRNA的名称，把p去掉
    tcga_mirna.columns = tcga_mirna.columns.str.replace(r'-\d+p$', '', regex=True)
    # 去重并以平均值替换
    tcga_mirna = tcga_mirna.groupby(tcga_mirna.columns, axis=1).mean()

    # 选择共同基因
    tcga_gene = tcga_mirna.columns
    ccle_gene = ccle_mirna.columns
    common_gene = list(set(tcga_gene).intersection(ccle_gene))
    # 保存有common gene的tcga mrna表达数据
    com_tcga_data = tcga_mirna[common_gene]
    # # 对每一行进行排名
    ranked_tcga_mirna = com_tcga_data.rank(axis=1, ascending=True, method='min')

    # 保存有common gene的ccle mrna表达数据
    com_ccle_data = ccle_mirna[common_gene]
    # # 对每一行进行排名
    ranked_ccle_mirna = com_ccle_data.rank(axis=1, ascending=True, method='min')

    # 将按列tcga和ccle的数据合并，保存
    ranked_tcga_ccle_mirna = pd.concat([ranked_tcga_mirna, ranked_ccle_mirna])
    ranked_tcga_ccle_mirna.to_csv(outdir +"_ranked_tcga_ccle_mirna.csv")


def Spatial_analyze(adata,outdir):
    # pca降维，主成分为50
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)

    sc.tl.pca(adata, svd_solver='arpack', n_comps=50)
    sc.pl.pca_variance_ratio(adata, log=True)

    # 构建邻域网络图
    sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
    # UMAP&tsne降维，计算出来的都是坐标值
    # t-SNE和UMAP是另外两种非线性的降维方法
    sc.tl.umap(adata)
    sc.tl.tsne(adata, n_pcs=40)

    # leiden算法聚类
    sc.tl.leiden(adata, key_added="clusters")
    # 保存ST 聚类信息文件
    adata.write(outdir + '_mrna.h5ad')

    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    sc.pl.umap(adata,
               color="clusters", use_raw=False, legend_loc='on data', legend_fontsize=8,
               ax=ax
               )

    plt.rcParams["figure.figsize"] = (6, 6)
    sc.pl.spatial(adata,
                  img_key="hires",
                  color=["total_counts", "n_genes_by_counts"])

    sc.pl.spatial(adata, img_key="hires", color="clusters", size=1.5)

    # 提取降维后的数据-->主成分为50
    # comp = pd.DataFrame(adata.obsm['X_pca'],index=adata.obs_names)
    # comp = comp.T
    # comp.to_csv('FRspatial_breast.csv')
