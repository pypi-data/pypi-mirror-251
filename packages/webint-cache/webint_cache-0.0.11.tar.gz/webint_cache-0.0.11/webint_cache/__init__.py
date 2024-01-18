""""""

import collections
import hashlib
import logging
import os
import pathlib
import subprocess
import time

import PIL
import requests
import web
import webagt
import whois
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from web import tx

from .silos import silos

logging.basicConfig(level=logging.DEBUG, filename="crawl.log", filemode="w", force=True)

app = web.application(
    __name__,
    prefix="cache",
    args={
        "site": r"[a-z\d.-]+\.[a-z]+",
        "page": r".*",
    },
    model={
        "cache": {
            "url": "TEXT UNIQUE NOT NULL",
            "crawled": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "details": "JSON NOT NULL",
        },
        "cache_redirects": {
            "incoming": "TEXT UNIQUE NOT NULL",
            "outgoing": "TEXT NOT NULL",
        },
    },
)

sites_path = pathlib.Path("sites")
sites_path.mkdir(exist_ok=True)

agent = webagt.Agent("webint-cache")
blocklist = ["accounts.google.com"]
ignored_rels = [
    "author",
    "bookmark",
    "canonical",
    "category",
    "contents",
    "home",
    "nofollow",
    "noreferrer",
    "noopener",
    "pingback",
    "profile",
    "shortcut",
    "shortlink",
    "syndication",
    "tag",
    "ugc",
]
social_network_rels = ["acquaintance", "colleague", "friend", "met"]

# def refresh_page(url):
#     try:
#         response = agent.get(domain)
#     except (requests.ConnectionError, requests.Timeout) as err:
#         return {"status": "not responding", "error": str(err)}
#     try:
#         tx.db.insert(
#             "cache",
#             url=url,
#             details={
#                 "metaverse":
#                   hashlib.sha256(domain.encode("utf-8")).hexdigest().upper(),
#                 "domain": {
#                     "name": domain,
#                     "suffix": domain_details.suffix,
#                     "hsts": domain_details.in_hsts,
#                 },
#             },
#         )
#         web.enqueue(query_whois, domain)
#     except tx.db.IntegrityError:
#         pass
#     return


