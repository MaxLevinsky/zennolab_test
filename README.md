# zennolab_test

## общий подход
применяем zero-shot object detection (groundingDino), из полученных bounding boxes счтаем их центры и считаем метрику

## как запустить
1. cd <dir>
2. git clone https://github.com/MaxLevinsky/zennolab_test.git
3. cd zennolab_test
4. bash docker_build.sh
5. bash docker_run.sh
во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта

пример входных данных

    - input dir
        - squirrels_head
            - <>.jpg
            - <>.json
        ...

## как запустить с CUDA
по умолчанию используется цпу, для того чтобы изменить на cuda нужно в файле docker_run
