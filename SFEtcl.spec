#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define _basedir /usr/gnu

Name:                SFEtcl
IPS_Package_Name:    runtime/tcl-85
Summary:             Tcl - Tool Command Language
Version:             8.5.11
Source:              %{sf_download}/tcl/tcl%{version}-src.tar.gz
SUNW_Copyright:      %{name}.copyright

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWcakr
Requires: SUNWckr
Requires: SUNWcnetr
Requires: SUNWlibms
Requires: SUNWgcmn

%package devel
Summary: %{summary} - development files
SUNW_BaseDir:        %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n tcl%version/unix

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	    --enable-shared \
	    --enable-threads

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-private-headers DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/tclConfig.sh
%{_libdir}/libtcl*
%dir %attr (0755, root, bin) %{_libdir}/tcl8
%{_libdir}/tcl8/*
%dir %attr (0755, root, bin) %{_libdir}/tcl8.5
%{_libdir}/tcl8.5/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, bin) %{_mandir}/mann
%{_mandir}/man1/*
%{_mandir}/mann/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thu Apr 26 2012 - Logan Bruns <logan@gedanken.org>
- Bump to 8.5.11. 
- Set IPS name to tcl-85 and moved to /usr/gnu to avoid conflict with OS provided package. 
- Switched to gcc to avoid needing to pull in sunmath which can cause
  problems for gcc compiled packages linking against IPS.
- Added copyright file.
* Tue Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 8.5.10
* Tue Jun 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 8.5.9
* Sun Nov 18 2007 - shivakumar.gn@gmail.com
- The -devel package needs to install private headers as well
- Most tcl extensions(iTcl) cannot be built without these headers.
* Sat Sep 29 2007 - dick@nagual.nl
- Bumped to version 8.4.16
* Wed Jul 11 2007 - dick@nagual.nl
- Bumped to version 8.4.15
* Sun Jun 03 2007 - dick@nagual.nl
- Corrected the location of the mann directory
* Mon May 28 2007 - dick@nagual.nl
- Initial spec
