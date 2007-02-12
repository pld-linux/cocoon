
%define fopver 0_15_0
%define xalanver 1_2_D02
%define xercesver 1_2

Summary:	The servlet XML transformation system
Summary(pl.UTF-8):	Serwletowy system transformacji XML-a
Name:		cocoon
Version:	1.8.2
Release:	3
License:	Apache
Group:		Applications/Publishing/XML/Java
# new versions in http://www.apache.org/dist/cocoon/
Source0:	http://www.apache.org/dist/cocoon/OLD/%{name}-%{version}.tar.gz
# Source0-md5:	57fc25fcbc96f51cb684741651e94e30
Source1:	%{name}-web.xml
Source2:	%{name}-webapp.conf
Source3:	%{name}-properties
Patch0:		%{name}-paths.patch
URL:		http://xml.apache.org/cocoon/
BuildRequires:	jar
Requires:	jre >= 1.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cocoon is a 100% pure Java publishing framework that relies on new W3C
technologies (such as XML and XSL) to provide web content.

%description -l pl.UTF-8
Cocoon jest napisanym w 100% w Javie środowiskiem publikowania, który
polega na nowych technologiach W3C (takich jak XML i XSL), aby
dostarczyć zawartość stron WWW.

%package doc
Summary:	Online manual for Cocoon
Summary(pl.UTF-8):	Podręcznik online do Cocoona
Group:		Applications/Publishing/XML/Java

%description doc
Documentation for Cocoon, viewable through your web server, too.

%description doc -l pl.UTF-8
Dokumentacja do Cocoona, dająca się oglądać także przez serwer WWW.

%package optional
Summary:	Optional jars for cocoon
Summary(pl.UTF-8):	Opcjonalne pakiety do Cocoona
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}-%{release}

%description optional
Additional functionality for Cocoon:
 - bsfengines - Bean Scripting Framework (Xalan existion)
 - bsf - Bean Scripting Framework (Xalan existion functions)
 - fop - converts xsl:fo into PDF output

%description optional -l pl.UTF-8
Dodatkowa funkcjonalność do Cocoona:
 - bsfengines - Bean Scripting Framework (Xalan)
 - bsf - Bean Scription Framework (funkcje Xalan)
 - fop - konwertuje xsl:fo na PDF

%package sax-bugfix
Summary:	Fixes error reporting bug
Summary(pl.UTF-8):	Poprawia błąd przy raportowaniu błędu
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}-%{release}

%description sax-bugfix
Note The sax-bugfix.jar is an optional, unofficial bugfix - which must
be ahead of xerces in the CLASSPATH to work - to allow you to see line
numbers and column numbers in XML parsing error messages, and is only
needed on some virtual machines. If you get "sealing violations", try
removing it from your CLASSPATH.

%description sax-bugfix -l pl.UTF-8
sax-bugfix.jar jest opcjonalną, nieoficjalną poprawką błędu - która
musi być przed xercesem w CLASSPATH - pozwalającą zobaczyć numery
wierszy i kolumn w komunikatach o błędach w analizie składniowej
XML-a, i jest potrzebna tylko na niektórych maszynach wirtualnych.
Jeżeli dostajesz "sealing violations", spróbuj usunąć ją z CLASSPATH.

%package samples
Summary:	Samples for cocoon
Summary(pl.UTF-8):	Przykłady do Cocoona
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}-%{release}

%description samples
This directory contains samples to show you the power of the Cocoon
Publishing Framework. Each subdirectory contains examples of possible
uses that should give you insights on Cocoon capabilities as well as
real-life suggestions on how to XML-ize your web-serving environment.

%description samples -l pl.UTF-8
Ten pakiet zawiera przykłady pokazujące siłę Środowiska Publikacji
Cocoon. Każdy podkatalog zawiera przykłady możliwych sposobów
wykorzystania możliwości Cocoona oraz sugestie, jak z-XML-izować swój
serwis WWW.

%package xmldoc
Summary:	Documentation for cocoon in XML
Summary(pl.UTF-8):	Dokumentacja do Cocoona w XML-u
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}-%{release}

%description xmldoc
Documentation for cocoon in XML.

%description xmldoc -l pl.UTF-8
Dokumentacja do Cocoona w XML-u.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{lib,conf,xsp-library} \
	$RPM_BUILD_ROOT/home/httpd/%{name}/WEB-INF \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/repository

install bin/cocoon.jar \
	lib/{turbine-pool,w3c,xalan_%{xalanver},xerces_%{xercesver}}.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/lib
install lib/{bsfengines,bsf,fop_%{fopver}}.jar \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/lib
install lib/sax-bugfix.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

jar xf bin/cocoon.jar org/apache/cocoon/processor/xsp/library
mv -f org/apache/cocoon/processor/xsp/library/* \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/xsp-library

install index.html $RPM_BUILD_ROOT/home/httpd/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/web.xml
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/webapp.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/cocoon.properties

cp -R samples $RPM_BUILD_ROOT/home/httpd/%{name}

mv -f {todo,changes}.xml xdocs
cp -Rf xdocs $RPM_BUILD_ROOT/home/httpd/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
ln -sf %{_datadir}/%{name}/conf/cocoon.properties /home/httpd/%{name}/WEB-INF

%postun
rm -rf /home/httpd/%{name}/WEB-INF/{lib,cocoon.properties}

%post doc
ln -sf %{_docdir}/%{name}-doc-%{version}/docs /home/httpd/%{name}

%postun doc
rm -rf /home/httpd/%{name}/docs

%files
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/conf/cocoon.properties
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/conf/webapp.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/%{name}/conf/web.xml
%dir %{_localstatedir}/lib/%{name}
%attr(770,root,http) %dir %{_localstatedir}/lib/%{name}/repository
%dir /home/httpd/%{name}
/home/httpd/%{name}/index.html
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/cocoon.jar
%{_datadir}/%{name}/lib/turbine-pool.jar
%{_datadir}/%{name}/lib/w3c.jar
%{_datadir}/%{name}/lib/xalan_%{xalanver}.jar
%{_datadir}/%{name}/lib/xerces_%{xercesver}.jar
%{_datadir}/%{name}/xsp-library
%doc LICENSE README

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
