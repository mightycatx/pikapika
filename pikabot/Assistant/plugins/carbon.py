__pika__="""
{i}carbon <reply to message>"""

from Asst_modules import _carbon


@ItzSjDude(pika=True, pattern="carbon (?: |$)(.*)")
@pikatgbot('AmIAdm')
@pikatgbot('AdmOnly')
async def _(e):
    await _carbon(e)
