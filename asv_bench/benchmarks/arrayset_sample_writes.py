# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.
from tempfile import mkdtemp
from shutil import rmtree
import numpy as np
from hangar import Repository
from hangar.utils import folder_size


class HDF5_00(object):

    params = [2_000, 5_000, 20_000]
    param_names = ['num_samples']
    processes = 2
    number = 1
    repeat = (2, 4, 60)
    warmup_time = 0

    def setup(self, num_samples):
        self.tmpdir = mkdtemp()
        self.repo = Repository(path=self.tmpdir, exists=False)
        self.repo.init('tester', 'foo@test.bar', remove_old=True)
        self.co = self.repo.checkout(write=True)

        aint = np.hamming(100).reshape(100, 1)
        bint = np.hamming(100).reshape(1, 100)
        cint = np.round(aint * bint * 1000).astype(np.uint16)
        self.arrint = np.zeros((100, 100), dtype=cint.dtype)
        self.arrint[:, :] = cint

        afloat = np.hamming(100).reshape(100, 1).astype(np.float32)
        bfloat = np.hamming(100).reshape(1, 100).astype(np.float32)
        cfloat = np.round(afloat * bfloat * 1000)
        self.arrfloat = np.zeros((100, 100), dtype=cfloat.dtype)
        self.arrfloat[:, :] = cfloat
        try:
            self.aset_int = self.co.arraysets.init_arrayset(
                'aset_int', prototype=self.arrint, backend_opts='00')
            self.aset_float = self.co.arraysets.init_arrayset(
                'aset_float', prototype=self.arrfloat, backend_opts='00')
        except TypeError:
            self.aset_int = self.co.arraysets.init_arrayset(
                'aset_int', prototype=self.arrint, backend='00')
            self.aset_float = self.co.arraysets.init_arrayset(
                'aset_float', prototype=self.arrfloat, backend='00')

    def teardown(self, num_samples):
        self.co.close()
        self.repo._env._close_environments()
        rmtree(self.tmpdir)

    def time_add_uint16_samples(self, num_samples):
        arr = np.copy(self.arrint)
        with self.aset_int as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i

    def time_add_float32_samples(self, num_samples):
        arr = np.copy(self.arrfloat)
        with self.aset_float as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i

    def track_repo_size_uint16_samples(self, num_samples):
        arr = np.copy(self.arrint)
        with self.aset_int as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i
        self.co.commit('first commit')
        nbytes = folder_size(self.repo._env.repo_path, recurse=True)
        return nbytes

    track_repo_size_uint16_samples.unit = 'bytes'

    def track_repo_size_float32_samples(self, num_samples):
        arr = np.copy(self.arrfloat)
        with self.aset_float as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i
        self.co.commit('first commit')
        nbytes = folder_size(self.repo._env.repo_path, recurse=True)
        return nbytes

    track_repo_size_float32_samples.unit = 'bytes'


class NUMPY_10(object):

    params = [2_000, 5_000]
    param_names = ['num_samples']
    processes = 2
    number = 1
    repeat = (2, 4, 60)
    warmup_time = 0

    def setup(self, num_samples):
        self.tmpdir = mkdtemp()
        self.repo = Repository(path=self.tmpdir, exists=False)
        self.repo.init('tester', 'foo@test.bar', remove_old=True)
        self.co = self.repo.checkout(write=True)

        aint = np.hamming(100).reshape(100, 1)
        bint = np.hamming(100).reshape(1, 100)
        cint = np.round(aint * bint * 1000).astype(np.uint16)
        self.arrint = np.zeros((100, 100), dtype=cint.dtype)
        self.arrint[:, :] = cint

        afloat = np.hamming(100).reshape(100, 1).astype(np.float32)
        bfloat = np.hamming(100).reshape(1, 100).astype(np.float32)
        cfloat = np.round(afloat * bfloat * 1000)
        self.arrfloat = np.zeros((100, 100), dtype=cfloat.dtype)
        self.arrfloat[:, :] = cfloat
        try:
            self.aset_int = self.co.arraysets.init_arrayset(
                'aset_int', prototype=self.arrint, backend_opts='10')
            self.aset_float = self.co.arraysets.init_arrayset(
                'aset_float', prototype=self.arrfloat, backend_opts='10')
        except TypeError:
            self.aset_int = self.co.arraysets.init_arrayset(
                'aset_int', prototype=self.arrint, backend='10')
            self.aset_float = self.co.arraysets.init_arrayset(
                'aset_float', prototype=self.arrfloat, backend='10')

    def teardown(self, num_samples):
        self.co.close()
        self.repo._env._close_environments()
        rmtree(self.tmpdir)

    def time_add_uint16_samples(self, num_samples):
        arr = np.copy(self.arrint)
        with self.aset_int as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i

    def time_add_float32_samples(self, num_samples):
        arr = np.copy(self.arrfloat)
        with self.aset_float as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i

    def track_repo_size_uint16_samples(self, num_samples):
        arr = np.copy(self.arrint)
        with self.aset_int as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i
        self.co.commit('first commit')
        nbytes = folder_size(self.repo._env.repo_path, recurse=True)
        return nbytes

    track_repo_size_uint16_samples.unit = 'bytes'

    def track_repo_size_float32_samples(self, num_samples):
        arr = np.copy(self.arrfloat)
        with self.aset_float as cm_aset:
            for i in range(num_samples):
                cm_aset[i] = arr + i
        self.co.commit('first commit')
        nbytes = folder_size(self.repo._env.repo_path, recurse=True)
        return nbytes

    track_repo_size_float32_samples.unit = 'bytes'
