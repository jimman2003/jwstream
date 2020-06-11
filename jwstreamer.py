import subprocess
import re
import requests
from time import sleep
import jsbeautifier
from loguru import logger
from sys import stderr

logger.remove()
logger.add(stderr, level="INFO")
regvurl = r"(https?://).*\.(mp4|m3u8|avi)"


def hdvidpro(hdl):
    alt_url = ["hdvid.live"]
    ems = "embed-"
    if hdl in alt_url:
        hdl = f'{hdl.replace(alt_url,"vidhd.pw")}.html'
    liedit = list(hdl.rpartition("/"))
    if not (ems in liedit):
        liedit.insert(2, ems)
    linksu = "".join(liedit)

    return linksu


def jwscrape(jwlink):
    logger.debug(jwlink)
    logger.info("Getting page..")
    html = requests.get(jwlink).text
    if "eval(" in html:
        jsstar = html.rfind("eval(")
        jsend = html.rfind("</script>")
        js = jsbeautifier.beautify(html[jsstar:jsend])
        if (match := re.search(regvurl, js)) is not None:
            return match.group()

        else:
            logger.error("Video link not found in source")
    else:
        logger.error("No eval found")


def jwstream(jwlink, subs=""):
    vlclink = jwscrape(jwlink)
    logger.debug(vlclink)
    subprocess.Popen(["vlc", vlclink, f"--sub-file={subs}"])


if __name__ == "__main__":
    linkuser = input()
    services = ["hdvid", "vidhd"]
    if linkuser in "hdvid":
        jwstream(hdvidpro(linkuser))
    elif linkuser in "vidhd":
        jwstream(hdvidpro(linkuser))
    else:
        jwstream(linkuser)
    sleep(0.5)
