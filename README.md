# VarGeneNetEntropy

A variant annotation tools that focus on projecting variants to its related genes and pathways, especially for non-coding regions. 

5.28起进行Docker开发以适应多平台适应性，请稍候再下载。
### Parameters

```
usage: main.py [-h] [-P PATH] [-I INPUT] [-LD {0,1}] [-H {0,1}] [-G {0,1}]
               [-E {0,1}] [-D EFO] [-S SAMPLE] [-T TISSUE]

Annotation of Variations with VarGeneNetEntropy.

optional arguments:
  -h, --help            show this help message and exit
  -P PATH, --path PATH  Annotation File Path URL
  -I INPUT, --input INPUT
                        Input File
  -LD {0,1}, --ld {0,1}
                        1: LD extension ;0, No LD extension.
  -H {0,1}, --eqtlhic {0,1}
                        1: eQTL + HiC Annotation;0, No eQTL + HiC Annotation.
  -G {0,1}, --gsea {0,1}
                        1:GSEA Annalysis;0, No GSEA Annalysis.
  -E {0,1}, --entropy {0,1}
                        1:GSEA Annalysis;0, No GSEA Annalysis.
  -D EFO, --efo EFO     EFO Diseases ID.
  -S SAMPLE, --sample SAMPLE
                        Sample Name.
  -T TISSUE, --tissue TISSUE
                        Tissue Name.
```

### examples 

In general, we don't do ld extension, use test snp files in example dict, and do eqtl and hic annotation. Entropy and GSEA are carried by default.

```
python3 main.py -I examples/test.txt -S test -T Blood &
```

### Result1: basic annotaion

```
TMEM86B	downstream-variant-2KB	rs56154925	55737797	chr19	T,0.169129	T	C	T,0.169129	0.2148	0.2104	0.1909	0.1452	0.0823
CD40	intron-variant	rs4810485	44747946	chr20	T,0.238419	G	T	T,0.238419	0.9463	0.7853	0.7406	0.7249	0.5595
?,MECP2	intron-variant,intron-variant	rs34313552	153343317	chrX	A,0.439735	T	TA	A,0.439735	0.3816	0.8381	0.2238	0.5725	0.7258
?,MECP2	intron-variant,intron-variant	rs3831674	153348218	chrX	-,0.45351	C	CT	-,0.45351	0.3593	0.8133	0.2016	0.4981	0.4148
		rs12841797	153370113	chrX	G,0.448212	G	T	G,0.448212	0.3565	0.8094	0.2003	0.4924	0.4038
GSDMB,GSDMB,GSDMB	reference,missense,downstream-variant-2KB	rs35104165	38062502	chr17	C,0.0157748	C	T	C,0.0157748	0.0038	0.0288	0.0358	0.01840
```

### Result2: eqtl and hic annotaion

```
rs56154925	chr19	55737797
rs4810485	chr20	44747946
rs34313552	chrX	153343317
rs3831674	chrX	153348218
rs12841797	chrX	153370113
rs35104165	chr17	38062502	GSDMA	3.92170870460641e-07
```

### Result3 : pathway annotation

For limitation of display, we only show several queries.

```
MIR7110_5P      http://www.gsea-msigdb.org/gsea/msigdb/cards/MIR7110_5P 9.923462309604568e-06   0.0031406200552568353   3       167     MECP2,MECP2,GSDMA
MIR6842_5P      http://www.gsea-msigdb.org/gsea/msigdb/cards/MIR6842_5P 7.940905313211482e-06   0.0032840588811046782   3       155     MECP2,MECP2,GSDMA
MIR6752_5P      http://www.gsea-msigdb.org/gsea/msigdb/cards/MIR6752_5P 3.875453172790878e-06   0.0026374520517219034   3       122     MECP2,MECP2,GSDMA
MIR4456 http://www.gsea-msigdb.org/gsea/msigdb/cards/MIR4456    5.021150229495132e-06   0.0031236284043582203   3       133     CD40,MECP2,MECP2
MIR647  http://www.gsea-msigdb.org/gsea/msigdb/cards/MIR647     1.1711647197915816e-06  0.0025426984760359966   3       82      GSDMB,GSDMB,GSDMB
MIR1322 http://www.gsea-msigdb.org/gsea/msigdb/cards/MIR1322    7.901794669887071e-07   0.004289871615853599    3       72      CD40,MECP2,MECP2
MODULE_147      http://www.gsea-msigdb.org/gsea/msigdb/cards/MODULE_147 2.612689471894635e-06   0.0054542232752112655   3       107     CD40,MECP2,MECP2
MODULE_195      http://www.gsea-msigdb.org/gsea/msigdb/cards/MODULE_195 6.776599497584286e-06   0.004389521790241621    3       147     CD40,MECP2,MECP2
MODULE_325      http://www.gsea-msigdb.org/gsea/msigdb/cards/MODULE_325 3.114729559618499e-07   0.009826053174846243    3       53      GSDMB,GSDMB,GSDMB
MODULE_356      http://www.gsea-msigdb.org/gsea/msigdb/cards/MODULE_356 7.198965437687919e-06   0.004026451766089239    3       150     CD40,MECP2,MECP2
MODULE_485      http://www.gsea-msigdb.org/gsea/msigdb/cards/MODULE_485 2.938970317341112e-07   0.02360428953321647     3       52      GSDMB,GSDMB,GSDMB
```

#### Tissue Names in eQTL

The Tissue Name in eQTL should be chose from this lists.
|Tissue Name|
|-----------|
|Nerve_Tibial|
|Brain_Cortex|
|Pituitary|
|Artery_Coronary|
|Whole_Blood|
|Ovary|
|Esophagus_Gastroesophageal_Junction|
|Vagina|
|Cells_Transformed_fibroblasts|
|Adipose_Visceral_Omentum|
|Cells_EBV-transformed_lymphocytes|
|Brain_Hippocampus|
|Brain_Cerebellar_Hemisphere|
|Testis|
|Brain_Nucleus_accumbens_basal_ganglia|
|Adrenal_Gland|
|Liver|
|Muscle_Skeletal|
Brain_Cerebellum
Adipose_Subcutaneous
Pancreas
Prostate
Brain_Hypothalamus
Esophagus_Muscularis
Heart_Atrial_Appendage
Brain_Caudate_basal_ganglia
Brain_Anterior_cingulate_cortex_BA24
Spleen
Stomach
Small_Intestine_Terminal_Ileum
Esophagus_Mucosa
Brain_Putamen_basal_ganglia
Breast_Mammary_Tissue
Lung
Colon_Transverse
Skin_Sun_Exposed_Lower_leg
Heart_Left_Ventricle
Colon_Sigmoid
Thyroid
Artery_Tibial
Skin_Not_Sun_Exposed_Suprapubic
Artery_Aorta
Brain_Frontal_Cortex_BA9
Uterus
