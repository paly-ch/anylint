# Lintr.org - linter container
#
# VERSION               0.0.1

FROM      ubuntu:14.04
MAINTAINER Pavel Lechenko <paly-ch@lintr.org>

RUN mkdir /tmp/builder
RUN cd /tmp/builder

# Install pre-requisites
RUN apt-get update
RUN apt-get install -y wget


# Install Java
RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" > /etc/apt/sources.list.d/webupd8team.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" >> /etc/apt/sources.list.d/webupd8team.list
RUN apt-get update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y oracle-java8-installer
RUN wget http://garr.dl.sourceforge.net/project/checkstyle/checkstyle/5.7/checkstyle-5.7-bin.tar.gz
RUN tar zxf checkstyle-5.7-bin.tar.gz

# Install Python
RUN apt-get install -y python python3 pypy python-pip
RUN pip install pep8 flake8 pyflakes pylint pep257 easy_install

# Install C/C++
RUN apt-get install -y gcc g++ clang 

# Install Ruby
RUN apt-get install -y ruby ruby1.9.1-dev
RUN gem install --no-rdoc --no-ri ruby-lint

# Install Puppet
RUN gem install --no-rdoc --no-ri puppet
RUN gem install --no-rdoc --no-ri puppet-lint

# Install Go
RUN apt-get install -y golang 

# Install Perl
RUN apt-get install -y perl
RUN wget https://github.com/Perl-Critic/Perl-Critic/archive/v1.121.tar.gz -o Perl-Critic-1.121.tar.gz
RUN tar -zxf Perl-Critic-1.121.tar.gz
RUN cd Perl-Critic-1.121
RUN perl Makefile.PL
RUN make
#  RUN make test
RUN make install

# Install JS
RUN apt-get install -y nodejs npm
RUN npm install jshint
RUN easy_install http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz

# Install PHP
RUN apt-get install -y php5 php5-dev php-pear
RUN pear install PHP_CodeSniffer-2.0.0a2
