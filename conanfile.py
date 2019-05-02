from conans import ConanFile, CMake, tools, errors
import os


class AppimagetoolinstallerConan(ConanFile):
    name = "appimagetool_installer"
    version = "11"
    license = "MIT"
    author = "Alexis Lopez Zubieta contact@azubieta.net"
    url = "https://github.com/appimage-conan-community/appimagetool_installer"
    description = "Package desktop applications as AppImages that run on common Linux-based operating systems, such as RHEL, CentOS, openSUSE, SLED, Ubuntu, Fedora, debian and derivatives."
    topics = ("AppImage", "Creation", "Tool")
    settings = "os", "compiler", "build_type", "arch"
    requires = ("zlib/1.2.11@conan/stable")
    keep_imports = True

    def configure(self):
        self.options["zlib"].shared = True

    def imports(self):
        self.copy("libz*.so*", src="lib", dst="squashfs-root/usr/lib")

    def build(self):
        if (self.settings.build_type != "Release"):
            raise errors.ConanInvalidConfiguration("Only Release builds are supported.")

        if (self.settings.arch == "x86" or self.settings.arch == "x86_64"):
            # match the arch naming convention used in AppImageKit
            appimagetool_arch_name = "i686" if self.settings.arch == "x86" else self.settings.arch

            tools.download("https://github.com/AppImage/AppImageKit/releases/download/%s/appimagetool-%s.AppImage"
                           % (self.version, appimagetool_arch_name), "appimagetool-x86_64.AppImage")
        else:
            raise errors.ConanInvalidConfiguration("Unsuported arch: %s" % self.settings.arch)

        self.run("chmod +x appimagetool-x86_64.AppImage && ./appimagetool-x86_64.AppImage --appimage-extract",
                 run_environment=True)

    def package(self):
        self.copy("*", dst="", src="squashfs-root/usr")

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
