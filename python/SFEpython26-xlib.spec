#
# spec file for package SFEpython26-xlib
#
# includes module(s): python-xlib
#
%include Solaris.inc

%define src_name        python-xlib
%define python_version  2.6

Name:                   SFEpython26-xlib
Summary:                A complete X11R6 client-side implementation in pure-python
URL:                    http://python-xlib.sourceforge.net/
Version:                0.14
Source:                 %{sf_download}/python-xlib/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython26
BuildRequires:          SUNWPython26-devel

%prep
%setup -q -n %{src_name}-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Sun May 09 2010 - Albert Lee <trisk@opensolaris.org>
- Update download URL
* Mon Aug 10 2009 - matt@greenviolet.net
- Initial spec file based on SFEpython-xlib.spec
* Tue Dec 25 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
