export LD_LIBRARY_PATH=".:$LD_LIBRARY_PATH"

./fem_3d 1 -chair chair_cooked.obj -human meat_cooked.obj -chair_cook chair_ls.dat -human_cook human_ls.dat -chair_pointcloud chair_pc.obj -max_dt 1e-3 -solver_tolerance 1e-2 -scale_E 150 -collision_res 450 -bcc_volume_res 300 -bcc_dx 0.03 -friction_up_mid_interface 0.64 -friction_mid_bot_interface 0.07 -friction_up 0 -friction_mid 1e-3 -friction_bot 1e-3 -fps 12 -o output -last_frame 120 -drag 50 -tx 0 -ty 3 -tz 0 -R11 1 -R12 0 -R13 0 -R21 0 -R22 1 -R23 0 -R31 0 -R32 0 -R33 1 -cook_levelset
