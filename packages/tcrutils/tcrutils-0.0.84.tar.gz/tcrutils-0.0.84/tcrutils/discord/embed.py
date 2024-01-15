import hikari

from ..src.tcr_null import Null


def embed(
  title: str,
  description: str,
  *,
  url=None,
  color=None,
  timestamp=None,
  thumbnail=None,
  footer=None,
  footer_icon=None,
  author: dict | None = None,
  image=None,
  fields: list | None = None,
) -> hikari.Embed:
  if (title is not Null and not title.strip()) or (
    description is not Null and not description.strip()
  ):
    msg = f'Both title and description must be non-whitespace-only strings unless explicitly specified the title to be Null, got Title: {title!r}, Description: {description!r}'
    raise ValueError(msg)

  if fields is None:
    fields = []

  if author is None:
    author = {}

  out = hikari.Embed(
    title=title if title is not Null else None,
    description=description if description is not Null else None,
    color=color,
    timestamp=timestamp,
    url=url,
  )

  if thumbnail:
    out = out.set_thumbnail(thumbnail)

  if footer:
    out = out.set_footer(text=footer, icon=footer_icon)
  if author:
    out = out.set_author(**author)
  if image:
    out = out.set_image(image)

  for field in fields:
    if len(field) == 2:
      field = (*field, False)
    out = out.add_field(field[0], field[1], inline=field[2])
  return out
