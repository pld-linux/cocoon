
%define fopver 0_15_0
%define xalanver 1_2_D02
%define xercesver 1_2

Summary:	The servlet XML transformation system
Summary(pl):	Serwletowy system transformacji XML
Name:		cocoon
Version:	1.8.2
Release:	3
License:	Apache
Group:		Applications/Publishing/XML/Java
Source0:	http://xml.apache.org/cocoon/dist/Cocoon-%{version}.tar.gz
# Source0-md5:	fb2e456f477c574f844a42b23e2bec48
Source1:	%{name}-web.xml
Source2:	%{name}-webapp.conf
Source3:	%{name}-properties
Patch0:		%{name}-paths.patch
URL:		http://xml.apache.org/cocoon/
Requires:	jre >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch
BuildRequires:	jar

%description
Cocoon is a 100% pure Java publishing framework that relies on new W3C
technologies (such as XML and XSL) to provide web content.

%description -l pl
Cocoon jest napisanym w 100% w Javie ¶rodowiskiem publikowania, który
polega na nowych technologiach W3C (takich jak XML i XSL), aby
dostarczyæ zawarto¶æ stron WWW.

%package doc
Summary:	Online manual for Cocoon
Summary(pl):	Podrêcznik online do Cocoona
Group:		Applications/Publishing/XML/Java

%description doc
Documentation for Cocoon, viewable through your web server, too.

%description doc -l pl
Dokumentacja do Cocoona, daj±ca siê ogl±daæ tak¿e przez serwer WWW.

%package optional
Summary:	Optional jars for cocoon
Summary(pl):	Opcjonalne pakiety do Cocoona
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}

%description optional
Additional functionality for Cocoon:
 - bsfengines - Bean Scripting Framework (Xalan existion)
 - bsf - Bean Scripting Framework (Xalan existion functions)
 - fop - converts xsl:fo into PDF output

%description optional -l pl
Dodatkowa funkcjonalno¶æ do Cocoona:
 - bsfengines - Bean Scripting Framework (Xalan)
 - bsf - Bean Scription Framework (funkcje Xalan)
 - fop - konwertuje xsl:fo na PDF

%package sax-bugfix
Summary:	Fixes error reporting bug
Summary(pl):	Poprawia b³±d przy raportowaniu b³êdu
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}

%description sax-bugfix
Note The sax-bugfix.jar is an optional, unofficial bugfix - which must
be ahead of xerces in the CLASSPATH to work - to allow you to see line
numbers and column numbers in XML parsing error messages, and is only
needed on some virtual machines. If you get "sealing violations", try
removing it from your CLASSPATH.

%description sax-bugfix -l pl
sax-bugfix.jar jest opcjonaln±, nieoficjaln± poprawk± b³êdu - która
mui byæ przed xercesem w CLASSPATH - pozwalaj±ca zobaczyæ numery linii
i kolumn w komunikatach o b³êdach w parsowaniu XML, i jest potrzebna
tylko na niektórych maszynach wirtualnych. Je¿eli dostajesz "sealing
violations", spróbuj usun±æ j± z CLASSPATH.

%package samples
Summary:	Samples for cocoon
Summary(pl):	Przyk³ady do Cocoona
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}

%description samples
This directory contains samples to show you the power of the Cocoon
Publishing Framework. Each subdirectory contains examples of possible
uses that should give you insights on Cocoon capabilities as well as
real-life suggestions on how to XML-ize your web-serving environment.

%description samples -l pl
Ten pakiet zawieraa przyk³ady pokazuj±ce si³ê ¦rodowiska Publikacji
Cocoon. Ka¿dy podkatalog zawiera przyk³ady mo¿liwych sposobów
wykorzystania mo¿liwo¶ci Cocoona oraz sugestie, jak z-XML-izowaæ swój
serwis WWW.

%package xmldoc
Summary:	Documentation for cocoon in XML
Summary(pl):	Dokumentacja do Cocoona w XML
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}

%description xmldoc
Documentation for cocoon in XML.

%description xmldoc -l pl
Dokumentacja do Cocoona w XML.

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

install %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/%{name}/conf/web.xml
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
ln -sf %{_defaultdocdir}/%{name}-doc-%{version}/docs /home/httpd/%{name}

%postun doc
rm -rf /home/httpd/%{name}/docs

%files
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/conf
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/%{name}/conf/cocoon.properties
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/%{name}/conf/webapp.conf
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/%{name}/conf/web.xml
%dir %{_localstatedir}/lib/%{name}
%attr(0770,root,http) %dir %{_localstatedir}/lib/%{name}/repository
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
