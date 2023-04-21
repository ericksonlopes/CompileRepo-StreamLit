from dataclasses import dataclass
from typing import List

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
    # extension: str = None


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

    def generate_tree(self, url, nivel=0):
        req = requests.get(url)

        soup = BeautifulSoup(req.text, "html.parser")

        list_itens = soup.find(class_="js-details-container Details")

        for row in list_itens.find_all(role='row')[1:]:
            name_ = row.text.split()[0].replace('\n', '')
            try:
                type_ = row.svg['aria-label']
                link_ = 'https://github.com' + str(row.span.a['href'])

                if name_ != "Go to parent directory":
                    if 'Directory' == type_:
                        self.__directories.append(DirectoryModel(name_, link_, name_))
                        st.text("|   " * nivel + "+-- " + name_)
                        self.generate_tree(link_, nivel + 1)

                    else:
                        req_file = requests.get(link_.replace('blob', 'blame'))

                        soup_file = BeautifulSoup(req_file.text, "html.parser")

                        # Recebe o texto
                        file_info: str = soup_file.find(class_='file-info').text

                        # Limpa os dados
                        file_cute: List[str] = file_info.strip().replace('\n', '').split()

                        st.text("|   " * nivel + "|-- " + name_ +
                                f" ({int(file_cute[1])} lines, {file_cute[-2]} {file_cute[-1]})")

                        self.__files.append(FileModel(
                            name=name_,
                            link=link_,
                            path=link_,
                            lines=int(file_cute[1]),
                            size=f"{file_cute[-2]} {file_cute[-1]}"))

            except Exception as e:
                print(e)
