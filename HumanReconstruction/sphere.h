/**
Copyright (c) 2016
Yixin Zhu, Chenfanfu Jiang, Yibiao Zhao, Demetri Terzopoulos and Song-Chun Zhu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
If the code is used in an article, the following publication shall be cited:
@InProceedings{CVPR16_Chair,
author = {Yixin Zhu, Chenfanfu Jiang, Yibiao Zhao, Demetri Terzopoulos and Song-Chun Zhu},
title = {Inferring Forces and Learning Human Utilities From Videos},
booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
year = {2016}
}
*/
#ifndef SPHERE_H
#define SPHERE_H

#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

struct SPHERE
{
    float center[3];
    float radius;
};


#endif
