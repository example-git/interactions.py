from typing import List, Optional, Union

from ..api.models.message import Emoji
from ..api.models.misc import DictSerializerMixin
from ..enums import ButtonStyle, ComponentType


class SelectOption(DictSerializerMixin):
    """
    A class object representing the select option of a select menu.

    :ivar str label: The label of the select option.
    :ivar str value: The returned value of the select option.
    :ivar Optional[str] description?: The description of the select option.
    :ivar Optional[Emoji] emoji?: The emoji used alongside the label of the select option.
    :ivar Optional[bool] default?: Whether the select option is the default for the select menu.
    """

    __slots__ = ("_json", "label", "value", "description", "emoji", "default")
    label: str
    value: str
    description: Optional[str]
    emoji: Optional[Emoji]
    default: Optional[bool]


class SelectMenu(DictSerializerMixin):
    """
    A class object representing the select menu of a component.


    :ivar ComponentType type: The type of select menu. Always defaults to ``3``.
    :ivar str custom_id: The customized "ID" of the select menu.
    :ivar List[SelectOption] options: The list of select options in the select menu.
    :ivar Optional[str] placeholder?: The placeholder of the select menu.
    :ivar Optional[int] min_values?: The minimum "options"/values to choose from the component.
    :ivar Optional[int] max_values?: The maximum "options"/values to choose from the component.
    :ivar Optional[bool] disabled?: Whether the select menu is unable to be used.
    """

    __slots__ = (
        "_json",
        "type",
        "custom_id",
        "placeholder",
        "min_values",
        "max_values",
        "disabled",
    )
    type: ComponentType
    custom_id: str
    options: List[SelectOption]
    placeholder: Optional[str]
    min_values: Optional[int]
    max_values: Optional[int]
    disabled: Optional[bool]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.type = ComponentType.SELECT
        self._json.update({"type": self.type.value})


class Button(DictSerializerMixin):
    """
    A class object representing the button of a component.


    :ivar ComponentType type: The type of button. Always defaults to ``2``.
    :ivar ButtonStyle style: The style of the button.
    :ivar str label: The label of the button.
    :ivar Optional[Emoji] emoji?: The emoji used alongside the laebl of the button.
    :ivar Optional[str] custom_id?: The customized "ID" of the button.
    :ivar Optional[str] url?: The URL route/path of the button.
    :ivar Optional[bool] disabled?: Whether the button is unable to be used.
    """

    __slots__ = ("_json", "type", "style", "label", "emoji", "custom_id", "url", "disabled")
    type: ComponentType
    style: ButtonStyle
    label: str
    emoji: Optional[Emoji]
    custom_id: Optional[str]
    url: Optional[str]
    disabled: Optional[bool]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.type = ComponentType.BUTTON
        self._json.update({"type": self.type.value, "style": self.style.value})


class Component(DictSerializerMixin):
    """
    A class object representing the component in an interaction response/followup.

    .. note::
        ``components`` is only applicable if an ActionRow is supported, otherwise
        ActionRow-less will be opted. ``list`` is in reference to the class.

    :ivar Union[ActionRow, Button, Menu] type: The type of component.
    :ivar Optional[str] custom_id?: The customized "ID" of the component.
    :ivar Optional[bool] disabled?: Whether the component is unable to be used.
    :ivar Optional[ButtonStyle] style?: The style of the component.
    :ivar Optional[str] label?: The label of the component.
    :ivar Optional[Emoji] emoji?: The emoji used alongside the label of the component.
    :ivar Optional[str] url?: The URl route/path of the component.
    :ivar Optional[List[SelectMenu]] options?: The "choices"/options of the component.
    :ivar Optional[str] placeholder?: The placeholder text/value of the component.
    :ivar Optional[int] min_values?: The minimum "options"/values to choose from the component.
    :ivar Optional[int] max_values?: The maximum "options"/values to choose from the component.
    :ivar Optional[Union[list, ActionRow, List[ActionRow], Button, List[Button], SelectMenu, List[SelectMenu]]] components?: A list of components nested in the component.
    """

    __slots__ = (
        "_json",
        "type",
        "custom_id",
        "disabled",
        "style",
        "label",
        "emoji",
        "url",
        "options",
        "placeholder",
        "min_values",
        "max_values",
        "components",
    )
    type: ComponentType
    custom_id: Optional[str]
    disabled: Optional[bool]
    style: Optional[ButtonStyle]
    label: Optional[str]
    emoji: Optional[Emoji]
    url: Optional[str]
    options: Optional[List[SelectMenu]]
    placeholder: Optional[str]
    min_values: Optional[int]
    max_values: Optional[int]
    components: Optional[
        Union[
            list, "ActionRow", List["ActionRow"], Button, List[Button], SelectMenu, List[SelectMenu]
        ]
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.type = ComponentType(self.type)


class ActionRow(DictSerializerMixin):
    """
    A class object representing the action row for interaction responses holding components.

    .. note::
        A message cannot have more than 5 ActionRow's supported.
        An ActionRow may also support only 1 text input component
        only.

    :ivar int type: The type of component. Always defaults to ``1``.
    :ivar Optional[Union[Component, List[Component]]] components?: A list of components the ActionRow has, if any.
    """

    __slots__ = ("_json", "type", "components")
    type: int
    components: Optional[Union[Component, List[Component]]]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.type = 1
