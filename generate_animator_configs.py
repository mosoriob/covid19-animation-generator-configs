import csv
import re
import unicodedata
from pathlib import Path

from jinja2 import Environment, select_autoescape, FileSystemLoader

COMUNA_INDEX = 1
COMUNA_ADYANCENTE_INDEX = 3
comunas_csv = 'adyacencia_comunas.csv'
CONFIG_FILE = "config.json"
CONFIG_DIR = Path('.') / "config"
COLORS = ["#F06AFF", "#F06AFF", "#FF6A6F", "#72CDFF",
          "#5FB9E1", "#72FFFF", "#72FFB7", "#7AFF72",
          "#BAFF72", "#FFF972", "#FFBB72", "#FF7772",
          "#FF729D", "#FF72CE", "#E072FF", "#B272FF",
          "#8672FF", "#ff7c43", "#72AEFF", "#d45087"]


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower()).strip()
    return re.sub(r'[-\s]+', '-', value)


def get_neighbours():
    with open(comunas_csv, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        comunas_dict = {}
        for row in csv_reader:
            comuna_name = row[COMUNA_INDEX]
            if comuna_name in comunas_dict:
                comunas_dict[comuna_name].append(row[COMUNA_ADYANCENTE_INDEX])
            else:
                comunas_dict[comuna_name] = [row[COMUNA_ADYANCENTE_INDEX], row[COMUNA_INDEX]]
    return comunas_dict


def generate_config():
    env = Environment(
        loader=FileSystemLoader('templates/'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=False,
        lstrip_blocks=False
    )
    CONFIG_DIR.mkdir(exist_ok=True)
    template = env.get_template(CONFIG_FILE)
    for key, item in get_neighbours().items():
        with open(CONFIG_DIR / "{}.json".format(slugify(key)), "w") as f:
            f.write(render_template(template=template, cities=item, colors=COLORS))


def render_template(template, **kwargs):
    return template.render(**kwargs)


if __name__ == '__main__':
    generate_config()
