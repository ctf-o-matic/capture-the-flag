ctfsite
=======

A Django project to use as the central hub of a Capture The Flag competition.

Initialize content
------------------

An easy way to create the content is to configure in the dev environment,
dump the relevant tables as JSON, and load them on the server.

Create data in dev environment:

- Find the IP addresses: login on Google Cloud Console, go to Compute Engine

- On Django Admin, delete and create Server instances appropriately

Create JSON files:

- Dump the Server instances with `./manage.sh dumpdata leaderboard.server | jq . > tmp/servers.json`

- Generate levels data with `./gen-leaderboard-levels.sh` script
  in image builder, store in `levels.json` file.

- Manually edit the old `users.json` file, create entries appropriately

Copy the JSON files to deployment, and import them with:

    ./manage.sh loaddata path/to/each.json
