from typing import Any, Dict, List, Optional

from tartiflette import Resolver

from model.main import ModelReadImageText

@Resolver("Query.image")
async def resolve_query_image(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> str:
    """
    Resolver for extract the text from an url image.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the field
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: the text of the image
    :rtype: str
    """

    url_file = args['url']
    read_image_text = ModelReadImageText()
    result = read_image_text.evaluate(url_file)
    return { 'text': result }
