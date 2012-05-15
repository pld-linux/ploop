%define _incdir /usr/include/ploop
%define rel 1
Summary:	ploop tools
Name:		ploop
Version:	1.2
Release:	%{rel}%{?dist}
License:	GNU GPL
Group:		Applications/System
Source0:	http://download.openvz.org/utils/ploop/1.2/src/%{name}-%{version}.tar.bz2
BuildRequires:	libxml2-devel
Requires:	parted
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains tools to work with ploop devices and images.

%prep
%setup -q

%build
%{__make} LIBDIR=%{_libdir} all

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sbindir}
%{__make} DESTDIR=$RPM_BUILD_ROOT LIBDIR=%{_libdir} install

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
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_sbindir}/ploop
%attr(755,root,root) %{_sbindir}/ploop-*

%package lib
Summary:	ploop library
Group:		Applications/System
Requires:	libxml2

%description lib
Parallels loopback (ploop) block device API library

%files lib
%defattr(644,root,root,755)
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/libploop.so
%dir /var/lock/ploop

%package devel
Summary: Devel files for ploop
Group:		Applications/System
%description devel
Headers and a static version of ploop library

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}
%dir %{_incdir}
%{_libdir}/libploop.a
%{_incdir}/libploop.h
%{_incdir}/ploop_if.h
%{_incdir}/ploop1_image.h
