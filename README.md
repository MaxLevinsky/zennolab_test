# zennolab_test

## общий подход
применяем zero-shot object detection (groundingDino), из полученных bounding boxes счтаем их центры и считаем метрику

## как запустить
1. git clone https://github.com/MaxLevinsky/zennolab_test.git
2. cd zennolab_test
3. bash Docker/docker_build.sh
4. ДЛЯ ЗАПУСКА на ГПУ: bash Docker/docker_run.sh
во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта

пример входных данных

    - input dir
        - squirrels_head
            - <>.jpg
            - <>.json
        ...

скрипт docker_run.sh запускается с параметром --gpus all, если нужно ограничить кол-во карт, этот параметр нужно исправить.

5. ДЛЯ ЗАПУСКА на CPU: bash Docker/docker_run_cpu.sh
