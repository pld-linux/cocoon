
%define fopver 0_15_0
%define xalanver 1_2_D02
%define xercesver 1_2

Summary:	The servlet XML transformation system
Name:		cocoon
Version:	1.8.2
Release:	1
License:	Apache
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Source0:	http://xml.apache.org/cocoon/dist/Cocoon-%{version}.tar.gz
Source1:	%{name}-web.xml
Source2:	%{name}-webapp.conf
Patch0:	%{name}-paths.patch
URL:		http://xml.apache.org/cocoon/
Requires:	java >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch

%description
Cocoon is a 100% pure Java publishing framework that relies on new W3C
technologies (such as XML and XSL) to provide web content.

%package doc
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Summary:	Online manual for Cocoon

%description doc
Documentation for Cocoon, viewable through your web server, too.

%package optional
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Requires:	cocoon = %{version}
Summary:	Optional jars for cocoon

%description optional
Additional functionality for Cocoon:
 - bsfengines - Bean Scripting Framework (Xalan existion)
 - bsf - Bean Scripting Framework (Xalan existion functions)
 - fop - converts xsl:fo into PDF output

%package sax-bugfix
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Requires:	cocoon = %{version}
Summary:	Fixes error reporting bug

%description sax-bugfix
Note The sax-bugfix.jar is an optional, unofficial bugfix - which must
be ahead of xerces in the CLASSPATH to work - to allow you to see line
numbers and column numbers in XML parsing error messages, and is only
needed on some virtual machines. If you get "sealing violations", try
removing it from your CLASSPATH.

%package samples
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Requires:	cocoon = %{version}
Summary:	Samples for cocoon

%description samples
This directory contains samples to show you the power of the Cocoon Publishing
Framework. Each subdirectory contains examples of possible uses that should
give you insights on Cocoon capabilities as well as real-life suggestions on
how to XML-ize your web-serving environment.

%package xmldoc
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Requires:	cocoon = %{version}
Summary:	Documentation for cocoon in XML

%description xmldoc
Documentation for cocoon in XML

%prep
%setup -q
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{lib,conf} \
	$RPM_BUILD_ROOT/home/httpd/%{name}/WEB-INF \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/repository

cp bin/cocoon.jar \
	lib/{turbine-pool,w3c,xalan_%{xalanver},xerces_%{xercesver}}.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp lib/{bsfengines,bsf,fop_%{fopver}}.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp lib/sax-bugfix.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

cp index.html $RPM_BUILD_ROOT/home/httpd/%{name}

cp %{SOURCE1} $RPM_BUILD_ROOT/home/httpd/%{name}/WEB-INF/web.xml
cp conf/cocoon.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/conf
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/webapp.conf

cp -R samples $RPM_BUILD_ROOT/home/httpd/%{name}

mv {todo,changes}.xml xdocs
cp -R xdocs $RPM_BUILD_ROOT/home/httpd/%{name}

gzip -9nf LICENSE README

%clean
rm -rf $RPM_BUILD_ROOT

%post
ln -sf %{_datadir}/%{name}/{lib,conf/cocoon.properties} /home/httpd/%{name}/WEB-INF

%postun
rm -rf /home/httpd/%{name}/WEB-INF/{lib,cocoon.properties}

%post doc
ln -sf %{_defaultdocdir}/%{name}-doc-%{version}/docs /home/httpd/%{name}

%postun doc
rm -rf /home/httpd/%{name}/docs

%files
%defattr(644,root,root,755)
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/%{name}/conf/cocoon.properties
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/%{name}/conf/webapp.conf
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) /home/httpd/%{name}/WEB-INF/web.xml
%attr(0750,root,http) %dir %{_localstatedir}/lib/%{name}/repository
/home/httpd/%{name}/index.html
%{_datadir}/%{name}/lib/cocoon.jar
%{_datadir}/%{name}/lib/turbine-pool.jar
%{_datadir}/%{name}/lib/w3c.jar
%{_datadir}/%{name}/lib/xalan_%{xalanver}.jar
%{_datadir}/%{name}/lib/xerces_%{xercesver}.jar
%doc LICENSE.gz README.gz

%files doc
%defattr(644,root,root,755)
%doc docs

%files optional
%defattr(644,root,root,755)
%{_datadir}/%{name}/lib/bsfengines.jar
%{_datadir}/%{name}/lib/bsf.jar
%{_datadir}/%{name}/lib/fop_%{fopver}.jar

%files sax-bugfix
%defattr(644,root,root,755)
%{_datadir}/%{name}/lib/sax-bugfix.jar

%files samples
%defattr(644,root,root,755)
/home/httpd/%{name}/samples

%files xmldoc
%defattr(644,root,root,755)
/home/httpd/%{name}/xdocs
