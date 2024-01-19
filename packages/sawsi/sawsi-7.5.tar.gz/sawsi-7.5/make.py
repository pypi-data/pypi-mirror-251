import click
import os


@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_name')
def initproject(project_name):
    # 프로젝트 구조를 생성하는 코드
    os.makedirs(project_name)
    # 추가적인 파일 생성 및 초기 설정 코드
    click.echo(f"Project {project_name} has been created.")


@cli.command()
@click.argument('app_name')
def startapp(app_name):
    # 프로젝트 구조를 생성하는 코드
    os.makedirs(app_name)
    # 추가적인 파일 생성 및 초기 설정 코드
    click.echo(f"App {app_name} has been created.")



if __name__ == '__main__':
    cli()
