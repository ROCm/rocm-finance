# AMD Finance Domain

The AMD ROCm™ platform is an open-source GPU computing ecosystem designed for high-performance workloads. Within this ecosystem, AMD ROCm™ Finance Domain includes official, production‑ready support for three industry‑leading Gradient Boosting Machine (GBM) libraries on ROCm 6.4 and 7.0 :

| Library    | Current Upstream Version | Primary Finance Use‑Cases                                                       |
|:----------:|:------------------------:|:-------------------------------------------------------------------------------:|
| LightGBM   | 4.6.0.99                 | Portfolio optimization, time‑series forecasting, market‑microstructure analysis |
| ThunderGBM | 0.3.16                   | High‑frequency trading, large‑scale scenario simulations                        |

These libraries are now fully accelerated on AMD GPUs via ROCm 6.4 and 7.0, leveraging the latest CDNA 3 and Instinct™ MI300X hardware. The integration includes optimized kernels, memory‑management enhancements, and seamless multi‑GPU scaling—delivering up to XX speed‑up over CPU‑only baselines in typical finance workloads.

## Overview

### LightGBM 

LightGBM shines in finance for its histogram-based splitting and leaf-wise tree growth, enabling faster convergence on large, imbalanced datasets with many categorical features (e.g., employment types, verification status—no need for one-hot encoding). It has a low memory footprint and handles sparsity well, ideal for credit datasets. GPU support is lightweight, offering 2-5x speedups via efficient histogram computation. Nuances: Prone to overfitting without min_data_in_leaf; excels where categorical features (>10) dominate, reducing preprocessing time in production pipelines. 

### ThunderGBM 

ThunderGBM is optimized for GPU-native execution with atomic operations and approximations for ultra-fast training on billion-scale data, making it ideal for high-velocity finance tasks like real-time fraud detection on sparse transaction logs (e.g., 400+ features with many zeros). It offers 10-20x speedups over CPU on GPUs for huge datasets, with low latency predictions. Nuances: CPU fallback is rudimentary (use only for comparison); limited hyperparams and no native early stopping/categoricals (preprocess); accuracy slightly lower (~1%) but negligible for speed-critical scoring. Best for sparse, massive workloads where GPU resources are abundant.

### Feature Comparison Table

| Feature                      | LightGBM         | ThunderGBM       |
|:----------------------------:|:----------------:|:----------------:|
| Tree Growth Strategy         | Leaf-wise        | Level-wise (GPU) |
| Categorical Feature Handling | Manual + binning | Manual encoding  |
| Overfitting Control          | L1/L2 + sampling | Regularization   |
| Best For                     | Large datasets   | GPU-heavy tasks  |


## Documentation

Refer to the individual component pages for documentation on system requirements, installation instructions and examples.

- [LightGBM](https://github.com/rocm/lightgbm)
- [ThunderGBM](https://github.com/rocm/thundergbm)
