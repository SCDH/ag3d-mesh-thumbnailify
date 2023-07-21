# Thumbnailify

**Generate low-res thumbnails of OBJ files using python, headless blender and docker**

## Usage

From the directory containing your OBJ file(s):

```bash
docker run -v="$(pwd):/var/tn/data" -u="$(id -u):$(id -g)" memowe/thumbnailify:0.0.2 Big.obj --percent 5
```

with `Big.obj` being a hi-res OBJ file:

- This will write new GLB data as `Big_thumbnail.glb`.
- The optional `--percent 42` argument defines in percent, which *collapse ratio* of the Blender [Decimate Modifier][decmod] should be used. Default is 10. If you prefer OBJ output, use the optional `--obj` argument.

When called with the `--all` flag instead of an OBJ file name, the tool converts all non-thumbnail OBJ files in the current directory (with the same given `--percent` and output format setting).

## Early development

This tool is in early [development][repo]. Please submit issues and feature requests in the project's [ZIVGitLab issue tracker][issues].

## Copyright and License

(c) 2022-2023 Mirko Westermeier, Service Center for Digital Humanities

Released under the MIT license, see [LICENSE][license] for details.

[decmod]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html
[repo]: https://zivgitlab.uni-muenster.de/SCDH/ag-3d/mesh-thumbnailify
[issues]: https://zivgitlab.uni-muenster.de/SCDH/ag-3d/mesh-thumbnailify/-/issues
[license]: LICENSE
