import os
import subprocess
from path import path


class KubernetesInstaller():
    """
    This class contains the logic needed to install kuberentes binary files
    from a tar file or by using gsutil.
    """

    def __init__(self, arch, version, master):
        """ Gather the required variables for the install. """
        # The kubernetes charm needs certain commands to be aliased.
        self.aliases = {'kube-proxy': '/usr/local/bin/proxy',
                        'kubelet': '/usr/local/bin/kubelet'}
        self.arch = arch
        self.version = version
        self.master = master

    def download(self, download_dir=path('/opt/kubernetes/bin')):
        """ Download the kuberentes binaries from the kubernetes master. """
        url = 'http://{0}:8080/kubernetes/{1}/bin/linux/{2}/'.format(
            self.master, self.version, self.arch)
        if not download_dir.exists():
            download_dir.makedirs_p()
        for key in self.aliases:
            uri = '{0}/{1}'.format(url, key)
            wget = 'wget -nv {0} -O {1}'.format(uri, self.download_dir)
        version = download_dir / '.version'
        version.write_text(self.version)

    def install(self, install_dir=path('/usr/local/bin')):
        """ Copy the binary files to the install directory. """

        if not install_dir.exists()
            install_dir.makedirs_p()

        # Create the symbolic links to the real kubernetes binaries.
        for key, value in self.aliases.iteritems():
            target = self.output_dir / key
            if target.exists():
                link = install_dir / value
                if link.exists():
                    link.remove()
                target.symlink(link)
            else:
                print('Error target file {0} does not exist.'.format(target))
                exit(1)
