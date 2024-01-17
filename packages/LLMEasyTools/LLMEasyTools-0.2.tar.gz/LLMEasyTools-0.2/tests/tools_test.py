import pytest
import json

from unittest.mock import Mock
from llm_easy_tools import ToolBox, SchemaGenerator, schema_name
from pydantic import BaseModel
from typing import Any

class ToolParam(BaseModel):
    value: int

class AdditionalToolParam(BaseModel):
    value: int

class TestTool:
    def tool_method(self, arg: ToolParam) -> str:
        return f'executed tool_method with param: {arg}'

    def additional_tool_method(self, arg: AdditionalToolParam) -> str:
        return f'executed additional_tool_method with param: {arg}'

    def _private_tool_method(self, arg: AdditionalToolParam) -> str:
        return str(arg.value * 4)


tool = TestTool()

def test_toolbox_init():
    toolbox = ToolBox()
    assert toolbox.strict == True
    assert toolbox.tool_registry == {}
    assert toolbox.name_mappings == []
    assert toolbox.tool_schemas == []
    assert isinstance(toolbox.generator, SchemaGenerator)

def test_toolbox_from_object():
    toolbox = ToolBox.toolbox_from_object(tool)
    assert "tool_method" in toolbox.tool_registry
    assert len(toolbox.tool_registry) == 2
    assert len(toolbox.tool_schemas) == 2

def test_schema_name_to_func():
    toolbox = ToolBox(name_mappings=[("tool_method", "TestTool")])
    assert toolbox.schema_name_to_func("TestTool") == "tool_method"
    assert toolbox.schema_name_to_func("NotFound") == "NotFound"


class FunctionCallMock:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

def test_process():
    toolbox = ToolBox.toolbox_from_object(tool)
    function_call = FunctionCallMock(name="tool_method", arguments=json.dumps(ToolParam(value=2).model_dump()))
    result = toolbox.process_function(function_call)
    assert result == 'executed tool_method with param: value=2'

    toolbox = ToolBox.toolbox_from_object(tool, name_mappings=[("additional_tool_method", "custom_name")])
    function_call = FunctionCallMock(name="custom_name", arguments=json.dumps(ToolParam(value=3).model_dump()))
    result = toolbox.process_function(function_call)
    assert result == "executed additional_tool_method with param: value=3"

    # Test with unknown function call name
    with pytest.raises(ValueError):
        function_call = FunctionCallMock(name="unknown_name", arguments=json.dumps(ToolParam(value=3).model_dump()))
        toolbox.process_function(function_call)


class UserDetail(BaseModel):
    name: str
    age: int

def test_process_with_identity():
    toolbox = ToolBox()
    toolbox.register_tool(UserDetail)
    assert "UserDetail" in toolbox.tool_registry
    original_user = UserDetail(name="John", age=21)
    function_call = FunctionCallMock(name="UserDetail", arguments=json.dumps(original_user.model_dump()))
    result = toolbox.process_function(function_call)
    assert result == original_user

def process_response():
    toolbox = ToolBox()
    toolbox.register_tool(UserDetail)
    original_user = UserDetail(name="John", age=21)
    function_call = FunctionCallMock(name="UserDetail", arguments=json.dumps(original_user.model_dump()))
    response = Mock(choices=[Mock(message=Mock(tool_calls=[Mock(function=function_call)]))])
    results = toolbox.process_response(response)
    assert len(results) == 1
    assert results[0] == original_user


# Define the test cases
def test_register_tool():
    class Tool(BaseModel):
        name: str

    def example_tool(tool: Tool):
        print('Running test tool')

    @schema_name("good_name")
    def bad_name_tool(tool: Tool):
        print('Running bad_name_tool')

    toolbox = ToolBox()

    # Test with correct parameters
    toolbox.register_tool(example_tool)
    assert 'example_tool' in toolbox.tool_registry
    assert toolbox.tool_registry['example_tool'][0] == example_tool
    assert toolbox.tool_registry['example_tool'][1] == Tool
    assert len(toolbox.tool_schemas) == 1
    assert len(toolbox.function_schemas) == 1
    assert toolbox.tool_schemas[0]['function']['name'] == 'example_tool'
    assert toolbox.function_schemas[0]['name'] == 'example_tool'

    # Test with function with more than one parameter
    with pytest.raises(TypeError):
        def two_parameters(a, b): pass
        toolbox.register_tool(two_parameters)

    # Test with function with no parameters
    with pytest.raises(TypeError):
        def no_parameters(): pass
        toolbox.register_tool(no_parameters)

    # Test with function having a parameter which isn't subclass of BaseModel
    with pytest.raises(TypeError):
        def wrong_parameter(a: Any): pass
        toolbox.register_tool(wrong_parameter)

    toolbox.register_tool(bad_name_tool)
    assert 'bad_name_tool' in toolbox.tool_registry
    assert toolbox.tool_registry['bad_name_tool'][0] == bad_name_tool
    assert toolbox.tool_registry['bad_name_tool'][1] == Tool
    assert toolbox.schema_name_to_func('good_name') == 'bad_name_tool'

def test_register_tool_with_model():
    class Tool(BaseModel):
        name: str

    class WikiSearch(BaseModel):
        query: str

    toolbox = ToolBox()
    toolbox.register_tool(Tool)

    identity_function = toolbox.tool_registry['Tool'][0]
    assert callable(identity_function)
    assert identity_function(Tool(name="test")) == Tool(name="test")
    assert toolbox.tool_registry['Tool'][1] is Tool
    assert len(toolbox.tool_schemas) == 1
    assert toolbox.tool_schemas[0]['function']['name'] == 'Tool'

    toolbox.register_tool(WikiSearch)
    identity_function = toolbox.tool_registry['WikiSearch'][0]
    assert callable(identity_function)
    assert identity_function(WikiSearch(query="test")) == WikiSearch(query="test")
    assert toolbox.tool_registry['WikiSearch'][1] is WikiSearch
    assert len(toolbox.tool_schemas) == 2
    assert toolbox.tool_schemas[1]['function']['name'] == 'WikiSearch'


pytest.main()
