#
# spec file for package SFEjam.spec
#
# includes module(s): jam
#
%include Solaris.inc

%define src_name	jam
%define src_url		ftp://ftp.perforce.com/jam

Name:                   SFEjam
IPS_Package_Name:	developer/build/jam
Summary:                make-like program
Version:                2.5
License:                jam License
SUNW_Copyright:         jam.copyright
URL:                    http://www.perforce.com/jam/jam.html
Source:                 %{src_url}/%{src_name}-%{version}.tar
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/jam
cp ./bin.solaris*/jam $RPM_BUILD_ROOT%{_bindir}
cp README *.html $RPM_BUILD_ROOT%{_datadir}/doc/jam


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/jam

%changelog
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thr Mar 17 2011 - Thomas Wagner
- simplify install bin.solaris*/ (failed on amd64)
* Thu Apr 08 2010 - Milan Jurik
- corrected path for x86 build
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- fix source url
* Sun May  6 2007 - dougs@truemail.co.th
- Fixed doc directory
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
