# deploy test

python /home/deploytest/deploy/Download_Package.py test_e1.tar /home/deploytest/local/ 001 test_e1_20200729001 192.168.137.82:21:ftpuser1:123456:/devops/

python /home/deploytest/deploy/Backup_Directory.py /home/deploytest/backup/ /home/deploytest/update/ exclude_dir1,exclude_dir2
