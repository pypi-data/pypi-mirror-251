# latvian_streets_neighborhoods

## install

`pip install latviastreetify`

or with CLI capabilities

`pip install latviastreetify[cli]`

### Using external files

You can use external files for address and neighbordhoods by setting the enviroment variables to external `.shp` files.

```bash
# for streets/address
export STREETS_FILE=
# for neighbordhoods
export NEIGHBORHOODS_FILE=
```

## Usage examples

### Head of the dataframe

```python
from latviastreetify.resolvers import Language, SteetsAndNeighborhoodsResolver
from pprint import pprint

resolver = SteetsAndNeighborhoodsResolver()
gdf = resolver.get_gdf(language=Language.EN)
pprint(gdf.head())
```

```
        Address     Street Number  Rotation                   Geometry        lat        lon  index_right     Name                       Website
1  pūku iela 14  pūku iela     14     110.0  POINT (24.25629 56.87265)  56.872648  24.256293          3.0  dārziņi  https://apkaimes.lv/darzini/
2  pūku iela 12  pūku iela     12     110.0  POINT (24.25618 56.87248)  56.872484  24.256180          3.0  dārziņi  https://apkaimes.lv/darzini/
3  pūku iela 10  pūku iela     10     110.0  POINT (24.25602 56.87228)  56.872280  24.256022          3.0  dārziņi  https://apkaimes.lv/darzini/
4   pūku iela 2  pūku iela      2     110.0  POINT (24.25694 56.87278)  56.872777  24.256936          3.0  dārziņi  https://apkaimes.lv/darzini/
5   pūku iela 4  pūku iela      4     110.0  POINT (24.25680 56.87260)  56.872602  24.256800          3.0  dārziņi  https://apkaimes.lv/darzini/
```

## CLI Usage

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `search-by-address`
* `search-by-code`
* `search-by-name`
* `search-by-number`
* `search-by-street`
* `search-multiple`

## `search-by-address`

**Usage**:

```console
$ search-by-address [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-code`

**Usage**:

```console
$ search-by-code [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-name`

**Usage**:

```console
$ search-by-name [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-number`

**Usage**:

```console
$ search-by-number [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-street`

**Usage**:

```console
$ search-by-street [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-multiple`

**Usage**:

```console
$ search-multiple [OPTIONS]
```

**Options**:

* `--address TEXT`
* `--name TEXT`
* `--street TEXT`
* `--number TEXT`
* `--code TEXT`
* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.
