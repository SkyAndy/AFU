#!/bin/bash
# installing ax25 from git

aptitude install libncursesw5-dev libncurses5-dev ncurses-dev autoconf automake libtool

git clone git://git.linux-ax25.org/pub/scm/libax25
git clone git://git.linux-ax25.org/pub/scm/ax25-apps
git clone git://git.linux-ax25.org/pub/scm/ax25-tools

cd libax25
autoreconf --install --force
./configure
make
make install

cd ..
cd ax25-apps
autoreconf --install --force
./configure
make
make install

cd ..
cd ax25-tools
autoreconf --install --force
./configure
make
make install
