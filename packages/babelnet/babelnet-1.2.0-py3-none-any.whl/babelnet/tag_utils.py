"""This module contains some utils for tags"""
from enum import Enum
from typing import Dict, Type, Optional, Mapping, Union

from babelnet.data.alphabet import Alphabet
from babelnet.data.category import BabelCategory
from babelnet.data.domain import BabelDomain
from babelnet.data.entity_type import EntityType
from babelnet.data.frame import VerbAtlasFrameID
from babelnet.data.locale import Locale
from babelnet.data.tag import Tag, StringTag, LabelTag
from babelnet.data.usage import Usage
from babelnet.synset import SynsetType

_tag_mapping: Dict[str, Type[Enum]] = {
    "it.uniroma1.lcl.babelnet.data.Alphabet": Alphabet,
    "it.uniroma1.lcl.babelnet.data.Locale": Locale,
    "it.uniroma1.lcl.babelnet.data.Usage": Usage,
}
# We can assume that tag values are completely disjoint


def get_tag(classpath: str, value: Union[str, dict]) -> Optional[Tag]:
    """
    Given a classpath and a value of a tag, returns the corresponding tag.

    @param classpath: the classpath
    @type classpath: str
    @param value: the value of the tag
    @type value: str
    @return: The tag
    """

    if classpath == "it.uniroma1.lcl.babelnet.data.LabelTag":
        from babelnet import Language
        if type(value) == dict:
            lang = value['language']
            label = value['label']
        else:
            lang, label = value.split("|")
        return LabelTag(Language[lang], label)

    assert isinstance(value, str)
    if classpath == "it.uniroma1.lcl.babelnet.data.BabelCategory":
        return BabelCategory.from_string(value)
    elif classpath == "it.uniroma1.lcl.babelnet.data.StringTag":
        return StringTag(value)


    assert (
        classpath in _tag_mapping
    ), f"This type of tag ({classpath}) is not (yet) supported!"

    return _tag_mapping[classpath][value]


_str_tag2tag: Mapping[str, Type[Enum]] = {
    tag.name: tag
    for tag_class in (SynsetType, BabelDomain, Usage, Locale, Alphabet, EntityType)
    for tag in tag_class
}


def parse_tag(tag_obj: Union[dict, str]):
    """
    Parse a tag

    @param tag_obj: a dict or a string to parse
    @type tag_obj: Union[dict, str]

    @return: the tag associated
    @rtype: Optional[Tag]
    """
    if isinstance(tag_obj, dict):
        classname: str = tag_obj["CLASSNAME"]
        data: Union[str, dict] = tag_obj["DATA"]

        # FrameID is not a tag, but has the same structure...
        if classname == "it.uniroma1.lcl.babelnet.VerbAtlasFrameID":
            return VerbAtlasFrameID(_id=data["id"])

        if classname == "it.uniroma1.lcl.babelnet.data.BabelCategory":
            return BabelCategory(**tag_obj["DATA"])

        if classname == "it.uniroma1.lcl.babelnet.data.StringTag":
            return StringTag(data["stringTag"])

        return get_tag(classpath=classname, value=data)

    if isinstance(tag_obj, str):
        # Check if it is an already defined enum constant
        if tag_obj in _str_tag2tag:
            return _str_tag2tag[tag_obj]
        # Fallback on a StringTag
        return StringTag(tag_obj)

    raise NotImplementedError
