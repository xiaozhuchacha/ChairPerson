# Copyright (c) 2016
# Yixin Zhu, Chenfanfu Jiang, Yibiao Zhao, Demetri Terzopoulos and Song-Chun Zhu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# If the code is used in an article, the following publication shall be cited:
# @InProceedings{cvpr2016chair,
#     author = {Zhu, Yixin and Jiang, Chenfanfu and Zhao, Yibiao and Terzopoulos, Demetri and Zhu, Song-Chun},
#     title = {Inferring Forces and Learning Human Utilities From Videos},
#     booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
#     year = {2016}}

# Copyright 1999-2007 Josh Bao, Robert Bridson, Douglas Enright, Ronald Fedkiw, Eran Guendelman, Frederic Gibou, Geoffrey Irving, Sergey Koltakov,
# Nipun Kwatra, Frank Losasso, Ian Mitchell, Neil Molino, Igor Neverov, Duc Nguyen, Nick Rasmussen, Avi Robinson-Mosher, Craig Schroeder, Andrew Selle,
# Tamar Shinar, Eftychios Sifakis, Jonathan Su, Jerry Talton, Joseph Teran, and Rachel Weinstein.  All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution. 

# THIS SOFTWARE IS PROVIDED BY THE PHYSBAM PROJECT ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE PHYSBAM PROJECT OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import numpy as np
import sys
import os
import colorama
from matplotlib import cm


def parse_force(input_force_file, bool_verbose):
    with open(input_force_file, 'r') as f:
        file_data = f.readlines()

    # count all properties in ply files
    # find data area
    all_properties = []

    data_start_line_num = -1
    vertex_size = -1
    face_size = -1

    for i, line in enumerate(file_data):
        if 'property' in line:
            all_properties.append(line.rstrip('\n')[len('property')+1:])
        elif 'end_header' in line:
            data_start_line_num = i + 1
        elif 'element vertex' in line:
            vertex_size = int(line.rstrip('\n')[len('element vertex')+1:])
        elif 'element face' in line:
            face_size = int(line.rstrip('\n')[len('element face')+1:])
    if len(all_properties) == 0 or data_start_line_num <= 0 or vertex_size <= 0 or face_size <= 0:
        raise ValueError('reading data error in ' + input_force_file)
    if bool_verbose:
        print 'all properties:', all_properties
        print 'vertex size:', vertex_size
        print 'face size:', face_size

    # parse fx, fy, fz line number
    fx_index = -1
    fy_index = -1
    fz_index = -1
    for i, line in enumerate(all_properties):
        if 'fx' in line:
            fx_index = i
        elif 'fy' in line:
            fy_index = i
        elif 'fz' in line:
            fz_index = i
    if fx_index < 0 or fy_index < 0 or fz_index < 0:
        raise ValueError('reading data error in ' + input_force_file)

    # read force and vertex data
    data = file_data[data_start_line_num:data_start_line_num+vertex_size]
    data = np.array([data.split(' ') for data in data]).astype('double')
    force_data = data[:, [fx_index, fy_index, fz_index]]
    vertex_data = data[:, range(3)]
    assert(force_data.shape[0] == vertex_size)
    assert(vertex_data.shape[0] == vertex_size)

    # read face data
    face_data = file_data[data_start_line_num+vertex_size:]
    assert(len(face_data) == face_size)

    return force_data, vertex_data, face_data


def parse_group(input_group_file, bool_verbose):
    with open(input_group_file, 'r', 0) as f:
        file_data = f.readlines()

    # count all properties in ply files
    # find data area
    all_properties = []
    data_start_line_num = -1
    data_size = -1
    for i, line in enumerate(file_data):
        if 'property' in line:
            all_properties.append(line.rstrip('\n')[len('property')+1:])
        elif 'end_header' in line:
            data_start_line_num = i + 1
        elif 'element vertex' in line:
            data_size = int(line.rstrip('\n')[len('element vertex')+1:])
    if len(all_properties) == 0 or data_start_line_num <= 0 or data_size <= 0:
        raise ValueError('reading data error in ' + input_group_file)
    if bool_verbose:
        print 'all properties:', all_properties
        print 'data size:', data_size

    # parse group line number
    group_index = []
    group_name = []
    for i, line in enumerate(all_properties):
        if 'float __inside_group_g' in line:
            group_index.append(i)
            group_name.append(line[len('float __inside_group_g'):])
    group_name = map(int, group_name)

    # read group data
    group_data = file_data[data_start_line_num:data_start_line_num+data_size]
    group_data = [data.strip() for data in group_data]
    group_data = np.array([data.split(' ') for data in group_data]).astype('double')
    group_data = group_data[:, group_index]

    # assertions
    # try:
    #     c1 = len(group_name)
    #     _, c2 = group_data.shape
    #     assert(c1 == c2)
    #
    #     unique, unique_count = np.unique(group_data, return_counts=True)
    #     count_0 = 0
    #     count_1 = 0
    #     for i in range(len(unique)):
    #         if unique[i] <= 0:
    #             count_0 += unique_count[i]
    #         elif unique[i] == 1:
    #             count_1 = unique_count[i]
    #     assert(count_0 + count_1 == group_data.shape[0] * group_data.shape[1])
    # except AssertionError:
    #     print 'reading data error in ' + input_group_file
    #     exit(-2)

    # remove duplicated data
    for i in range(group_data.shape[0]):
        index = [j for j, x in enumerate(group_data[i, :]) if x == 1]
        if len(index) > 1:
            group_data[i, index[1:]] = 0
            index = [j for j, x in enumerate(group_data[i, :]) if x == 1]
            assert(len(index) is 1)

    return group_data, group_name, group_index


