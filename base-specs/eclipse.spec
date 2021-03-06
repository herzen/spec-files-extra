#
# spec file for package eclipse
#
# includes module(s): eclipse
#

%define src_ver 3.4M2
%define src_name eclipse
%define src_url http://mirror.calvin.edu/eclipse/downloads/drops/S-3.4M2-200709210919

%ifarch i386 
%define	_eclipse_arch x86
%else
%define	_eclipse_arch sparc
%endif

Name:		eclipse
Summary:	Eclipse IDE
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-sourceBuild-srcIncluded-%{version}.zip

Source1:	%{name}.desktop
URL:		http://www.eclipse.org
Patch1:		eclipse-01-make.diff
Patch2:		eclipse-02-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -c -n %{src_name}-%{version}
( cd "plugins/org.eclipse.swt/Eclipse SWT PI/gtk/library/"
%patch1 -p0
)
%patch2 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export OPTFLAGS="$CFLAGS"

export JAVA_HOME=/usr/java
export CDE_HOME=/usr/dt

./build -os solaris -ws gtk -arch %{_eclipse_arch} -compilelibs -target compilelibs

gmake -C plugins/org.eclipse.core.filesystem/natives/unix/solaris
( cd plugins/org.eclipse.update.core.solaris/src && ant )

%install
export JAVA_HOME=/usr/java
export CDE_HOME=/usr/dt
%define _desktopdir %{_datadir}/applications
%define _pixmapsdir %{_datadir}/pixmaps
%define _javadir %{_datadir}/java

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_bindir},%{_libdir}/%{name}}
# place for arch independent plugins
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{features,plugins}

(
  cd swttmp && bash build.sh 
  cp lib*.so* $RPM_BUILD_ROOT%{_libdir}
)
install plugins/org.eclipse.core.filesystem/natives/unix/solaris/lib*.so $RPM_BUILD_ROOT%{_libdir}/%{name}

find plugins/org.eclipse.update.core.solaris -name lib\*.so -exec cp {} $RPM_BUILD_ROOT%{_libdir}/%{name} \;

./build -os solaris -ws gtk -arch %{_eclipse_arch} -target install
gtar xfz result/solaris-gtk-%{_eclipse_arch}-sdk.tar.gz -C $RPM_BUILD_ROOT%{_libdir} 
cp plugins/org.eclipse.swt.gtk.solaris.%{_eclipse_arch}/swt.jar $RPM_BUILD_ROOT%{_libdir}/%{name}/org.eclipse.swt.gtk.solaris.%{_eclipse_arch}.jar 

install -d $RPM_BUILD_ROOT%{_javadir}
(
  cd $RPM_BUILD_ROOT%{_javadir}
  ln -sf %{_libdir}/%{name}/org.eclipse.swt.gtk.solaris.%{_eclipse_arch}.jar swt.jar
)
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}


#wrapper
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/eclipse << 'EOF'
#!/bin/bash
exec %{_libdir}/%{name}/eclipse ${1:+"$@"}
EOF

:> $RPM_BUILD_ROOT%{_datadir}/%{name}/.eclipseextension

if [ ! -f "$RPM_BUILD_ROOT%{_libdir}/%{name}/icon.xpm" ]; then
        install features/org.eclipse.equinox.executable/bin/gtk/solaris/x86/icon.xpm $RPM_BUILD_ROOT%{_libdir}/%{name}/icon.xpm
fi

install -D features/org.eclipse.equinox.executable/bin/gtk/solaris/x86/icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/eclipse-icon.xpm

chmod 755 $RPM_BUILD_ROOT%{_libdir}/eclipse/eclipse

%changelog
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Workaround to properly generate the swt jar
* Wed Oct  3 2007 - Doug Scott
- Added src_url
- bump to eclipse-3.4M2
* Sat Sep  8 2007 - dougs@truemail.co.th
- Added swt.jar
* Sat Sep  8 2007 - dougs@truemail.co.th
- Initial base spec file
