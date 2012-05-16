# TODO:
# - triggerin modifying /lib/udev/rules.d/60-persistent-storage.rules is big
#   NO, patch udev to include the change or make new .rule file
# - should libploop.so be SONAME versioned?
# - unbashism in *mount tools
Summary:	ploop tools
Name:		ploop
Version:	1.2
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://download.openvz.org/utils/ploop/%{version}/src/%{name}-%{version}.tar.bz2
BuildRequires:	libxml2-devel
Requires:	parted
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains tools to work with ploop devices and images.

%package libs
Summary:	ploop library
Group:		Libraries
Obsoletes:	ploop-lib

%description libs
Parallels loopback (ploop) block device API library.

%package devel
Summary:	header files for ploop library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Headers ploop library.

%prep
%setup -q

%build
%{__make} all \
	V=1 \
	CC="%{__cc}" \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	LIBDIR=%{_libdir} \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

# static not packaged
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libploop.a

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- udev
SCRIPT="/lib/udev/rules.d/60-persistent-storage.rules"
if [ -f $SCRIPT ]; then
	fgrep 'KERNEL=="ploop*", GOTO="persistent_storage_end"' $SCRIPT > /dev/null 2>&1 ||
	sed -i -e '1 s/^/KERNEL=="ploop*", GOTO="persistent_storage_end"\n/;' $SCRIPT
fi

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
