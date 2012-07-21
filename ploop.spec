# TODO:
# - triggerin modifying /lib/udev/rules.d/60-persistent-storage.rules is big
#   NO, patch udev to include the change or make new .rule file
# - should libploop.so be SONAME versioned?
# - unbashism in *mount tools
Summary:	Tools for ploop devices and images
Summary(pl.UTF-8):	Narzędzia do urządzeń i obrazów ploop
Name:		ploop
Version:	1.4
Release:	0.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://download.openvz.org/utils/ploop/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	f8ff18050ffad9b44361f36bb29970aa
URL:		http://wiki.openvz.org/Ploop
BuildRequires:	libxml2-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	parted
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

%{__sed} -i -e 's,-O2,%{rpmcflags} %{rpmcppflags},' Makefile.inc

%build
%{__make} all \
	V=1 \
	DEBUG=no \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags} -L$(pwd)/lib" \
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

%files
%defattr(644,root,root,755)
%doc tools/README
%attr(755,root,root) /sbin/mount.ploop
%attr(755,root,root) /sbin/umount.ploop
%attr(755,root,root) %{_sbindir}/ploop
%attr(755,root,root) %{_sbindir}/ploop-balloon
%attr(755,root,root) %{_sbindir}/ploop-copy
%attr(755,root,root) %{_sbindir}/ploop-fsck
%attr(755,root,root) %{_sbindir}/ploop-grow
%attr(755,root,root) %{_sbindir}/ploop-merge
%attr(755,root,root) %{_sbindir}/ploop-stat

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libploop.so
%dir /var/lock/ploop

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/ploop
%{_includedir}/ploop/libploop.h
%{_includedir}/ploop/ploop1_image.h
%{_includedir}/ploop/ploop_if.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libploop.a
