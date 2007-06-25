#
# spec file for package SFEcompiz-extra
#

%include Solaris.inc

Name:                    SFEcompiz-extra
Summary:                 Extra compiz plugin
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
Source0:		 http://www.anykeysoftware.co.uk/compiz/plugins/extra-plugins-0.5.0.2.tar.gz
URL:		         http://compiz.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Patch1:			 compiz-extra-01-solaris-port.diff

%package root

Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires:		 SUNWpostrun-root
Requires:		 SUNWgnome-config
BuildRequires:           SFEbcop

%prep
rm -rf %name-%version
mkdir %name-%version
%setup -c -n %name-%version
gtar -xzf %SOURCE0
cd extra-plugins-0.5.0
%patch1 -p1

%build
cd extra-plugins-0.5.0/
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

rm -r resize
rm *.sh
for plugin in `ls`
do
cd $plugin
if test "X$plugin" = "Xvignettes"; then
        CFLAGS="$RPM_OPT_FLAGS" \
        ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--localstatedir=%{_localstatedir} \
	--disable-scrollkeeper
	make 
	cd ..
else
	if test -a $plugin.options; then
	   bcop -g $plugin.options
	fi
	if test "X$plugin" = "Xscreensaver"; then
	   MODE=noXExt make -j $CPUS DESTDIR=$RPM_BUILD_ROOT
	else
	   make -j $CPUS DESTDIR=$RPM_BUILD_ROOT
	fi
	cd ..
fi
done

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/
cd extra-plugins-0.5.0/
for plugin in `ls`
do
cd $plugin
if test "X$plugin" = "Xvignettes"; then
  make DESTDIR=$RPM_BUILD_ROOT install
else    
  make DESTDIR=$RPM_BUILD_ROOT/%{_libdir}/compiz IMAGEDIR=$RPM_BUILD_ROOT/%{_datadir}/compiz install
fi
if test -a $plugin.schema; then
  cp *.schema $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/
fi
cd ..
done

rm $RPM_BUILD_ROOT/%{_libdir}/compiz/*.a 
rm $RPM_BUILD_ROOT/%{_libdir}/compiz/*.la

# fix file attribute problems
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/compiz/*.png
chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/gconf/schemas/*.schema

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait


%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS


%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:/etc/gconf/gconf.xml.defaults';
  echo 'export GCONF_CONFIG_SOURCE';
  echo '/usr/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schema'
) | $BASEDIR/var/lib/postrun/postrun -u -c JDS_wait

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x $PKG_INSTALL_ROOT/usr/bin/gconftool-2 || {';
  echo '  echo "WARNING: gconftool-2 not found; not uninstalling gconf schemas"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$BASEDIR/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$BASEDIR%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/3d.schema';
  echo '         $SDIR/animation.schema';
  echo '         $SDIR/bench.schema';
  echo '         $SDIR/bs.schema';
  echo '         $SDIR/crashhandler.schema';
  echo '         $SDIR/fakergb.schema';
  echo '         $SDIR/flash.schema';
  echo '         $SDIR/group.schema';
  echo '         $SDIR/kiosk.schema';
  echo '         $SDIR/mblur.schema';
  echo '         $SDIR/mousegestures.schema';
  echo '         $SDIR/neg.schema';
  echo '         $SDIR/opacify.schema';
  echo '         $SDIR/put.schema';
  echo '         $SDIR/quickchange.schema';
  echo '         $SDIR/reflex.schema';
  echo '         $SDIR/ring.schema';
  echo '         $SDIR/screensaver.schema';
  echo '         $SDIR/showdesktop.schema'; 
  echo '         $SDIR/snow.schema';
  echo '         $SDIR/snap.schema';
  echo '         $SDIR/splash.schema';
  echo '         $SDIR/thumbnail.schema';
  echo '         $SDIR/tile.schema';
  echo '         $SDIR/trailfocus.schema';
  echo '         $SDIR/wall.schema';
  echo '         $SDIR/wallpaper.schema"';
  echo '         $SDIR/widget.schema';
  echo '         $SDIR/winrules.schema';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/compiz
%dir %attr (0755, root, bin) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/compiz
%{_datadir}/compiz/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*.schema

%changelog
* Mon June 25 2007 - <erwann.chenede@sun.com>
- modification/polish for SFE integration
* Thu May 29 2007 - <chris.wang@sun.com>
- initial creation


