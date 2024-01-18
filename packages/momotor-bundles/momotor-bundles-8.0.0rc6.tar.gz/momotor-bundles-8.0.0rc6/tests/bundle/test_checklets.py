import pytest

from momotor.bundles import RecipeBundle
from momotor.bundles.exception import InvalidRefError

from bundle_test_helpers import parametrize_use_lxml


@parametrize_use_lxml
def test_checklet_refs(use_lxml):
    recipe = RecipeBundle.from_bytes_factory(b"""<?xml version="1.0" encoding="UTF-8"?>
    <recipe xmlns="http://momotor.org/1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://momotor.org/1.0 http://momotor.org/schema/momotor-1.0.xsd"
        id="test-ref">
        
        <checklets basename='base1'>
            <checklet id='c1' name='checklet1' />
        </checklets>
        
        <steps>
            <checklets>
                <checklet id='c2' name='checklet2' />
            </checklets>
        
            <checklets basename='base2'>
                <checklet id='c3' name='checklet3' />
            </checklets>
        
            <step id='s1'>
                <checklet ref='c1' />
            </step>

            <step id='s2'>
                <checklet ref='c2' />
            </step>

            <step id='s3'>
                <checklet ref='c3' />
            </step>

            <step id='s4'>
                <checklet name='checklet4' />
            </step>

            <step id='s5'>
                <checklet name='checklet5' />
            </step>
        </steps>
    </recipe>
    """, use_lxml=use_lxml, legacy=False)

    names = [
        step.checklet.name for step in recipe.steps
    ]

    assert ['base1.checklet1', 'checklet2', 'base2.checklet3', 'checklet4', 'checklet5'] == names


@parametrize_use_lxml
def test_checklet_invalid_ref(use_lxml):
    with pytest.raises(InvalidRefError, match=r'Unable to find checklet id=c1'):
        RecipeBundle.from_bytes_factory(b"""<?xml version="1.0" encoding="UTF-8"?>
            <recipe xmlns="http://momotor.org/1.0"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://momotor.org/1.0 http://momotor.org/schema/momotor-1.0.xsd"
                id="test-invalid-ref">
                
                <steps>
                    <step id='s1'>
                        <checklet ref='c1' />
                    </step>
                </steps>
            </recipe>
        """, use_lxml=use_lxml, legacy=False)
