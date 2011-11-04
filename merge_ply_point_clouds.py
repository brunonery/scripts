#!/usr/bin/python
__author__ = "Bruno Nery"
__email__ = "brunonery@brunonery.com"

from sys import argv

HELP = """Merge two PLY files consisting of point clouds.

Usage:
  merge_ply_point_clouds.py <file1.ply> <file2.ply> > <output.ply>
"""

if __name__ == '__main__':
    if len(argv) != 3:
        print HELP
    else:
        first_file = open(argv[1], 'r')
        first_lines = first_file.readlines()
        first_file.close()
        second_file = open(argv[2], 'r')
        second_lines = second_file.readlines()
        second_file.close()
        first_count = int(first_lines[2].split()[2])
        second_count = int(second_lines[2].split()[2])
        print 'ply'
        print 'format ascii 1.0'
        print 'element vertex %d' % (first_count + second_count)
        print 'property float x'
        print 'property float y'
        print 'property float z'
        print 'end_header'
        for l in first_lines[7:]:
            print l.strip()
        for l in second_lines[7:]:
            print l.strip()
