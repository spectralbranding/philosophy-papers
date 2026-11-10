"""Persistence-content coding for the IBM / Red Hat perimeter-event (2019-07-09).

This is the SECOND half of the dual coding specified in `../CASE_FILE.md` §3. It is run
against sources that share NO document with the legal-perimeter coding: the legal side
came from SEC filings (Exhibit 21.1, the merger 8-K set, the merger proxy); this side
comes from product release engineering metadata published by the distribution itself,
authored by packagers for package managers, with no reference to corporate structure.

THE CODING QUESTION (fixed before the data was fetched, `CASE_FILE.md` §3.2):

    Would the firm's principal products still be producible six months from now if this
    item vanished, holding all owned assets and all personnel constant?

Counterfactual necessity, NOT value. Coding on value would key on valuation difficulty,
which is exactly the variable Iacobucci & Triantis (2007) say drives perimeter placement
-- see `../../PHASE_2_NOTES.md` Q3. That constraint is why the operational proxy below is
provenance-of-upstream and not anything resembling importance, revenue or replacement cost.

UNIT: one source package (SRPM) of Red Hat Enterprise Linux 8.0, the principal product,
released 2019-05-07 -- inside the window between the last audited subsidiary list
(2019-02-28) and the perimeter-event (2019-07-09).

DATA: `repodata/primary.xml.gz` for the BaseOS and AppStream *Source* repositories of
CentOS 8.0.1905, the public rebuild of RHEL 8.0, from vault.centos.org. Downloaded to
`../data/`. The RHEL binaries themselves are subscription-gated; the rebuild is
package-for-package the same source composition and is the publicly checkable form.

OPERATIONAL PROXY, and its direction of error:

    A package is coded INSIDE when its upstream `<url>` is on a Red-Hat-controlled or
    Red-Hat-sponsored host, and OUTSIDE otherwise.

This is deliberately GENEROUS TO THE PERIMETER. None of redhat.com, fedoraproject.org,
pagure.io or centos.org is an entity on the subsidiary list -- the Fedora Project is not a
subsidiary of anything -- so counting them as INSIDE credits the perimeter with content it
does not legally contain. If the finding survives a coding rigged against it, it is not an
artefact of the coding. A second sensitivity pass reclassifies EVERY github.com package as
INSIDE, which is far past defensible, to establish a floor.

WHAT WOULD FALSIFY THE THESIS ON THIS CASE: a product whose source composition is
dominated by components originating inside the firm. That is not a hypothetical -- it is
what this script would report for a vertically integrated proprietary vendor. The
measurement can fail, and the pre-registered failure condition is INSIDE > .500.

Run:
    uv run python code/code_persistence_content.py

Deterministic; no network, no randomness. Reads only the two files in ../data/.
"""

from __future__ import annotations

import collections
import gzip
import pathlib
import re
import xml.etree.ElementTree as ET

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
NS = {
    "c": "http://linux.duke.edu/metadata/common",
    "rpm": "http://linux.duke.edu/metadata/rpm",
}

# Pre-registered as Red-Hat-controlled or Red-Hat-sponsored. Note that NONE of these is an
# entity on the audited subsidiary list; they are counted INSIDE to bias against the thesis.
REDHAT_HOSTS = (
    "redhat.com",
    "fedoraproject.org",
    "fedorahosted.org",
    "pagure.io",
    "centos.org",
    "openshift.com",
    "openshift.org",
    "gluster.org",
    "ovirt.org",
    "cockpit-project.org",
    "freeipa.org",
    "keycloak.org",
    "wildfly.org",
    "jboss.org",
    "libvirt.org",
    "systemd.io",
)

REPOS = {"BaseOS": "baseos-primary.xml.gz", "AppStream": "appstream-primary.xml.gz"}


def host_of(url: str) -> str:
    """Bare lowercase host, no scheme, no www, no port, no path."""
    if not url:
        return ""
    h = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", url.strip()).split("/")[0]
    h = h.split("@")[-1].split(":")[0].lower()
    return h[4:] if h.startswith("www.") else h


def is_redhat_host(host: str) -> bool:
    return any(host == d or host.endswith("." + d) for d in REDHAT_HOSTS)


