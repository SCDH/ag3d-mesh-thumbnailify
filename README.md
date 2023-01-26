# Thumbnailify

**Generate low-res thumbnails of OBJ files using python, headless blender and docker**

## Usage

From the directory containing your OBJ file `Big.obj`:

```bash
docker run -v="$(pwd):/var/tn/data" -u="$(id -u):$(id -g)" memowe/thumbnailify:0.0.1 Big.obj --percent 5
```

This will write new OBJ data as `Big_thumbnail.obj`.

The optional `--percent` argument defines in percent, which *collapse ratio* of the Blender [Decimate Modifier][decmod] should be used. Default is 10.

## Early development

This tool is in early [development][repo]. Please submit issues and feature requests in the project's [ZIVGitLab issue tracker][issues].

## Copyright and License

(c) 2022-2023 Mirko Westermeier, Service Center for Digital Humanities

Released under the MIT license, see [LICENSE][license] for details.

[decmod]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html
[repo]: https://zivgitlab.uni-muenster.de/SCDH/ag-3d/mesh-thumbnailify
[issues]: https://zivgitlab.uni-muenster.de/SCDH/ag-3d/mesh-thumbnailify/-/issues
[license]: LICENSE
