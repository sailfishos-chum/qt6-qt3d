%global  qt_version 6.7.2

Summary: Qt6 - Qt3D QML bindings and C++ APIs
Name:    qt6-qt3d
Version: 6.7.2
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

BuildRequires: clang
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt6-rpm-macros >= %{qt_version}
BuildRequires: qt6-qtbase-static >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtshadertools-devel
BuildRequires: qt6-qtimageformats
%if 0%{?fedora} && 0%{?fedora} >= 40
%global bundled_assimp 0
BuildRequires: pkgconfig(assimp) >= 3.3.1
%else
%global bundled_assimp 1
%endif
Requires: qt6-qtimageformats%{?_isa} >= %{qt_version}

%description
Qt 3D provides functionality for near-realtime simulation systems with
support for 2D and 3D rendering in both Qt C++ and Qt Quick applications).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF \
  -DQT_FEATURE_qt3d_system_assimp=OFF

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt6_libdir}/libQt63DAnimation.so.6*
%{_qt6_libdir}/libQt63DCore.so.6*
%{_qt6_libdir}/libQt63DExtras.so.6*
%{_qt6_libdir}/libQt63DInput.so.6*
%{_qt6_libdir}/libQt63DLogic.so.6*
%{_qt6_libdir}/libQt63DQuick.so.6*
%{_qt6_libdir}/libQt63DQuickAnimation.so.6*
%{_qt6_libdir}/libQt63DQuickExtras.so.6*
%{_qt6_libdir}/libQt63DQuickInput.so.6*
%{_qt6_libdir}/libQt63DQuickRender.so.6*
%{_qt6_libdir}/libQt63DQuickScene2D.so.6*
%{_qt6_libdir}/libQt63DRender.so.6*
%{_qt6_plugindir}/geometryloaders/
%{_qt6_plugindir}/renderers/
%{_qt6_plugindir}/renderplugins/
%{_qt6_plugindir}/sceneparsers/
%{_qt6_qmldir}/Qt3D/
%{_qt6_qmldir}/QtQuick/Scene2D/
%{_qt6_qmldir}/QtQuick/Scene3D/

%files devel
%dir %{_qt6_libdir}/cmake/Qt63DAnimation
%dir %{_qt6_libdir}/cmake/Qt63DCore/
%dir %{_qt6_libdir}/cmake/Qt63DExtras
%dir %{_qt6_libdir}/cmake/Qt63DInput
%dir %{_qt6_libdir}/cmake/Qt63DLogic
%dir %{_qt6_libdir}/cmake/Qt63DQuick
%dir %{_qt6_libdir}/cmake/Qt63DQuickAnimation
%dir %{_qt6_libdir}/cmake/Qt63DQuickExtras
%dir %{_qt6_libdir}/cmake/Qt63DQuickInput
%dir %{_qt6_libdir}/cmake/Qt63DQuickRender/
%dir %{_qt6_libdir}/cmake/Qt63DQuickScene2D
%dir %{_qt6_libdir}/cmake/Qt63DRender/
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_includedir}/Qt3DAnimation
%{_qt6_includedir}/Qt3DCore/
%{_qt6_includedir}/Qt3DExtras
%{_qt6_includedir}/Qt3DInput/
%{_qt6_includedir}/Qt3DLogic/
%{_qt6_includedir}/Qt3DQuick
%{_qt6_includedir}/Qt3DQuickAnimation
%{_qt6_includedir}/Qt3DQuickExtras
%{_qt6_includedir}/Qt3DQuickInput/
%{_qt6_includedir}/Qt3DQuickRender/
%{_qt6_includedir}/Qt3DQuickScene2D
%{_qt6_includedir}/Qt3DRender/
%{_qt6_libdir}/cmake/Qt6/FindWrapQt3DAssimp.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/Qt3DTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt63DAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt63DCore/*.cmake
%{_qt6_libdir}/cmake/Qt63DExtras/*.cmake
%{_qt6_libdir}/cmake/Qt63DInput/*.cmake
%{_qt6_libdir}/cmake/Qt63DLogic/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuick/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickExtras/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickInput/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickRender/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickScene2D/*.cmake
%{_qt6_libdir}/cmake/Qt63DRender/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/libQt63DAnimation.prl
%{_qt6_libdir}/libQt63DAnimation.so
%{_qt6_libdir}/libQt63DCore.prl
%{_qt6_libdir}/libQt63DCore.so
%{_qt6_libdir}/libQt63DExtras.prl
%{_qt6_libdir}/libQt63DExtras.so
%{_qt6_libdir}/libQt63DInput.prl
%{_qt6_libdir}/libQt63DInput.so
%{_qt6_libdir}/libQt63DLogic.prl
%{_qt6_libdir}/libQt63DLogic.so
%{_qt6_libdir}/libQt63DQuick.prl
%{_qt6_libdir}/libQt63DQuick.so
%{_qt6_libdir}/libQt63DQuickAnimation.prl
%{_qt6_libdir}/libQt63DQuickAnimation.so
%{_qt6_libdir}/libQt63DQuickExtras.prl
%{_qt6_libdir}/libQt63DQuickExtras.so
%{_qt6_libdir}/libQt63DQuickInput.prl
%{_qt6_libdir}/libQt63DQuickInput.so
%{_qt6_libdir}/libQt63DQuickRender.prl
%{_qt6_libdir}/libQt63DQuickRender.so
%{_qt6_libdir}/libQt63DQuickScene2D.prl
%{_qt6_libdir}/libQt63DQuickScene2D.so
%{_qt6_libdir}/libQt63DRender.prl
%{_qt6_libdir}/libQt63DRender.so
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
