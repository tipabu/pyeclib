What's wrong with sdists?
=========================

Source distributions (sdists) include just the source files. This works well
enough for pure-Python projects, but pyeclib makes use of C extenstions,
which must be compiled. Publishing only sdists essentially leaves users with
two options:

- Rely upon their linux distribution to build and publish pyeclib packages.
  This often means delays in getting new code and may not work well with
  Python virtual environments.
- Have a build environment available at install time, complete with
  liberasurecode header files. This is a significant burden, increasing
  both the packages required to install and install time.

Is bdist_wheel enough?
======================

No. While ``python setup.py bdist_wheel`` will take care of compiling the C
extension, a naively-built wheel is very much tied to the environment in which
it was built. A wheel built on a recent Ubuntu host, for example, would not
be expected to work on even an older Ubuntu system, much less a Red Hat or
SUSE system.

For more information, see `PEP 513
<https://peps.python.org/pep-0513/#key-causes-of-inter-linux-binary-incompatibility>`__.

Because of these incompatibilities, PyPI won't even accept ``linux_x86_64``
wheel uploads.

OK, well what about manylinux and auditwheel?
=============================================

The manylinux spec (now updated by `PEP 600
<https://peps.python.org/pep-0600/>`__) defines a common base for building
useful wheels, and `auditwheel <https://github.com/pypa/auditwheel>`__
can take such a wheel, bundle in required libraries, and update the platform
tag appropriately. The `manylinux project <https://github.com/pypa/manylinux>`__
offers Docker images to help streamline this process.

However, just these tools will be insufficient. Using auditwheel ensures that
dynamic *linking* works correctly, but pyeclib depends on liberasurecode which
makes extensive use of dynamic **loading** as well. The result is a package
which may be imported, but which has no available backends, not even the one
provided by liberasurecode itself.

Well what are we to do then?
============================

We have to build the wheel to include the required libraries ourselves. In
order to avoid interfering with system packages, we also have to ensure they
are renamed, any dynamic links are updated, and liberasurecode's dynamic
loading `can find the renamed library
<https://github.com/openstack/liberasurecode/commit/53b5c564>`__.

This involves reimplementing a decent bit of auditwheel, but we still want to
call it to update the platform tag.

Isn't this just vendoring?
==========================

Yup. And in general, I'd be opposed; however, pyeclib only needs to vendor
two projects, ``liberasurecode`` and ``isa-l``. The other backends are either
deprecated or proprietary.

Neither ``liberasurecode`` nor ``isa-l`` is terribly active; at the time of
writing, the former had one release within the last year and only three within
the last five, while the latter had one release in the last year and four in the
last five. We should be able to periodically watch for releases and put out a
fresh pyeclib release with any new versions.
