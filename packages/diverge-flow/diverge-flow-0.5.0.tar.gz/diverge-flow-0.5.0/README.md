# DivERGe implements various ERG examples
DivERGe provides a versatile framework to set up (one,) two and three
dimensional functional renormalization group (FRG/ERG) calculations under the
static vertex approximation.

It implements three backends, the grid FRG, truncated unity FRG (TUFRG) and
orbital space n-patch FRG.

For maximum performance, the code is written in C/C++ with extensions in CUDA
(GPUs). It makes minimal use of other dependencies, only FFTW and LAPACK are
required. MPI may be used if desired. DivERGe can be interfaced from C/C++ or
python, with an existing python FFI wrapper. This wrapper is published in pypi,
such that you can run
```
pip install diverge-flow
```
on a 64bit linux machine and directly use divERGe. For different architectures,
compilation is additionally required (and putting the correct
```libdivERGe.so``` in your ```LD_LIBRARY_PATH```). You can verify the .so file
in use by calling ```diverge.info()``` from python. For any other language, you
must write all the FFI wrappers yourself.

# [Documentation](https://frg.pages.rwth-aachen.de/diverge/)
[https://frg.pages.rwth-aachen.de/diverge/](https://frg.pages.rwth-aachen.de/diverge/)

# [Download CPU release](https://git.rwth-aachen.de/frg/diverge/-/raw/master/public/releases/v0.4/divERGe.tar.gz)
Generic linux (amd64) builds (GLIBC>=2.17, this should be given almost anywhere
to date) can be downloaded
[here](https://git.rwth-aachen.de/frg/diverge/-/tree/master/public/releases). We
recommend building from source for an optimized version on the HPC
infrastructure to your availability.

# Testing
We use a slightly modified version of
[Catch2](https://github.com/catchorg/Catch2) for testing. To check divERGe's
health from python, run
```
import diverge
diverge.init(None, None)
diverge.run_tests()
diverge.finalize()
```

# Citation
Please cite [arXiv.2311.07667](https://doi.org/10.48550/arXiv.2311.07667) when
using divERGe.

# License
divERGe is published under the
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html). The releases include
non-free parts ([CUDA](https://developer.nvidia.com/cuda-toolkit)) and
differently licensed software ([OpenBLAS](https://www.openblas.net/),
[FFTW](https://www.fftw.org/)) in binary form.

# Authors
**Jonas B. Hauck** and **Lennart Klebl**, 2023.
