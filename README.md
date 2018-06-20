## Makeshift Courseradl

Generally I use coursera-dl to download coursera courses, but one fine day I tried using it and it failed it turns out Coursera.org revamped their API which rendered coursera-dl broken, so I reverse-engineered the new API and wrote this script, as I needed video lectures only this script does not download quizzes and subtiles.

### Usage

- Go through the comments in the script and substitute values for some variables as appropriate.

- The script can download individual course as well as whole specialization, it correctly renames downloaded lectures and makes appropriate directories per course.

- check out the originally reported issue on coursera-dl page [here](https://github.com/coursera-dl/coursera-dl/issues/673)
