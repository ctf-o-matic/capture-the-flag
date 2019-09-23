ctfsite
=======

A Django project to use as the central hub of a Capture The Flag competition.

Initialize content
------------------

Create JSON files:

- Generate servers data by running the script `$PROJECT/gen-leaderboard-servers.sh`
  from inside the terraform workspace of the deployment environment,
  store in `servers.json` file.

- Generate levels data with `./gen-leaderboard-levels.sh` script
  in image builder, store in `levels.json` file.

- Manually edit the old `users.json` file, create entries appropriately

Copy the JSON files to deployment, and import them with:

    ./manage.sh loaddata path/to/each.json