# usage: python Parse_Force.py -i 'output/ply/69.ply' -v -p
def main():
    colorama.init()

    # parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-p', '--ply', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    input_force_file = args.input
    bool_output_ply = False
    bool_verbose = False
    if args.ply:
        bool_output_ply = True
    if args.verbose:
        bool_verbose = True

    ##
    # force data from ply file
    ##
    if bool_verbose:
        print colorama.Fore.GREEN, '\tparse force data from ply file', colorama.Fore.RESET

    print 'input ply file:', input_force_file

    force_data, vertex_data, face_data = parse_force(input_force_file, bool_verbose)

    ##
    # group data from ply file
    ##
    if bool_verbose:
        print colorama.Fore.GREEN, '\tparse group data from ply file', colorama.Fore.RESET
    input_group_file = 'painted.ply'
    if bool_verbose:
        print 'input group file:', input_group_file

    group_data, group_name, group_index = parse_group(input_group_file, bool_verbose)
    # print 'group index-number', zip(group_index, group_name)

    ##
    # print results
    ##
    if bool_verbose:
        print colorama.Fore.GREEN, '\tprint results', colorama.Fore.RESET

    # average force
    force_one_part = np.zeros((group_data.shape[1], 3))
    for i in range(group_data.shape[1]):
        force_one_part[i, :] = np.sum(force_data[group_data[:, i] == 1, :].T, axis=1).transpose()
    if bool_verbose:
        print 'fx fy fz for comparison:', np.sum(force_one_part, axis=0)
    force_ordered = zip(np.sum(force_one_part, axis=1), group_name)
    if bool_verbose:
        print 'force of each part (14):', force_ordered
    force_final = np.sqrt(np.sum(np.square(force_one_part), axis=1))
    if bool_verbose:
        print 'force all:', np.sum(force_final)

    # group number
    group_count_contacted = np.array([sum(sum(abs(force_data[group_data[:, i] == 1, :].transpose())) > 0.00001)
                                      for i in range(group_data.shape[1])])
    group_count_contacted[group_count_contacted == 0] = sys.maxint
    group_count_all = np.array([sum(group_data[:, i] == 1) for i in range(group_data.shape[1])])

    group_contacted_ordered = zip(group_count_contacted, group_name)
    group_all_ordered = zip(group_count_contacted, group_name)
    if bool_verbose:
        print 'group_count_contacted:', group_contacted_ordered
    if bool_verbose:
        print 'group_count_all:', group_all_ordered

    # average pressure 1
    pressure_ordered1 = zip(force_final / group_count_contacted, group_name)
    if bool_verbose:
        print 'pressure divided by contact points:', pressure_ordered1

    # average pressure 2
    pressure_ordered2 = zip(force_final / group_count_all, group_name)
    if bool_verbose:
        print 'pressure divided by all points:', pressure_ordered2

    ##
    # write data
    ##
    if bool_verbose:
        print colorama.Fore.GREEN, '\twrite data to txt', colorama.Fore.RESET

    output_filename = 'output/force/txt_force.txt'
    with open(output_filename, 'w') as f:
        np.savetxt(output_filename, force_final, fmt='%.5f')
    output_filename = 'output/force/txt_pressure.txt'
    with open(output_filename, 'w') as f:
        np.savetxt(output_filename, force_final / group_count_contacted, fmt="%.5f")


    if bool_output_ply:
        if bool_verbose:
            print colorama.Fore.GREEN, '\twrite to ply', colorama.Fore.RESET

        output_filename = 'output/force/force.ply'

        with open(output_filename, 'w') as f:
            # generate header
            f.write('ply\n')
            f.write('format ascii 1.0\n')
            f.write('element vertex ' + str(vertex_data.shape[0]) + '\n')

            f.write('property float x\n')
            f.write('property float y\n')
            f.write('property float z\n')
            f.write('property uchar red\n')
            f.write('property uchar green\n')
            f.write('property uchar blue\n')

            f.write('element face ' + str(len(face_data)) + '\n')
            f.write('property list uchar int vertex_indices\n')
            f.write('end_header\n')

            # generate colormap
            color_map = np.zeros((group_data.shape[1], 3))
            for i in range(group_data.shape[1]):
                color_index = int(i * 255 / (group_data.shape[1] + 1))
                color_map[i, :] = cm.jet(color_index)[:3]
            color_map *= 255
            color_map = color_map.astype('int')
            # print color_map

            # sort data
            sort_order = np.argsort(force_final)

            # write vertex data
            for i in range(group_data.shape[0]):
                group_index = [j for j, x in enumerate(group_data[i, :]) if x == 1]
                if group_index:
                    assert(len(group_index) is 1)
                    current_color = color_map[np.where(sort_order == group_index), :].transpose()
                else:
                    current_color = [255, 255, 255]
                f.write('%f %f %f %d %d %d\n' %
                        (vertex_data[i, 0], vertex_data[i, 1], vertex_data[i, 2],
                         current_color[0], current_color[1], current_color[2]))

            # write face data
            f.writelines(face_data)


if __name__ == "__main__":
    main()
