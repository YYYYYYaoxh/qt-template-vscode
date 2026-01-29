from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps


class QtTemplateRecipe(ConanFile):
    """
    Conan recipe for Qt Template project.
    
    This recipe manages third-party dependencies while Qt is handled
    externally via CMAKE_PREFIX_PATH or system installation.
    """

    name = "qt-template"
    version = "1.0.1"

    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        """
        Define project dependencies here.
        
        Examples:
            self.requires("fmt/10.2.1")
            self.requires("spdlog/1.13.0")
            self.requires("nlohmann_json/3.11.3")
            self.requires("gtest/1.14.0", visible=False)
        """
        self.requires("fmt/10.2.1")

    def build_requirements(self):
        """
        Define build-only dependencies here (tools, test frameworks, etc.)
        
        Examples:
            self.tool_requires("cmake/3.28.1")
            self.test_requires("gtest/1.14.0")
        """
        pass

    def layout(self):
        self.folders.build = "build"
        self.folders.generators = "build/generators"

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.user_presets_path = False
        tc.generate()
