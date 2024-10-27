Summary:	Tools for ploop devices and images
Summary(pl.UTF-8):	Narzędzia do urządzeń i obrazów ploop
Name:		ploop
Version:	9.0.30
Release:	1
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/OpenVZ/ploop/tags
Source0:	https://github.com/OpenVZ/ploop/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8d4f8666f2841f0a4a9686c9ef2e338c
Patch0:		%{name}-python.patch
Patch1:		no-Werror.patch
Patch2:		%{name}-glibc.patch
URL:		https://wiki.openvz.org/Ploop
BuildRequires:	device-mapper-devel
BuildRequires:	glibc-devel >= 6:2.36
BuildRequires:	json-c-devel
BuildRequires:	libblkid-devel
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpmbuild(macros) >= 1.673
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

%package -n bash-completion-ploop
Summary:	Bash completion for ploop commands
Summary(pl.UTF-8):	Bashowe dopełnianie składni poleceń ploop
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-ploop
Bash completion for ploop commands.

%description -n bash-completion-ploop -l pl.UTF-8
Bashowe dopełnianie składni poleceń ploop.

%package libs
Summary:	ploop library
Summary(pl.UTF-8):	Biblioteka ploop
Group:		Libraries
Obsoletes:	ploop-lib < 1.4

%description libs
Parallels loopback (ploop) block device API library.

%description libs -l pl.UTF-8
Biblioteka do obsługi urządzeń blokowych ploop (Parallels loopback).

%package devel
Summary:	Header files for ploop library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ploop
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libxml2-devel >= 2.0

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

%package -n python3-libploop
Summary:	Python 3 interface to ploop library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki ploop
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-libploop
Python 3 interface to ploop library.

%description -n python3-libploop -l pl.UTF-8
Interfejs Pythona 3 do biblioteki ploop.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# honour %{_libexecdir} whatever it's set to
%{__sed} -i -e '/exe = / s,/usr/libexec,%{_libexecdir},' scripts/crypthelper
%{__sed} -i -e '/define CRYPT_BIN/ s,/usr/libexec,%{_libexecdir},' lib/crypt.c
# drop /usr/libexec/{tune,resize,dumpe}2fs from tools search
%{__sed} -i -e '/\/usr\/libexec\/.*2fs/d' lib/fsutils.c

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
	COMPLETIONDIR=%{bash_compdir} \
	LIBDIR=%{_libdir} \
	LIBSCRIPTDIR=%{_libexecdir}/ploop \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_sbindir}/ploop-test
%{__rm} -r $RPM_BUILD_ROOT/usr/libexec/ploop-test

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

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
%attr(755,root,root) %{_sbindir}/ploop-cbt
%attr(755,root,root) %{_sbindir}/ploop-volume
%attr(755,root,root) %{_sbindir}/ploop-e4defrag
%dir %{_libexecdir}/ploop
%attr(755,root,root) %{_libexecdir}/ploop/crypthelper
/etc/modules-load.d/ploop.conf
%dir /var/lock/ploop
%{systemdtmpfilesdir}/ploop.conf
%{_mandir}/man8/ploop.8*

%files -n bash-completion-ploop
%defattr(644,root,root,755)
%{bash_compdir}/ploop

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libploop.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libploop.so.9
%dir /var/lock/ploop

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libploop.so
%{_includedir}/ploop
%{_pkgconfigdir}/ploop.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libploop.a

%files -n python3-libploop
%defattr(644,root,root,755)
%dir %{py3_sitedir}/libploop
%attr(755,root,root) %{py3_sitedir}/libploop/libploopapi.cpython-*.so
%{py3_sitedir}/libploop/__init__.py
%{py3_sitedir}/libploop/__pycache__
%{py3_sitedir}/libploop-0.0.0-py*.egg-info
