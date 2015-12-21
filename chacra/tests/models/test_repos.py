from chacra.models import Project, Repo, Binary


class TestRepoModification(object):

    def setup(self):
        self.p = Project('ceph')

    def test_created_slaps_a_modified_attr(self, session):
        repo = Repo(
            self.p,
            ref='firefly',
            distro='centos',
            distro_version='7',
            )
        assert repo.modified.timetuple()

    def test_update_triggers_a_change_in_modified(self, session):
        initial_repo = Repo(
            self.p,
            ref='firefly',
            distro='centos',
            distro_version='7',
            )
        initial_timestamp = initial_repo.modified.time()
        session.commit()
        repo = Repo.get(1)
        repo.distro = 'rhel'
        session.commit()

        assert initial_timestamp < repo.modified.time()

    def test_created_no_binaries_is_not_generic(self, session):
        repo = Repo(
            self.p,
            ref='firefly',
            distro='centos',
            distro_version='7',
            )
        assert repo.is_generic is False


class TestInferType(object):

    def setup(self):
        self.p = Project('ceph')

    def test_rpm_is_inferred(self, session):
        binary = Binary(
            'ceph-1.0.rpm',
            self.p,
            distro='centos',
            distro_version='7',
            arch='x86_64',
            )
        session.commit()
        repo = Repo.get(1)
        assert repo.infer_type() == 'rpm'

    def test_deb_is_inferred(self, session):
        binary = Binary(
            'ceph-1.0.deb',
            self.p,
            distro='ubuntu',
            distro_version='trusty',
            arch='x86_64',
            )
        session.commit()
        repo = Repo.get(1)
        assert repo.infer_type() == 'deb'
