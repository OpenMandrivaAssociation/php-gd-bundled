Summary:	GD extension module for PHP
Name:		php-gd-bundled
Version:	5.2.4
Release:	%mkrel 1
Group:		Development/PHP
URL:		http://www.php.net
License:	PHP License
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:  XFree86-devel
BuildRequires:  freetype2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel 
BuildRequires:  libxpm-devel
Provides:	php-gd
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
    --enable-gd-native-ttf 

%make

mv modules/*.so .
chrpath -d gd.so

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 gd.so %{buildroot}%{_libdir}/php/extensions/gd-bundled.so

cat > %{buildroot}%{_sysconfdir}/php.d/23_gd-bundled.ini << EOF
extension = gd-bundled.so
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/23_gd-bundled.ini
%attr(0755,root,root) %{_libdir}/php/extensions/gd-bundled.so