def refresh_site(domain):
    """Fetch `domain` and store site details and related media."""
    if domain in blocklist or not webagt.uri(domain).suffix:
        logging.debug(f"skipping {domain}")
        return
    # TODO logging.debug("getting previous details..")  # for etag
    start = time.time()
    logging.debug("downloading HTML..")
    try:
        response = agent.get(domain)
    except (requests.ConnectionError, requests.Timeout) as err:
        return {"status": "not responding", "error": str(err)}
    if domain != response.url.host:
        try:
            tx.db.insert("cache_redirects", incoming=domain, outgoing=response.url.host)
        except tx.db.IntegrityError:
            tx.db.update(
                "cache_redirects",
                outgoing=response.url.host,
                where="incoming = ?",
                vals=[domain],
            )
        refresh_site(response.url.host)
        return
    domain_details = webagt.uri(domain)
    try:
        tx.db.insert(
            "cache",
            url=domain,
            details={
                "metaverse": hashlib.sha256(domain.encode("utf-8")).hexdigest().upper(),
                "domain": {
                    "name": domain,
                    "suffix": domain_details.suffix,
                    "hsts": domain_details.in_hsts,
                },
            },
        )
        web.enqueue(query_whois, domain)
    except tx.db.IntegrityError:
        pass
    site_path = sites_path / domain
    site_path.mkdir(parents=True, exist_ok=True)

    web.enqueue(run_lighthouse, domain)
    web.enqueue(run_pa11y, domain)

    update_details = get_updater(domain)
    update_details(
        accessed=web.now().to_iso8601_string(),
        response={
            "status": response.status,
            "time": time.time() - start,
            "headers": dict(response.headers),
            "length": round(len(response.text) / 1000),
        },
    )
    logging.debug("parsing Microformats..")
    mf2json = response.mf2json
    rels = dict(mf2json["rels"])

    if authorization_endpoint := rels.pop("authorization_endpoint", None):
        indieauth_details = {"authorization_endpoint": authorization_endpoint}
        if token_endpoint := rels.pop("token_endpoint", None):
            indieauth_details["token_endpoint"] = token_endpoint
        update_details(indieauth=indieauth_details)
    if indieauth_metadata_endpoint := rels.pop("indieauth-metadata", None):
        web.enqueue(get_indieauth_metadata, domain, indieauth_metadata_endpoint[0])

    if search := rels.pop("search", None):
        web.enqueue(get_search_description, domain, search[0])

    if manifest := rels.pop("manifest", None):
        web.enqueue(get_manifest, domain, manifest[0])

    if hub_endpoint := rels.pop("hub", None):
        web.enqueue(
            get_websub_hub, domain, hub_endpoint[0], rels.pop("self", [domain])[0]
        )

    web.enqueue(get_activitypub, domain)

    card = response.card
    update_details(mf2json=mf2json, card=card, rels=rels)
    photo_url = rels.pop("apple-touch-icon", None)
    card_type = None
    if card:
        card_type = "person"
        if card_org := card.get("org"):
            if card["name"][0] == card_org[0]:
                card_type = "organization"
        if emails := card.get("email"):
            gravatars = {}
            for email in emails:
                email = email.removeprefix("mailto:")
                gravatars[email] = hashlib.md5(
                    email.strip().lower().encode("utf-8")
                ).hexdigest()
            # TODO SET `gravatars`
        if photo_urls := card.get("photo"):  # TODO move to on-demand like icon?
            if isinstance(photo_urls[0], dict):
                photo_url = photo_urls[0]["value"]
            else:
                photo_url = photo_urls[0]
    try:
        icon_url = rels.pop("icon")[0]
    except KeyError:
        icon_url = f"{domain}/favicon.ico"
    web.enqueue(get_media, domain, photo_url, icon_url)

    scripts = []
    for script in response.dom.select("script"):
        script_details = dict(script.element.attrib)
        script_details["content_length"] = len(script.text)
        script_details["text"] = script.text
        scripts.append(script_details)
    stylesheets = rels.pop("stylesheet", [])
    for stylesheet in response.dom.select("style"):
        stylesheets.append(
            {
                "content_length": len(stylesheet.text),
                "text": stylesheet.text,
            }
        )
    whostyle = rels.pop("whostyle", None)
    try:
        title = response.dom.select("title")[0].text
    except IndexError:
        title = ""
    update_details(
        scripts=scripts, stylesheets=stylesheets, whostyle=whostyle, title=title
    )

    for ignored_rel in ignored_rels:
        rels.pop(ignored_rel, None)
    social_network = {}
    for social_network_rel in social_network_rels:
        if people_rels := rels.pop(social_network_rel, None):
            social_network[social_network_rel] = people_rels
    logging.debug("determining reciprocal rel=me..")
    reciprocals = set()
    rel_me_silos = []
    for silo, silo_details in silos.items():
        if len(silo_details) == 3:
            rel_me_silos.append(silo_details[0])
    rel_mes = rels.pop("me", [])
    url = webagt.uri(domain)  # TODO XXX
    for me_url in rel_mes:
        if not me_url.startswith(("http", "https")):
            continue
        me_url = webagt.uri(me_url)
        logging.debug(f"  rel=me {me_url}")
        # XXX if (me_url.domain, me_url.suffix) == ("twitter", "com"):
        # XXX     if "/" in me_url.path:
        # XXX         continue
        # XXX     twitter_id = me_url.path.split("/")[0]
        # XXX     twitter_bearer = app.cfg.get("TWITTER")
        # XXX     print(
        # XXX         agent.get(
        # XXX             f"https://api.twitter.com/2/users"
        # XXX             f"/by/username/{twitter_id}?user.fields=url",
        # XXX             headers={"Authorization": f"Bearer {twitter_bearer}"},
        # XXX         ).json
        # XXX     )
        # XXX     twitter_profile = agent.get(
        # XXX         f"https://api.twitter.com/2/users"
        # XXX         f"/by/username/{twitter_id}?user.fields=url",
        # XXX         headers={"Authorization": f"Bearer {twitter_bearer}"},
        # XXX     ).json["data"]
        # XXX     if twitter_profile_url := twitter_profile.get("url", None):
        # XXX         try:
        # XXX             recip_url = agent.get(twitter_profile_url).url
        # XXX         except requests.Timeout:
        # XXX             continue
        # XXX         if recip_url == url:
        # XXX             reciprocals.add(me_url.minimized)
        if (me_url.subdomain, me_url.domain, me_url.suffix) == (
            "en",
            "wikipedia",
            "org",
        ):
            wp_props = agent.get(me_url).mf2json["items"][0]["properties"]
            if wp_url := wp_props.get("url"):
                if wp_url[0] == url:
                    reciprocals.add(me_url.minimized)
        if me_url.host not in rel_me_silos:
            continue
        try:
            reverse_rel_mes = agent.get(me_url).mf2json["rels"]["me"]
        except KeyError:
            continue
        for reverse_rel_me in reverse_rel_mes:
            if webagt.uri(reverse_rel_me).minimized == url.minimized:
                reciprocals.add(me_url.minimized)
    update_details(
        social_network=social_network, reciprocals=list(reciprocals), rel_me=rel_mes
    )

    feed = response.feed
    alt_feed_urls = set()
    if not feed["items"]:
        try:
            alt_feed_urls = set(rels["home"]) & set(rels["alternate"])
        except KeyError:
            pass
    alternate_reprs = rels.pop("alternate", [])
    alternate_feeds = rels.pop("feed", [])
    if not feed["items"]:
        for alt_feed_url in alternate_reprs + alternate_feeds:
            try:
                feed = agent.get(alt_feed_url).feed
            except ValueError:  # XML feed
                pass
            finally:
                print("using", alt_feed_url)
    # rels.pop("alternate", None)
    for entry in feed["items"]:
        try:
            published = entry["published"]
            permalink = entry["url"]
            entry.pop("published-str")
        except KeyError:
            continue
        entry.pop("uid", None)
        # TODO refresh_page(permalink)
    update_details(feed=feed)

    # logging.debug("archiving to WARC..")
    # warc_file = site_path / "warc_output"
    # subprocess.run(
    #     [
    #         "wget",
    #         "-EHkpq",
    #         site,
    #         f"--warc-file={warc_file}",
    #         "--no-warc-compression",
    #         "--delete-after",
    #     ]
    # )

    logging.debug("calculating IndieMark score..")
    scores = [
        [(3, None)] * 10,
        [(3, None)] * 10,
        [(3, None)] * 10,
        [(3, None)] * 10,
        [(3, None)] * 10,
    ]

    # L1 Identity
    if card:
        if "icon" in rels:
            scores[0][0] = (0, "contact info and icon on home page")
        else:
            scores[0][0] = (1, "contact info but no icon on home page")
    else:
        scores[0][0] = (2, "no contact info on home page")

    # L1 Authentication
    if rel_mes:
        scores[0][1] = (
            1,
            "<code>rel=me</code>s found but none for GitHub or Twitter",
        )
        for rel_me in rel_mes:
            if rel_me.startswith(("https://github.com", "https://twitter.com/")):
                scores[0][1] = (
                    0,
                    "<code>rel=me</code>s found for GitHub and/or Twitter",
                )
                break
    else:
        scores[0][1] = (2, "no <code>rel=me</code>s found")

    # L1 Posts
    if feed["items"]:
        if len(feed["items"]) > 1:
            scores[0][2] = (0, "more than one post")
        else:
            scores[0][2] = (1, "only one post")
    else:
        scores[0][2] = (2, "no posts")

    # L1 Search
    # XXX if details["ddg"]:
    # XXX     scores[0][6] = (0, "your content was found on DuckDuckgo")
    # XXX else:
    # XXX     scores[0][6] = (
    # XXX         1,
    # XXX         "your content was <strong>not</strong> found on DuckDuckgo",
    # XXX     )

    # L1 Interactivity
    scores[0][8] = (0, "content is accessible (select/copy text/permalinks)")

    # L2 Identity
    scores[1][0] = (0, "you've linked to silo profiles")

    # L3 'h-card contact info and icon on homepage'
    # L3 'multiple post types'
    # L3 'POSSE'
    # L3 'Posting UI'
    # L3 'Next/Previus Navigation between posts'
    # L3 'Search box on your site'
    # L3 'Embeds/aggregation'
    # L3 'Web Actions'

    # L4 'Send Webmentions'
    # L4 'PubSubHubbub support'
    # L4 'Display Search Results on your site'
    # L4 'Display Reply Context'

    # L5 'Automatic Webmentions'
    # L5 'Handle Webmentions'
    # L5 'Display full content rich reply-contexts'
    # L5 'Search on your own search backend'
    # L5 'Multiple Reply Types'
    # L5 'Display Backfeed of Comments'

    update_details(scores=scores)
    # logging.debug("dumping details..")
    # details["stored"] = web.now().to_iso8601_string()
    web.dump(scores, path=site_path / "scores.json")
    logging.debug("generating scoreboard..")
    subprocess.run(["node", "../index.js", domain])


