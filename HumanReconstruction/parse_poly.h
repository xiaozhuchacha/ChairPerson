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
@InProceedings{cvpr2016chair,
    author = {Zhu, Yixin and Jiang, Chenfanfu and Zhao, Yibiao and Terzopoulos, Demetri and Zhu, Song-Chun},
    title = {Inferring Forces and Learning Human Utilities From Videos},
    booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
    year = {2016}}
*/
#ifndef PARSE_POLY_H
#define PARSE_POLY_H

#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

#include "sphere.h"

void parse_poly_add_to_spheres(    const std::string& filename,    const int number_of_points,    const float radius,    std::vector<SPHERE>& spheres)
{
    using namespace std;
    std::ifstream fs;
    fs.open(filename.c_str());
    float head[3], tail[3];
    int line_number = 1;
    string line;
    while(getline(fs,line)){
        if(line_number == 2){
            std::stringstream ss(line);
            ss.ignore();
            ss.ignore();
            ss>>head[0]>>head[1]>>head[2];
        }
        else if(line_number == 3){
            std::stringstream ss(line);
            ss.ignore();
            ss.ignore();
            ss>>tail[0]>>tail[1]>>tail[2];
        }
        line_number++;
    }
    fs.close();

    float dx[3];
    dx[0] = (tail[0]-head[0]) / (float)(number_of_points-1);
    dx[1] = (tail[1]-head[1]) / (float)(number_of_points-1);
    dx[2] = (tail[2]-head[2]) / (float)(number_of_points-1);

    for(int k=0; k<number_of_points; k++){
        SPHERE sphere;
        for(int d=0; d<3; d++){
            sphere.center[d] = head[d] + dx[d]*k;
        }
        sphere.radius = radius;
        spheres.push_back(sphere);
    }
}


#endif
