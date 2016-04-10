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
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <openvdb/openvdb.h>
#include <openvdb/tools/LevelSetSphere.h>
#include <openvdb/tools/Composite.h>

#include <openvdb/tools/VolumeToMesh.h>


#include <iostream>

#include "parse_poly.h"

int main (int argc, char *argv[])
{
    using namespace std;
    std::vector<SPHERE> spheres;

    vector<string> files_to_read;
    vector<int> points_N;
    vector<float> radius;

    files_to_read.push_back("poly_files/skeleton_ElbowLeft_WristLeft.poly");
    points_N.push_back(20);
    radius.push_back(0.035);
    files_to_read.push_back("poly_files/skeleton_ElbowRight_WristRight.poly");
    points_N.push_back(20);
    radius.push_back(0.035);
    files_to_read.push_back("poly_files/skeleton_HipLeft_KneeLeft.poly");
    points_N.push_back(20);
    radius.push_back(0.05);
    files_to_read.push_back("poly_files/skeleton_HipRight_KneeRight.poly");
    points_N.push_back(20);
    radius.push_back(0.05);
    files_to_read.push_back("poly_files/skeleton_KneeLeft_AnkleLeft.poly");
    points_N.push_back(20);
    radius.push_back(0.047);
    files_to_read.push_back("poly_files/skeleton_KneeRight_AnkleRight.poly");
    points_N.push_back(20);
    radius.push_back(0.047);
    files_to_read.push_back("poly_files/skeleton_Neck_Head.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_ShoulderLeft_ElbowLeft.poly");
    points_N.push_back(20);
    radius.push_back(0.035);
    files_to_read.push_back("poly_files/skeleton_ShoulderRight_ElbowRight.poly");
    points_N.push_back(20);
    radius.push_back(0.035);
    files_to_read.push_back("poly_files/skeleton_SpineBase_HipLeft.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineBase_HipRight.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineMidLeft01_HipLeft01.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineMidLeft01_ShoulderLeft01.poly");
    points_N.push_back(20);
    radius.push_back(0.085);
    files_to_read.push_back("poly_files/skeleton_SpineMidLeft02_HipLeft02.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineMidLeft02_ShoulderLeft02.poly");
    points_N.push_back(20);
    radius.push_back(0.085);
    files_to_read.push_back("poly_files/skeleton_SpineMidRight01_HipRight01.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineMidRight01_ShoulderRight01.poly");
    points_N.push_back(20);
    radius.push_back(0.085);
    files_to_read.push_back("poly_files/skeleton_SpineMidRight02_HipRight02.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineMidRight02_ShoulderRight02.poly");
    points_N.push_back(20);
    radius.push_back(0.085);
    files_to_read.push_back("poly_files/skeleton_SpineMid_SpineBase.poly");
    points_N.push_back(20);
    radius.push_back(0.05);
    files_to_read.push_back("poly_files/skeleton_SpineShoulder_Neck.poly");
    points_N.push_back(20);
    radius.push_back(0.05);
    files_to_read.push_back("poly_files/skeleton_SpineShoulder_ShoulderLeft.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineShoulder_ShoulderRight.poly");
    points_N.push_back(20);
    radius.push_back(0.06);
    files_to_read.push_back("poly_files/skeleton_SpineShoulder_SpineMid.poly");
    points_N.push_back(20);
    radius.push_back(0.085);

    for(int i =0 ; i<24; i++){
        parse_poly_add_to_spheres(files_to_read[i],points_N[i],radius[i],spheres);
    }

    openvdb::initialize();

    openvdb::FloatGrid::Ptr gridFULL;

    for(size_t i=0 ; i<spheres.size(); i++){
        SPHERE sphere = spheres[i];


        openvdb::FloatGrid::Ptr grid =
        openvdb::tools::createLevelSetSphere<openvdb::FloatGrid>(
            /*radius=*/sphere.radius, /*center=*/openvdb::Vec3f(sphere.center[0], sphere.center[1], sphere.center[2]),
            /*voxel size=*/0.01, /*width=*/4.0);

            if(i==0) gridFULL = grid->deepCopy();
            else    openvdb::tools::csgUnion(*gridFULL, *grid);
    }

    // openvdb::io::File file("reconstruction.vdb");
    // openvdb::GridPtrVec grids;
    // grids.push_back(gridFULL);
    // file.write(grids);
    // file.close();

    using namespace openvdb;
    std::vector< Vec3s >  	points;
    std::vector< Vec4I >  	quads;
    openvdb::tools::volumeToMesh	(*gridFULL,points,quads); // quads is zero indexed

    for(size_t i=0; i<points.size(); i++){
        cout << points[i][0] <<" "<<points[i][1]  << " "<<points[i][2]<<endl;
    }

    for(size_t i=0; i<quads.size(); i++){
        cout << quads[i][0] <<" "<<quads[i][1]  << " "<<quads[i][2]<<" "<<quads[i][3]<<endl;
    }

    bool write_obj = 1;
    if(write_obj)
    {
        std::string filename("reconstruction.obj");
        std::ofstream fs;fs.open(filename.c_str());
        int nX=points.size();
        int nE=quads.size()*2;
        int nQUARD = quads.size();

        for(int i=0;i<nX;i++)
            fs<<"v "<<points[i][0] <<" "<<points[i][1]  << " "<<points[i][2]<<std::endl;
        fs<<std::endl;

        for(int i=0;i<nQUARD;i++){
            int a = quads[i][0]+1;
            int b = quads[i][1]+1;
            int c = quads[i][2]+1;
            int d = quads[i][3]+1;
            fs<<"f "<<a<<" "<<b<<" "<<c<<std::endl;
            fs<<"f "<<a<<" "<<c<<" "<<d<<std::endl;
        }
        fs.close();
    }


    return 0;
}
