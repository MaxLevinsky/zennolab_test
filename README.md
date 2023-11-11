# zennolab_test

## общий подход
применяем zero-shot object detection (**GroundingDino*), из полученных bounding boxes счтаем их центры и считаем метрику

## как запустить
1. *git clone https://github.com/MaxLevinsky/zennolab_test.git*
2. *cd zennolab_test*

### для запуска на GPU
1. *bash Docker/docker_build.sh*
2. *bash Docker/docker_run.sh*

во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта

скрипт *docker_run.sh* запускается с параметром *--gpus all*, если нужно ограничить кол-во карт, этот параметр нужно исправить.

### для запуска на CPU
1. *bash Docker/cpu/docker_build.sh*
2. *bash Docker/cpu/docker_run.sh*

во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта


пример входных данных

    - input dir
        - squirrels_head
            - <>.jpg
            - <>.json
        ...

## сохраняемые аретфакты
в output директории, файл result.csv содержит усредненную метрику и усредненное евклидово расстояние
