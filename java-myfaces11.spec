# TODO:
# - build it from sources (requires maven)
# - Requires: (?)

# Conditional build:
%include	/usr/lib/rpm/macros.java

%define		srcname		myfaces
%define		apiver		1.1
Summary:	Implementation of JavaServer Faces %{apiver}
Name:		java-myfaces11
Version:	1.1.6
Release:	2
License:	Apache v2.0
Group:		Libraries/Java
Source0:	myfaces-api-%{version}.jar
# Source0-md5:	def6a9475ce8dc64a3861a260efd6894
Source1:	myfaces-impl-%{version}.jar
# Source1-md5:	6f5644e0a538df20554345dcdff67080
URL:		http://myfaces.apache.org/core11/index.html
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Provides:	java(JavaServerFaces) = %{apiver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of JavaServer Faces %{apiver}.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a %{SOURCE0} $RPM_BUILD_ROOT%{_javadir}/%{srcname}-api-%{version}.jar
ln -s %{srcname}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-api-%{apiver}.jar
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_javadir}/%{srcname}-impl-%{version}.jar
ln -s %{srcname}-impl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-impl-%{apiver}.jar

# for P: java(JavaServerFaces)
ln -s %{srcname}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/faces-api-%{apiver}.jar
ln -s %{srcname}-impl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/faces-impl-%{apiver}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
