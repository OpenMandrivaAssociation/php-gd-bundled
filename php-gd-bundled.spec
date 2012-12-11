Summary:	GD extension module for PHP
Name:		php-gd-bundled
Version:	5.4.4
Release:	%mkrel 1
Group:		Development/PHP
URL:		http://www.php.net
License:	PHP License
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:  X11-devel
BuildRequires:  freetype2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libxpm-devel
BuildRequires:	t1lib-devel
Provides:	php-gd = 0:%{version}-%{release}
Conflicts:	php-gd < 0:5.2.6-1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a dynamic shared object (DSO) for PHP that will add GD support,
allowing you to create and manipulate images with PHP using the gd library.

PHP is not limited to creating just HTML output. It can also be used to create
and manipulate image files in a variety of different image formats, including
gif, png, jpg, wbmp, and xpm. Even more convenient, PHP can output image
streams directly to a browser. You will need to compile PHP with the GD library
of image functions for this to work. GD and PHP may also require other
libraries, depending on which image formats you want to work with.
 
You can use the image functions in PHP to get the size of JPEG, GIF, PNG, SWF,
TIFF and JPEG2000 images. 

This package is built against the bundled gd library that comes with the php
source. Currently it has some additional features, but I expect the extra
features to be merged upstream into the "official" libgd very soon. 

%prep

%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/gd/* .

%build
%serverbuild

export LIBS="$LIBS -lm"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-gd \
    --with-jpeg-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-zlib-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix}/X11R6 \
    --with-ttf=%{_prefix} \
    --with-freetype-dir=%{_prefix} \
    --enable-gd-native-ttf \
    --with-t1lib=%{_prefix}

%make

mv modules/*.so .
chrpath -d gd.so

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 gd.so %{buildroot}%{_libdir}/php/extensions/gd-bundled.so

cat > %{buildroot}%{_sysconfdir}/php.d/23_gd-bundled.ini << EOF
extension = gd-bundled.so
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/23_gd-bundled.ini
%attr(0755,root,root) %{_libdir}/php/extensions/gd-bundled.so


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 5.4.4-1mdv2012.0
+ Revision: 806384
- 5.4.4

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 5.4.1-1
+ Revision: 795391
- 5.4.1

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 5.3.9-1
+ Revision: 761192
- 5.3.9

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 5.3.8-1
+ Revision: 696383
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 5.3.7-1
+ Revision: 695343
- rebuilt for php-5.3.7

* Sun Jun 19 2011 Oden Eriksson <oeriksson@mandriva.com> 5.3.7-0.0.RC1.1
+ Revision: 685984
- rebuilt for php-5.3.7RC1

* Mon Mar 21 2011 Oden Eriksson <oeriksson@mandriva.com> 5.3.6-1
+ Revision: 647234
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 5.3.5-1mdv2011.0
+ Revision: 629758
- 5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 5.3.4-1mdv2011.0
+ Revision: 628064
- 5.3.4

* Thu Nov 25 2010 Oden Eriksson <oeriksson@mandriva.com> 5.3.4-0.0.RC1.1mdv2011.0
+ Revision: 600985
- use the correct version

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 5.3.3-2mdv2011.0
+ Revision: 600487
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 5.3.3-1mdv2011.0
+ Revision: 588735
- 5.3.3

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 5.3.2-1mdv2010.1
+ Revision: 514543
- rebuilt for php-5.3.2

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 5.3.2-0.0.RC2.1mdv2010.1
+ Revision: 506499
- rebuilt against php-5.3.2RC2

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 5.3.2-0.0.RC1.2mdv2010.1
+ Revision: 492344
- rebuild for new libjpeg v8

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 5.3.2-0.0.RC1.1mdv2010.1
+ Revision: 485332
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 5.3.1-1mdv2010.1
+ Revision: 468100
- rebuilt against php-5.3.1

* Wed Oct 21 2009 Oden Eriksson <oeriksson@mandriva.com> 5.3.1-0.0.RC1.2mdv2010.0
+ Revision: 458510
- rebuilt to pickup the CVE-2009-3546 fixes

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 5.3.1-0.0.RC1.1mdv2010.0
+ Revision: 451500
- rebuild

* Mon Aug 17 2009 Oden Eriksson <oeriksson@mandriva.com> 5.3.0-2mdv2010.0
+ Revision: 417294
- rebuilt against libjpeg v7

* Mon Jul 20 2009 Oden Eriksson <oeriksson@mandriva.com> 5.3.0-1mdv2010.0
+ Revision: 398148
- 5.3.0

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 5.3.0-0.0.RC2.2mdv2010.0
+ Revision: 397526
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 5.3.0-0.0.RC2.1mdv2010.0
+ Revision: 376991
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 5.2.9-1mdv2009.1
+ Revision: 346386
- 5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 5.2.9-0.0.RC2.1mdv2009.1
+ Revision: 341474
- 5.2.9RC2

* Mon Feb 02 2009 Oden Eriksson <oeriksson@mandriva.com> 5.2.8-1mdv2009.1
+ Revision: 336374
- 5.2.8 (also fixes CAN-2008-5498)

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.7-2mdv2009.1
+ Revision: 321731
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.7-1mdv2009.1
+ Revision: 310268
- rebuilt against php-5.2.7

* Thu Sep 11 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-3mdv2009.0
+ Revision: 283769
- fix #35040 (gd-bundled not enabled after install)
- enable t1lib

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-2mdv2009.0
+ Revision: 238395
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-1mdv2009.0
+ Revision: 200202
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.5-2mdv2008.1
+ Revision: 162224
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.5-1mdv2008.1
+ Revision: 107589
- 5.2.5
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.4-1mdv2008.0
+ Revision: 77543
- rebuilt against php-5.2.4

* Wed Jun 20 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-1mdv2008.0
+ Revision: 41799
- Import php-gd-bundled



* Mon Jun 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-1mdv2008.0
- initial Mandriva package
