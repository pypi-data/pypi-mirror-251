import os
import click
from gentccode.check_version import check_package_version, get_current_version
from gentccode.convert_to_jmx import convert_payloads_of_curl_to_jmx_file
from gentccode.convert_to_locust import product_locust_code
from gentccode.produce_search_case import gen_cp_test_case
from gentccode.produce_test_case import ProduceTestCase


ptc = ProduceTestCase()
# 生成的接口信息会保存到这个文件中
api_yaml_file_path = "api.yaml"
# 生成的接口代码会保存到这个文件中
case_file_path = "test_cases.py"

package_name = "gentccode"


@click.group()
def cli1():
    pass


# cli1的回调函数
@cli1.result_callback()
def check_update(curl):
    check_package_version(package_name)


@click.command(help="generate test code by http's payload")
@click.option("-n", "--node", required=True, help="json node, like: '.','a.','a.b.'")
@click.argument("filename", type=click.Path(exists=True))
def cp(node, filename):
    gen_cp_test_case(
        node=node,
        curl_file=filename,
    )


@click.command(help="generate test code by curl file")
@click.argument("filename", type=click.Path(exists=True))
def curl(filename):
    ptc.produce_case_by_yaml_for_curl(filename, api_yaml_file_path, case_file_path)


@click.command(help="generate test code by swagger json file")
@click.argument("filename", type=click.Path(exists=True))
def swagger2(filename):
    ptc.produce_case_by_yaml_for_swagger2(filename, api_yaml_file_path, case_file_path)


@click.command(help="auto generate openapi document's test code")
@click.argument("filename", type=click.Path(exists=True))
def openapi(filename):
    ptc.produce_merged_case_for_openapi_and_curl(curl_file_path=filename)


@click.command(help="generate locust script by curl file")
@click.argument("filename", type=click.Path(exists=True))
def locust(filename):
    product_locust_code(curl_file_path=filename)


@click.command(help="generate jmeter script by curl file")
@click.argument("filename", type=click.Path(exists=True))
def jmeter(filename):
    convert_payloads_of_curl_to_jmx_file(curl_file_path=filename)


@click.command(help="auto generate swagger2 document's test code")
@click.argument("filename", type=click.Path(exists=True))
def swagger_at(filename):
    ptc.produce_merged_case_for_swagger_and_curl(curl_file_path=filename)


@click.command()
def version():
    current_version = get_current_version(package_name=package_name)
    click.echo(f"{package_name}: v{current_version}")


def main():
    # clear api yaml content.
    if os.path.exists(api_yaml_file_path):
        with open(api_yaml_file_path, "w") as f:
            f.write("")
    cli1.add_command(curl)
    cli1.add_command(swagger2)
    cli1.add_command(openapi)
    cli1.add_command(locust)
    cli1.add_command(cp)
    cli1.add_command(jmeter)
    cli1.add_command(swagger_at)
    cli1.add_command(version)
    cli1()
