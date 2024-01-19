from lxml import etree

from spei.resources import Acuse


class MensajeElement(object):
    def __new__(cls, body):
        mensaje = body.find(
            '{http://cep.fyg.com/}respuestaCDA',
        )
        return etree.fromstring(mensaje.text)  # noqa: S320


class BodyElement(object):
    def __new__(cls, mensaje):
        return mensaje.find(
            '{http://schemas.xmlsoap.org/soap/envelope/}Body',
        )


class AcuseResponse(object):
    def __new__(cls, acuse, acuse_cls=Acuse):
        mensaje = etree.fromstring(acuse)  # noqa: S320
        mensaje_element = MensajeElement(BodyElement((mensaje)))
        return acuse_cls.parse_xml(mensaje_element)
