#
# spec file for package SFEafterstep.spec
#
# includes module(s): afterstep
#
%include Solaris.inc
%include packagenamemacros.inc

%include base.inc
%use afterstep = afterstep.spec

Name:                   SFEafterstep
Summary:                %{afterstep.summary}
Version:                %{afterstep.version}
SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:         %{name}.copyright
Group:			Graphics
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEfltk
BuildRequires:  %{pnm_buildrequires_library_readline}
Requires:       %{pnm_requires_library_readline}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%afterstep.prep -d %name-%version/%{base_arch}

%build
export CC=/usr/sfw/bin/gcc
%afterstep.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%afterstep.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/afterstep
%{_datadir}/afterstep_old
%{_datadir}/xsessions

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sat Dec 15 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_library_readline}, %include packagenamemacros.inc
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add licensing and grouping.
* Sat Apr 28 2007 - dougs@truemail.co.th
- Initial version
