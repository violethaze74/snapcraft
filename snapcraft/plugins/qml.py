# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import snapcraft.common

from snapcraft.plugins.ubuntu import UbuntuPlugin


class QmlPlugin(snapcraft.BasePlugin):

    def __init__(self, name, options):
        options.package = None
        super().__init__(name, options)

        class QmlPackageOptions:
            package = ["qmlscene", "qtdeclarative5-qtmir-plugin", "mir-graphics-drivers-desktop", "qtubuntu-desktop"]
            recommends = False

        self.ubuntu = UbuntuPlugin(name, QmlPackageOptions())

    def pull(self):
        return self.ubuntu.pull()

    def snap_files(self):
        include, exclude = self.ubuntu.snap_files()
        # print("Snap files '" + ", ".join(include) + "', '" + ", ".join(exclude) + "'")
        return (include, exclude)

    def build(self):
        return self.ubuntu.build()

    def env(self, root):
        arch = 'x86_64-linux-gnu' # TODO figure this out
        envs = self.ubuntu.env(root)
        envs.extend([
            # Mir config
            "MIR_SOCKET=/run/mir_socket",
            "MIR_CLIENT_PLATFORM_PATH=%s/usr/lib/%s/mir/client-platform" % (root, arch),
            # Qt Platform to Mir
            "QT_QPA_PLATFORM=ubuntumirclient",
            "QTCHOOSER_NO_GLOBAL_DIR=1",
            # Qt Libs
            "LD_LIBRARY_PATH=%s/usr/lib/%s/qt5/libs:$LD_LIBRARY_PATH" % (root, arch),
            "LD_LIBRARY_PATH=%s/usr/lib/%s/pulseaudio:$LD_LIBRARY_PATH" % (root, arch),
            # Qt Modules
            "QT_PLUGIN_PATH=%s/usr/lib/%s/qt5/plugins" % (root, arch),
            "QML2_IMPORT_PATH=%s/usr/lib/%s/qt5/qml" % (root, arch),
            # Mesa Libs
            "LD_LIBRARY_PATH=%s/usr/lib/%s/mesa:$LD_LIBRARY_PATH" % (root, arch),
            "LD_LIBRARY_PATH=%s/usr/lib/%s/mesa-egl:$LD_LIBRARY_PATH" % (root, arch),
            # XDG Config
            "XDG_CONFIG_DIRS=%s/usr/xdg:/etc/xdg:$XDG_CONFIG_DIRS" % root
        ])
        return envs

