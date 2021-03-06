#
#
# spec file for package SFEfusefs
#
# includes module(s): fusefs
#
%include Solaris.inc
%include packagenamemacros.inc

%define src_name fusefs
%define src_url http://sfe.opencsw.org/files
%define tarball_version	20100615

%define usr_kernel /usr/kernel
%define drv_base %{usr_kernel}/drv

Name:		SFEfusefs
IPS_Package_Name:	system/file-system/fusefs
Summary:	File system in User Space (/usr/gnu)
Version:	0.%{tarball_version}.2
License:	CDDL and BSD
Group:		System/File System
SUNW_Copyright:	fusefs.copyright
#is gone! URL:		http://hub.opensolaris.org/bin/view/Project+fuse/
Source:		%{src_url}/%{src_name}-%{tarball_version}.tgz
Patch1:		fuse-01-jean-pierre.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWonbld}

%description
FUSE stands for 'File system in User Space'. It provides a simple
interface to allow implementation of a fully functional file system
in user-space.  FUSE originates from the Linux community and is
included in the Linux kernel (2.6.14+).

%prep
%setup -q -n %{src_name}
%patch1 -p1

%build
export PATH=/opt/onbld/bin/`uname -p`:$PATH
cd kernel
/usr/ccs/bin/make

%install
rm -rf $RPM_BUILD_ROOT
cd kernel
/usr/ccs/bin/make install

cp -r proto/ $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( retval=0; 
  /usr/sbin/add_drv -m 'fuse 0666 root sys' fuse || retval=1;
  [ "$retval" = 0 ] && ln -s /devices/pseudo/fuse@0:fuse /dev/fuse || retval=1;
  exit $retval
)

%preun
( retval=0;
  /usr/sbin/rem_drv fuse || retval=1;
  [ "$retval" = 0 ] && rm /dev/fuse || retval=1;
  exit $retval
)

%actions
driver name=fuse devlink=type=ddi_pseudo;name=fuse\t\D perms="* 0666 root sys"

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{usr_kernel}
%dir %attr (0755, root, sys) %{drv_base}
%{drv_base}/fuse
%{drv_base}/fuse.conf
%ifarch amd64 sparcv9
%dir %attr (0755, root, sys) %{drv_base}/%{_arch64}
%{drv_base}/%{_arch64}/fuse
%endif

%changelog
* Wed Jan 30 2014 - Thomas Wagner
- change to (Build)Requires: %{pnm_buildrequires_SUNWonbld}, #include packagenamemacros.inc
* Thu Jun 20 2013 - Thomas Wagner
- new download url
* Fri Aug 31 2012 - Milan Jurik
- bump version with new patch from Jean-Pierre Andre 
* Sat Jan 28 2012 - Milan Jurik
- add patches from Jean-Pierre Andre 
* Fri Nov 04 2011 - Guido Berhoerster <gber@openindiana.org>
- fixed driver action to create devlinks entry
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jul 07 2011 - Alex Viskovatoff
- Revert previous change: source file does not get found
* Mon Jun 06 2011 - Ken Mays <kmays2000@igmail.com>
- Bumped to 2.8.5
* Sat Jun 19 2010 - Milan Jurik
- Initial spec
