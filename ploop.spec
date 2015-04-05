Summary:	Tools for ploop devices and images
Summary(pl.UTF-8):	Narzędzia do urządzeń i obrazów ploop
Name:		ploop
Version:	1.12.2
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://download.openvz.org/utils/ploop/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	75ddd6a972a531a1555d21572092a69d
URL:		http://wiki.openvz.org/Ploop
BuildRequires:	libxml2-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	/sbin/modprobe
Requires:	awk
Requires:	parted
Requires:	sed
Requires:	udev-core >= 1:182-6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains tools to work with ploop devices and images.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia do pracy z urządzeniami o obrazami ploop.

%package libs
Summary:	ploop library
Summary(pl.UTF-8):	Biblioteka ploop
Group:		Libraries
Obsoletes:	ploop-lib

%description libs
Parallels loopback (ploop) block device API library.

%description libs -l pl.UTF-8
Biblioteka do obsługi urządzeń blokowych ploop (Parallels loopback).

%package devel
Summary:	Header files for ploop library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ploop
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for ploop library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ploop.

%package static
Summary:	Static ploop library
Summary(pl.UTF-8):	Biblioteka statyczna ploop
Group:		Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ploop library.

%description static -l pl.UTF-8
Biblioteka statyczna ploop.

%prep
%setup -q

%build
LDFLAGS="%{rpmldflags}" \
LDLIBS="-lpthread" \
%{__make} all \
	V=1 \
	DEBUG= \
	CC="%{__cc}" \
	CPPFLAGS="%{rpmcppflags}" \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	V=1 \
	INSTALL="install -p" \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc tools/README
%attr(755,root,root) /sbin/mount.ploop
%attr(755,root,root) /sbin/umount.ploop
%attr(755,root,root) %{_sbindir}/ploop
%attr(755,root,root) %{_sbindir}/ploop-balloon
%{_mandir}/man8/ploop.8*
%{systemdtmpfilesdir}/ploop.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libploop.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libploop.so.1
%dir /var/lock/ploop

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libploop.so
%dir %{_includedir}/ploop
%{_includedir}/ploop/libploop.h
%{_includedir}/ploop/dynload.h
%{_includedir}/ploop/ploop1_image.h
%{_includedir}/ploop/ploop_if.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libploop.a
