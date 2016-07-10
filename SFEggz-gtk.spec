#
# spec file for package SFEggz-gtk
#
# includes module(s): ggz-gtk-client
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use ggzgtk = ggz-gtk-client.spec

Name:               SFEggz-gtk
IPS_Package_Name:	games/library/ggz-gtk
Summary:            ggz-gtk - Gtk+ client libraries for GGZ gaming zone
Version:            %{ggzgtk.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-common-devel
BuildRequires:	SFElibggz_devel
Requires:	SFElibggz

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ggzgtk.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%ggzgtk.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%ggzgtk.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ggz-gtk
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/ggz
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/ggz-*.h

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Dec  8 2013 - Thomas Wagner
- change BuildRequires: to %{pnm_buildrequires_SFElibggz_devel} (S11, S12 has none, OI has)
* Fri Nov 15 2013 - Thomas Wagner
- require always SFElibggz as S11 has none
* Sun Oct  3 2013 - Thomas Wagner
- change (Build)Requires to pnm_buildrequires_SUNWgnome_games_devel, %include packagenamemacros.inc
* Tue Jan 15 2009 - halton.huo@sun.com
- Initial version
