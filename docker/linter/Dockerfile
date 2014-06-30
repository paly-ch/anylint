# Lintr.org - linter container
#
# VERSION               0.0.1

FROM      ubuntu:14.04
MAINTAINER Pavel Lechenko <paly-ch@lintr.org>

RUN mkdir /tmp/builder
RUN cd /tmp/builder
RUN mkdir /linter

# Install pre-requisites
RUN apt-get update
RUN apt-get install -y wget git-core

# Install Java
RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" > /etc/apt/sources.list.d/webupd8team.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" >> /etc/apt/sources.list.d/webupd8team.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886
RUN apt-get update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN sleep 3
RUN apt-get install -y oracle-java8-installer
RUN wget http://garr.dl.sourceforge.net/project/checkstyle/checkstyle/5.7/checkstyle-5.7-bin.tar.gz
RUN tar zxf checkstyle-5.7-bin.tar.gz
RUN mkdir -p /linter/checkstyle
RUN cp checkstyle-5.7/checkstyle-5.7-all.jar checkstyle-5.7/sun_checks.xml /linter/checkstyle/
ENV CLASSPATH /linter/checkstyle/checkstyle-5.7-all.jar

# Install Python
RUN apt-get install -y python python3 pypy python-pip
RUN pip install pep8 flake8 pyflakes pylint pep257 setuptools

# Install Ruby
RUN apt-get install -y ruby1.9.1-dev
RUN gem install --no-rdoc --no-ri ruby-lint

# Install Puppet
RUN gem install --no-rdoc --no-ri puppet
RUN gem install --no-rdoc --no-ri puppet-lint

# Install PHP
RUN apt-get install -y php5-dev php-pear
RUN pear install PHP_CodeSniffer-2.0.0a2

# Install JS, Coffee, TS, CSS
RUN apt-get install -y nodejs npm
RUN npm install -g jshint
RUN npm install -g coffeelint
RUN npm install -g tslint
RUN npm install -g csslint
RUN easy_install http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz

# Install C/C++
RUN apt-get install -y gcc g++ clang

# Install Go
RUN apt-get install -y golang
RUN mkdir -p /linter/golang/
ENV GOPATH /linter/golang/
RUN go get github.com/golang/lint/golint

# # Install Perl
RUN apt-get install -y perl libperl-critic-perl
