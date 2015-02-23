import os
import subprocess
from path import path


class KubernetesInstaller():
    """
    This class contains the logic needed to install kuberentes binary files
    from a tar file or by using gsutil.
    """

    def __init__(self, arch, version, kubernetes_file):
        """ Gather the required variables for the install. """
        # The kubernetes charm needs certain commands to be aliased.
        self.aliases = {'kube-proxy': '/usr/local/bin/proxy',
                        'kubelet': '/usr/local/bin/kubelet'}
        self.arch = arch
        self.version = version
        self.kubernetes_file = path(kubernetes_file)

    def install(self, output_dir=path('/opt/kubernetes/bin')):
        """ Install kubernetes binary files from the tar file or gsutil. """
        if output_dir.isdir():
            # Remote old content to remain idempotent.
            output_dir.rmtree()

        # Create the output directory.
        output_dir.makedirs()

        # Write the version and arch to a dot file.
        (output_dir / '.kubernetes').write_text('{0} {1}'.format(self.version,
                                                                 self.arch))

        if self.kubernetes_file.exists():
            # Untar the file to the output directory.
            command = 'tar -xvzf {0} -C {1}'.format(self.kubernetes_file,
                                                    output_dir)
            print(command)
            output = subprocess.check_output(command, shell=True)
            print(output)
        else:
            # Get the binaries from the gsutil command.
            self.get_kubernetes_gsutil(output_dir)

        # Create the symbolic links to the real kubernetes binaries.
        usr_local_bin = path('/usr/local/bin')
        for key, value in self.aliases.iteritems():
            target = output_dir / key
            link = usr_local_bin / value
            if link.exists():
                link.remove()
            target.symlink(link)

    def get_kubernetes_gsutil(self, directory):
        """ Download the kubernetes binary objects from gsutil. """
        uri = 'gs://kubernetes-release/release/{0}/bin/linux/{1}/'.format(
              self.version, self.arch)
        gs_command = 'gsutil cp {0} {1}'
        # Download all the keys in the aliases dictionary to this machine.
        for key in self.aliases:
            # Create the remote target by appending the key to the uri string.
            remote = uri + key
            # Create the local path and file name string.
            local = os.path.join(directory, key)
            command = gs_command.format(remote, local)
            print(command)
            subprocess.check_call(command.split())
