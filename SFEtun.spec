#
#
# spec file for package SFEtun
#
# includes module(s): tun
#
%include Solaris.inc
%define src_name tuntap
#%define src_url http://www.whiteboard.ne.jp/~admin2/tuntap/source/%{src_name}

#description of this download method:
#https://fedorahosted.org/fpc/attachment/ticket/233/slask

#tuntap
%define githubowner1  kaizawa
%define githubproject1 tuntap
#for github commits see link on the right with the shortened commitid on the Webpage
#  -> https://github.com/kaizawa/tuntap/commit/43816b1ac8b050e45a6f7882058755fe753a9992
%define commit1 43816b1ac8b050e45a6f7882058755fe753a9992
#remember to increas with every changed commit1 value
%define increment_version_helper 1
%define shortcommit1 %(c=%{commit1}; echo ${c:0:7})
#


%define usr_kernel /usr/kernel
%define drv_base %{usr_kernel}/drv

Name:		SFEtun
IPS_Package_Name:	system/network/tuntap
Summary:	Virtual Point-to-Point network device
URL:		http://www.whiteboard.ne.jp/~admin2/tuntap/
License:        GPLv2
SUNW_Copyright:	tuntap.copyright
Meta(info.upstream): Kazuyoshi Aizawa <admin2@whiteboard.ne.jp>
Version:        1.3.2.0.0.%{increment_version_helper}
Source:         http://github.com/%{githubowner1}/%{githubproject1}/archive/%{shortcommit1}/%{githubproject1}-%{commit1}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
tuntap is a TAP driver for Solaris that can be used for OpenVPN, OpenConnect,
and vpnc.

The code is based on the Universal TUN/TAP driver. Some changes were made and
code added for supporting Ethernet tunneling feature, since the Universal
TUN/TAP driver for Solaris only supports IP tunneling known as TUN.

Note: github checkout commit version %{shortcommit1} / %{commit1} 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n %{githubproject1}-%{commit1}

%build
export LD=/usr/bin/ld

autoconf -f
./configure
gsed -i -e 's/-melf_x86_64_sol2//' Makefile
make LD=$LD
%ifarch sparcv9 amd64
mv tun tun64
mv tap tap64
make clean
./configure --disable-64bit
make
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -D if_tun.h $RPM_BUILD_ROOT%{_includedir}/net/if_tun.h
install -D tun $RPM_BUILD_ROOT%{drv_base}/tun
install -D tap $RPM_BUILD_ROOT%{drv_base}/tap
%ifarch sparcv9 amd64
install -D tun64 $RPM_BUILD_ROOT%{drv_base}/%{_arch64}/tun
install -D tap64 $RPM_BUILD_ROOT%{drv_base}/%{_arch64}/tap
%endif
install -D tun.conf $RPM_BUILD_ROOT%{drv_base}/tun.conf
install -D tap.conf $RPM_BUILD_ROOT%{drv_base}/tap.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
( PATH=/usr/bin:/usr/sfw/bin; export PATH ;
  retval=0;
  /usr/sbin/add_drv tun || retval=1;
  [ "$retval" = 0 ] && /usr/sbin/add_drv tap || retval=1;
  exit $retval ) 

%preun
( echo PATH=/usr/bin:/usr/sfw/bin; export PATH ;
  /usr/sbin/rem_drv tun || retval=1;
  /usr/sbin/rem_drv tap || retval=1;
  exit 0
)

%actions
driver name=tun
driver name=tap

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/net
%{_includedir}/net/if_tun.h
%dir %attr (0755, root, sys) %{usr_kernel}
%dir %attr (0755, root, sys) %{drv_base}
%{drv_base}/tun
%{drv_base}/tap
%{drv_base}/tun.conf
%{drv_base}/tap.conf
%ifarch amd64 sparcv9
%dir %attr (0755, root, sys) %{drv_base}/%{_arch64}
%{drv_base}/%{_arch64}/tun
%{drv_base}/%{_arch64}/tap
%endif

%changelog
* Sun Jan 26 2014 - Thomas Wagner
- bump to 1.3.2 github 43816b1ac8 / 43816b1ac8b050e45a6f7882058755fe753a9992
- change Source to github checkout to get current code, fixes Solaris 11 compile (undefined symbol: ddi_power)
- gitbug checkout to solve unversioned tarball name which never gets updates once downloaded
- set LD=/usr/bin/ld , edit Makefile to not use -melf_x86_64_sol2
* Sat Aug  3 2013 - Thomas Wagner
- bump to 1.3.2
* Thu Oct 06 2011 - Milan Jurik
- add IPS package name
* Fri Jul 29 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Wed May 12 2010 - Milan Jurik
- update according the latest upstream
- IPS support added
* Wed Oct  3 2007 - Doug Scott
- Added base spec
- Updated to build tap from latest source
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
