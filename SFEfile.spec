#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%include usr-gnu.inc
%include base.inc

Name:		SFEfile
IPS_Package_Name:	file/file
Summary:	determine file type (/usr/gnu)
Version:	5.25
Group:		Applications/System Utilities
License:	BSD3c
SUNW_Copyright:	file.copyright
Source:		ftp://ftp.astron.com/pub/file/file-%version.tar.gz

SUNW_BaseDir:        %{_basedir}
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_library_zlib}
Requires:      %{pnm_requires_library_zlib}

%prep
%setup -q -n file-%version

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rmdir ${RPM_BUILD_ROOT}%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/misc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr (0755, root, bin) %{_mandir}/man4
%{_mandir}/man4/*.4

%changelog
* Tue Jan  5 2016 - Alex Viskovatoff
- bump to 5.25
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Fri Jan  2 2015 - Thomas Wagner
- bump to 5.21
- add dependencies
* Sun Feb 16 2014 - Alex Viskovatoff
- bump to 5.17
* Sun Aug 05 2012 - Milan Jurik
- bump to 5.11
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Mon Jun 6 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 5.07
* Fri Apr 15 2011 - Alex Viskovatoff
- Bump to 5.06
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Bump to 5.04
* Tue Oct 22 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 4.26
* Sat Jul 15 2007 - dougs@truemail.co.th
- Bump to 4.21
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Bump to 4.20.
- Add patch file-01-REG_STARTEND.diff, get original copy from
  ftp://ftp.astron.com/pub/file/patch-4.20-REG_STARTEND
* Mon Jan 15 2007 - laca@sun.com
- bump to 4.19
* Tue Nov 07 2006 - Eric Boutilier
- Initial spec
