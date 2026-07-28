# ROCm Finance Contributing Guide

To ensure the quality of the ROCm-Finance codebase, the ROCm-Finance team has established a code review process to guide developers through the steps required to contribute changes to the repository.

## Table of Contents

- [How to Get Started](#how-to-get-started)
- [How Do I Contribute?](#how-do-i-contribute)
  - [Reporting Issues](#reporting-issues)
    - [Bugs](#bugs)
    - [Enhancement Requests](#enhancement-requests)
  - [Creating a Pull Request](#creating-a-pull-request)
- [Responsibility of the Author](#responsibility-of-the-author)
- [Responsibility of the Reviewer](#responsibility-of-the-reviewer)
- [Passing CI](#passing-ci)
- [The Review Process](#the-review-process)

## How to Get Started

AMD ROCm-Finance is a toolkit containing highly optimized gradient boosting machine (GBM) libraries for financial workloads on AMD GPUs. The toolkit includes three core libraries: XGBoost, LightGBM, and ThunderGBM, providing GPU-accelerated implementations for training and inference of gradient boosted decision trees commonly used in financial applications.

The easiest way to get started is to read the documentation for each library:

- [XGBoost](https://rocm.docs.amd.com/projects/xgboost/en/latest/)
- [LightGBM](https://rocm.docs.amd.com/projects/lightgbm/en/latest/)
- [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm/en/latest/)

All contributions you make will be under the [Apache License 2.0](https://github.com/ROCm/rocm-finance/blob/main/LICENSE).

## How Do I Contribute?

### Reporting Issues

We use [GitHub Issues](https://github.com/ROCm/rocm-finance/issues) to track public **bugs** and **enhancement requests**.

Before submitting an issue, please check the documentation for [XGBoost](https://rocm.docs.amd.com/projects/xgboost/en/latest/), [LightGBM](https://rocm.docs.amd.com/projects/lightgbm/en/latest/), or [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm/en/latest/) to verify whether the issue is a known limitation or if the feature is already supported in the latest version of ROCm Finance.

#### Bugs

Use the following template when reporting bugs in ROCm Finance:

1. **Description**: *Please be clear and descriptive*
2. **How to Reproduce**:
   - Hardware information
   - Docker environment or software version
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
3. **Additional Information**: Any other context, logs, or screenshots

#### Enhancement Requests

Use the following template when submitting enhancement requests for ROCm Finance:

1. **Description**: *Please be clear and descriptive*
2. **Value and Motivation**:
   - Features and functionalities enabled
   - Use cases
   - Alternatives considered
3. **Additional Information**: Any other relevant context

**Note on Labels**: Authors should set labels and milestones according to their understanding. Other contributors may adjust these values if they disagree, and are encouraged to add a brief comment explaining their reasoning. This keeps the process flexible while promoting mutual understanding. Labels such as "bug," "feature," or "complexity*" are typically stable, while "value*" or "urgency*" may be adjusted based on team consensus.

### Creating a Pull Request

No changes may be committed directly to the `develop` branch of the ROCm-Finance repository. All authors must develop their changesets on a separate branch and create a pull request (PR) to merge changes into the `develop` branch.

When creating a PR, the author must select **two reviewers**:

1. **Technical Expert**: A developer with expertise in the affected component (XGBoost, LightGBM, or ThunderGBM)
2. **Peer Reviewer**: Any other ROCm-Finance developer

## Responsibility of the Author

The author of a PR is responsible for:

- Writing clear, well-documented code
- Meeting code quality expectations
- Verifying that changes do not break existing functionality
- Writing tests to ensure adequate code coverage
- Reporting on performance impact (if applicable)

## Responsibility of the Reviewer

Each reviewer is responsible for verifying that the changes are clearly written, follow the library's coding standards, are well-documented for future maintainability, and maintain or improve the overall quality of the codebase.

### Reviewer's Checklist

1. Has the PR passed all necessary CI checks?
2. Does the PR consist of a well-organized sequence of small, logical commits, each addressing a specific feature or fix (and ideally passing CI independently)?
3. Is the PR a reviewable size? If not, should it be broken into smaller, testable, and reviewable tasks?
4. Does the PR include sufficient documentation? Is the code easy to read, understand, test, and maintain?
5. If the API or functionality has changed, has the appropriate library documentation been updated ([XGBoost](https://rocm.docs.amd.com/projects/xgboost/en/latest/), [LightGBM](https://rocm.docs.amd.com/projects/lightgbm/en/latest/), or [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm/en/latest/))?
6. For bugfixes and new features, have new regression tests been created and included in CI or another test pipeline?
7. Is the PR associated with a ticket or issue number for tracking purposes?

## Passing CI

CI testing is a critical component of the PR process. **All PRs must pass CI** to be considered for merge. Reviewers may defer their review until CI testing has passed.

## The Review Process

During the review, reviewers will examine the changes and provide suggestions or request modifications.

To help reviewers prioritize their efforts, authors can:

- Set appropriate urgency and value labels
- Assign the milestone for when the changes need to be delivered
- Describe the testing procedure and document the measured impact of the changes
- Send a reminder email if a PR requires attention
- If a PR is time-sensitive, explain to reviewers why it should be prioritized

---

**Thank you for contributing to ROCm Finance!**
