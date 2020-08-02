# Download-Tasks-For-Youtube
Make tasks to downloads youtube videos or musics, and tries to run the tasks regularly until you have some connexion. (uses cron to do so)

Ever tried to watch videos or listen to some musics on youtube with a bad connexion? **It sucks.**
You can still try to download the musics or videos yourself but doing it one video at a time is not a fun way to spend your time either.
Worst! You might have such a bad connexion that you have to try and wait for hours before it starts even being possible to download a video or a music.

So here comes this repo.
Put your urls in a txt file, setup a cron job and wait.
When you come back your videos and musics will be downloaded and the urls will be cleared for new videos or musics to download.

This program will try to download the videos or musics every 5 minutes or so (you choose by setting up the cron job) until the download is successful.

# Q&A
* Why not try to make a cron job to download the videos without this program at all?

=> If the download is successful you don't want to download the videos twice or more, that's why there is a task list.
