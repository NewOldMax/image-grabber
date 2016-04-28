# Image Grabber Application (Docker)

Build environment
----------------

    docker-compose build

Start Application
----------------

    docker-compose up

Start using at
----------------

    http://localhost:8082

Go to ``/createtbl`` to create tables in database.

Go to ``/droptbl`` to drop all tables.

At this moment, safe to use "Single page" work type (correct work with WebSockets and image count).

"Web Crawler" work type buggy and unstoppable (grab all images of all pages).