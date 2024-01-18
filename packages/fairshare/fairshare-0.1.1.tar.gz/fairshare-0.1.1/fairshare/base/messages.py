from pydantic import BaseModel, Extra, Field

from fairshare.helpers import get_id


class BaseMessage(BaseModel, extra=Extra.allow):
    id: str = Field(
        pattern=r'^([^uU]|u[^sS]|us[^eE]|use[^rR]|user[^sS])[a-z0-9-]*$',
        default_factory=get_id
    )
    share_id: str = Field(
        pattern=r'^([^rR]|r[^eE]|re[^aA]|rea[^dD]|read[^yY]|u[^nN]|un[^aA]|una[^cC]|unac[^kK]|unack[^eE]|unacke[^dD]|'
                r'unacked[^$]|p[^eE]|pe[^nN]|pen[^dD]|pend[^iI]|pendi[^nN]|pendin[^gG]|pendin[^gG])[a-z0-9-]*$'
    )
