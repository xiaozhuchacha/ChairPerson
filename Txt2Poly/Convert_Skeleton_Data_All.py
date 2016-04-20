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

import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D # needed for axes 3d projection


# usage: python Convert_Skeleton_Data.py -i 'data' -o 'skeleton_' -s 1 -r 1
def main():
    # parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-r', '--range')
    parser.add_argument('-s', '--show')
    args = parser.parse_args()

    py_plot_show = False
    if args.show:
        py_plot_show = True
        print 'py_plot_show = True'

    for iFile in range(int(args.range)):
        # skeleton data type dict
        skt_idx2name = dict(zip([0, 1, 2, 3,
                                 4, 5, 6,
                                 8, 9, 10,
                                 12, 13, 14,
                                 16, 17, 18,
                                 20],
                                ['SpineBase', 'SpineMid', 'Neck', 'Head',
                                 'ShoulderLeft', 'ElbowLeft', 'WristLeft',
                                 'ShoulderRight', 'ElbowRight', 'WristRight',
                                 'HipLeft', 'KneeLeft', 'AnkleLeft',
                                 'HipRight', 'KneeRight', 'AnkleRight',
                                 'SpineShoulder']))

        skt_name2idx = dict(zip(['SpineBase', 'SpineMid', 'Neck', 'Head',
                                 'ShoulderLeft', 'ElbowLeft', 'WristLeft',
                                 'ShoulderRight', 'ElbowRight', 'WristRight',
                                 'HipLeft', 'KneeLeft', 'AnkleLeft',
                                 'HipRight', 'KneeRight', 'AnkleRight',
                                 'SpineShoulder'],
                                [0, 1, 2, 3,
                                 4, 5, 6,
                                 8, 9, 10,
                                 12, 13, 14,
                                 16, 17, 18,
                                 20]))

        ignore_list = [7, 11, 15, 19, 21, 22, 23, 24]

        input_filename = '%s/skeleton_%05d_00.txt' % (args.input, iFile+1)
        output_filename_prefix = args.input + '/' + str(iFile+1)
        if not os.path.exists(output_filename_prefix):
            os.makedirs(output_filename_prefix)
        output_filename_prefix += '/' + args.output
        print 'input filename:'
        print input_filename
        print 'output filename prefix:'
        print output_filename_prefix

        # load data
        skt_pos_data = []
        skt_ori_data = []
        with open(input_filename) as f:
            line_number = 0
            for line in f:
                if 1 <= line_number <= 25:
                    skt_pos_data.append(line.split()[1:4])
                if 28 <= line_number:
                    skt_ori_data.append(line.split())
                line_number += 1

        skt_pos_data = np.array(skt_pos_data).astype(np.float)
        skt_ori_data = np.array(skt_ori_data).astype(np.float)

        # add points in shoulder and hip
        point_start = ['ShoulderRight', 'ShoulderLeft', 'HipRight', 'HipLeft']
        point_end = ['SpineShoulder', 'SpineShoulder', 'SpineBase', 'SpineBase']
        distance = [0.05, 0.05, 0.03, 0.03]
        move_direction = []
        num_more_points = 3
        for j in range(len(distance)):
            tmp_move_direction = skt_pos_data[skt_name2idx[point_start[j]], :] - skt_pos_data[skt_name2idx[point_end[j]], :]
            tmp_move_direction /= np.linalg.norm(tmp_move_direction)
            move_direction.append(tmp_move_direction)
            for i in range(1, num_more_points):
                new_point = skt_pos_data[skt_name2idx[point_end[j]], :] + np.dot(distance[j]*i, tmp_move_direction)
                skt_pos_data = np.append(skt_pos_data, new_point.reshape((1, 3)), axis=0)
                skt_idx2name.update({max(max(ignore_list), max(skt_idx2name.keys()))+1: '%s%02d' % (point_start[j], i)})
                skt_name2idx.update({'%s%02d' % (point_start[j], i): max(max(ignore_list), max(skt_idx2name.keys()))})

        # add points in spine mid
        for j in range(len(distance)/2):
            tmp_move_direction = (move_direction[j] + move_direction[j+len(distance)/2]) / 2
            tmp_move_direction /= np.linalg.norm(tmp_move_direction)
            for i in range(1, num_more_points):
                new_point = skt_pos_data[skt_name2idx['SpineMid'], :] + np.dot(0.02*i, tmp_move_direction)
                skt_pos_data = np.append(skt_pos_data, new_point.reshape((1, 3)), axis=0)
                if j == 0:
                    tmp_name = 'SpineMidRight%02d' % i
                if j == 1:
                    tmp_name = 'SpineMidLeft%02d' % i
                skt_idx2name.update({max(skt_idx2name.keys())+1: tmp_name})
                skt_name2idx.update({tmp_name: max(skt_idx2name.keys())})

        # format point data
        x_point = skt_pos_data[:, 0]
        y_point = skt_pos_data[:, 1]
        z_point = skt_pos_data[:, 2]

        # add line
        line_index = [[skt_name2idx['SpineShoulder'], skt_name2idx['Neck']],
                      [skt_name2idx['Neck'], skt_name2idx['Head']],
                      [skt_name2idx['SpineShoulder'], skt_name2idx['ShoulderRight']],
                      [skt_name2idx['ShoulderRight'], skt_name2idx['ElbowRight']],
                      [skt_name2idx['ElbowRight'], skt_name2idx['WristRight']],
                      [skt_name2idx['SpineShoulder'], skt_name2idx['ShoulderLeft']],
                      [skt_name2idx['ShoulderLeft'], skt_name2idx['ElbowLeft']],
                      [skt_name2idx['ElbowLeft'], skt_name2idx['WristLeft']],
                      [skt_name2idx['SpineShoulder'], skt_name2idx['SpineMid']],
                      [skt_name2idx['SpineMid'], skt_name2idx['SpineBase']],
                      [skt_name2idx['SpineBase'], skt_name2idx['HipRight']],
                      [skt_name2idx['SpineBase'], skt_name2idx['HipLeft']],
                      [skt_name2idx['HipRight'], skt_name2idx['KneeRight']],
                      [skt_name2idx['KneeRight'], skt_name2idx['AnkleRight']],
                      [skt_name2idx['HipLeft'], skt_name2idx['KneeLeft']],
                      [skt_name2idx['KneeLeft'], skt_name2idx['AnkleLeft']]]
        for i in range(1, num_more_points):
            line_index.append([skt_name2idx['SpineMidRight%02d' % i], skt_name2idx['ShoulderRight%02d' % i]])
            line_index.append([skt_name2idx['SpineMidRight%02d' % i], skt_name2idx['HipRight%02d' % i]])
            line_index.append([skt_name2idx['SpineMidLeft%02d' % i], skt_name2idx['ShoulderLeft%02d' % i]])
            line_index.append([skt_name2idx['SpineMidLeft%02d' % i], skt_name2idx['HipLeft%02d' % i]])
        line_index = np.array(line_index)

        # format line data
        x_line = x_point[line_index]
        y_line = y_point[line_index]
        z_line = z_point[line_index]

        # plot data
        if py_plot_show:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            for i in range(len(skt_pos_data)):
                if i in ignore_list:
                    continue
                ax.scatter(x_point[i], y_point[i], z_point[i], c='r', marker='o', s=50)
            [ax.plot(x_line[i, :], y_line[i, :], z_line[i, :], linewidth=5) for i in range(len(x_line))]

            # create cubic bounding box to simulate equal aspect ratio
            max_range = np.array([x_point.max()-x_point.min(),
                                  y_point.max()-y_point.min(),
                                  z_point.max()-z_point.min()]).max()
            x_bbox = 0.5*max_range*np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5*(x_point.max()+x_point.min())
            y_bbox = 0.5*max_range*np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5*(y_point.max()+y_point.min())
            z_bbox = 0.5*max_range*np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5*(z_point.max()+z_point.min())
            for xb, yb, zb in zip(x_bbox, y_bbox, z_bbox):
                ax.plot([xb], [yb], [zb], 'w')

            plt.grid()
            plt.show()

        # write point data to obj files
        # for i in range(len(skt_pos_data)):
        #     if i in ignore_list:
        #         continue
        #     output_filename = output_filename_prefix + '%s.obj' % skt_idx2name[i]
        #     with open(output_filename, 'w') as f:
        #         f.write('v %.3f %.3f %.3f' % (x_point[i], y_point[i], z_point[i]))

        # write skeleton data to poly files
        for i in range(len(line_index)):
            output_filename = output_filename_prefix + '%s_%s.poly' %\
                                                       (skt_idx2name[line_index[i][0]], skt_idx2name[line_index[i][1]])
            with open(output_filename, 'w') as f:
                f.write('POINTS\n')
                f.write('1: %.3f %.3f %.3f\n' %
                        (x_point[line_index[i][0]], y_point[line_index[i][0]], z_point[line_index[i][0]]))
                f.write('2: %.3f %.3f %.3f\n' %
                        (x_point[line_index[i][1]], y_point[line_index[i][1]], z_point[line_index[i][1]]))
                f.write('POLYS\n')
                f.write('1: 1 2\n')
                f.write('END\n')


if __name__ == "__main__":
    main()
