#!/usr/bin/env python3

"""
TODO
[?] bs4 для создания HTML
[-] Добавление классов для CSS
[-] Добавление CSS
[-] Оформление кода в main()
[-] Создание пакета
[-] Интеграция с catalogue
"""

import os
import time

start_time = time.time()
files_created = 1

if not os.path.exists("root"):
    os.mkdir("root")
os.chdir("root")

first = True
root_dirs = []

# Прогон для сканирования
for a, b, c in os.walk("/home/ash/build/lib/root/"):
    if first:
        first = False
        root_dirs = b
        continue

    if not c:
        for entity in b:
            full_path = os.path.join(*os.path.join(a, entity).split("/")[-2:])

            if not os.path.exists(full_path):
                os.makedirs(full_path)

    if c and not b:
        lib_path = a
        index_path = os.path.join(*a.split("/")[-2:])

        for entity in os.listdir(lib_path):
            if not entity.endswith(".meta") and entity != "index.html":
                file_name = entity.split("/")[-1]

                src_path = os.path.join(lib_path, entity)
                end_path = os.path.join(index_path, file_name)

                if not os.path.exists(end_path):
                    os.symlink(src_path, end_path)
                    files_created += 1

        with open(os.path.join(index_path, "index.html"), "w") as index:
            index.writelines(["<html>",
                              "<body>",
                              "<p><a href='../index.html'>../<a></p>",
                              *["<p><a href='{0}'>{0}</a></p>".format(entity) for entity in os.listdir(index_path) if not entity.endswith(".meta") and entity != "index.html"],
                              "</body>",
                              "</html>"])
        files_created += 1

# Мы в каталоге root/
with open("index.html", "w") as index:
    index.writelines(["<html>",
                      "<body>",
                      *["<p><a href='{0}/index.html'>{0}</a></p>".format(entity) for entity in os.listdir(os.getcwd()) if entity != "index.html"],
                      "</body>",
                      "</html>"])

# Прогон для заполнения
first = True
for a, b, c in os.walk("/home/ash/build/lib/root/"):
    if first:
        for directory in root_dirs:
            contents = os.listdir(directory)
            with open(os.path.join(directory, "index.html"), 'w') as index:
                index.writelines(["<html>",
                                  "<body>",
                                  "<p><a href='../index.html'>../<a></p>",
                                  *["<p><a href='{0}/index.html'>{0}</a></p>".format(entity) for entity in contents if entity != "index.html"],
                                  "</body>",
                                  "</html>"])
                files_created += 1
        first = False


def super_round(number):
    start_precision = 0
    while round(number, start_precision) == 0:
        start_precision += 1

    return round(number, start_precision)

print("Индексирование завершено.\nСоздано файлов: {}\nВремя: {} с.".format(files_created, super_round(time.time()-start_time)))
