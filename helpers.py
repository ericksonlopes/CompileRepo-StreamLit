from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt
import networkx as nx
import requests
from bs4 import BeautifulSoup
import requests
import streamlit as st
from bs4 import BeautifulSoup


@dataclass
class PropertyModel:
    path: str
    name: str
    link: str


@dataclass
class FileModel(PropertyModel):
    type: str = "File"
    size: str = None
    lines: int = None
    extension: str = None


@dataclass
class DirectoryModel(PropertyModel):
    type: str = "Directory"


class GitHub:
    def __init__(self):
        self.__files: List[FileModel] = []
        self.__directories: List[DirectoryModel] = []

    @property
    def files(self) -> List[FileModel]:
        return self.__files

    @property
    def directories(self) -> List[DirectoryModel]:
        return self.__directories

    @staticmethod
    def convert_to_kilobytes(size, unit):
        unit = unit.upper()
        units = {"B": 1, "BYTES": 1,
                 "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
        if unit in units:
            return size * units[unit] / 1024
        else:
            raise ValueError("Invalid unit")

    def build_graph(self, url, graph, progress_bar):
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        list_items = soup.find(class_="js-details-container Details")

        num_rows = len(list_items.find_all(role='row')[1:])

        for i, row in enumerate(list_items.find_all(role='row')[1:]):

            name = row.text.split()[0].replace('\n', '')

            if name == ".":
                continue

            try:
                type_ = row.svg['aria-label']
                link = 'https://github.com' + str(row.span.a['href'])
                node = link.split("/")[-1]

                if name != "Go to parent directory":
                    if 'Directory' == type_:
                        self.__directories.append(DirectoryModel(name, link, name))

                        graph.add_node(node)
                        graph.add_edge(link.split("/")[-2], node)

                        text = f"Processando {name} ({i + 1}/{num_rows})"
                        # Atualiza a barra de progresso a cada iteração do loop
                        progress_bar.progress((i + 1) / num_rows, text=text)

                        graph = self.build_graph(link, graph, progress_bar)

                    else:
                        graph.add_node(node)
                        graph.add_edge(link.split("/")[-2], node)

                        req_file = requests.get(link.replace('blob', 'blame'))

                        soup_file = BeautifulSoup(req_file.text, "html.parser")

                        file_info: str = soup_file.find(class_='file-info').text

                        file_cute: List[str] = file_info.strip().replace('\n', '').split()

                        size = self.convert_to_kilobytes(float(file_cute[-2]), file_cute[-1].upper())

                        self.__files.append(FileModel(
                            name=name,
                            link=link.replace("https://github.com", ""),
                            path=link.split('blob')[-1].replace('/', '\\' if '\\' in link else '/'),
                            lines=int(file_cute[1]),
                            size=f"{size:.2f} KB",
                            extension=name.split('.')[-1]))

            except Exception as e:
                print(e, name)

        progress_bar.progress(1.0, text="Concluído!")
        return graph
