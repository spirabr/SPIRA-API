# SPIRA-API

## Project Overview
This is a multi-container project used to serve inference requests to ML models and register their predictions in the context of the research project [SPIRA](https://spira.ime.usp.br/coleta/).


The source code is contained in the directory `src`.

The containers used in this project and their connections are configured in the file  `docker-compose.yml`.

The tests are contained in the `tests` directory.



## Environment Variables

The file `docker-compose.yml` also specifies the necessary env files for the project, that should be contained in the `envs` directory.

The variables of each env file are the same as the attributes of the classes declared in `src/settings.py`. The main application uses pydantic to directly bind the environment variables to the respective attributes of the Settings classes. Additional environment files for the services other than the main one are specified by their respective documentations and the files should also be contained in in the `envs` directory.

## Dependencies

Dependency management is done with [`poetry`](https://python-poetry.org/docs/) and they are configured in the file `poetry.lock`. Dependencies can be added and removed using the poetry cli. 

## Running the project

Build the docker-compose:

```
docker-compose build
```

Run the docker-compose:

```
docker-compose up
```

Run the tests:

```
make -f tests.mk
```
