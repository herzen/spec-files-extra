#
# spec file for package clutter-gtk
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

Summary:      clutter-gtk - GTK+ integration library for clutter
Name:         clutter-gtk
Version:      0.9.0
Release:      1
License:      GPL
Group:        System/Libraries
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Source:	  http://www.clutter-project.org/sources/clutter-gtk/0.9/clutter-gtk-%{version}.tar.bz2
# Patch taken from here:
# http://bugzilla.o-hand.com/show_bug.cgi?id=1490
Patch1:                  clutter-gtk9-01-introspection.diff
URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n clutter-gtk-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
./configure --prefix=%{_prefix}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove gtk docs since they are installed with the 0.8 package.
rm -fR $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*


%changelog
* Tue May 12 2009  brian.cameron@sun.com
- Created.


