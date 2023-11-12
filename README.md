# zennolab_test

---
**IMPORTANT**
код (инструкция запуска) локально протестирована для запуска на CPU, нет возможности запустить код на сервере 
с GPU, возможны ошибки описанные ниже.
Я получил метрики на google colab с маунтом своего google drive (предварительно перенеся туда исходные данные).

---

### Общий подход
применяем zero-shot object detection (**GroundingDino**), из полученных bounding boxes считаем их центры и считаем метрику

### Как запустить

    git clone https://github.com/MaxLevinsky/zennolab_test.git

    cd zennolab_test

### Для запуска на GPU

    bash Docker/docker_build.sh

    bash Docker/docker_run.sh

во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта

скрипт *docker_run.sh* запускается с параметром *--gpus all*, если нужно ограничить кол-во карт, этот параметр нужно исправить.

### Для запуска на CPU
    bash Docker/cpu/docker_build.sh

    bash Docker/cpu/docker_run.sh

во время выполения docker_run.sh нужно будет указать директорию со входными данными и директорию для артефактов работы скрипта


пример входных данных

    - input dir
        - squirrels_head
            - <>.jpg
            - <>.json
        ...

### Сохраняемые аретфакты
в output директории, файл result.csv содержит усредненную метрику и усредненное евклидово расстояние


---
**IMPORTANT**

в случае если возникает следующая оибка

    NameError: name '_C' is not defined

нужно установить переменную окружения CUDA_HOME

    export CUDA_HOME=/path/to/cuda

пример:

для того чтобы узнать где установлен CUDA toolkit нужно в терминале ввести
    
    which nvcc

если вывод будет **/usr/local/cuda/bin/nvcc** то

    export CUDA_HOME=/usr/local/cuda

и повторить описанные выше шаги

---