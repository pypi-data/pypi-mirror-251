from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union
from momotor.bundles.binding.xml import LangValue

__NAMESPACE__ = "http://momotor.org/1.0"


@dataclass
class DependsComplexType:
    class Meta:
        name = "dependsComplexType"

    step: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class FileComplexType:
    class Meta:
        name = "fileComplexType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    any_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


@dataclass
class LinkComplexType:
    class Meta:
        name = "linkComplexType"

    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class OptionComplexType:
    class Meta:
        name = "optionComplexType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    domain: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    any_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


class OutcomeSimpleType(Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


class PropertyComplexTypeAccept(Enum):
    EQ = "eq"
    NE = "ne"
    LT = "lt"
    LE = "le"
    GT = "gt"
    GE = "ge"
    ONE_OF = "one-of"
    IN_RANGE = "in-range"
    ANY = "any"
    NONE = "none"


@dataclass
class ResourceComplexType:
    class Meta:
        name = "resourceComplexType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


class StepComplexTypePriority(Enum):
    MUST_PASS = "must-pass"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    DEFAULT = "default"


@dataclass
class DependenciesComplexType:
    class Meta:
        name = "dependenciesComplexType"

    depends: list[DependsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class FilesComplexType:
    class Meta:
        name = "filesComplexType"

    file: list[FileComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    baseclass: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    basename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    basesrc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class MetaComplexType:
    class Meta:
        name = "metaComplexType"

    name: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    version: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    author: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    description: list["MetaComplexType.Description"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    source: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    generator: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )

    @dataclass
    class Description:
        lang: Optional[Union[str, LangValue]] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "namespace": "http://www.w3.org/XML/1998/namespace",
            }
        )
        content: list[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "mixed": True,
            }
        )


@dataclass
class OptionsComplexType:
    class Meta:
        name = "optionsComplexType"

    option: list[OptionComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    domain: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PropertyComplexType:
    class Meta:
        name = "propertyComplexType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    accept: Optional[PropertyComplexTypeAccept] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    any_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


@dataclass
class ResourcesComplexType:
    class Meta:
        name = "resourcesComplexType"

    resource: list[ResourceComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class CheckletComplexType:
    class Meta:
        name = "checkletComplexType"

    repository: list["CheckletComplexType.Repository"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    link: list[LinkComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    index: list[LinkComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    package_version: list["CheckletComplexType.PackageVersion"] = field(
        default_factory=list,
        metadata={
            "name": "package-version",
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    resources: list[ResourcesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    extras: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    entrypoint: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Repository:
        src: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        type_value: Optional[str] = field(
            default=None,
            metadata={
                "name": "type",
                "type": "Attribute",
                "required": True,
            }
        )
        revision: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass
    class PackageVersion:
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        version: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )


@dataclass
class ConfigComplexType:
    class Meta:
        name = "configComplexType"

    meta: list[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: list[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PropertiesComplexType:
    class Meta:
        name = "propertiesComplexType"

    property: list[PropertyComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class CheckletsComplexType:
    class Meta:
        name = "checkletsComplexType"

    checklet: list[CheckletComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    basename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Config(ConfigComplexType):
    class Meta:
        name = "config"
        namespace = "http://momotor.org/1.0"


@dataclass
class ExpectComplexType:
    class Meta:
        name = "expectComplexType"

    properties: list[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    step: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    outcome: Optional[OutcomeSimpleType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ProductComplexType:
    class Meta:
        name = "productComplexType"

    meta: list[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: list[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    properties: list[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ResultComplexType:
    class Meta:
        name = "resultComplexType"

    checklet: list[CheckletComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    properties: list[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: list[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    step: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    outcome: Optional[OutcomeSimpleType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class StepComplexType:
    class Meta:
        name = "stepComplexType"

    meta: list[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    dependencies: list[DependenciesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklet: list[CheckletComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    resources: list[ResourcesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: list[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    priority: StepComplexTypePriority = field(
        default=StepComplexTypePriority.DEFAULT,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ExpectedResultComplexType:
    class Meta:
        name = "expectedResultComplexType"

    expect: list[ExpectComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Product(ProductComplexType):
    class Meta:
        name = "product"
        namespace = "http://momotor.org/1.0"


@dataclass
class Result(ResultComplexType):
    class Meta:
        name = "result"
        namespace = "http://momotor.org/1.0"


@dataclass
class ResultsComplexType:
    class Meta:
        name = "resultsComplexType"

    meta: list[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklets: list[CheckletsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    result: list[ResultComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class StepsComplexType:
    class Meta:
        name = "stepsComplexType"

    step: list[StepComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: list[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklets: list[CheckletsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class Results(ResultsComplexType):
    class Meta:
        name = "results"
        namespace = "http://momotor.org/1.0"


@dataclass
class TestComplexType:
    class Meta:
        name = "testComplexType"

    meta: list[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    product: list[ProductComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    expected_result: list[ExpectedResultComplexType] = field(
        default_factory=list,
        metadata={
            "name": "expectedResult",
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class TestResultComplexType:
    class Meta:
        name = "testResultComplexType"

    results: list[ResultsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class Testresult(TestResultComplexType):
    class Meta:
        name = "testresult"
        namespace = "http://momotor.org/1.0"


@dataclass
class TestsComplexType:
    class Meta:
        name = "testsComplexType"

    expected_result: list[ExpectedResultComplexType] = field(
        default_factory=list,
        metadata={
            "name": "expectedResult",
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    expect: list[ExpectComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    properties: list[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    test: list[TestComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class RecipeComplexType:
    class Meta:
        name = "recipeComplexType"

    meta: list[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: list[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklets: list[CheckletsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: list[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    steps: list[StepsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    tests: list[TestsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Recipe(RecipeComplexType):
    class Meta:
        name = "recipe"
        namespace = "http://momotor.org/1.0"
