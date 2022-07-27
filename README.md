# Python dependency pinner

Too often, I see dependencies pinned at version `*` in Pipfile and pyproject.toml
files. This is a terrible practice, and is quite exactly the road to dependency hell. 
Any time you want to update a single dependency, you end up updating all your dependencies 
to their latest version, which usually includes some backwards incompatible major version 
bumps. If you have more than one dependency, trying to comprehend all of the changes that
were just installed and verifying that they all worked is overwhelmingly cumbersome.

So, I wrote two small, untested, no-dependency python scripts to replace the `*` in the 
dependency file with whatever version is listed for that dependency in the lock file.
I configured the dependencies to allow _patch_ updates whenever dependencies are updated,
but not minor or major updates.
