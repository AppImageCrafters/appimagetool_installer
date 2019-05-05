import os

from conans import ConanFile, CMake, tools


class AppimagetoolinstallerTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = ("appimage.svg", "org.appimagecraft.TestApp.desktop")
    # build_requires = ("cmake_installer/3.10.0@conan/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.build_folder + "/AppDir"
        cmake.configure()
        cmake.build(target="install")

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("appimagetool %s" % (self.build_folder + "/AppDir"), run_environment=True)
            self.run(self.build_folder + "/Test_App-x86_64.AppImage --appimage-extract-and-run")
