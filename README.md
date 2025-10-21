# AI jammer

This is a simple AI honeypot that does nothing but generate nonsense webpages that AI crawlers will eat up, wasting their resources and reducing their models' efficacy. It's ideal to run this on its own dedicated server and only connect a subdomain or domain that you don't care about to it.

You can run an instance yourself on your own server by installing [poetry](https://python-poetry.org) (I recommend using [pipx](https://pipx.pypa.io) to do so), and then clone this repo. Inside the directory you can run `./start.sh` to start the server up, and then route your fronting webserver to do a reverse proxy to `http://127.0.0.1:8000`. `start.sh` can also be given optional parameters for [hypercorn](https://hypercorn.readthedocs.io), such as [`--bind`](https://hypercorn.readthedocs.io/en/latest/how_to_guides/binds.html) to use an alternate port or a UNIX socket.

For your nginx configuration, you can do something like:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location / {
        proxy_pass "http://127.0.0.1:8000";
    }
}
```

and add whatever SSL configuration is appropriate for your setup. Then have a hidden link on your website that points to the tarpit, and cackle with glee as AI scrapers and other such nonsense gets mired in the muck.

Here are some public instances you can use:

* @fluffy-critter - [170.187.142.27](http://170.187.142.27)

    You can theoretically map any hostname to this, but for https to work you'll need to run your own fronting proxy. Cloudflare should Just Work™ with it.

If you also run a public instance, please let me know and I can add it to the list!