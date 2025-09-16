Reorganized Structure for Intel-Labeled PRs
# 1. Operator Optimization (Major Focus)
## oneDNN/MKLDNN Optimization
## Integration and upgrade (e.g., oneDNN v3.5, v3.6 upgrades)
## Kernel fusion and placement improvements
## BFloat16 and INT8 related optimizations
## Specific operator enhancements (e.g., conv2d, matmul, FC, scale_matmul)
# Performance Improvements

## Speed and fuse pass improvements

## Layout and data format fixes (e.g., NHWC, memory format)

## Cache and threading optimizations

## Bug Fixes for Optimization

## Operator-specific bug fixes for inference and training correctness

# 2. Quantization
## INT8 and PTQ/QAT related PRs

## Fusion passes for quantized ops

## Specific operator quantization support (matmul, conv, gru, lstm)

## Tools and helper fixes (scale calculations, cache)

# 3. BF16 / Low Precision Support
## BFloat16 data type addition and support in various ops

## Precision mode support and fixes (FP32/BF16)

## Unit tests and validation on BF16 functionality

# 4. CI / Infrastructure
## Docker, workflow, continuous integration improvements

## Build system fixes supporting specific Intel hardware or OS

## Cache and environment related automation fixes

# 5. Documentation
## Docs updates related to Intel/oneDNN

## README and API documentation improvements

# 6. Bugfix
## Bug fixes ranging from core operators to environment and testing failures

## Fixes related to segfault, crash, and accuracy issues on Intel platforms

# 7. API / Interface
## PRs related to improving or expanding API compatibility or functionality

# 8. Refactor
## Code base refactoring mostly for oneDNN integration or operator cleanup

# 9. Tests
## New tests or fixes to existing ones targeting Intel-specific behaviors or general coverage

# 10. Build
## Build system changes supporting Intel-related optimizations or cross-platform compatibility

# 11. Uncategorized
PRs not yet categorized or requiring special assignment
