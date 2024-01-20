import warnings
warnings.filterwarnings("ignore")
import scanpy as sc
import anndata
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib import rcParams
rcParams['pdf.fonttype'] = 42 # enables correct plotting of text
import cell2location

from cell2location.utils.filtering import filter_genes
from cell2location.models import RegressionModel

sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
sc.logging.print_header()
sc.settings.set_figure_params(dpi=100, facecolor='white')


def Build_ref(adata_ref, meta, sample_counts):
    adata_ref.obs['Celltype'] = meta['Celltype (major-lineage)'].values
    adata_ref.obs['Cluster'] = meta['Cluster'].values
    adata_ref.obs['UMAP_1'] = meta['UMAP_1'].values
    adata_ref.obs['UMAP_2'] = meta['UMAP_2'].values

    # feature过滤，去掉一些表达比例比较低或者表达量低的基因
    selected = filter_genes(adata_ref, cell_count_cutoff=5, cell_percentage_cutoff2=0.03, nonz_mean_cutoff=1.12)
    adata_ref = adata_ref[:, selected].copy()
    unnormal = np.exp(adata_ref.to_df()) - 1
    unnormal = np.floor(unnormal)
    adata_ref.X = unnormal.values

    # 这里将raw设置成当前的数据，否则后面的sampling会出问题
    adata_ref.raw = adata_ref
    sc.pp.subsample(adata_ref, n_obs=sample_counts)
    return adata_ref


# cell2location会对reference fit Negative binomial distribution,
def SC_estimation(adata_ref, celltype,ref_run_name):
    # 去除batch effects
    cell2location.models.RegressionModel.setup_anndata(adata=adata_ref,
                                                       #                         batch_key='CellID',
                                                       labels_key=celltype
                                                       )
    mod = RegressionModel(adata_ref)
    mod.view_anndata_setup()

    mod.train(max_epochs=800, accelerator='gpu')
    mod.plot_history()
    # In this section, we export the estimated cell abundance (summary of the posterior distribution).
    adata_ref = mod.export_posterior(
        adata_ref,
        sample_kwargs={'num_samples': 1000, 'batch_size': 2500,
                       'use_gpu': True}
    )

    # Save model
    mod.save(f"{ref_run_name}", overwrite=True)

    # Save anndata object with results
    adata_file = f"{ref_run_name}/sc.h5ad"
    adata_ref.write(adata_file)
    return adata_ref, mod


def PreprocessST(adata_vis, inf_aver):
    adata_vis.obs_names_make_unique()
    adata_vis.var_names_make_unique()

    adata_vis.obs['sample'] = list(adata_vis.uns['spatial'].keys())[0]  # 标记样本名字

    # find shared genes and subset both anndata and reference signatures
    intersect = np.intersect1d(adata_vis.var_names, inf_aver.index)
    adata_vis = adata_vis[:, intersect].copy()
    inf_aver = inf_aver.loc[intersect, :].copy()
    return adata_vis, inf_aver


def ST_estimation(adata_vis, inf_aver,run_name):
    # prepare anndata for cell2location model
    cell2location.models.Cell2location.setup_anndata(adata=adata_vis, batch_key="sample")

    # create and train the model
    mod = cell2location.models.Cell2location(
        adata_vis, cell_state_df=inf_aver,
        # the expected average cell abundance: tissue-dependent
        # hyper-prior which can be estimated from paired histology:
        N_cells_per_location=30,
        # hyperparameter controlling normalisation of
        # within-experiment variation in RNA detection:
        detection_alpha=20
    )
    mod.view_anndata_setup()

    mod.train(max_epochs=30000,
              # train using full data (batch_size=None)
              batch_size=None,
              # use all data points in training because
              # we need to estimate cell abundance at all locations
              train_size=1,
              #           use_gpu=False,
              accelerator='gpu'
              )

    # plot ELBO loss history during training, removing first 100 epochs from the plot
    mod.plot_history(50)
    plt.legend(labels=['full data training'])

    # In this section, we export the estimated cell abundance (summary of the posterior distribution).
    adata_vis = mod.export_posterior(
        adata_vis,
        sample_kwargs={'num_samples': 1000, 'batch_size': mod.adata.n_obs, 'use_gpu': True}
    )

    # Save model
    mod.save(f"{run_name}", overwrite=True)
    # mod = cell2location.models.Cell2location.load(f"{run_name}", adata_vis)

    # Save anndata object with results
    adata_file = f"{run_name}/sp.h5ad"
    adata_vis.write(adata_file)
    return adata_vis, mod


def Visual_abundance(adata_vis, adata_ref):
    # add 5% quantile, representing confident cell abundance, 'at least this amount is present',
    # to adata.obs with nice names for plotting
    adata_vis.obs[adata_vis.uns['mod']['factor_names']] = adata_vis.obsm['q05_cell_abundance_w_sf']

    # plot in spatial coordinates
    with mpl.rc_context({'axes.facecolor': 'black',
                         'figure.figsize': [4.5, 5]}):
        sc.pl.spatial(adata_vis, cmap='magma',
                      # show first 8 cell types
                      color=adata_ref.obs["Celltype"].unique().tolist(),
                      ncols=3, size=1.5,
                      img_key='hires',
                      # limit color scale at 99.2% quantile of cell abundance
                      vmin=0, vmax='p99.2'
                      )
