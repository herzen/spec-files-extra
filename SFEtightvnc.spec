#
# spec file for package SFEtightvnc
#
# includes module(s): tightvnc
#
%include Solaris.inc

Name:                    SFEtightvnc
Summary:                 tightvnc - remote control software package derived from the popular VNC software
Version:                 1.3.8
Source:                  http://mesh.dl.sourceforge.net/sourceforge/vnc-tight/tightvnc-%{version}_unixsrc.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWjpg
Requires: SUNWlibmsr
Requires: SUNWperl584core
Requires: SUNWxwplt
Requires: SUNWzlib
BuildRequires: SUNWxwopt

%package -n SFEvncviewer
Summary:                 vncviewer - a vnc client from tightvnc
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWjpg
Requires: SUNWlibmsr
Requires: SUNWxwplt
Requires: SUNWzlib

%prep
%setup -q -n vnc_unixsrc

#correct cc path
cp ./Xvnc/config/cf/sun.cf ./Xvnc/config/cf/sun.cf.orig
export cc_dir=`dirname $CC`
echo $cc_dir|sed 's/\//\\\//g' > $$.1
echo "s/\/opt\/SUNWspro\/bin/`cat $$.1`/g" > $$.2
cat ./Xvnc/config/cf/sun.cf|sed -f $$.2 > ./Xvnc/config/cf/sun.cf.1
rm -rf $$.1 $$.2

export CC_include=`find $cc_dir/.. -name "CC"|grep include|head -1`
echo $CC_include|sed 's/\//\\\//g' > $$.1
echo "s/\/opt\/SUNWspro\/SC3.0\/include\/CC/`cat $$.1`/g" > $$.2
cat ./Xvnc/config/cf/sun.cf.1|sed -f $$.2 > ./Xvnc/config/cf/sun.cf
rm -rf $$.1 $$.2 ./Xvnc/config/cf/sun.cf.1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PATH=/usr/openwin/bin:${PATH}
export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"
xmkmf
make World
cd Xvnc
./configure 
#make -j $CPUS
make

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
./vncinstall $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/vncconnect
%{_bindir}/vncpasswd
%{_bindir}/vncserver
%{_bindir}/Xvnc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files -n SFEvncviewer
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/vncviewer

%changelog
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.

* Mon Mar 05 2007 - nonsea@users.sourceforge.net
- Bump to 1.3.8.

* Mon Jan 22 2007 - daymobrew@users.sourceforge.net
- Add -n so that the viewer pkg is SFEvncviewer not SFEtightvnc-SFEvncviewer.

* Fri Jan 19 2007 - daymobrew@users.sourceforge.net
- Use $CC instead of `which cc`. Remove '-j $CPUS' from 'make' call as it
  breaks the build.

* Thu Jan 18 2007 - halton.huo@sun.com
- Make it can be built when SunStudio is not installed under /opt/SUNWspro
- Fix build and install error
- Add package SFEvncviewer

* Fri Jan 12 2007 - daymobrew@users.sourceforge.net
- Initial spec

