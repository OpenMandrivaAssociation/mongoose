Name:		mongoose
Group:		System/Servers
Summary:	An easy-to-use self-sufficient web server
Version:	5.3
Release:	3
License:	MIT
URL:		http://code.google.com/p/mongoose
Source0:	http://mongoose.googlecode.com/files/mongoose-%{version}.zip
BuildRequires:	openssl-devel

%description
Mongoose web server executable is self-sufficient, it does not depend on 
anything to start serving requests. If it is copied to any directory and 
executed, it starts to serve that directory on port 8080 (so to access files, 
go to http://localhost:8080). If some additional configuration is required - 
for example, different listening port or IP-based access control, then a 
'mongoose.conf' file with respective options can be created in the same 
directory where executable lives. This makes Mongoose perfect for all sorts 
of demos, quick tests, file sharing, and Web programming.

%prep
%setup -q

%build
pushd examples
sed -e "s|g++ unit_test.c -Wall -W -pedantic -lssl|%{__cc} unit_test.c -Wall -W -pedantic -lssl -pthread|" -i Makefile
export CC=%{__cc}
%make server
popd

%install
pushd examples
mkdir -p %buildroot/%{_bindir}/
install server %buildroot/%{_bindir}/mongoose
popd
mkdir -p %buildroot/%{_docdir}/mongoose/
cp -r docs/{FAQ,LuaSqlite,Options,SSL,Usage}.md %buildroot/%{_docdir}/mongoose/

%files
%{_bindir}/%{name}
%{_docdir}/%{name}/*.md