def load(path: pathlib.Path) -> list[dict]:
    # Hardening. stdlib ElementTree does not resolve EXTERNAL entities, so XXE is not
    # reachable here, but it will happily expand internal ones (billion laughs). repodata
    # carries no DTD, so refusing any declaration is exact rather than merely cautious --
    # and avoids taking a dependency for one parse of one downloaded file.
    with gzip.open(path, "rb") as fh:
        raw = fh.read()
    if re.search(rb"<!\s*(DOCTYPE|ENTITY)", raw, re.IGNORECASE):
        raise ValueError(
            f"{path.name}: refusing to parse XML carrying a DTD or entity declaration"
        )
    root = ET.fromstring(raw)
    out = []
    for pkg in root.findall("c:package", NS):
        name = pkg.findtext("c:name", default="", namespaces=NS)
        url = pkg.findtext("c:url", default="", namespaces=NS) or ""
        fmt = pkg.find("c:format", NS)
        lic = (
            fmt.findtext("rpm:license", default="", namespaces=NS)
            if fmt is not None
            else ""
        )
        vendor = (
            fmt.findtext("rpm:vendor", default="", namespaces=NS)
            if fmt is not None
            else ""
        )
        out.append(
            {
                "name": name,
                "url": url.strip(),
                "host": host_of(url),
                "license": lic,
                "vendor": vendor,
            }
        )
    return out


def main() -> None:
    pkgs: list[dict] = []
    for repo, fname in REPOS.items():
        got = load(DATA / fname)
        for p in got:
            p["repo"] = repo
        pkgs += got
        print(f"[load] {repo:<10} {len(got):>5} source packages")

    # one row per distinct source package name (a name may appear in both repos)
    by_name: dict[str, dict] = {}
    for p in pkgs:
        by_name.setdefault(p["name"], p)
    rows = sorted(by_name.values(), key=lambda r: r["name"])
    total = len(rows)
    print(f"[load] {'DISTINCT':<10} {total:>5} source packages\n")

    no_url = [r for r in rows if not r["host"]]
    inside = [r for r in rows if r["host"] and is_redhat_host(r["host"])]
    github = [r for r in rows if r["host"].endswith("github.com")]
    outside = [r for r in rows if r["host"] and not is_redhat_host(r["host"])]

    coded = total - len(no_url)

    def pct(n: int, d: int) -> str:
        return f"{n / d:.3f}".lstrip("0") if d else "n/a"

    print("=" * 74)
    print(
        "PRIMARY CODING -- share of the product's source composition by upstream origin"
    )
    print("=" * 74)
    print(f"  distinct source packages          {total:>5}")
    print(
        f"  no upstream URL declared          {len(no_url):>5}   (excluded from rates)"
    )
    print(f"  codeable                          {coded:>5}")
    print()
    print(
        f"  INSIDE  (Red Hat / Fedora host)   {len(inside):>5}   {pct(len(inside), coded)}"
    )
    print(
        f"  OUTSIDE (independent upstream)    {len(outside):>5}   {pct(len(outside), coded)}"
    )
    print()
    print(
        f"  pre-registered failure condition: INSIDE > .500 -> "
        f"{'THESIS FAILS' if len(inside) / coded > 0.5 else 'not met'}"
    )
    print()

    print("=" * 74)
    print("SENSITIVITY -- reclassify EVERY github.com package as INSIDE (indefensible,")
    print("but it establishes a floor: many github orgs are not Red Hat's)")
    print("=" * 74)
    s_inside = len(inside) + len(github)
    print(f"  github.com-hosted upstreams       {len(github):>5}")
    print(f"  INSIDE  (generous floor)          {s_inside:>5}   {pct(s_inside, coded)}")
    print(
        f"  OUTSIDE (generous floor)          {coded - s_inside:>5}   {pct(coded - s_inside, coded)}"
    )
    print()

    print("=" * 74)
    print("TOP 20 UPSTREAM HOSTS")
    print("=" * 74)
    for host, n in collections.Counter(
        r["host"] for r in rows if r["host"]
    ).most_common(20):
        tag = "RH " if is_redhat_host(host) else "   "
        print(f"  {tag}{host:<42} {n:>4}   {pct(n, coded)}")
    print()

    print("=" * 74)
    print(
        "NAMED CHECK -- components on which the product is uncontroversially dependent"
    )
    print("=" * 74)
    for name in (
        "kernel",
        "glibc",
        "gcc",
        "systemd",
        "python3",
        "openssl",
        "bash",
        "coreutils",
    ):
        r = by_name.get(name)
        if r:
            where = "INSIDE" if is_redhat_host(r["host"]) else "OUTSIDE"
            print(f"  {name:<12} {where:<8} {r['host'] or '(no url)'}")

    out = DATA / "persistence_coding_rows.tsv"
    with out.open("w") as fh:
        fh.write("name\tclassification\thost\tlicense\turl\n")
        for r in rows:
            cls = (
                "NO_URL"
                if not r["host"]
                else ("INSIDE" if is_redhat_host(r["host"]) else "OUTSIDE")
            )
            fh.write(f"{r['name']}\t{cls}\t{r['host']}\t{r['license']}\t{r['url']}\n")
    print(f"\n[write] per-package coding -> {out}")


if __name__ == "__main__":
    main()