def get_updater(url):
    """Return an update function catered to `domain`."""

    def update_details(**kwargs):
        """Atomically update the resource's details with `kwargs`."""
        keys = ", ".join([f"'$.{key}', json(?)" for key in kwargs.keys()])
        tx.db.update(
            "cache",
            what=f"details = json_set(details, {keys})",
            where="url = ?",
            vals=[web.dump(v) for v in kwargs.values()] + [url],
        )

    return update_details


def query_whois(domain):
    """Update the creation date for the domain."""
    logging.debug("querying WHOIS")
    domain_created = whois.whois(domain)["creation_date"]
    if isinstance(domain_created, list):
        domain_created = domain_created[0]
    try:
        domain_created = domain_created.isoformat()
    except AttributeError:
        pass
    get_updater(domain)(**{"domain.created": domain_created})


def get_media(domain, photo_url, icon_url):
    """Download the representative photo for the domain."""
    site_path = sites_path / domain
    if photo_url:
        logging.debug("downloading representative photo..")
        filename = photo_url.rpartition("/")[2]
        suffix = filename.rpartition(".")[2]
        if not suffix:
            suffix = "jpg"
        original = site_path / f"photo.{suffix}"
        webagt.download(photo_url, original)
        final = site_path / "photo.png"
        if suffix != "png":
            if suffix == "svg":
                drawing = svg2rlg(original)
                renderPM.drawToFile(drawing, final, fmt="PNG")
            else:
                try:
                    image = PIL.Image.open(original)
                except PIL.UnidentifiedImageError:
                    pass
                else:
                    image.save(final)
    logging.debug("downloading iconography..")
    final = site_path / "icon.png"
    filename = icon_url.rpartition("/")[2]
    suffix = filename.rpartition(".")[2]
    original = site_path / f"icon.{suffix}"
    try:
        download = webagt.download(icon_url, original)
    except web.ConnectionError:
        pass
    else:
        if download.status == 200 and suffix != "png":
            try:
                image = PIL.Image.open(original)
            except PIL.UnidentifiedImageError:
                pass
            else:
                image.save(final)


