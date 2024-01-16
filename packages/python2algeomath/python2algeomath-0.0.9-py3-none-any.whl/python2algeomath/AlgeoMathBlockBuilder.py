import xml.etree.ElementTree as ET
import random as rd


class Builder:
    def __init__(self):
        self.root = ET.Element("xml", xmlns="https://developers.google.com/blockly/xml")
        self.current_block = self.root
        self.block_stack = []

    def to_xml_string(self):
        return ET.tostring(self.root, encoding="utf-8", method="xml")

    def add_block(self, block_type, x=None, y=None):
        block_id = str(rd.random())
        if x is not None and y is not None:
            block = ET.SubElement(
                self.current_block, "block", type=block_type, id=block_id, x=x, y=y
            )
        else:
            block = ET.SubElement(
                self.current_block, "block", type=block_type, id=block_id
            )
        self.block_stack.append(self.current_block)
        self.current_block = block

    def add_field(self, name, text):
        field = ET.SubElement(self.current_block, "field", name=name)
        field.text = text

    def add_value(self, name):
        value = ET.SubElement(self.current_block, "value", name=name)
        self.block_stack.append(self.current_block)
        self.current_block = value

    def end_block(self):
        if self.block_stack:
            self.current_block = self.block_stack.pop()
        else:
            self.current_block = self.root

    def add_next(self):
        next_block = ET.SubElement(self.current_block, "next")
        self.block_stack.append(self.current_block)
        self.current_block = next_block

    def init_variable(self, var_list):
        variables = ET.SubElement(self.current_block, "variables")
        for var_name in var_list:
            var_id = str(rd.random())
            variable = ET.SubElement(variables, "variable", id=var_id)
            variable.text = var_name
        self.add_block("algeo_start", x="90", y="50")
        self.add_field("state", "START")
        self.add_next()

    def add_dot_block(self, x, y, name):
        self.add_block("algeo_create_point")
        self.add_value("x")
        self.add_basic_input_block(str(x))
        self.end_block()
        self.add_value("y")
        self.add_basic_input_block(str(y))
        self.end_block()
        self.add_value("name")
        self.add_basic_input_block(f"{name}")
        self.end_block()
        self.add_next()

    def add_basic_input_block(self, value):
        self.add_block("basic_input_value")
        self.add_field("value", value)
        self.end_block()

    def add_two_point_block(self, start, end, name):
        self.add_block("algeo_create_twopoint_object")
        self.add_field("object", "선분")
        self.add_value("segmentName1")
        self.add_basic_input_block(f"{start}")
        self.end_block()
        self.add_value("segmentName2")
        self.add_basic_input_block(f"{end}")
        self.end_block()
        self.add_value("name")
        self.add_basic_input_block(f"{name}")
        self.end_block()
        self.add_next()

    def start_control_for(self, variable, start, end, step):
        self.add_block("control_for")
        self.add_value("initial")
        self.add_basic_input_block(f"{variable} = {start}")
        self.end_block()
        self.add_value("end")
        self.add_basic_input_block(f"{variable} <= {end}")
        self.end_block()
        self.add_value("step")
        self.add_basic_input_block(f"{variable} += {step}")
        self.end_block()
        block = ET.SubElement(self.current_block, "statement", name="statements")
        # control_for 블록을 stack에 추가합니다.
        self.block_stack.append(self.current_block)
        self.current_block = block

    def end_control_for(self):
        while self.block_stack:
            # 현재 블록을 스택에서 꺼냅니다.
            self.current_block = self.block_stack.pop()

            # <statement> 태그를 찾았을 경우 더 이상 스택에서 꺼내지 않고 종료합니다.
            if self.current_block.tag == "statement":
                break

        # 스택이 비어있으면 root로 돌아갑니다.
        if not self.block_stack:
            self.current_block = self.root

        self.end_block()
        self.add_next()

    def hide_point(self):
        self.add_block("turtle_all_dot_name_show_hide")
        self.add_field("fielditem_object", "점과 점의 이름")
        self.add_field("fielditem_object", "감추기")
        self.end_block()
        self.add_next()

    def execute_set(self, name, latex):
        self.add_block("algeo_execute_set_name")
        self.add_value("name")
        self.add_basic_input_block(f"{name}")
        self.end_block()
        self.add_value("code")
        self.add_basic_input_block(f"{latex}")
        self.end_block()
        self.add_next()

    def create_function_graph(self, latex):
        self.add_block("create_function_fx")
        self.add_value("xValue")
        self.add_basic_input_block(f'"{latex}"')
        self.end_block()
        self.add_next()

    # function 관련 기능 구현

    def add_function_graph(self, func_initial, latex):
        self.execute_set(f'"{func_initial}"', f'"{func_initial}(x)={latex}"')

    def add_function_dot(self, name, x, func_initial):
        self.execute_set(name, f'"("+({x})+",{func_initial}("+({x})+"))"')

    # polygon관련 기능 구현

    def add_polygon(self, name, list):
        polygonStr = ",".join(list)
        self.execute_set(f'"{name}"', f'"Polygon({polygonStr})"')
