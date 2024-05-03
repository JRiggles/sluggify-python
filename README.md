# sluggify-python
### A Python implementation of [skeddles/sluggify](https://github.com/skeddles/sluggify) for generating URL slugs

The following manipluations are performed in this order:
1. replace slashes `/` `\` and spaces ` ` with dashes `-`
2. replace any accented characters with their closest non-accented equvalent, e.g. `é` becomes `e`
3. remove all non-alphanumeric characters (anything other than `A-Z`, `a-z`, `0-9`, and `-`)
4. replace multiple consecutive dashes `---` with a single dash `-`
5. remove leading dashes, e.g. `-Gengar-` becomes `Gengar-`
6. remove trailing dashes, e.g. `Gengar-` becomes `Gengar`
7. convert to lowercase, e.g. `Gengar` becomes `gengar`

## Dependencies
None

## Example
```python
import sluggify

slug = sluggify.sluggify("Pokémon Yellow!")
print(slug)
assert(slug == "pokemon-yellow")  # expected output
```
### outputs...
```txt
pokemon-yellow
```

## Installation
Download `sluggify.py` and place it in your project's root

## TODO
- [ ] Publish to PyPI