def get_indieauth_metadata(domain, indieauth_metadata_endpoint):
    """Download IndieAuth metadata for the domain."""
    logging.debug("downloading IndieAuth metadata..")
    metadata = agent.get(indieauth_metadata_endpoint).json
    get_updater(domain)(**{"indieauth": {"metadata": metadata}})


def get_search_description(domain, search_url):
    """Download OpenSearch description document at `search_url`."""
    logging.debug("downloading OpenSearch description..")
    search_xml = agent.get(search_url).xml
    search_url = webagt.uri(search_xml.find("Url", search_xml.nsmap).attrib["template"])
    search_endpoint = f"//{search_url.host}/{search_url.path}"
    name = None
    for name, values in search_url.query.items():
        if values[0] == "{template}":
            break
    get_updater(domain)(**{"search_url": [search_endpoint, name]})


def get_manifest(domain, manifest_url):
    """Download site manifest at `manifest_url`."""
    logging.debug("downloading site manifest..")
    # if "patches" in web.get(manifest_url).headers:
    #     get_updater(domain)(**{"manifest": "hot"})
    webagt.download(manifest_url, sites_path / domain / "manifest.json")


def get_websub_hub(domain, endpoint, self):
    """Subscribe to site via WebSub `endpoint`."""
    # TODO subscribe if not already
    logging.debug("subscribing to WebSub hub..")
    get_updater(domain)(**{"hub": [endpoint, self]})


def run_lighthouse(domain):
    """Run lighthouse for the domain."""
    logging.debug("running lighthouse..")
    subprocess.Popen(
        [
            "lighthouse",
            f"https://{domain}",
            "--output=json",
            f"--output-path={sites_path}/{domain}/audits.json",
            "--only-audits=total-byte-weight",
            '--chrome-flags="--headless"',
            "--quiet",
        ],
        stdout=subprocess.PIPE,
    ).stdout.read()


