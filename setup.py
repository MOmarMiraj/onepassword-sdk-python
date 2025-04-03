from setuptools import setup, find_packages, Distribution
from sysconfig import get_platform
import platform
import os

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
            # This platform naming is sufficient for distributing this package via source cloning (e.g. pip + GitHub) since the wheel will be built locally
            # for each user's platform: https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#basic-platform-tags
            self.plat_name = get_platform().translate({"-": "_", ".": "_"})
            self.plat_name_supplied = True
except ImportError:
    bdist_wheel = None

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

def get_shared_library_data_to_include():
    # Return the correct uniffi C shared library extension for the given platform
    machine_type = os.getenv("PYTHON_MACHINE_PLATFORM", platform.machine().lower())
    platform_name = os.getenv("PYTHON_OS_PLATFORM", platform.system())
    python_version = platform.python_version()[:4]

    arch_map = {
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "aarch64": "aarch64",
        "arm64": "aarch64",
    }

    include_path = ["lib"]

    if platform_name == "Darwin":
        if machine_type in arch_map:
            if arch_map[machine_type] == "x86_64":
                macos_version = "x86_64_macosx_10_13" if python_version >= "3.13" else "x86_64_macosx_10_9"
            else:
                macos_version = "aarch64_macosx_11_0"
        include_path.append(macos_version)
    else:
        if machine_type in arch_map:
            include_path.append(arch_map[machine_type])

    include_path = os.path.join(*include_path)

    # Map current platform to the correct shared library file name
    platform_to_lib = {
        "Darwin": "libop_uniffi_core.dylib",
        "Linux": "libop_uniffi_core.so",
        "Windows": "op_uniffi_core.dll",
    }
    c_shared_library_file_name = platform_to_lib.get(platform_name, "")
    c_shared_library_file_name = os.path.join(include_path, c_shared_library_file_name)

    uniffi_bindings_file_name = "op_uniffi_core.py"
    uniffi_bindings_file_name = os.path.join(include_path, uniffi_bindings_file_name)
    return [c_shared_library_file_name, uniffi_bindings_file_name]

setup(
    packages=find_packages(
        where="src",
    ),
    distclass=BinaryDistribution,
    package_dir={"": "src"},
    cmdclass={"bdist_wheel": bdist_wheel},
    package_data={"": get_shared_library_data_to_include()},
)
