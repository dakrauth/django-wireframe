from functools import partial
import qrcode
import qrcode.image.svg
from qrcode.compat.etree import ET


class SvgPathFragmentImage(qrcode.image.svg.SvgPathImage):
    def _write(self, stream):
        ET.ElementTree(self._img).write(stream, xml_declaration=False)


SVG_FACTORY = {
    "SVG": qrcode.image.svg.SvgImage,
    "SVGFRAG": qrcode.image.svg.SvgFragmentImage,
    "SVGPATH": qrcode.image.svg.SvgPathImage,
    "SVGPATHFRAG": SvgPathFragmentImage,
}


def make(data, **kwargs):
    factory = kwargs.pop("factory", None)
    svg_factory = SVG_FACTORY.get(factory, None)
    result = qrcode.make(data, image_factory=svg_factory, **kwargs)
    return result.to_string().decode() if svg_factory else result


def email(email, **kwargs):
    return make(f"mailto:{email}", **kwargs)


def wifi(ssid, passwd, kind="WPA2", **kwargs):
    return make(f"WIFI:T:{kind};S:{ssid};P:{passwd};;", **kwargs)


def mecard(name, addr="", tel="", email="", **kwargs):
    return make(f"MECARD:N:{name};ADR:{addr};TEL:{tel};EMAIL:{email};;", **kwargs)


make_svg_path_frag = partial(make, factory="SVGPATHFRAG")
