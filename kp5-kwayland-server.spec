#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# wayland-scanner from wayland project
#
%define		kdeplasmaver	5.24.5
%define		qtver		5.15.2
%define		kpname		kwayland-server

Summary:	Qt-style Client and Server library wrapper for the Wayland libraries
Name:		kp5-%{kpname}
Version:	5.24.5
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	598ae49b82277a94c5b35ac2b22f2cee
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5WaylandClient-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-kwindowsystem-devel >= 5.82.0
BuildRequires:	kf5-plasma-wayland-protocols-devel >= 1.6.0
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	wayland-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
Qt-style Client and Server library wrapper for the Wayland libraries.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories5/kwaylandserver.categories
%ghost %{_libdir}/libKWaylandServer.so.5
%attr(755,root,root) %{_libdir}/libKWaylandServer.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/kwaylandserver_version.h
%dir %{_includedir}/KWaylandServer
%{_includedir}/KWaylandServer/*.h
%dir %{_libdir}/cmake/KWaylandServer
%{_libdir}/cmake/KWaylandServer/KWaylandServerConfig.cmake
%{_libdir}/cmake/KWaylandServer/KWaylandServerConfigVersion.cmake
%{_libdir}/cmake/KWaylandServer/KWaylandServerTargets-pld.cmake
%{_libdir}/cmake/KWaylandServer/KWaylandServerTargets.cmake
%{_libdir}/libKWaylandServer.so
