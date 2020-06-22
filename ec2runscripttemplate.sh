#!/bin/sh

#
#  AWS Technical Test
#
#  Created by Suzy on 21/06/2020.
#  Copyright © 2020 Suzy. All rights reserved.

sudo yum -y update
sudo amazon-linux-extras install -y python3.8
sudo yum install -y python3
sudo amazon-linux-extras install -y R3.4
wget https://cran.r-project.org/src/contrib/jsonlite_1.6.1.tar.gz
sudo R CMD INSTALL jsonlite_1.6.1.tar.gz
wget https://cran.r-project.org/src/contrib/rappdirs_0.3.1.tar.gz
sudo R CMD INSTALL rappdirs_0.3.1.tar.gz
wget https://cran.r-project.org/src/contrib/Rcpp_1.0.4.6.tar.gz
sudo R CMD INSTALL Rcpp_1.0.4.6.tar.gz
wget https://cran.r-project.org/src/contrib/reticulate_1.16.tar.gz
sudo R CMD INSTALL reticulate_1.16.tar.gz

