#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEprtpci
License:             CDDL
Summary:             A tool for summarizing PCI information from prtconf output
Version:             1.11
Patch1:              prtpci-01-etc.diff

URL:                 http://blogs.sun.com/dmick/entry/prtpci_digest_and_display_prtconf
Source:              http://playground.sun.com/pub/dmick/prtpci.tar.Z
Source1:             http://pciids.sourceforge.net/pci.ids

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc
Requires: SUNWcsr

%package root
Summary:        %{name} - / filesystem
SUNW_BaseDir:   /
%include default-depend.inc

%prep
rm -rf prtpci
mkdir prtpci
cd prtpci
uncompress -c %{SOURCE} | tar xvf - 
%patch1 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT

cd prtpci
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/pciids

cp prtpci ${RPM_BUILD_ROOT}%{_bindir}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/prtpci
cp pciids/* ${RPM_BUILD_ROOT}%{_sysconfdir}/pciids
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/pciids/pci.ids

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Wed Feb 23 2011 - Milan Jurik
- fix packaging
* Mon Feb 04 2008 - moinak.ghosh@sun.com
- Initial spec.