def run_pa11y(domain):
    """Run pa11y for the domain."""
    site_path = sites_path / domain

    bindir = pathlib.Path("/usr/bin")
    if (bindir / "google-chrome").exists():
        binname = "google-chrome"
    elif (bindir / "chromium").exists():
        binname = "chromium"
    else:
        return

    config = pathlib.Path.home() / ".pa11y.json"
    if not config.exists():
        with config.open("w") as fp:
            fp.write(
                f"""{{
                  "chromeLaunchConfig": {{
                    "executablePath": "/usr/bin/{binname}",
                    "ignoreHTTPSErrors": false
                  }}
                }}"""
            )

    logging.debug("running pa11y..")
    web.dump(
        web.load(
            subprocess.Popen(
                [
                    "pa11y",
                    domain,
                    "--config",
                    "/home/admin/.pa11y.json",
                    "--reporter",
                    "json",
                    "--screen-capture",
                    site_path / "site.png",
                ],
                stdout=subprocess.PIPE,
            ).stdout.read()
        ),
        path=site_path / "a11y.json",
    )

    found_icon = True  # TODO XXX
    logging.debug("finding most used color, generating images..")
    try:
        screenshot = PIL.Image.open(site_path / "site.png")
    except FileNotFoundError:
        pass
    else:
        screenshot.crop((0, 0, 1280, 1024)).save(site_path / "screenshot.png")
        colors = collections.Counter()
        for x in range(screenshot.width):
            for y in range(screenshot.height):
                colors[screenshot.getpixel((x, y))] += 1
        most_used_color = colors.most_common()[0][0]
        icon = PIL.Image.new("RGB", (1, 1), color=most_used_color)
        if not found_icon:
            icon.save(site_path / "icon.png")
        if not (site_path / "photo.png").exists():
            icon.save(site_path / "photo.png")


def get_activitypub(domain):
    webfinger = agent.get(f"https://{domain}/.well-known/webfinger")


@app.query
def get_posts(db):
    return []


@app.query
def get_people(db):
    return {
        url: details["card"]
        for url, details in tx.db.select("cache", what="url, details", order="url ASC")
    }


@app.query
def get_people_details(db):
    return tx.db.select("people", order="url ASC")


@app.query
def get_categories(db):
    categories = collections.Counter()
    with db.transaction as cur:
        for post in cur.cur.execute(
            "select json_extract(cache.details, '$.category') "
            "AS categories from cache"
        ):
            if not post["categories"]:
                continue
            if post_categories := web.load(post["categories"]):
                for post_category in post_categories:
                    categories[post_category] += 1
    return categories


@app.query
def get_resources(db):
    return db.select(
        "cache",
        where="crawled > ?",
        vals=[web.now().subtract(days=7)],
        order="crawled DESC",
    )


@app.control("")
class Cache:
    """All cached resources."""

    def get(self):
        """Return a list of all cached resources."""
        return app.view.index()

    def post(self):
        address = web.form("address").address
        details = get_resource(address)
        raise web.SeeOther(f"/cache/{address}")

        # TODO if no-flash-header or use form argument:
        # TODO     raise web.SeeOther(); flash user's session with message to insert as CSS
        # TODO elif flash-header:
        # TODO     return just message as JSON
        # TODO
        # TODO raise web.flash("crawl enqueued")


@app.control("resource")
class PreviewResource:
    """"""

    def get(self):
        url = web.form(url=None).url
        web.header("Content-Type", "application/json")
        if not url:
            return {}
        resource = web.get(url)
        if resource.entry:
            return resource.entry
        if resource.event:
            return resource.event
        if resource.feed:
            return resource.feed
        return {}

        # XXX data = cache.parse(url)
        # XXX if "license" in data["data"]["rels"]:
        # XXX     data["license"] = data["data"]["rels"]["license"][0]
        # XXX try:
        # XXX     edit_page = data["html"].cssselect("#ca-viewsource a")[0]
        # XXX except IndexError:
        # XXX     # h = html2text.HTML2Text()
        # XXX     # try:
        # XXX     #     data["content"] = h.handle(data["entry"]["content"]).strip()
        # XXX     # except KeyError:
        # XXX     #     pass
        # XXX     try:
        # XXX         markdown_input = ("html", data["entry"]["content"])
        # XXX     except (KeyError, TypeError):
        # XXX         markdown_input = None
        # XXX else:
        # XXX     edit_url = web.uri.parse(str(data["url"]))
        # XXX     edit_url.path = edit_page.attrib["href"]
        # XXX     edit_page = fromstring(requests.get(edit_url).text)
        # XXX     data["mediawiki"] = edit_page.cssselect("#wpTextbox1")[0].value
        # XXX     data["mediawiki"] = (
        # XXX         data["mediawiki"].replace("{{", r"{!{").replace("}}", r"}!}")
        # XXX     )
        # XXX     markdown_input = ("mediawiki", data["mediawiki"])

        # XXX if markdown_input:
        # XXX     markdown = str(
        # XXX         sh.pandoc(
        # XXX         "-f", markdown_input[0], "-t", "markdown", _in=markdown_input[1]
        # XXX         )
        # XXX     )
        # XXX     for n in range(1, 5):
        # XXX         indent = "    " * n
        # XXX         markdown = markdown.replace(f"\n{indent}-",
        # XXX                                     f"\n{indent}\n{indent}-")
        # XXX     markdown = re.sub(r'\[(\w+)\]\(\w+ "wikilink"\)', r"[[\1]]", markdown)
        # XXX     markdown = markdown.replace("–", "--")
        # XXX     markdown = markdown.replace("—", "---")
        # XXX     data["content"] = markdown

        # XXX data.pop("html")
        # XXX # XXX data["category"] = list(set(data["entry"].get("category", [])))
        # XXX web.header("Content-Type", "application/json")
        # XXX return dump_json(data)


