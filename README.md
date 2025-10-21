# AI jammer

This is a simple AI honeypot that does nothing but generate nonsense webpages that AI crawlers will eat up, wasting their resources and reducing their models' efficacy. It's ideal to run this on its own dedicated server and only connect a subdomain or domain that you don't care about to it.

You can run an instance yourself on your own server by installing [poetry](https://python-poetry.org) (I recommend using [pipx](https://pipx.pypa.io) to do so), and then clone this repo. Inside the directory you can run `./start.sh` to start the server up, and then route your fronting webserver to do a reverse proxy to `http://127.0.0.1:8000`. `start.sh` can also be given optional parameters for `hypercorn`, such as `--bind` to use an alternate port or a UNIX socket.

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

and add whatever SSL configuration is appropriate for your setup.

I am running a public instance at IP address [170.187.142.27](http://170.187.142.27) which you can feel free to map any hostname to it, although for https you'll have to run your own termination to it. The [Cloudflare](https://cloudflare.com/) free plan can automatically enable https termination for this as well.

