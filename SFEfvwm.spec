#
# spec file for package SFEfvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%include base.inc
%use fvwm = fvwm.spec

Name:                   SFEfvwm
Summary:                %{fvwm.summary}
Version:                %{fvwm.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnu-readline
Requires: SFElibstroke

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%fvwm.prep -d %name-%version/%{base_arch}

%build
%fvwm.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%fvwm.install -d %name-%version/%{base_arch}
(
  cd $RPM_BUILD_ROOT%{_datadir}/locale
  mv sv_SE sv
  ln -s sv sv_SE
)

%if %build_l10n
%else
rm -rf %{buildroot}%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%{_mandir}
%{_datadir}/fvwm

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Jul 11 2011 - Milan Jurik
- fix packaging
* Jul 2009 - dauphin@enst.fr
- SUNWreadline is in B117
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
