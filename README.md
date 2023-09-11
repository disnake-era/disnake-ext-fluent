<!-- SPDX-License-Identifier: LGPL-3.0-only -->

# disnake-ext-fluent

`LocalizationProtocol` implementation for projects using Fluent.

For usage example, see [the `example` folder](./example).

This library supports `logging`.

## Version Guarantees

This project strictly follows [Cargo SemVer](https://doc.rust-lang.org/cargo/reference/semver.html).
If you're used to Rust ecosystem, feel free to skip over. Otherwise, read next.

The TL;DR of Cargo SemVer is that here, unlike "normal" SemVer where "major", "minor" and "patch"
points are "hardcoded" in their positions, "major" version number corresponds to "the left-most
non-zero version number", and "minor" and "patch" versions are counted to the right from "major"
(if possible).

Notably, this means that while the project's version stays "instable" (i.e. the leftmost version
number is 0), breaking changes can occur on what most people consider "minor" version number,
and everything else can happen on what most people consider "patch" version number.

This scheme allows the project to give strong version guarantees without compromising on the ease
of development and improvement and without breaking people's expectations. (If some project wants
to strictly follow the "official" SemVer *and* frequently make breaking changes (for the better,
we hope), they must constantly increase the major version number, which after just 5 breaking
changes results in project's version being "5.x.x", which in turn may give observers falsy look of
a "mature, stable and long-in-development" project).

## License

This project is licensed under the GNU Lesser General Public License, version 3; see
[LICENSE](./LICENSE) for more.

## Acknowledgements

This project has portions of other software incorporated into it; please read
[ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md) for more.
