## Overview of the SPremiRNA workflow  
(1) Perform basic analysis of the spatial transcriptome data from Visium, and in using the bulk sequenced data, pick out the common mRNA genes and miRNA genes between them.  
(2) Build an xgboost model, train it using the bulk sequencing dataset, and then perform migration learning to predict miRNAs from the spatial transcriptome data.  
(3) Use single-cell expression profiles of the same tissue to get the cell type in each spot in the spatial transcriptome data using cell2location.  
(4) Correlation analysis of miRNA and mRNA expression for malignant cell types.  
## Installation

We suggest using a separate conda environment for installing SPremiRNA.

Create conda environment and install?`SPremiRNA`?package

```shell
conda create -y -n SPremiRNA_env python=3.9

conda activate SPremiRNA_env
pip install SPremiRNA
```

Finally, to use this environment in jupyter notebook, add jupyter kernel for this environment:

```shell
conda activate SPremiRNA_env
python -m ipykernel install --user --name=SPremiRNA_env --display-name='Environment (SPremiRNA)'
```
Before installing cell2location and it's dependencies, it could be necessary to make sure that you are creating a fully isolated conda environment by telling python to NOT use user site for installing packages by running this line before creating conda environment and every time before activatin conda environment in a new terminal session:

```shell
export PYTHONNOUSERSITE="literallyanyletters"
```

## Usage and Tutorial
SPremiRNA Steps to run the package:
- spatial_process  
Input£ºVisium_FFPE_Human_X_Cancer_filtered_feature_bc_matrix.h5  
Output£ºX_mrna.h5ad£¬X_ranked_tcga_ccle_mirna.csv£¬X_ranked_tcga_ccle_mrna.csv£¬X_st_mrna.csv  
 
- spatial_xgboost   
Input£ºX_ranked_tcga_ccle_mirna.csv£¬X_ranked_tcga_ccle_mrna.csv£¬X_st_mrna.csv  
Output£ºX_Prest_mirna.csv  
In the model parameters, the depth of the tree is set smaller to help improve the model prediction accuracy.  

- cell2loc   
Input£ºsingle cell expression profile X_expression.loom    
Output£ºX_analysis directory  
 
- malig_mirna   
Input£ºX_mrna.h5ad£¬PreXst_mirna.csv£¬sp.h5ad in X_analysis directory  
Output£ºX_mirna.h5ad  

- ccle_gct2csv.R£¨Process CCLE data£©    
- tcga_xena2csv.R£¨Process TCGA data£©  
- sc_process.R£¨Process single cell data£©  
 