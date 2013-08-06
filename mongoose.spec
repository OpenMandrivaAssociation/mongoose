%define major   3
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Name:		mongoose
Group:		System/Servers
Summary:	An easy-to-use self-sufficient web server
Version:	3.1
Release:	1
License:	MIT
URL:		http://code.google.com/p/mongoose
Source0:	http://mongoose.googlecode.com/files/mongoose-%{version}.tgz
Source1:	mongoose.conf
BuildRequires:	openssl-devel

# Build changes:
# http://code.google.com/p/mongoose/issues/detail?id=372 
Patch0:		mongoose-fix-libmongoose-so-build.patch
# http://code.google.com/p/mongoose/issues/detail?id=371
Patch1:		mongoose-fix-no-ssl-dl-build-error.patch

%description
Mongoose web server executable is self-sufficient, it does not depend on 
anything to start serving requests. If it is copied to any directory and 
executed, it starts to serve that directory on port 8080 (so to access files, 
go to http://localhost:8080). If some additional configuration is required - 
for example, different listening port or IP-based access control, then a 
'mongoose.conf' file with respective options can be created in the same 
directory where executable lives. This makes Mongoose perfect for all sorts 
of demos, quick tests, file sharing, and Web programming.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Shared Object for applications that use %{name} embedded

%description -n %{libname}
This package contains the shared library required by applications that
are using %{name}'s embeddable API to provide web services. 

%package -n	%{devname}
Group:		System/Libraries
Summary:	Header files and development libraries for %{name}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the header files and development libraries
for %{name}. If you like to develop programs embedding %{name} on them,
you will need to install %{name}-devel and check %{name}'s API at its
comprisable header file.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .solib-build
%patch1 -p1 -b .nossldl-build
%{__install} -p -m 0644  %{SOURCE1} .

%build
export VERSION=%{version}
%make VER="$VERSION" SOVER="${VERSION%.?}" \
			CFLAGS="%{optflags} -lpthread -lssl -lcrypto -DNO_SSL_DL" linux 

%install
%{__install} -D -p -m 0755 %{name} %{buildroot}/%{_bindir}/%{name}
%{__install} -D -p -m 0644 %{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1
# -lib subpackage
export VERSION=%{version}
%{__install} -D -p -m 0755 lib%{name}.so.%{version} \
		%{buildroot}/%{_libdir}/lib%{name}.so.$VERSION
ln -s %{_libdir}/lib%{name}.so.$VERSION \
		%{buildroot}/%{_libdir}/lib%{name}.so.${VERSION%.?}
# -devel subpackage
%{__install} -D -p -m 0644 %{name}.h %{buildroot}/%{_includedir}/%{name}.h
ln -s %{_libdir}/lib%{name}.so.$VERSION \
		%{buildroot}/%{_libdir}/lib%{name}.so

%files
%doc %{name}.conf LICENSE
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/lib%{name}.so.* 

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
