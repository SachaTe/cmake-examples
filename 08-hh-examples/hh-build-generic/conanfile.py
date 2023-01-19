from conans import CMake, ConanFile
from conans.errors import ConanInvalidConfiguration
import os


class CvEngine(ConanFile):
    name = "cv-engine"
    version = "1.14"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    options = {"build_type_override": "ANY", "enable_code_analysis": "ANY"}

    default_options = {"build_type_override": None, "enable_code_analysis": None}

    @property
    def _macos(self):
        return self.settings.os == "Macos"

    @property
    def _ios(self):
        return self.settings.os == "iOS"

    @property
    def _linux(self):
        return self.settings.os == "Linux" and self.settings.arch == "x86_64"

    @property
    def _ubuntu20(self):
        return (
            self.settings.os == "Linux"
            and self.settings.arch == "x86_64"
            and self.conf["user.distro"] == "ubuntu20.04"
        )

    @property
    def _android(self):
        return self.settings.os == "Android"

    @property
    def _mobile(self):
        return self._ios or self._android

    def _req_add(self, req, options=None):
        if options is None:
            options = {}

        self.requires.add(req)

        package = req.split("/")[0]

        for option, value in options.items():
            setattr(self.options[package], option, value)

    # wrapper around _req_add, to signal to the read that this dependency is
    # added for override reasons and is not directly consumed
    def _req_override(self, *args, **kwargs):
        return self._req_add(*args, **kwargs)

    def configure(self):
        if self._linux or self._macos:
            self.generators.append("cmake_find_package")

    def build_requirements(self):
        if self._linux:
            self.build_requires("patchelf/0.13")

    def requirements(self):
        self._req_add("fmt/9.1.0")

    def build(self):
        generator = {
            "iOS": "Xcode",
            "Macos": "Ninja",
            "Linux": {"x86_64": "Ninja", "armv8": "Unix Makefiles"}[
                str(self.settings.arch)
            ],
            "Android": "Unix Makefiles",
        }[str(self.settings.os)]

        cmake = CMake(self, generator=generator)

        # Generate compile_commands.json, for use with tooling such as clangd
        cmake.definitions["CMAKE_EXPORT_COMPILE_COMMANDS"] = True

        if self.options.build_type_override:
            self.output.info(
                f"Overriding build type with: {self.options.build_type_override}"
            )
            cmake.definitions["CMAKE_BUILD_TYPE"] = self.options.build_type_override

        if self.options.enable_code_analysis:
            cmake.definitions[
                "ENABLE_CODE_ANALYSIS"
            ] = self.options.enable_code_analysis

        # Choose inference framework
        if self._ios or self._macos:
            cmake.definitions["wrWITH_COREML"] = True
        elif not (self._android or self._linux):
            raise ConanInvalidConfiguration("Only iOS, macOS, Linux, Android supported")

        cmake.definitions["wrWITH_TFLITE"] = True

        if self._linux:
            cmake.definitions["pybind11_DIR"] = os.path.join(
                self.deps_cpp_info["pybind11"].rootpath, "share", "cmake", "pybind11"
            )

        cmake.configure()
        cmake.build()
