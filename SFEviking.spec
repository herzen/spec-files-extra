#
# spec file for package SFEviking
#
# includes module(s): viking
#

%include Solaris.inc
Name:		SFEviking
License:	GPL v2
Group:		Applications
Summary:	GPS Viewer
Version:	1.1
URL:		http://viking.sf.net
Source:		%{sf_download}/project/viking/viking/%{version}/viking-%{version}.tar.gz
License:	GPLv2
Patch1:		viking-01-return.diff
Patch2:		viking-02-wall.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:	viking.copyright
SUNW_BaseDir:	%{_basedir}

%include default-depend.inc
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWgnome-doc-utils
BuildRequires:	SUNWlxsl
BuildRequires:	SUNWgawk
BuildRequires:	library/perl-5/xml-parser
BuildRequires:	SUNWcurl
Requires:	SUNWcurl
BuildRequires:	SFEgpsd-devel
Requires:	SFEgpsd

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n viking-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} 

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if %build_l10n
%else
rm -rf %{buildroot}%{_datadir}/locale
%endif


%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/viking.desktop
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/viking.png
%{_mandir}
%{_datadir}/omf/viking/viking-C.omf
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_localedir}
%endif

%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- add SUNW_Copyright
* Fri Feb 11 2011 - Milan Jurik
- bump to 1.1
* Sat Jan 15 2011 - Milan Jurik
- initial spec
