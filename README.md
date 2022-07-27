# Python dependency pinner

Sometimes, dependencies are pinned at version `*` in Pipfile and pyproject.toml
files. This is a terrible practice, resulting in dependency hell. 
Any time you want to update a single dependency, you end up updating _all_ your dependencies 
to their latest version, which usually includes some backwards incompatible major version 
bumps. If you have more than one dependency, trying to comprehend all of the changes that
were just installed and verifying that they all worked is overwhelmingly cumbersome.

I faced this dependency hell several times at my previous job. I wrote these
scripts so I could pin dependencies any time I came across a project that used
the `*` dependency version pattern and thus keep my sanity.

So, I wrote two small, untested, no-dependency python scripts to replace the `*` in the 
dependency file with whatever version is listed for that dependency in the lock file.
I configured the dependencies to allow _patch_ updates whenever dependencies are updated,
but not minor or major updates.

These scripts were written at different times and have different output formats.
Maybe someday I'll get around to making them look similar. 

Disclaimer: I've only run these scripts a handful of times. They're not robust,
probably have bugs, and won't handle every usecase. Feel free to make suggestions
or extend them at your own discretion.

## Usage

For pinning pipenv projects, make sure you are in the directory that has the Pipfile
and Pipfile.lock and then run:

```
python /path/to/pipfile_pinner.py
```

For pinning poetry projects, make sure you are in the directory that has the pyproject.toml
and poetry.lock file and then run:
```
python /path/to/poetry_pinner.py
```
