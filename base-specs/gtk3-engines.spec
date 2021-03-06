#
# spec file for package gtk3-engines
#
# Copyright (c) 2011, 2012, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner erwannc
#

%define OSR LFI#105446 (gnome Exec. summary):n/a

Name:         gtk3-engines
License:      LGPL v2.1
Group:        System/GUI/GNOME
Version:      2.91.1
Release:      1
Distribution: Java Desktop System
Vendor:	      Gnome Community
Summary:      Engines for GTK2 Themes
Source:       http://ftp.gnome.org/pub/GNOME/sources/gtk-engines/2.91/gtk-engines-%{version}.tar.bz2
# date:2011-07-14 owner:yippi type:feature bugzilla:654719
URL:          http://www.gnome.org
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define       gtk2_version 2.4.0

BuildRequires: gtk2-devel >= %{gtk2_version}
Requires:      gtk2 >= %{gtk2_version}

%description
This packages contains Theme-Engine libraries for GTK2

%prep
%setup -q -n gtk-engines-%{version}

%build
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
./configure --prefix=%{_prefix}		\
	    --libdir=%{_libdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Clean up unpackaged files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm {} \;
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/gtk-3.0/*/engines/*.so
%{_datadir}/themes/*
%{_libdir}/pkgconfig/*.pc

%changelog -n gtk2-engines
* Fri May 11 2012 - brian.cameron@oracle.com
- Add -lm to LDFLAGS.
* Thu Jul 07 2011 - brian.cameron@oracle.com
- Created with 2.91.1.