@app.control("details/{site}(/{page})?")
class SiteDetails:
    """A web resource."""

    def get(self, site, page=None):
        web.header("Content-Type", "application/json")
        return tx.db.select("cache", where="url = ?", vals=[site])[0]["details"]


@app.control("a11y/{site}(/{page})?")
class Accessibility:
    """A web resource."""

    def get(self, site, page=None):
        try:
            a11y = web.load(path=sites_path / site / "a11y.json")
        except FileNotFoundError:
            a11y = None
        return app.view.a11y(site, a11y)


@app.control("sites")
class Sites:
    """Index of sites as HTML."""

    def get(self):
        """Return a list of indexed sites."""
        # TODO # accept a
        # TODO tx.db.select(
        # TODO     tx.db.subquery(
        # TODO         "crawls", where="url not like '%/%'", order="crawled desc"
        # TODO     ),
        # TODO     group="url",
        # TODO )
        with tx.db.transaction as cur:
            urls = cur.cur.execute(
                " select * from ("
                + "select * from cache where url not like '%/%' order by crawled desc"
                + ") group by url"
            )
        return app.view.sites(urls)


@app.control("sites/{site}/screenshot.png")
class SiteScreenshot:
    """A site's screenshot."""

    def get(self, site):
        """Return a PNG document rendering given site's screenshot."""
        if os.getenv("WEBCTX") == "dev":
            return sites_path / site / "screenshot.png"
        web.header("Content-Type", "image/png")
        web.header("X-Accel-Redirect", f"/X/sites/{site}/screenshot.png")


@app.control("sites/{site}/scoreboard.svg")
class SiteScoreboard:
    """A site's scoreboard."""

    def get(self, site):
        """Return an SVG document rendering given site's scoreboard."""
        if os.getenv("WEBCTX") == "dev":
            return sites_path / site / "scoreboard.svg"
        web.header("Content-Type", "image/svg+xml")
        web.header("X-Accel-Redirect", f"/X/sites/{site}/scoreboard.svg")


@app.control("{site}")
class Site:
    """A website."""

    def get(self, site):
        """Return a site analysis."""
        # TODO if site in [s[0] for s in silos.values()]:
        # TODO     return app.view.silo(site, details)
        return app.view.site(*get_site(site))


@app.control("{site}/{page}")
class Page:
    """A webpage."""

    def get(self, site, page):
        return app.view.page(*get_page(f"{site}/{page}"))


def get_resource(url):
    url = webagt.uri(str(url))
    min_url = url.minimized
    redirect = tx.db.select(
        "cache_redirects", what="outgoing", where="incoming = ?", vals=[min_url]
    )
    try:
        raise web.SeeOther(redirect[0]["outgoing"])
    except IndexError:
        pass
    try:
        details = tx.db.select("cache", where="url = ?", vals=[min_url])[0]["details"]
    except IndexError:
        web.enqueue(refresh_site, min_url)
        raise web.Accepted(app.view.crawl_enqueued(min_url))
    return url, details


def get_site(site):
    url, details = get_resource(site)
    try:
        audits = web.load(path=sites_path / site / "audits.json")
    except FileNotFoundError:
        audits = None
    try:
        a11y = web.load(path=sites_path / site / "a11y.json")
    except FileNotFoundError:
        a11y = None
    try:
        manifest = web.load(path=sites_path / site / "manifest.json")
    except FileNotFoundError:
        manifest = None
    return url, details, audits, a11y, manifest


def get_page(page_url):
    url, details = get_resource(page_url)
    return url, details
