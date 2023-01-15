from typing import Any

from jinja2 import pass_context
from starlette.templating import Jinja2Templates


@pass_context
def url_for(context: dict, name: str, **path_params: Any) -> str:
    request = context["request"]
    return request.url_for(name, **path_params, token=request.path_params["token"])

templates = Jinja2Templates("villageblog/templates")
templates.env.globals["url_for"] = url_for
