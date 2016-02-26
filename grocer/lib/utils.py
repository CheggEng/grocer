import os
import subprocess
import logging

log = logging.getLogger('grocer-utils')
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def foodcritic(fc_bin, path, fc_strict=False):
    """
    Execute foodcritic
    :rtype : tuple
    :param fc_bin: path to food critic binary
    :param path: dir path to exectue FC on
    :param fc_strict: bool. true if foodcritic should fail if any of the checks do not pass
    :return: tpl. output, errors, returncode
    """
    if fc_strict:
        cmd = '{0} -f any {1}'.format(fc_bin, path)
    else:
        cmd = '{0} {1}'.format(fc_bin, path)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    output, errors = p.communicate()
    return output, errors, p.returncode


def rubocop(rubocop_bin, path):
    """
    Execute rubocop
    :rtype : tuple
    :param rubocop_bin: path to food critic binary
    :param path: dir path to exectue rubocop on
    :return: tpl. output, errors, returncode
    """
    cmd = '{0} {1}'.format(rubocop_bin, path)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    output, errors = p.communicate()
    return output, errors, p.returncode


def berks(berks_bin, path, action='update'):
    """
    Execute various berks commands
    :rtype : tuple
    :param berks_bin: path to berks bin
    :param path: path to change directory to before running berks commands (berks is a dir context aware tool)
    :param action: berks action to run, e.g. berks install
    :return: tpl. output, errors, returncode
    """
    cmd = 'cd {0} && {1} {2}'.format(path, berks_bin, action)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    output, errors = p.communicate()
    return output, errors, p.returncode


def ruby_syntax(ruby_bin, path):
    """
    Check ruby syntax using ruby interpreter -c flag
    :rtype : tuple
    :param ruby_bin: path to ruby bin
    :param path: file path to ruby code to check
    :return: tpl. output, errors, returncode
    """
    cmd = '{0} -c {1}'.format(ruby_bin, path)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    output, errors = p.communicate()
    return output, errors, p.returncode


def chefspec(chefspec_bin, path):
    raise NotImplementedError


def get_file_types(dir_path):
    """
    Get the files in a directory based on type
    :rtype : tuple
    :param dir_path: str. path to directory to search
    :return: 4-part tuple. ruby_files, json_files, md_files, other_type
    """
    ruby_files = []
    json_files = []
    md_files = []
    other_type = []
    for root, dirs, files in os.walk(dir_path):
        if "git" in root:
            pass
        else:
            for _file in files:
                if _file[-3:] == '.rb':
                    ruby_files.append(os.path.join(root,_file))
                elif _file[-5:] == '.json':
                    json_files.append(os.path.join(root,_file))
                elif _file[-3:] == '.md':
                    md_files.append(os.path.join(root,_file))
                else:
                    other_type.append(_file)
    return ruby_files, json_files, md_files, other_type


def rspec_test(rspec_bin, path):
    """
    excute rspec tests
    :param rspec_bin: path to rspec bin
    :param path: dir path to recipe dir root
    :return:  tpl. output, errors, returncode
    """
    path = os.path.join(path,'test/integration/default')
    if not os.path.isdir(path):
        return "No rspec tests found in {0}".format(path), None, 0
    cmd = '{0} -c {1}/*'.format(rspec_bin, path)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    output, errors = p.communicate()
    return output, errors, p.returncode
