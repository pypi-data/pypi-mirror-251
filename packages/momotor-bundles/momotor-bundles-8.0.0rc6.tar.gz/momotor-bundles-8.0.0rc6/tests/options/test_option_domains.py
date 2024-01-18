import typing

from momotor.bundles import RecipeBundle
from momotor.bundles.elements.content import NoContent
from momotor.bundles.elements.options import OptionsType, Option

# This recipe contains all possible combinations of option domains

recipe_xml = b'''<?xml version="1.0" encoding="UTF-8"?>
<recipe xmlns="http://momotor.org/1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://momotor.org/1.0 http://momotor.org/schema/momotor-1.0.xsd"
    id="recipe">
    <options>
        <option id="option1" name="option1" value="1" type="int" />
        <option id="option2" domain="domain2" name="option2" value="2" type="int" />
        <option id="option3" domain="#sub3" name="option3" value="3" type="int" />
        <option id="option4" domain="domain4#sub4" name="option4" value="4" type="int" />
    </options>
    <options domain="group2">
        <option id="option5" name="option5" value="5" type="int" />
        <option id="option6" domain="domain6" name="option6" value="6" type="int" />
        <option id="option7" domain="#sub7" name="option7" value="7" type="int" />
        <option id="option8" domain="domain8#sub8" name="option8" value="8" type="int" />
    </options>
    <options domain="#subgroup3">
        <option id="option9" name="option9" value="9" type="int" />
        <option id="option10" domain="domain10" name="option10" value="10" type="int" />
        <option id="option11" domain="#sub11" name="option11" value="11" type="int" />
        <option id="option12" domain="domain12#sub12" name="option12" value="12" type="int" />
    </options>
    <options domain="group4#subgroup4">
        <option id="option13" name="option13" value="13" type="int" />
        <option id="option14" domain="domain14" name="option14" value="14" type="int" />
        <option id="option15" domain="#sub15" name="option15" value="15" type="int" />
        <option id="option16" domain="domain16#sub16" name="option16" value="16" type="int" />
    </options>
    <steps>
        <options>
            <option id="option17" name="option17" value="17" type="int" />
            <option id="option18" domain="domain18" name="option18" value="18" type="int" />
            <option id="option19" domain="#sub19" name="option19" value="19" type="int" />
            <option id="option20" domain="domain20#sub20" name="option20" value="20" type="int" />
        </options>
        <options domain="group6">
            <option id="option21" name="option21" value="21" type="int" />
            <option id="option22" domain="domain22" name="option22" value="22" type="int" />
            <option id="option23" domain="#sub23" name="option23" value="23" type="int" />
            <option id="option24" domain="domain24#sub24" name="option24" value="24" type="int" />
        </options>
        <options domain="#subgroup7">
            <option id="option25" name="option25" value="25" type="int" />
            <option id="option26" domain="domain26" name="option26" value="26" type="int" />
            <option id="option27" domain="#sub27" name="option27" value="27" type="int" />
            <option id="option28" domain="domain28#sub28" name="option28" value="28" type="int" />
        </options>
        <options domain="group8#subgroup8">
            <option id="option29" name="option29" value="29" type="int" />
            <option id="option30" domain="domain30" name="option30" value="30" type="int" />
            <option id="option31" domain="#sub31" name="option31" value="31" type="int" />
            <option id="option32" domain="domain32#sub32" name="option32" value="32" type="int" />
        </options>
        <step id="step1">
            <options>
                <option ref="option1"/>   <!-- # -->
                <option ref="option2"/>   <!-- domain2 -->
                <option ref="option3"/>   <!-- #sub3 -->
                <option ref="option4"/>   <!-- domain4#sub4 -->
                <option ref="option5"/>   <!-- group2 -->
                <option ref="option6"/>   <!-- domain6 -->
                <option ref="option7"/>   <!-- group2#sub7 -->
                <option ref="option8"/>   <!-- domain8#sub8 -->
                <option ref="option9"/>   <!-- #subgroup3 -->
                <option ref="option10"/>  <!-- domain10#subgroup3 -->
                <option ref="option11"/>  <!-- #sub11 -->
                <option ref="option12"/>  <!-- domain12#sub12 -->
                <option ref="option13"/>  <!-- group4#subgroup4 -->
                <option ref="option14"/>  <!-- domain14#subgroup4 -->
                <option ref="option15"/>  <!-- group4#sub15 -->
                <option ref="option16"/>  <!-- domain16#sub16 -->
                <option ref="option17"/>  <!-- # -->             
                <option ref="option18"/>  <!-- domain18 -->      
                <option ref="option19"/>  <!-- #sub19 -->        
                <option ref="option20"/>  <!-- domain20#sub20 -->
                <option ref="option21"/>  <!-- group6 -->             
                <option ref="option22"/>  <!-- domain22 -->      
                <option ref="option23"/>  <!-- group6#sub23 -->        
                <option ref="option24"/>  <!-- domain24#sub24 -->
                <option ref="option25"/>  <!-- #subgroup7 -->             
                <option ref="option26"/>  <!-- domain26#subgroup7 -->      
                <option ref="option27"/>  <!-- #sub27 -->        
                <option ref="option28"/>  <!-- domain28#sub28 -->
                <option ref="option29"/>  <!-- group8#subgroup8 -->             
                <option ref="option30"/>  <!-- domain30#subgroup8 -->      
                <option ref="option31"/>  <!-- group8#sub31 -->        
                <option ref="option32"/>  <!-- domain32#sub32 -->
                <option id="option33" name="option33" value="33" type="int" />
                <option id="option34" domain="domain34" name="option34" value="34" type="int" />
                <option id="option35" domain="#sub35" name="option35" value="35" type="int" />
                <option id="option36" domain="domain36#sub36" name="option36" value="36" type="int" />
            </options>
            <options domain="group10">
                <option ref="option1"/>   <!-- # -->
                <option ref="option2"/>   <!-- domain2 -->
                <option ref="option3"/>   <!-- #sub3 -->
                <option ref="option4"/>   <!-- domain4#sub4 -->
                <option ref="option5"/>   <!-- group2 -->
                <option ref="option6"/>   <!-- domain6 -->
                <option ref="option7"/>   <!-- group2#sub7 -->
                <option ref="option8"/>   <!-- domain8#sub8 -->
                <option ref="option9"/>   <!-- #subgroup3 -->
                <option ref="option10"/>  <!-- domain10#subgroup3 -->
                <option ref="option11"/>  <!-- #sub11 -->
                <option ref="option12"/>  <!-- domain12#sub12 -->
                <option ref="option13"/>  <!-- group4#subgroup4 -->
                <option ref="option14"/>  <!-- domain14#subgroup4 -->
                <option ref="option15"/>  <!-- group4#sub15 -->
                <option ref="option16"/>  <!-- domain16#sub16 -->
                <option ref="option17"/>  <!-- # -->             
                <option ref="option18"/>  <!-- domain18 -->      
                <option ref="option19"/>  <!-- #sub19 -->        
                <option ref="option20"/>  <!-- domain20#sub20 -->
                <option ref="option21"/>  <!-- group6 -->             
                <option ref="option22"/>  <!-- domain22 -->      
                <option ref="option23"/>  <!-- group6#sub23 -->        
                <option ref="option24"/>  <!-- domain24#sub24 -->
                <option ref="option25"/>  <!-- #subgroup7 -->             
                <option ref="option26"/>  <!-- domain26#subgroup7 -->      
                <option ref="option27"/>  <!-- #sub27 -->        
                <option ref="option28"/>  <!-- domain28#sub28 -->
                <option ref="option29"/>  <!-- group8#subgroup8 -->             
                <option ref="option30"/>  <!-- domain30#subgroup8 -->      
                <option ref="option31"/>  <!-- group8#sub31 -->        
                <option ref="option32"/>  <!-- domain32#sub32 -->
                <option id="option37" name="option37" value="37" type="int" />
                <option id="option38" domain="domain38" name="option38" value="38" type="int" />
                <option id="option39" domain="#sub39" name="option39" value="39" type="int" />
                <option id="option40" domain="domain40#sub40" name="option40" value="40" type="int" />
            </options>
            <options domain="#subgroup11">
                <option ref="option1"/>   <!-- # -->
                <option ref="option2"/>   <!-- domain2 -->
                <option ref="option3"/>   <!-- #sub3 -->
                <option ref="option4"/>   <!-- domain4#sub4 -->
                <option ref="option5"/>   <!-- group2 -->
                <option ref="option6"/>   <!-- domain6 -->
                <option ref="option7"/>   <!-- group2#sub7 -->
                <option ref="option8"/>   <!-- domain8#sub8 -->
                <option ref="option9"/>   <!-- #subgroup3 -->
                <option ref="option10"/>  <!-- domain10#subgroup3 -->
                <option ref="option11"/>  <!-- #sub11 -->
                <option ref="option12"/>  <!-- domain12#sub12 -->
                <option ref="option13"/>  <!-- group4#subgroup4 -->
                <option ref="option14"/>  <!-- domain14#subgroup4 -->
                <option ref="option15"/>  <!-- group4#sub15 -->
                <option ref="option16"/>  <!-- domain16#sub16 -->
                <option ref="option17"/>  <!-- # -->             
                <option ref="option18"/>  <!-- domain18 -->      
                <option ref="option19"/>  <!-- #sub19 -->        
                <option ref="option20"/>  <!-- domain20#sub20 -->
                <option ref="option21"/>  <!-- group6 -->             
                <option ref="option22"/>  <!-- domain22 -->      
                <option ref="option23"/>  <!-- group6#sub23 -->        
                <option ref="option24"/>  <!-- domain24#sub24 -->
                <option ref="option25"/>  <!-- #subgroup7 -->             
                <option ref="option26"/>  <!-- domain26#subgroup7 -->      
                <option ref="option27"/>  <!-- #sub27 -->        
                <option ref="option28"/>  <!-- domain28#sub28 -->
                <option ref="option29"/>  <!-- group8#subgroup8 -->             
                <option ref="option30"/>  <!-- domain30#subgroup8 -->      
                <option ref="option31"/>  <!-- group8#sub31 -->        
                <option ref="option32"/>  <!-- domain32#sub32 -->
                <option id="option41" name="option41" value="41" type="int" />
                <option id="option42" domain="domain42" name="option42" value="42" type="int" />
                <option id="option43" domain="#sub43" name="option43" value="43" type="int" />
                <option id="option44" domain="domain44#sub44" name="option44" value="44" type="int" />
            </options>
            <options domain="group12#subgroup12">
                <option ref="option1"/>   <!-- # -->
                <option ref="option2"/>   <!-- domain2 -->
                <option ref="option3"/>   <!-- #sub3 -->
                <option ref="option4"/>   <!-- domain4#sub4 -->
                <option ref="option5"/>   <!-- group2 -->
                <option ref="option6"/>   <!-- domain6 -->
                <option ref="option7"/>   <!-- group2#sub7 -->
                <option ref="option8"/>   <!-- domain8#sub8 -->
                <option ref="option9"/>   <!-- #subgroup3 -->
                <option ref="option10"/>  <!-- domain10#subgroup3 -->
                <option ref="option11"/>  <!-- #sub11 -->
                <option ref="option12"/>  <!-- domain12#sub12 -->
                <option ref="option13"/>  <!-- group4#subgroup4 -->
                <option ref="option14"/>  <!-- domain14#subgroup4 -->
                <option ref="option15"/>  <!-- group4#sub15 -->
                <option ref="option16"/>  <!-- domain16#sub16 -->
                <option ref="option17"/>  <!-- # -->             
                <option ref="option18"/>  <!-- domain18 -->      
                <option ref="option19"/>  <!-- #sub19 -->        
                <option ref="option20"/>  <!-- domain20#sub20 -->
                <option ref="option21"/>  <!-- group6 -->             
                <option ref="option22"/>  <!-- domain22 -->      
                <option ref="option23"/>  <!-- group6#sub23 -->        
                <option ref="option24"/>  <!-- domain24#sub24 -->
                <option ref="option25"/>  <!-- #subgroup7 -->             
                <option ref="option26"/>  <!-- domain26#subgroup7 -->      
                <option ref="option27"/>  <!-- #sub27 -->        
                <option ref="option28"/>  <!-- domain28#sub28 -->
                <option ref="option29"/>  <!-- group8#subgroup8 -->             
                <option ref="option30"/>  <!-- domain30#subgroup8 -->      
                <option ref="option31"/>  <!-- group8#sub31 -->        
                <option ref="option32"/>  <!-- domain32#sub32 -->
                <option id="option45" name="option45" value="45" type="int" />
                <option id="option46" domain="domain46" name="option46" value="46" type="int" />
                <option id="option47" domain="#sub47" name="option47" value="47" type="int" />
                <option id="option48" domain="domain48#sub48" name="option48" value="48" type="int" />
            </options>
        </step>
    </steps>
</recipe>
'''


