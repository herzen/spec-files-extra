#
# spec file for package SFElibchamplain
#
# includes module(s): libchamplain
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby
#

%include Solaris.inc

%use libchamplain = libchamplain.spec

Name:               SFElibchamplain
Summary:            libchamplain - a Clutter based widget to display rich, eye-candy and interactive maps
#SUNW_Copyright:     %{name}.copyright
License:            LGPLv2
Version:            %{libchamplain.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWclutter
BuildRequires:      SUNWclutter-devel
Requires:           SUNWclutter-gtk
BuildRequires:      SUNWclutter-gtk-devel
BuildRequires:      SUNWgobject-introspection 
BuildRequires:      SUNWvala-devel
Requires:           SUNWvala
BuildRequires:      SFEmemphis-devel
Requires:           SFEmemphis

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libchamplain.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%libchamplain.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libchamplain.install -d %name-%version

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d libchamplain-%{libchamplain.version} README AUTHORS INSTALL NEWS
%doc(bzip2) -d libchamplain-%{libchamplain.version} ChangeLog COPYING  
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gir*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir*
%{_datadir}/vala

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%changelog
* Fri Jan 07 2011 - Milan Jurik
- missing deps added
* Mon Jan 02 2010 - yuntong.jin@sun.com
- Add doc like copyright file etc and licence info  
* Wed Aug 05 2009 - halton.huo@sun.com
- Initial spec
