#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif
#
%include	/usr/lib/rpm/macros.java

# Name without java- prefix. If it is aplication, not a library,
# just do s/srcname/name/g
%define		srcname		myfaces
Summary:	Implementation of JavaServer Faces 1.1.
Name:		java-myfaces
Version:	1.1.6
Release:	0.1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/myfaces/source/myfaces-core-1.1.6-src.tar.gz
# Source0-md5:	04b9bfdd801fa23fadbeb8c58100ee98
URL:		http://myfaces.apache.org/core11/index.html
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Provides:	java(JavaServerFaces) = 1.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%package doc
Summary:	Manual for %{name}
Summary(fr.UTF-8):	Documentation pour %{name}
Summary(it.UTF-8):	Documentazione di %{name}
Summary(pl.UTF-8):	Podręcznik dla %{name}
Group:		Documentation

%description doc
Documentation for %{name}.

%description doc -l fr.UTF-8
Documentation pour %{name}.

%description doc -l it.UTF-8
Documentazione di %{name}.

%description doc -l pl.UTF-8
Dokumentacja do %{name}.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%description javadoc -l fr.UTF-8
Javadoc pour %{name}.

%package demo
Summary:	Demo for %{name}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{name}.

%package manual
Summary:	Tutorial for %{name}
Group:		Documentation

%description manual
Manual for %{name}.

%prep
%setup -q
#%{__sed} -i -e 's,\r$,,' build.xml

%build
export JAVA_HOME="%{java_home}"

required_jars="jaxp_parser_impl"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

export LC_ALL=en_US # source code not US-ASCII

%ant
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a dist/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# for jakarta packages:
for a in dist/*.jar; do
	jar=${a##*/}
	cp -a dist/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
done

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# demo
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%files doc
%defattr(644,root,root,755)
%doc docs/*

%if 0
%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
