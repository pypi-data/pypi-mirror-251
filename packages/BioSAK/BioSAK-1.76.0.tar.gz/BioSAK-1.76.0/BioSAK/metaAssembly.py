import os
import argparse
import subprocess


metaAssembly_usage = '''
==================== metaAssembly example commands ====================

BioSAK metaAssembly -i GCA_947846245.1 -o output_dir -f
BioSAK metaAssembly -i assembly_id.txt -o output_dir -f

# format of assembly_id.txt (one id per line)
GCA_947846245.1
GCF_026914265.1
GCF_002022765.2

Dependencies: datasets and dataformat
https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/

=======================================================================
'''


def check_executables(program_list):

    not_detected_programs = []
    for needed_program in program_list:

        if subprocess.call(['which', needed_program], stdout=open(os.devnull, 'wb')) != 0:
            not_detected_programs.append(needed_program)

    if not_detected_programs != []:
        print('%s not detected, program exited!' % ','.join(not_detected_programs))
        exit()


def metaAssembly(args):

    assembly_id_txt = args['i']
    op_dir          = args['o']
    force_overwrite = args['f']

    check_executables(['datasets', 'dataformat'])

    if os.path.isdir(op_dir) is True:
        if force_overwrite is True:
            os.system('rm -r %s' % op_dir)
        else:
            print('Output folder detected, program exited!')
            exit()

    tmp_dir = '%s/tmp'          % op_dir
    op_txt  = '%s/output.txt'   % op_dir

    os.mkdir(op_dir)
    os.mkdir(tmp_dir)

    assembly_id_set = set()
    if os.path.isfile(assembly_id_txt):
        for assembly_id in open(assembly_id_txt):
            assembly_id_set.add(assembly_id.strip())
        if len(assembly_id_set) == 0:
            print('No id found in %s, program exited!' % assembly_id_txt)
            exit()
    else:
        assembly_id_set.add(assembly_id_txt)


    op_txt_handle = open(op_txt, 'w')
    op_txt_handle.write('Assembly\tBioSample\tTitle\tDescription\n')
    op_txt_handle.close()

    processing_index = 1
    for assembly_id in assembly_id_set:
        print('Processing %s/%s: %s' % (processing_index, len(assembly_id_set), assembly_id))
        op_metadata_tsv   = '%s/%s_data_report.tsv' % (tmp_dir, assembly_id)
        ncbi_datasets_cmd = 'datasets summary genome accession %s --as-json-lines | dataformat tsv genome > %s' % (assembly_id, op_metadata_tsv)
        os.system(ncbi_datasets_cmd)
        biosample_title = ''
        biosample_accession = ''
        biosample_description = ''
        col_index = dict()
        line_num_index = 0
        for each_line in open(op_metadata_tsv):
            line_num_index += 1
            line_split = each_line.strip().split('\t')
            if line_num_index == 1:
                col_index = {key: i for i, key in enumerate(line_split)}
            elif line_num_index == 2:
                biosample_accession   = line_split[col_index['Assembly BioSample Accession']]
                biosample_title       = line_split[col_index['Assembly BioSample Description Title']]
                biosample_description = line_split[col_index['Assembly BioSample Description Comment']]
        str_to_write = '%s\t%s\t%s\t%s' % (assembly_id, biosample_accession, biosample_title, biosample_description)

        with open(op_txt, 'a') as op_txt_handle:
            op_txt_handle.write(str_to_write + '\n')

        processing_index += 1


if __name__ == '__main__':

    metaAssembly_parser = argparse.ArgumentParser(usage=metaAssembly_usage)
    metaAssembly_parser.add_argument('-i', required=True,                         help='file contains assembly ids')
    metaAssembly_parser.add_argument('-o', required=True,                         help='output directory')
    metaAssembly_parser.add_argument('-f', required=False, action="store_true",   help='force overwrite')
    args = vars(metaAssembly_parser.parse_args())
    metaAssembly(args)
