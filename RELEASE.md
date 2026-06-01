---
myst:
  html_meta:
    "description lang=en": "ROCm-Finance 26.05 Release Notes"
    "keywords": "amd, rocm, gpu, finance, financial, sdk, gbm, credit, risk, forecast, simulation, trade, stock, optimize, portfolio, time, model"
---

# AMD ROCm Finance 26.05 release notes

This release introduces an update to the popular XGBoost library in the ROCm-Finance
toolkit, enhancing machine learning capabilities for financial workloads.

## Release highlights

```{note}
ROCm-Finance libraries introduced in the 25.11 release, LightGBM and
ThunderGBM, are currently only supported on MI300X GPUs, and ROCm 7.0.2
and 6.4.4.
```

XGBoost is fully accelerated on AMD Instinct MI300X and MI325X GPUs (gfx942)
through ROCm 7.2.3, 7.1.1, 7.0.2, and 6.4.4. With the update to XGBoost in this release,
it is additionally supported on MI355X GPUs (only with ROCm 7.2.3). The XGBoost integration 
optimizes kernels, improves memory management, and enables seamless multi-GPU scaling on supported
AMD GPUs.

Key benefits of this integration include:

* **Hardware acceleration:** Parallelizes split-finding on the GPU to deliver significant performance gains over CPU-only baselines.
* **Financial risk optimization:** Accelerates large-scale tasks such as credit risk scoring, fraud detection, and loan default modeling.
* **Compliance and precision:** Increases throughput while maintaining the native robustness (L1/L2 regularization) and missing value handling of XGBoost.


## Supported platforms

To learn about hardware and software environment requirements, see the
{doc}`/about/compatibility-matrix` and the {doc}`/install/prerequisites`.


## ROCm-Finance components

The following table lists ROCm-Finance component versions for the 26.05 release. 
Click {fab}`github` to go to the component's source on GitHub.

<div class="pst-scrollable-table-container">
    <table id="rocm-rn-components" class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Version</th>
                <th>Source</th>
            </tr>
        </thead>
        <colgroup>
            <col span="1">
            <col span="1">
        </colgroup>
        <tbody class="rocm-finance-components">
            <tr>
                <td><a href="https://rocm.docs.amd.com/projects/xgboost-internal/en/docs-26.05/">XGBoost</a></td>
                <td>3.1.1&nbsp;&Rightarrow;&nbsp;<a href="#xgboost-3-2-0">3.2.0</a></td>
                <td><a href="https://github.com/ROCm/xgboost/tree/release/3.2.0"><i class="fab fa-github fa-lg"></i></a></td>
            </tr>
            <tr>
                <td><a href="https://rocm.docs.amd.com/projects/lightgbm/en/docs-25.11/">LightGBM</a></td>
                <td>4.6.0.99</td>
                <td><a href="https://github.com/ROCm/LightGBM/tree/release/4.6.0.99"><i class="fab fa-github fa-lg"></i></a></td>
            </tr>
            <tr>
                <td><a href="https://rocm.docs.amd.com/projects/thundergbm/en/docs-25.11/">ThunderGBM</a></td>
                <td>0.3.16</td>
                <td><a href="https://github.com/ROCm/ThunderGBM/tree/release/0.3.16"><i class="fab fa-github fa-lg"></i></a></td>
            </tr>
        </tbody>
    </table>
</div>

## Detailed component changelogs

### XGBoost 3.2.0

XGBoost 3.2.0 emphasizes external-memory training on GPUs, deeper multi-target / vector-leaf tree support, general GPU hist improvements, and housekeeping such as removal of the deprecated CLI.

The full list is available in the [XGBoost 3.2.0 changelog](https://xgboost.readthedocs.io/en/release_3.2.0/changes/v3.2.0.html).

#### Key features and improvements

External memory training:
- Adaptive cache behavior: Automatically adjusts cache strategy across different device types (CPU/GPU)
- CUDA async memory pool: Optional experimental async memory pool for improved GPU memory management (Linux CUDA ecosystem)
- Mixed GPU-host cache: Flexible configuration for caching data between GPU and host memory
- Simplified pipeline: Removed older "page concat" path in favor of full dataset training approach

Multi-target (vector leaf) support:
- Enhanced vector-leaf trees: Improved implementation for multi-target regression
- Sketch boost: Reduced-gradient ideas for better histogram scalability
- Broader GPU support: More regression objectives available on GPU hist
- Status: Upstream marks parts of vector leaf as work in progress

Performance improvements for GPU histograms: 
- Device memory model storage: Trees stored in device memory to reduce host/device transfer overhead
- Kernel refinements: Optimized histogram building kernels for AMD GPUs
- Reduced memory churn: Minimized host-device data transfers during training and inference

#### Known limitations

- GPU SHAP fallback: SHAP value computation falls back to CPU
- Additional dependencies: Features requiring extra packages (for example, RMM) are not supported
- Multi-GPU limitations: Supported only via PySpark with limited functionality, other frameworks are unsupported
- API support for Python and C++ only
