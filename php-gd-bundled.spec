Summary:	GD extension module for PHP
Name:		php-gd-bundled
Version:	5.4.4
Release:	3
Group:		Development/PHP
URL:		https://www.php.net
License:	PHP License
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  jpeg-devel
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(xpm)
BuildRequires:	t1lib-devel
Provides:	php-gd = 0:%{version}-%{release}
Conflicts:	php-gd < 0:5.2.6-1

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

%files 
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/23_gd-bundled.ini
%attr(0755,root,root) %{_libdir}/php/extensions/gd-bundled.so
