osm_where
=========

Simple tool to get [GeoURI](https://geouri.org/) for given
location identified by URL or by its name (not 100% reliable, as
we don’t have any interface to choose between multiple options).

Currently defaults to looking at Ukraine.

**Quick Start**:
```bash
# Get help message
python src/osm_where.py --help

# Query by URL
python src/osm_where.py https://www.openstreetmap.org/node/4126283179

# Query by place name
python src/osm_where.py --name Kropyvnytskyi
```

All issues, questions, complaints, or (even better!) patches
should be send via [email to me](mailto:mcepl@cepl.eu) (for
patches use [git send-email](https://git-send-email.io/)).
