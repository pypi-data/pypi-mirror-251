# fvirt - A command-line frontend for libvirt.

fvirt is a command-line frontend for libvirt that is intended to fill
a similar role to the `virsh` frontend, but be more human-friendly and
require less scripting to cover some very common use cases.

It also includes enhanced Python bindings for the libvirt API that wrap
the low-level official bindings in a more Pythonic manner, making it
nicer to work with libvirt from Python.

## What does it do?

### fvirt CLI

The fvirt CLI tool can:

- List libvirt objects in much greater detail than virsh, with
  configurable columns and color highlighting of some values. For example,
  when listing domains, it can include everything that `virsh list`
  does, as well as extra info like the generation ID, the OS type,
  the CPU architecture, and the domain ‘title’.
- Perform most common lifecycle operations on libvirt objects, including
  defining, starting, stopping, and undefining them.
- Use a custom timeout to wait for domains to shut down. This cleanly
  encapsulates a relatively common use case which requires scripting to
  work with virsh, allowing for much simpler scripts.
- Modify libvirt object XML using XSLT documents. This allows complex
  programmatic editing of domain configuration without needing complex
  scripting to extract the XML, process it, and then feed it back in to
  libvirt to redefine the object.
- Match objects to operate on using XPath expressions and Python
  regexes. Special options are provided to simplify matching on commonly
  used properties, such as domain architecture or storage pool type. This
  matching works with a significant majority of commands provided by
  fvirt, allowing you to easily operate on groups of objects in bulk.
- Generate object configurations from relatively simple YAML or JSON
  templates describing the object properties.
- Still interoperate cleanly with `virsh`. fvirt stores no state
  client-side, so there’s nothing to get out of sync relative to what
  `virsh` would see or operate on. This means you can use fvirt as your
  primary frontend for libvirt, but still pop out to `virsh` when you
  need to do something fvirt doesn’t support without having to worry
  about it possibly causing fvirt to stop working.

### fvirt.libvirt

The libvirt bindings included with fvirt provide a number of enhancements
over the official bindings for Python, including:

- Hypervisor connections support the context manager protocol.
- Hypervisor objects provide iterator and mapping access to objects like
  domains and storage pools, including reference-counted automatic
  connection management.
- Storage pools provide iterator and mapping access to their volumes.
- Object states are enumerables (like they are in the C API) instead
  of a somewhat opaque list of integer constants (like they are in
  libvirt-python).
- Object XML is directly accessible as lxml Element objects.
- Things that should logically return an empty sequence when nothing
  is matched usually do so, in contrast to libvirt-python often returning
  None instead.
- libvirt URIs are objects that can be easily modified to change things
  like the driver or host, as opposed to being strings you have to
  manipulate with regexes.
- Many common properties of objects are accessible using regular attribute
  access instead of requiring either method calls or manual lookup in the
  object’s XML config. This includes writability for many of these
  properties (though this currently does not work for transient objects).

## What doesn’t it do?

fvirt is designed first and foremost as a lightweight frontend for
libvirt. libvirt provides a _huge_ amount of functionality, much of which
is actually never used by most users. fvirt does not support a lot of
that less commonly used functionality, both because it’s a potential
source of confusion for some users, and because it makes fvirt itself
eaasier to maintain and more robust.

Currently, fvirt and fvirt.libvirt also do not support working with
most libvirt objects other than domains, storage pools, and volumes. This
is because that functionality is what I specifically needed for my own
usage, thus it was the first thing I implemented. I plan to expand this
further to at least include netowrks and network interfaces, but it’s
not a priority at the moment.

## Installation

fvirt is packaged on the Python Package Index with the package name
`fvirt`. It can be easily installed using any Python packag emanagement
tool that works with pypi. As usual with Python packages, use of a
virtual environment is highly recommended.

The actual CLI tool is installed as a script with the name `fvirt`.

fvirt requires Python 3.11 or newer, and installation will also usually
require the tools needed to build the libvirt-python package.

## Contributing

fvirt's dependencies are managed using [Poetry](https://python-poetry.org/).
Assuming you have Poetry installed and have cloned the repository, you
can set up almost everything that’s needed for development by running
`poetry install --all-extras`

In addition to the Python dependencies, a number of tests in our test
suite require additional tooling, specifically a usable local install
of libvirt (including `virtqemud`) and a working install of QEMU’s
full system emulation tooling. Full details can be found in the
`README.md` file in the `tests` directory of the repository.

## Licensing

fvirt is licensed under a modified version of the MIT license commonly
known as the ‘MIT +no-false-attribs license'. This license is a free
software license and is GPL compatible, but is not formally FSF or
OSI approved.