def _collect_name_domain(options: OptionsType) -> list[tuple[str, str, int]]:
    result = []
    for option in options:
        try:
            result.append((option.domain, option.name, option.value))
        except NoContent:
            pass

    return result


def test_option_domain_parsing():
    recipe = RecipeBundle.from_bytes_factory(recipe_xml, legacy=False)

    default = Option.DEFAULT_DOMAIN

    recipe_options = [
        (default, 'option1', 1),
        ('domain2', 'option2', 2),
        (f'{default}#sub3', 'option3', 3),
        ('domain4#sub4', 'option4', 4),
        ('group2', 'option5', 5),
        ('domain6', 'option6', 6),
        ('group2#sub7', 'option7', 7),
        ('domain8#sub8', 'option8', 8),
        (f'{default}#subgroup3', 'option9', 9),
        ('domain10#subgroup3', 'option10', 10),
        (f'{default}#sub11', 'option11', 11),
        ('domain12#sub12', 'option12', 12),
        ('group4#subgroup4', 'option13', 13),
        ('domain14#subgroup4', 'option14', 14),
        ('group4#sub15', 'option15', 15),
        ('domain16#sub16', 'option16', 16),
    ]

    steps_options = [
         (f'{default}', 'option17', 17),
         ('domain18', 'option18', 18),
         (f'{default}#sub19', 'option19', 19),
         ('domain20#sub20', 'option20', 20),
         ('group6', 'option21', 21),
         ('domain22', 'option22', 22),
         ('group6#sub23', 'option23', 23),
         ('domain24#sub24', 'option24', 24),
         (f'{default}#subgroup7', 'option25', 25),
         ('domain26#subgroup7', 'option26', 26),
         (f'{default}#sub27', 'option27', 27),
         ('domain28#sub28', 'option28', 28),
         ('group8#subgroup8', 'option29', 29),
         ('domain30#subgroup8', 'option30', 30),
         ('group8#sub31', 'option31', 31),
         ('domain32#sub32', 'option32', 32),
    ]

    # Test 'global' options on the recipe
    assert _collect_name_domain(recipe.options) == recipe_options

    # Test options on the step
    assert _collect_name_domain(recipe.steps[0].options) == [
         *recipe_options,
         *steps_options,
         (f'{default}', 'option33', 33),
         ('domain34', 'option34', 34),
         (f'{default}#sub35', 'option35', 35),
         ('domain36#sub36', 'option36', 36),
         *recipe_options,
         *steps_options,
         ('group10', 'option37', 37),
         ('domain38', 'option38', 38),
         ('group10#sub39', 'option39', 39),
         ('domain40#sub40', 'option40', 40),
         *recipe_options,
         *steps_options,
         (f'{default}#subgroup11', 'option41', 41),
         ('domain42#subgroup11', 'option42', 42),
         (f'{default}#sub43', 'option43', 43),
         ('domain44#sub44', 'option44', 44),
         *recipe_options,
         *steps_options,
         ('group12#subgroup12', 'option45', 45),
         ('domain46#subgroup12', 'option46', 46),
         ('group12#sub47', 'option47', 47),
         ('domain48#sub48', 'option48', 48),
    ]
